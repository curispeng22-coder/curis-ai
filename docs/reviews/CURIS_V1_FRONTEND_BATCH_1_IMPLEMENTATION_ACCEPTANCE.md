# CURIS V1 — FRONTEND BATCH 1 IMPLEMENTATION ACCEPTANCE

**Status:** Frozen
**Authority Class:** FROZEN / IMPLEMENTATION ACCEPTANCE RECORD
**Disposition:** V1 FRONTEND BATCH 1 — IMPLEMENTED / ACCEPTED WITH RECORDED BOUNDARIES
**Date:** 2026-08-29
**Evidence:** `docs/reviews/CURIS_V1_FRONTEND_BATCH_1_FINAL_ACCEPTANCE.md`

## Accepted implemented scope

The fresh Browser and packaged `Curis.app` acceptance proves the restart-safe mainline:

```text
Welcome → optional Skip / Empty Curis
→ CEO Display Identity + Company
→ canonical CEO Assistant presence
→ CEO Desk
→ Business Proposal
→ canonical Business + first General Workspace
→ packaged restart reread
```

The following are **IMPLEMENTED / ACCEPTED** for Batch 1: App Shell; seven-area Navigation; Welcome; optional Skip; truthful Empty Curis; CEO Display Identity; Company Creation; canonical CEO Assistant presence; Empty Company; Model Management UI with the M3 boundary; Create Business Proposal Flow; canonical General Business; first General Workspace materialization; CEO Desk Operating; Company Attention Projection; restart recovery; and the packaged Desktop Batch 1 mainline.

The final evidence includes Browser and packaged Desktop flows, restart/reload, no-fake-data checks, isolated SQLite integrity and unchanged active databases. See the final acceptance for exact paths, hashes, test counts and screenshots.

## Recorded partial boundaries

| Capability | Status | Boundary |
|---|---|---|
| Avatar | IMPLEMENTED / PARTIAL | Preset, fallback and persistence verified; upload interaction and crop decision remain open. |
| Conversation | IMPLEMENTED / PARTIAL | Main path does not fake AI output; legacy floating `GlobalAssistant` remains user-visible, may auto-open, uses a separate identity and can synthesize a local Runtime-summary answer. |
| Composer | IMPLEMENTED / PARTIAL | Attachment slot, Model Selector, Voice affordance and Send exist; attachment and Voice are not connected. |
| Model Selector | IMPLEMENTED / PARTIAL | Session-scoped choice exists; durable cross-restart selection and live-model execution are not accepted. |
| 1024 / Assistant layout | IMPLEMENTED / P1 ADAPTATION DEBT | Functional, but legacy auto-open Assistant compresses the attention surface. |
| First General Workspace operating loop | P1 OPEN | Materialization is accepted; full operating loop is not. |

## Separate blockers and deferred boundaries

- M3 native macOS Keychain is a separate `BLOCKED / SECURITY ISSUE`; it blocks durable cloud credential recovery and packaged restart AI readiness, not Batch 1 acceptance.
- Professional Workspace automatic matcher/materializer is `DEFERRED`; this does not mean Professional Workspace capability is unimplemented.
- Real external AI execution is `NOT VERIFIED BY BATCH 1`.
- Legacy `GlobalAssistant` is `LEGACY / P1 UNIFICATION REQUIRED`, not the Current Accepted CEO Assistant.

## Non-regression rules

`UI ACCEPTED ≠ IMPLEMENTED`; `IMPLEMENTED ≠ V1 COMPLETE`; `PARTIAL ≠ FAILED`; `BLOCKED ≠ 全部阻塞`。No-fake-data, canonical identity, isolated database and restart-safe evidence remain required for later batches.

## Next implementation target

**GENERAL WORKSPACE P1 OPERATING CLOSURE**

First priority: **CANONICAL CEO ASSISTANT / CONVERSATION UNIFICATION**. It requires a separate bounded implementation Issue and must replace/unify the legacy user-visible `GlobalAssistant` without creating a second identity or conversation system.

No Runtime, Schema, DB or code change is authorized by this registration.

**FRONTEND BATCH 1 IMPLEMENTATION ACCEPTANCE REGISTERED**
