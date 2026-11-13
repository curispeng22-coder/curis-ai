# CURIS-V1-M2.5-GENERAL-WORKSPACE-CONTEXT-001

Status: IMPLEMENTED — M2.5A CLOSED / M2.5B UI-HOLD / CEO REVIEW REQUIRED

Authority Class: CURRENT / IMPLEMENTATION

Owner: Main Development / Runtime Integration

Date: 2026-08-27

## Goal

Propagate existing canonical Business, Workspace and General Work Cycle truth into the existing Team Operating Provider Task without creating another Context system. Preserve an exact missing-fact reason and recovery instruction when a real Provider result is rejected, then allow the same Work to resume without duplicate active execution or Result.

## Authority

- `docs/00_Context/CURRENT_STATE.md`
- `issues/CURIS-V1-UI-INDEPENDENT-DELIVERY-EPIC.md`
- `docs/reviews/CURIS_GENERAL_WORKSPACE_CONTEXT_SUFFICIENCY_AUDIT.md`
- CEO acceptance: `CONTEXT CAPTURE + PROPAGATION FIX REQUIRED`

## Pre-change baseline

- HEAD: `c797db840bad285d7e9f1962d06eac61aa28508b`
- `backend/app/api/team_operating_router.py`: `32e8eab7857effbeeafa39ea5696f702ba80ee9be9c42e8c06c353bfe7aa3add`
- `backend/app/runtime/responsibility_routing.py`: `9b22c0889ba3adae306074ec4f1bffa7f509924905df4f65b2cc424a5c5666fe` (preserved mixed-source; no modification planned)
- `backend/tests/test_v1_general_operating_contract.py`: `64bf0e72abf2308e9f0da83c14ef8a1ef10aa7a09510af6a30ce3c36cd12ff1d`
- `backend/tests/test_canonical_usage_attribution.py`: `697f23462408a3e630fe88bccf6f8601209e4770f390d527963b6ae597ac754d`

Active database fingerprints:

- `data/curis.sqlite`: size `1232896`, mtime `1786873339`, SHA-256 `2ea2506f90f764e834d47d8f6bae3cb41c22d457757e0e9216c0ae8c39a39ec6`, integrity `ok`.
- `backend/data/curis.sqlite`: size `1277952`, mtime `1786783659`, SHA-256 `a9d96a9536a5bce3b3b30f912e86a37f61d28527a8eb2d35af7a5857d29414e4`, integrity `ok`.

## Allowed Files

- `backend/app/api/team_operating_router.py`
- `backend/tests/test_v1_general_operating_contract.py`
- `backend/tests/test_canonical_usage_attribution.py`
- `issues/CURIS-V1-M2.5-GENERAL-WORKSPACE-CONTEXT-001.md`
- `docs/reviews/CURIS-V1-M2.5-GENERAL-WORKSPACE-CONTEXT-001_review.md`
- `issues/CURIS-V1-UI-INDEPENDENT-DELIVERY-EPIC.md` (status only)
- `docs/00_Context/CURRENT_STATE.md` (status only)

## Explicit Exclusions

- No Context, Memory, Knowledge, Prompt or Workflow V2.
- No new Runtime primitive, Project, state enum or schema.
- No whole Workspace, Business, Conversation, History, Knowledge or Memory hydration.
- No RD, Content Growth, UI redesign, Keychain, active database, commit or push change.
- `backend/app/runtime/responsibility_routing.py` remains untouched unless evidence proves the existing execution record cannot preserve the accepted truth; any such need is a stop/amend gate.

## Runtime truth

- General Work context is resolved from the existing Work `cycleRef`, `GENERAL_WORK_CYCLE.contract`, canonical Workspace relation, canonical Business and current Assignment/Employee.
- Only selected input/Result/Artifact/Evidence references are passed, reference-first and bounded.
- Cross-tenant/company/workspace references that resolve to Curis-owned objects fail closed before Provider launch.
- A rejected real result leaves the Work `WAITING`, Holder retained and Current Executor empty; its exact missing fact and recovery instruction are durable in the existing execution record.
- Retry uses the same Work identity and existing duplicate guard.

## Acceptance

1. Problem, expected result and constraints reach Provider context.
2. Canonical Business/Workspace facts reach Provider context without Project.
3. Selected input/result/artifact/evidence refs reach context; whole history does not.
4. Cross-scope Curis-owned refs reject before Provider launch.
5. Missing source remains `REJECTED → WAITING`; reason/recovery are durable.
6. Holder remains and Current Executor clears.
7. Supplying a source and continuing the same Work creates no duplicate active execution/Result.
8. Restart preserves Cycle context and WAITING/retry truth.
9. RD, Team Operating and canonical usage attribution regressions pass.
10. Active databases remain byte-identical.

## Phase B decision gate

The current onboarding page is preserved mixed-source and intentionally stores only an opaque intent reference. Connecting natural-language intent to normalized First Run materialization requires final interaction semantics, not a runtimeApi-only change. M2.5B remains `UI-HOLD`; this Issue does not modify frontend files.
