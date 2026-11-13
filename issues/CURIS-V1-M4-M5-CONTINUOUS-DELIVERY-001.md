# CURIS V1 M4 + M5 Continuous Delivery

Authority Class: CURRENT IMPLEMENTATION ISSUE
Status: Review — IMPLEMENTED / CEO IMPLEMENTATION REVIEW REQUIRED
Date: 2026-08-27

## Goal

Close the UI-independent M4 RD canonical integration and M5 Content Growth headless
integration by reusing the accepted Business Spine, canonical Work, Team Operating,
Result/Evidence, Usage Attribution and Context systems.

## Pre-change truth

- HEAD: `c797db840bad285d7e9f1962d06eac61aa28508b`
- `backend/app/main.py`: `cd0d86b8c2f36f1751433e53c9ecd253d35a389baef70b646ca02ea7be6cdc16`
- `backend/app/runtime/workspace.py`: `5b56d5c855fcd52f3d1bd666e51e384bca39000ce7c5ba2a307346a27f1e86c0`
- Active databases are fingerprinted in the Review and must remain byte-identical.

## Allowed Files

- `backend/app/main.py` — RD execution bridge owned hunks only
- `backend/app/runtime/workspace.py` — RD canonical Work integration owned hunks only
- `backend/tests/test_v1_m4_m5_continuous_delivery.py`
- `issues/CURIS-V1-M4-M5-CONTINUOUS-DELIVERY-001.md`
- `issues/CURIS-V1-UI-INDEPENDENT-DELIVERY-EPIC.md` — status only
- `docs/reviews/CURIS_V1_M4_M5_CONTINUOUS_DELIVERY_REVIEW.md`
- `docs/reviews/CURIS_V1_UI_INDEPENDENT_DELIVERY_REPORT.md` — status only
- `docs/reviews/CURIS_V1_UI_DEPENDENCY_MATRIX.md` — status only
- `docs/reviews/CURIS_V1_EXECUTION_BACKLOG.md` — status only
- `docs/00_Context/CURRENT_STATE.md` — accepted implementation status only

## M4 acceptance

RD Workspace creates one canonical Work under its existing Cycle, pins the real RD
Employee/Responsibility, launches Codex through the existing adapter, and records each
provider usage call with Company/Department/Business/Workspace/Work/Execution plus optional
Project attribution. File change, test, Artifact/Evidence, restart and failure truth
remain intact. General Workspace without Project remains valid.

## M5 acceptance

A canonical Content Growth Business/Generic Workspace runs sequential Research and
Content Work through existing Team/child-Work Runtime, with bounded context, separate
Result/Artifact/Evidence/Acceptance, a real Handoff/release and honest WAIT/UNKNOWN
truth for publishing/analytics. No XHS/Douyin/TikTok Workspace identity is created.

## Explicit Exclusions

No UI, navigation, channel connector, fake publication/analytics, new schema, new
Runtime primitive, Workflow/DAG engine, Product Authority change, M3 Keychain work,
active database write, commit or push.

## Stop conditions

Stop on a required new Runtime primitive, Frozen conflict, destructive migration,
active database risk or ambiguous mixed-source ownership. External platform capability
absence is recorded locally and does not stop headless core proof.

## Implementation result

- M4: existing RD Cycle now creates one canonical child Work and pinned
  Responsibility Assignment before the existing Codex execution path. Provider Task,
  usage ledger, Artifact/Evidence and restart truth carry canonical Workspace/Business/
  Work/Execution attribution plus optional RD Project attribution.
- M5: one canonical Generic Content Growth Workspace runs three distinct child Work
  contracts (Research, Content, Evaluation) through existing Team Operating. Controlled
  proof completed Research/Content with separate Result/Evidence/Acceptance and two
  persisted Handoffs; Evaluation remained `WAITING` because publishing and analytics are
  not connected. A live Codex proof independently rejected missing source content rather
  than fabricating a business result.
- No schema, UI, channel connector, new Runtime primitive, XHS identity, synthetic
  Project, active database write, commit or push was introduced.
