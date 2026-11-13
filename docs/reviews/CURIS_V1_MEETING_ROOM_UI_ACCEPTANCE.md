# CURIS V1 — MEETING ROOM UI ACCEPTANCE

Status: Frozen
Authority Class: CURRENT UI ACCEPTANCE / DESIGN BASELINE
Date: 2026-09-02
Disposition: UI ACCEPTED

## Accepted result

- **Meeting Room Product:** ACCEPTED
- **Meeting Room UX:** ACCEPTED
- **Meeting Room UI:** UI ACCEPTED（1440 × 900 Light）
- **Current Figma baseline:** `214:3` Overview · `247:2` Start Meeting Overlay · `214:279` Active Conversation · `214:555` Decision Moment · `214:831` Responsibility + Result Continuity
- **Remaining P1:** None

## Source authority

This registration consumes the Current Meeting semantics already expressed in the Product Blueprint / Master Map, the Current UI Blueprint meeting surface, Frozen Shell / Conversation / Composer / Decision / Responsibility / Work / Result / Evidence authorities, and the registered three-area design asset recovery. The Figma frames are the Current Design Baseline for this bounded UI acceptance; they do not supersede Product Truth or prove implementation.

## Frozen product/UI responsibilities

- Meeting Room is a persistent discussion space for real operating matters. Its product chain is `Conversation → Evidence / Proposal → Decision → Responsibility → Work → Result / Review → Continue / Close`.
- Overview → temporary Start Meeting Overlay → Start Meeting creates one persistent Meeting identity. The overlay is not a second Meeting page.
- Participants come from canonical Company Employees. Recommendations are not automatic invitations, and no Meeting Contacts or second Employee system is introduced.
- CEO participation may be **参加讨论** or **只在需要我决定时通知**. CEO view/session lifecycle does not end the Meeting; leaving and returning preserves the same Meeting.
- The conversation uses a mature group-chat pattern with structured operating messages: Evidence Reference, Proposal, Decision Request / Result, Work Created and Result Returned. Meeting reuses the canonical Decision / P7, Responsibility, Work and Result; it is not a Workspace copy.
- Overview may show current and recent meetings. Only a truly ended/archived Meeting enters history; leaving the page does not archive it.

## Productization boundary

UI acceptance does not claim Runtime / Data implementation. The next gate is **MEETING ROOM PRODUCTIZATION CLOSURE**, beginning with a canonical runtime audit. Implementation must prove persistent Meeting identity, participants, context references, conversation, proposal state, canonical Decision linkage, Responsibility / Work creation, bounded continuation after CEO leaves, Result return to the same Meeting, truthful history and restart recovery. Missing identity, relation or persistence must stop at a precise architecture gate; Frontend must not fabricate it.

The historical `coverage-exploration-2026-08-17/06-meeting.html` remains historical structure input, not the Current Visual Authority. No Figma edit, Frontend, Backend, Runtime, Schema, DB, redesign, release, commit or push was performed by this registration.
