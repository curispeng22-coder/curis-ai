# CURIS-V1-GENERAL-WORKSPACE-P1-OPERATING-CLOSURE

Status: Implemented / Partial — Packaged native interaction gate remains
Authority Class: CURRENT / IMPLEMENTATION ISSUE
Owner: Main Development Session
Date: 2026-08-29

## Goal

Close the first bounded General Workspace operating surface over existing canonical Company OS primitives, starting with one canonical CEO Assistant identity and truthful Conversation behavior.

The user-visible chain is:

`Goal → Responsibility → Employee → Work → Execution / Waiting → Result/Evidence → Next Responsibility → Company Attention`.

No second Work, Employee, Decision, Result, Conversation or notification system may be created.

## Current Gap

- The legacy floating Global Assistant auto-opens on the CEO Desk, reads a separate legacy identity and can synthesize a local answer.
- General Workspace materializes correctly but only renders an entry card.
- Headless General Workspace Work creation/execution already exists, but its Responsibility routing truth is not fully projected into the current product read model.
- Fresh General Workspaces have no invented Employee or Capability; therefore they must stop truthfully at a responsibility/capability gap until supply exists.

## Allowed Files

### Backend

- `backend/app/runtime/general_workspace_delivery.py` — reuse-only Team materialization and General P7 adapter.
- `backend/app/api/shared_workspace_router.py` — bounded General commands over existing Runtime primitives.
- `backend/app/shared_workspace_projection.py` — bounded General Workspace read-model projection only.
- `backend/app/runtime/responsibility_routing.py` — no semantic change; only if an existing shared seam must expose accepted P7 truth.
- `backend/tests/test_v1_general_workspace_p1_operating_closure.py` — isolated focused acceptance.

### Frontend

- `frontend/components/assistant/GlobalAssistant.js` — canonical identity, on-demand behavior, no canned response.
- `frontend/components/v1/GeneralWorkspaceOperating.js` — bounded General Workspace product surface.
- `frontend/components/workspace/SharedEmployeeWorkArea.js` — reuse only; no General-specific fork.
- `frontend/app/ceo-office/workspace/page.js` — generic Workspace adapter seam only.
- `frontend/lib/runtimeApi.js` — existing shared/general and Work execution API wrappers only.
- `frontend/tests/v1GeneralWorkspaceOperating.test.mjs` — focused source/contract regression.

### Delivery

- `issues/CURIS-V1-GENERAL-WORKSPACE-P1-OPERATING-CLOSURE.md`
- `docs/reviews/CURIS_V1_GENERAL_WORKSPACE_P1_OPERATING_CLOSURE_REVIEW.md`
- `docs/reviews/CURIS_V1_EXECUTION_BACKLOG.md` — status line only.
- `docs/00_Context/CURRENT_STATE.md` — implementation truth entry only after evidence.

## Pre-change Hashes

- `backend/app/shared_workspace_projection.py`: `841b10555e72e56dac9139be6be0cb49732d388499542089861296a714f1af90`
- Completion pre-change `backend/app/runtime/general_workspace_delivery.py`: `ba9f733e80af652f0f0502622bc6ce73ca8e0cb97d37d20db1e9602be426a8b8`
- Completion pre-change `backend/app/api/shared_workspace_router.py`: `8417e29d19cb0836ce437fc6ceef17d37453810ed2f9e4f912b9334b14d7b017`
- Completion pre-change `backend/app/shared_workspace_projection.py`: `679a964444380a446c7915c69af889422a4989b4c539864fb859725bc605cffc`
- Completion pre-change `backend/app/runtime/responsibility_routing.py`: `9b22c0889ba3adae306074ec4f1bffa7f509924905df4f65b2cc424a5c5666fe`
- `frontend/components/assistant/GlobalAssistant.js`: `4031ae48c618cff3db7ca0f9a4a156b6701d2943426a6137444809fa88083077`
- `frontend/app/ceo-office/workspace/page.js`: `f0f4ec1cc3513cde1ffc9672db9d36895da9d2f7a2eee74ecadd6e4a992bc627`
- `frontend/lib/runtimeApi.js`: `3e47ab9d14cc2774b8a12f456be67fba766a05fddbf2b720191597223f760a07`
- Completion pre-change `frontend/components/v1/GeneralWorkspaceOperating.js`: `3082c2ae95dfe7c3dda993d896b3cb4a995ba22eb2c9d5a60f59a8370d994408`
- Completion pre-change `frontend/lib/runtimeApi.js`: `7f8beaabe35b88ee32cc8fc28f71c4dd739b802220e75aba7924c018d469c186`
- Completion pre-change `frontend/components/workspace/SharedEmployeeWorkArea.js`: `d5599b5620ce33c61f60e2da7c4e79c7a2ae7dd518c52793e3664fe34452b592`

## Backend Seams

- Reuse `SharedWorkspaceProjection.general_workspace()`.
- Reuse `GeneralWorkspaceDelivery.create_work()`.
- Reuse Team Operating `/works/{work_ref}/execute`.
- Project existing `responsibilityRouting`, Employee, execution, Result and Evidence references; do not persist a second read model.

## Frontend Seams

- Reuse `TerraShell`, seven-area navigation and current General Workspace route.
- Reuse existing shared Conversation/Composer product language.
- Keep the floating Assistant on demand, but derive its identity from the canonical Runtime CEO Assistant and disable fake local replies.
- Keep RD/XHS dedicated routes unchanged.

## Test Matrix

1. Canonical CEO Assistant is the only Company-level Assistant identity.
2. CEO Desk does not auto-open the floating Assistant.
3. No-model floating Conversation cannot emit a canned answer.
4. Generic Workspace reads canonical Business, Workspace goal, Team and current Work.
5. No Employee/Capability returns a precise, side-effect-free responsibility gap.
6. Valid Employee/Capability creates one idempotent canonical Work.
7. Routing projection separates Holder, Current Executor and execution state.
8. Accepted execution exposes Result/Evidence references without copying content.
9. Waiting/failure preserves reason, Holder and recovery path.
10. Restart recovers canonical identities and does not claim stale RUNNING as live.
11. Company Attention continues to reference existing Decision/Handoff/Result truth.
12. Batch 1, RD, XHS, P7, usage attribution, M2.5A and DB-safety regressions pass.

## DB Safety

- All tests use one repository-external SQLite selected by `CURIS_DB`, `CURIS_DB_PATH` and `CURIS_WORKSPACE_DB`.
- Repository active SQLite files are fingerprinted before and after.
- No active DB initialization, migration or write is allowed.

## Stop Gates

- Frozen Authority conflict.
- Need for a new shared Runtime primitive or schema migration.
- Need to invent an Employee, Capability, Result or Provider response.
- Mixed-source hunk ownership collision in an Allowed File.
- Active DB mutation.
- UI composition requiring a new design decision rather than reuse of accepted patterns.

## Explicit Non-goals

- No Workflow Builder, DAG, new Task/Matter/Decision/Result/Model system.
- No professional matcher/materializer.
- No M3 Keychain workaround.
- No App Entry or CEO Desk redesign.
- No RD/XHS/TTK domain change.
- No avatar, voice or attachment closure.
- No deletion of legacy routes before replacement proof.
- No commit or push.

## P1 Completion Scope

1. Automatically publish the existing Workspace-scoped Responsibility definition only when the current canonical Role, Employee, Capability and Assignment facts are sufficient; never invent a generic role or employee template.
2. Reuse canonical Handoff and one P7 `DECISION_PACKET`; Company Attention references the same object.
3. Reuse shared Result/Artifact/Evidence references for a reference-first Utility drill-down.
4. Validate restart/idempotency, Browser and fresh packaged Desktop separately.

If no authority-backed Employee/Responsibility template exists, a newly founded empty General Workspace remains `NEEDS_DECISION`; that truthful boundary is not bypassed by this Issue.

## Acceptance

Final status is evidence-based: `IMPLEMENTED / ACCEPTED`, `IMPLEMENTED / PARTIAL`, or `BLOCKED AT PRECISE STOP GATE`.

## Implementation Result

- Canonical Runtime `CEO_ASSISTANT` is now the floating Assistant identity source; the legacy identity editor, CEO Desk auto-open and local synthesized answer were removed from the primary path.
- Generic Workspace routes now open a real operating surface over `SharedWorkspaceProjection.general_workspace()`.
- Existing General Workspace Delivery and Team Operating APIs create/execute canonical Work; no new Runtime primitive or schema was introduced.
- Holder, Current Executor, Work status and Result/Artifact/Evidence references are projected from persisted `responsibilityRouting` truth.
- Fresh Workspaces without a legal Team stop at `NEEDS_DECISION` and create no Cycle/Work.
- Existing explicit Role/Employee/Capability/Assignment truth can now materialize one idempotent Workspace-scoped `general-operating` workflow. Empty truth remains `NEEDS_DECISION`; no Employee, Role or Capability is invented.
- Persisted canonical Handoff, one P7 `DECISION_PACKET`, CEO Attention reference, CEO choice and automatic Runtime continuation are projected from the same objects.
- Shared Result Utility now opens real Task/Artifact references with owner, source Work, execution provenance and verification truth; failed local execution remains `FAILED / UNVERIFIED` and never becomes a fake result.
- Browser full-path and restart acceptance passed against one isolated SQLite. A fresh `Curis.app` was built and launched twice with isolated app-data; CEO Desk, Company recovery, three sidecars and packaged Gateway reread of the same Team/Work/Handoff/Decision/Result IDs passed.
- Packaged native Workspace interaction remains unaccepted because Computer Use consistently failed at the Tauri WebView click boundary with `Sky Computer Use native pipe closed before response`. Browser navigation and packaged HTTP evidence are not substituted for that missing native click proof.

Formal evidence: `docs/reviews/CURIS_V1_GENERAL_WORKSPACE_P1_FINAL_IMPLEMENTATION_REVIEW.md`.

## V1-P1-010 Native Interaction Acceptance — 2026-08-30

Verdict: `BLOCKED BY NATIVE AUTOMATION TOOLING`.

- The exact packaged app at `desktop/target/release/bundle/macos/Curis.app` launched with isolated app-data, rendered the CEO Desk, exposed the canonical `workspace-v1-general` link through the native Accessibility tree, and recovered the same Company/Workspace entry after restart.
- Every real Computer Use action against that packaged WebView failed with `Sky Computer Use native pipe closed before response`; both element-index and coordinate clicks produced no navigation.
- One automation-created duplicate Curis process from another worktree was identified and removed. A subsequent full-path click with only the accepted package running failed identically, so the remaining gate is not attributed to a process conflict or a demonstrated Curis defect.
- No Browser/API/SQLite evidence is substituted for native user interaction. Workspace reached: `NO`; real UI interaction: `NO`; restart interaction: `NO`.
- Repository-active SQLite files remained byte-identical with `integrity_check=ok`.

Formal record: `docs/reviews/CURIS_V1_GENERAL_WORKSPACE_NATIVE_INTERACTION_ACCEPTANCE.md`.

Issue status remains `Implemented / Partial — Packaged native interaction gate remains`. Recovery is limited to retrying this exact native gate with a working native automation bridge; no feature or Runtime change is authorized by this result.
