# XHS-WORKSPACE-INSTANCE-001 Review

**Status:** XHS IMPLEMENTATION ACCEPTED
**Date:** 2026-08-15
**Scope:** Phase 0–6, first XHS Workspace vertical slice
**Record type:** Formal Acceptance Record
**Isolation:** `/tmp/curis-xhs-phase6-ywHEww/curis.sqlite` only; no active database, secret, platform account, or external publication used.

## Result

The XHS Workspace vertical slice is runtime-backed through `SCHEDULED` and is accepted as
Instance v1. It does **not** claim a real XHS publication or analytics integration.

```text
Calendar (four Notes on one date)
→ selected Note / three-pane office
→ persisted Note version
→ real Employee references
→ persisted HANDOFF
→ one DECISION_PACKET WAITING_CEO
→ CEO APPROVE
→ same packet APPLIED; Note SCHEDULED
→ executor none + publish System Activity waiting
→ no trusted receipt; no analytics metrics
```

The two execution-completion calls used to create the review input were explicit Runtime Simulation only. They did not invoke an XHS connector, publish content, or produce an external result.

## Runtime evidence

- Main Note: `content_item-7aff…f211`, persisted as `SCHEDULED` after the CEO choice.
- Handoff: `handoff-6bef…e86`, parent is that same Note, lifecycle `ACKNOWLEDGED`; both references resolve to actual scoped `AI_EMPLOYEE` entities.
- Decision: `decision_packet-bad5…3916`, parent is that same Note, lifecycle `APPLIED` after CEO approval. The Employee conversation, Layer 0 banner, and P7 package were all projections of this one packet.
- Packet provenance was visible in Browser: FACT, POLICY and UNK labels accompany happened, options, impact, risk, cost, recommendation and reason.
- Current Note context after approval: `PUBLISH_EXECUTION`, `waiting`, and `currentExecutorRef = null`. No employee is presented as publishing or analysing.
- A `CEO_MANUAL` receipt fixture remains `UNVERIFIED`; generic CEO transition to `PUBLISHED` is rejected. A Note becomes `PUBLISHED` only from an existing verified `PLATFORM_API` receipt with an external ID.
- Analytics projection remains `UNAVAILABLE` / no metrics with no verified data source.

## Browser evidence

Fresh local Browser session, `localhost:3001`, isolated backend `127.0.0.1:8022`:

1. Calendar showed four same-day Notes, including the required `+1 篇` density treatment.
2. A Note selection opened Split Working; Context showed an honest no-signal state and Utility showed only the saved Note version.
3. Browser saved a real draft version for `同日排期 Note 2`; its body and tags reappeared in Utility after reload.
4. The review Note showed actual employee responsibility/executor before CEO review, an `ACKNOWLEDGED` Handoff, CEO-readable Conversation, Layer 0 actions, and P7 detail for the same packet.
5. Choosing `按建议处理` moved the Note to `已排期` with no manual “next step” button. Publication became `等待发布能力`; analytics remained `暂无数据`.
6. T1 navigation, T2 Context, T3 Utility, Utility maximize dialog, scoped Search empty state, and navigation collapse were exercised. No browser console error was reported.

One transient “暂时无法读取运营办公室” surface appeared immediately after a development hot refresh during `开始起草`; the `accept-idea` request had already returned 200 and a single `重新读取` showed the persisted DRAFT. It did not recur after the same-DB backend restart, but it is not counted as a failure/recovery acceptance proof.

## Persistence evidence

- Backend was stopped and restarted with the same isolated `CURIS_DB`.
- The same selected workspace and review Note reloaded as `SCHEDULED`, retaining Handoff, applied Decision Packet, waiting publish activity and no analytics.
- The independently saved Note version reloaded with its body and tags.
- `PRAGMA integrity_check` returned `ok`.

## Focused checks

```text
backend/.venv/bin/python -m pytest backend/tests/test_xhs_calendar_note_runtime.py backend/tests/test_runtime_workspace_foundation.py -q
14 passed

node --test frontend/tests/runtimeWorkspaceUi.test.mjs
7 passed

frontend: eslint on XHS/runtime API files
passed

frontend: npm run build
passed; 45 routes generated
```

The Python suite emitted pre-existing FastAPI deprecation warnings. Node emitted the existing module-type warning for `runtimeApi.js`; neither failed the checks.

## No-regression boundary

- No RD or TTK source file was changed.
- The focused UI test confirms RD and TTK retain the legacy Runtime view while XHS uses the isolated Workspace shell.
- The focused shared Runtime Foundation suite passed.

## Acceptance closure: resizable panes and packaged Desktop

- A fresh current-source Tauri app was built on 2026-08-15. Its embedded runtime manifest records `builtAt: 2026-08-15T10:07:07Z`.
- The app was launched directly with an isolated temporary HOME. Its only database was `/tmp/curis-xhs-desktop-home.gmZFUJ/Library/Application Support/com.curis.desktop/data/curis.sqlite`; it did not read or write the active database.
- Real pointer drags widened Context continuously, then widened Utility continuously while both were open. Further drags hit the rendered min/max limits without overlap; Main narrowed responsively and headers remained aligned.
- Utility close → reopen worked. Utility maximize → exit restored the three-pane layout and the adjusted widths. T1 navigation, T2 Context and T3 Utility remained visible.
- In the packaged app, Portal → XHS Calendar → Note showed Employee Presence, Handoff, the P7 conversation/banner/detail, and one CEO `按建议处理` action. The same Note then read `SCHEDULED`, `PUBLISH_EXECUTION waiting`, no executor, `等待发布能力`, and `暂无数据`.
- Packaged frontend and gateway error logs were empty. Workspace log contains only the pre-existing non-fatal `D1 toolchain unavailable; service continues without it` startup notice; XHS requests and state transitions completed normally.

## Changed files

- `backend/app/runtime/workspace.py`
- `backend/app/api/runtime_foundation_router.py`
- `backend/tests/test_xhs_calendar_note_runtime.py`
- `frontend/components/xhs/XhsWorkspacePhaseOne.js`
- `frontend/lib/runtimeApi.js`
- `frontend/tests/runtimeWorkspaceUi.test.mjs`
- `issues/XHS-WORKSPACE-INSTANCE-001.md`
- `docs/04_Development/XHS_IMPLEMENTATION_GAP_AUDIT.md`
- `docs/04_Development/XHS_RUNTIME_ARCHITECTURE_REVIEW.md`
- `docs/04_Development/XHS_IMPLEMENTATION_PLAN_v1.md`

## Remaining issues / review limits

1. **No real XHS publishing connector or analytics connector is configured.** This is accurately shown as waiting/unavailable; no publication, receipt, date, metric or trend is fabricated.
2. The implementation does not yet claim an external publishing/analytics recovery scenario because no connector failure can truthfully be induced without an actual connector.

## Review decision

The XHS Instance is accepted. Real publishing and analytics remain explicit unconnected capability limits, not a reason to fabricate product output.
