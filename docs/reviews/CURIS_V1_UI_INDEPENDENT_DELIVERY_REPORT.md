# CURIS V1 UI-INDEPENDENT DELIVERY REPORT

Status: Review

Authority Class: REVIEW / EVIDENCE

Date: 2026-08-27

## Completed

- Added an atomic, deterministic First Run Runtime path from a CEO-confirmed `FoundingRun` to the existing Company/CEO Assistant, a real Department, canonical Business and first `GENERIC` Workspace.
- Reused the existing Business Spine transaction and parent resolver; no parallel Company, Business or Workspace system was created.
- Added a stable General Workspace read contract over the existing Shared Workspace projection.
- General Workspace readiness is truthful: no unique Team responsibility definition or no eligible Employee returns `NEEDS_DECISION` and creates no Runtime object.
- Added the ordinary-language General Work command over existing Cycle, canonical child Work and Responsibility Routing primitives. It resolves an existing workflow, canonical Employee and active capability binding without inventing Team facts.
- Atomic Cycle/Work creation, idempotent replay, conflict rejection and restart identity are verified in isolated SQLite.
- M4 closes RD canonical integration: an accepted RD Cycle now creates a canonical
  child Work/Responsibility Assignment and the real Codex path records canonical
  Workspace/Business/Work/Execution attribution alongside optional RD Project context.
- M5 closes headless Content Growth integration on a canonical Generic Workspace:
  Research → Content → Evaluation are distinct child Work contracts with per-Work
  Result/Evidence, persisted Handoff and honest waiting when source/channel facts are absent.

## UI Contracts Ready

- First Run materialization returns stable Department/Business/Workspace/version identities, template match truth, next action and canonical parent path.
- General Workspace read model returns goal, proposal, Team facts, current Work, Result references, System Activity and operating readiness.
- Existing Shared Runtime continues to expose Employee identity, holder/executor separation, capability truth, Result/Evidence, Team Operating, Handoff/P7 and sequential child Work.

## UI-Dependent Hold

- Final First Run interaction and Proposal presentation.
- CEO Desk first-business composition and final navigation placement.
- General Workspace Main/Context/Utility and Conversation composition.
- Content Growth final professional surfaces.

## External / Security Blockers

- Durable packaged secrets: current `LocalDevCredentialBackend` stores plaintext only in process memory. No registered macOS Keychain backend exists. A native, bounded security implementation is required; environment variables, files or command-line plaintext are not acceptable substitutes.
- Real channel publish/analytics require legitimate platform access and real-world evidence.
- Developer ID signing/notarization requires Apple distribution credentials.

## Architecture Blocker

- CLOSED 2026-08-27 by `CURIS-CANONICAL-USAGE-ATTRIBUTION-001`.
- The existing usage ledger now supports verified canonical `Company → Department → Business → Workspace → Work / Execution` ownership while retaining verified legacy Project attribution.
- A real installed Codex provider launched from a General Workspace without Project and persisted canonical usage, Result, Artifact and Evidence. No synthetic Project or validation bypass was added.

## Remaining V1 Gaps

- Browser and fresh Packaged Desktop acceptance for First Run.
- Safe Team materialization remains a product gap; when an existing Team is present, the ordinary-language command now creates canonical Work truthfully.
- General Workspace context assembly must provide enough relevant business facts for useful Provider outcomes. The real proof truthfully returned a rejected business result and left Work `WAITING`; this is not an attribution blocker or a completed business outcome.
- Canonical RD UI/Packaged entry-to-outcome assembly; the UI-independent Runtime chain is closed.
- Content Growth final IA/UI and real source/channel integration; the headless shared Runtime chain is closed.
- Backup/restore, update recovery and whole-app packaged acceptance.

## Evidence

- Current M1/M2 focused suite: 15 passed, including command gaps, atomic creation, idempotency, restart, child Work, routing and DB safety.
- Existing reusable Runtime regression: 24 passed across Team Operating real Employee E2E, Responsibility Routing, canonical child Work, cross-surface sequential multi-Work, RD real execution, Package Runtime and Shared Workspace projection.
- Earlier M1 bounded regression: 24 passed, Python compile passed, isolated SQLite integrity `ok`.
- Live isolated M1 API proof created exactly one Company/Department/Business/Workspace, resolved the canonical parent path, then reread it after Runtime restart.
- M2 isolated restart proof returned the same General Workspace read model and zero Runtime entities when Team truth was absent.
- M2 isolated command proof returned the same Cycle/Work after restart and rejected a conflicting replay.
- M2 canonical attribution proof: focused core/migration `21 passed`, billing `33 passed`, RD `16 passed`, General/Team/Responsibility `15 passed`.
- M2 live isolated Provider proof launched installed `codex-cli 0.144.6` without Project, persisted one canonical usage attempt and one Artifact, and reread the same attribution after restart. The Provider returned a truthful rejected business result due insufficient context; Work remained `WAITING` and no fake completion was created.
- M4/M5 final regression: `40 passed`; M4 live Codex changed a real isolated file and
  passed its test; M5 live Codex rejected a missing source body and stopped at
  `WAITING` rather than fabricating content or channel facts.
- Browser acceptance: NOT RUN for this Epic slice.
- Packaged Desktop acceptance: NOT RUN; therefore V1-P0-001 and V1-P1-001 remain `PARTIAL`.
- Active SQLite fingerprints remained unchanged from preflight; final values are recorded in the handoff response.

## Decision

The UI-independent M1, M2, M2.5A, M4 and M5 Runtime contracts are closed. M2.5B
remains `UI-HOLD`; M3 remains stopped at its independent native Keychain security gate.
This is not a claim that the whole app or final UI is V1 ready.
