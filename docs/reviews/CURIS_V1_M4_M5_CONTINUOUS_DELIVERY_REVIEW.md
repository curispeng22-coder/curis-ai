# CURIS V1 M4 + M5 Continuous Delivery Review

Status: Review — CEO IMPLEMENTATION REVIEW REQUIRED

Authority Class: REVIEW / EVIDENCE

Date: 2026-08-27

## Scope result

M4 and M5 are implemented inside the bounded Issue
`CURIS-V1-M4-M5-CONTINUOUS-DELIVERY-001`. The implementation reused canonical
Business/Workspace lineage, child Work, Responsibility Routing, Team Operating,
Employee execution identity, ResultStore, Artifact/Evidence and the existing usage
ledger. No new schema or parallel Runtime was created.

## M4 — RD canonical integration

- Existing RD `Project → Cycle` remains the domain path.
- Starting an RD Cycle now creates a canonical child Work and Cycle-scoped pinned
  Responsibility Assignment instead of relying only on the RD execution bridge.
- The existing Codex path records Workspace, Business, Work and Execution attribution;
  RD Project remains optional domain attribution on the same ledger.
- A real installed Codex session ran in an isolated temporary project, changed
  `src/calc.py`, passed the real pytest command, persisted Task/Artifact/Evidence and
  survived Runtime reread. Runtime effective computer access remained `UNKNOWN` where
  the provider could not prove it.
- Legacy RD slices and General Workspace without Project remain compatible.

## M5 — Content Growth headless integration

- Identity is a canonical Generic `CONTENT_GROWTH` Workspace, not XHS/Douyin/TikTok.
- One Cycle produced three distinct canonical Work objects: Research, Content and
  Evaluation. Research and Content produced separate Result, Artifact, Evidence and
  Acceptance records; two persisted Handoffs transferred accountability.
- Controlled provider proof exercised the full shared mechanical chain and ended
  Evaluation in `WAITING` with `publishing=NOT_CONNECTED` and
  `analytics=UNAVAILABLE` inputs.
- A real installed Codex proof ran on the same headless Team execution path. It rejected
  the missing `brief:content-growth-goal` body and left the first Work `WAITING` with the
  exact missing-input reason. It did not invent research, content, publication,
  analytics or completion.
- Local controlled-provider usage events retain canonical Workspace/Business/Work/
  Execution provenance; external provider quality/cost and real channel facts remain
  unverified.

## Evidence

- New focused tests: `2 passed`.
- Final M4/M5 + RD + General + usage + child Work + Team Operating + DB Safety suite:
  `40 passed`.
- Real Codex M4 proof: `1 passed` in `167.54s`.
- Real Codex M5 truth proof: `1 passed` in `15.39s`; Provider callback/session
  verified, business result `REJECTED`, and Work remained `WAITING` because the
  referenced brief body was absent.
- Python compile: PASS.
- `git diff --check`: PASS for Issue-owned paths.
- Isolated SQLite restart/integrity: PASS.

## Active database safety

Both active databases were byte-identical to preflight and returned
`integrity_check=ok`:

- `data/curis.sqlite`: size `1232896`, mtime `1786873339`, SHA-256
  `2ea2506f90f764e834d47d8f6bae3cb41c22d457757e0e9216c0ae8c39a39ec6`.
- `backend/data/curis.sqlite`: size `1277952`, mtime `1786783659`, SHA-256
  `a9d96a9536a5bce3b3b30f912e86a37f61d28527a8eb2d35af7a5857d29414e4`.

## Remaining boundaries

- M3 native durable Keychain: `SECURITY BLOCKED` and independent of M4/M5.
- M2.5B First Run capture: `UI-HOLD`.
- Real Content Growth source ingestion, publishing, receipt and analytics connectors:
  `NOT CONNECTED / REAL-WORLD EVIDENCE REQUIRED`.
- Browser, final UI and Packaged Desktop are outside this UI-independent Issue.
- No commit and no push were performed.

## Verdict

`M4 RD CANONICAL INTEGRATION = CLOSED`

`M5 CONTENT GROWTH HEADLESS INTEGRATION = CLOSED WITH HONEST CAPABILITY GAPS`

`CURIS V1 UI-INDEPENDENT DELIVERY EPIC = UI-INDEPENDENT CORE CLOSED; M3 REMAINS SECURITY BLOCKED`
