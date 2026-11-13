# CURIS V1 — CEO DESK OPERATING UI ACCEPTANCE

**Status:** Frozen
**Authority Class:** FROZEN / UI ACCEPTANCE RECORD
**Disposition:** CEO DESK PRODUCT STRUCTURE ACCEPTED; OPERATING COMPOSITION ACCEPTED; OPERATING UI ACCEPTED
**Implementation:** PENDING ENGINEERING RECONCILIATION (not implemented)
**Date:** 2026-08-28

## Current design baseline

- Figma: [Curis V1 — App Entry & CEO Assistant Experience](https://www.figma.com/design/2Fh7DgPPfLgdbvNtnzPnk9/Curis-V1-App-Entry-CEO-Assistant-Experience)
- File key: `2Fh7DgPPfLgdbvNtnzPnk9`
- Frame: `CEO Desk — Operating / Matters Present`
- Node: [`69:3`](https://www.figma.com/design/2Fh7DgPPfLgdbvNtnzPnk9/Curis-V1-App-Entry-CEO-Assistant-Experience?node-id=69-3)
- Accepted scope: 1440 × 900, Light, Operating / Matters Present

## Accepted reading model

```text
Company State
→ Today Brief
→ Primary Matter
→ Watching
→ Important Result
→ Next Responsibility
→ CEO Assistant（按需）
```

These are information and attention responsibilities, not mandatory independent cards. CEO Desk is attention-first, not a Dashboard, Task Manager, Notification Center, Analytics page, Business list or Chat Homepage. Business / Workspace / Employee appear as Matter, Result and Responsibility context.

## Shared patterns

Reuse the accepted App Entry patterns: seven-area navigation, Sparse Iris cue, CEO Display Name + Avatar, Pane-local Shell, Direction D, CEO / Employee Conversation, Composer, Model Selector, Structured Surface and Neutral Foundation. CEO Assistant remains a Company-level coordinator with lightweight presence and on-demand Conversation; it does not occupy the Main Primary.

## Remaining adaptation / engineering boundary

Dark, 1024, higher Matters density, Assistant / Decision / Evidence expanded states, real Attention Ranking, Runtime data projection, accessibility and small optical polish are `ADAPTATION / VALIDATION ONLY`; they do not reopen `69:3`. Historical `81:113`, `81:3` and old HTML remain provenance/reference. Old green, Dashboard/Card Wall, fixed Assistant sidebar, six-area navigation and hardcoded Business copy are `SUPERSEDED FOR CURRENT UI`.

Next: `CEO DESK IMPLEMENTATION / ADAPTATION READINESS REVIEW`. No Figma, Frontend, Runtime, Schema, DB or Prototype implementation is implied.

**CEO DESK OPERATING UI ACCEPTANCE REGISTERED**
