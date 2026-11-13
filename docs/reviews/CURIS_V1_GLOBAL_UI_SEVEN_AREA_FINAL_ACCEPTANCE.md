# Curis V1 — Global UI / Seven-area Final Acceptance

Status: Review
Authority Class: REVIEW / EVIDENCE
Disposition: PRODUCT COMPLETE — ACCEPTED WITH RECORDED P2; CEO final review required
Owner: Main Development
Date: 2026-09-08
Source: CEO final seven-area instruction and current accepted area records.
Issue: CURIS-V1-GLOBAL-UI-SEVEN-AREA-FINAL-ACCEPTANCE-001.

## Final verdict — 2026-09-08 authorized native closure

CURIS V1 PRODUCT: PRODUCT COMPLETE within the accepted V1 scope.
Seven primary areas: ACCEPTED. Global UI: ACCEPTED WITH RECORDED P2.
Release authorization: NOT GRANTED. No commit, staging, push or release.
The checkpoints below are historical evidence, not remaining authorization gates.

CEO native authorization succeeded. Task `88e798fa-83fb-4ac0-916c-8b436dcf1bbc`
completed at 2026-09-08 12:58:22 with one real provider request
`72173f4a-c496-4909-adad-09512d2bd70f`, artifact
`artifact-d78270c9-463c-409c-91dd-517f621e8caf`, evidence event `150`.
Its Work remained PAUSED, holder remained 小策, current executor became null.
Native Workspace displayed that distinction and the actual returned summary.
Explicit native Result open displayed readable content, not JSON; closing it
returned to the same Workspace. No additional model call was initiated here.
Business and Workspace both now show six result references (not six independent
completed Works). Existing task/artifact reference semantics are retained.

After normal quit, :3010/:8002/:8080 and matching app/sidecar processes were absent.
The exact same package was relaunched with all three DB variables and
CURIS_DESKTOP_DATA_ROOT pointing to `/tmp/curis-ceo-native.ydOJRf`.
Actual native clicks recovered CEO → same Conversation → Organization/Employee
directory → Talent → Insights → Knowledge → same Meeting/P7 → CEO.
The latest viewed Result did not reappear in Attention. The distinct unviewed
result and WAITING_CEO decision correctly remained. No Meeting cloud run was made.

Post-authorization counts: Tasks 6, executions 5, artifacts 5, Usage 6,
Knowledge 1, runtime entities 24, conversation/viewed events 10.
First restart preserved all these counts and every table hash except Tasks.
The new Task's execution_state_changed_at equals startup time; database.py's
existing null timestamp backfill explains the likely source. Without a full
pre-restart row snapshot this first Task hash delta is not claimed exactly proven.
A second full quit/restart then preserved **all seven complete row-set hashes**,
including Tasks. No duplicate Work, reply, result, execution or Usage occurred.
Stable hashes: Tasks `f06ffb75822d7c908b9d458546204bf6971497a8d0172c653ed33a903bba58e2`;
runtime entities `58ee37beded3b65c98a58a48b5ab9cacffd2f1831d88c735b54d4fa232ede305`;
conversation/viewed `e4c3a3f91333a1f5a18ebc70a944cbd3ed4126697ae5fc7c9b7d86c2cfebadcb`;
Usage `d96e072a44e3b655535003779314e96349e381715ba5e7118d936ed4cedbcfde`.

### Whole-product matrix

| Area | Product | UI | Frontend | Runtime | Native | Restart | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CEO Desk | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| Business / Workspace | PASS | PASS | PASS | PASS | PASS | PASS | PASS WITH FOLLOW-UP |
| Organization | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| Talent | PASS | PASS WITH FOLLOW-UP | PASS | PASS | PASS | PASS | PASS WITH FOLLOW-UP |
| Operating Intelligence | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| Knowledge | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| Meeting | PASS | PASS | PASS | PASS | PASS | PASS | PASS WITH FOLLOW-UP |

Runtime PASS preserves each accepted area's boundaries; it does not assert
external connectors, future formats or final Meeting multi-cycle cloud acceptance.

### Horizontal matrix

| Capability | Cross-area verdict |
| --- | --- |
| Navigation / canonical identity / return | PASS; seven entries, no eighth area |
| Employee identity / Conversation / Composer | PASS; persisted reply and identity restored |
| Work / Result / Evidence | PASS; paused Work and completed attempt remain distinct |
| Decision | PASS; existing P7 reference; artificial navigation fixture disclosed |
| Attention | PASS; viewed receipt survives, unhandled decision remains |
| References | PASS; original canonical objects, no duplicate truth |
| Error language / Direction D | PASS WITH FOLLOW-UP; bounded corrections only |
| Persistence | PASS; stable full restart hash comparison above |

Native evidence in the isolated root: `seven-authorized-native-result.png`,
`seven-authorized-restart-conversation.png`, `seven-authorized-restart-employees.png`,
`seven-authorized-restart-talent.png`, `seven-authorized-restart-insights.png`,
`seven-authorized-restart-knowledge.png`, `seven-authorized-restart-meeting.png`.
Browser 1440×900 and prior fresh-native journey evidence remains listed below.
Browser is not substituted for Desktop. Native tested its actual window size;
1440×900 Light is the Browser visual baseline. Talent screenshot confirms the
shared neutral/Iris shell and row/detail hierarchy, not a redesigned catalog.

### Tests, safety and remaining scope

Selected backend 58 PASS; new frontend focused 6 PASS; full frontend 89/95,
six previously documented legacy expectation failures, not an all-green claim.
Scoped ESLint, Python compile, production/sidecars/Tauri package and diff check PASS.
The three protected SQLite size/mtime/SHA match intake exactly; integrity=ok.
Their unchanged fingerprints are retained below. Isolated state alone was written.

Recorded follow-ups: legacy frontend assertion maintenance; startup old-company
cache transient; null Task timestamp initialization; official English expert
template names and small visual polish; global search remains truthfully disabled;
Dark/1024, full accessibility and independent native-console certification;
future connectors/formats; Meeting final multi-cycle real-world evidence.
These are not renewed P1 implementation gates. No claim of zero native console
messages or external analytics/publishing connectivity is made.

Owner: Main Development. Next gate: CEO / ChatGPT final product review.
Remaining blocking P1: None identified by this bounded acceptance.

## Historical checkpoint

This is an intermediate evidence record, not a product-complete registration.
Accepted area implementations are preserved. Current fixes cover shared
navigation selection, unavailable search, result display title and bounded
ordinary-language labels. Result title now comes from scoped canonical
Work/Cycle facts; execution prompts remain unchanged and are not displayed as
Attention titles. No second data authority or execution state was introduced.

## Evidence to date

- Backend: 47 focused tests passed across projection/routes, conversation,
  attention, usage, organization, talent, knowledge and DB safety.
- Frontend focused: 10 passed. Entire existing set: 85 passed / 6 failed.
  Failures assert legacy workforce/Assistant/nav/layout wording and previous
  gateway config syntax. Do not treat these as a green suite; disposition is
  pending final reconciliation.
- Scoped ESLint PASS; Python syntax PASS; git diff --check PASS.
- Fresh frontend production/sidecars/Cargo/Tauri build PASS.
- Native CEO now shows business problem rather than embedded context JSON;
  Business/Workspace/Organization navigation works on same isolated data.
- Screenshots: `/tmp/curis-ceo-native.ydOJRf/seven-fresh-ceo.png`,
  `seven-fresh-workspace.png`, `seven-fresh-organization.png`.
- Package: `/Users/yy/Documents/Curis AI Workspace/desktop/target/release/bundle/macos/Curis.app`.
  Main binary SHA256 fe66764ff1ae6e2e62aa29ccd534be5ebb26ac82027373989baf7d24d160bd1d.
  Main binary unchanged is expected for frontend/sidecar-only corrections;
  build command actually regenerated package resources.

## Remaining checks

Complete continuous Browser and native seven-area journey, reference return,
same-root full restart/no duplicates, final DB comparison and matrices remain.
Observed role keys in employee/talent projection and some technical wording
still need bounded reconciliation. General avatar fallback is a recorded
minor identity presentation issue; do not substitute mock identity.

## Authorization gate resolved / continuing verification

Same authorized external root: `/tmp/curis-ceo-native.ydOJRf`.
CEO completed native authorization. DeepSeek recovered and one bounded real
Employee reply was persisted: 小策 replied “已收到验收说明” in conversation
conversation-ffc46060999cea278fa0f248750a77e37f9e961477164dc0ccbc22725e536ec1.
Native Employee Detail and return restored the same messages and participant.
No credential was read/copied and no bypass attempted.

Additional focused backend tests: 6 PASS (Meeting productization, General
operating contract, scoped result title). Frontend selected regressions: 9 PASS.
Result explicitly opened through CEO Attention reduced existing result attention
from two to one; source history remained. A subsequent restart preserved the
same conversation/reply, usage count 5, executions 4, artifacts 4, Knowledge 1,
and nine conversation/viewed events. Task row checksum differs; per-field restart
reconciliation is still required before final no-replay verdict.

An explicitly labeled artificial navigation fixture was created ONLY in external
SQLite through MeetingService and legal Decision transitions, without an execution
adapter or cloud calls: meeting-92d9e0f7-7a40-4a66-b779-9336d9c8f09c / decision_packet-b525338ed7c6aae981db811292983346dc61032e2fc4d1c7af90db4132afb9e9.
Native Meeting → View options opened that WAITING_CEO P7 packet. This proves
product entry/projection, NOT autonomous Meeting cloud proposal generation.

## Protected DB / git

Latest read-only verification matches all three Issue intake fingerprints,
including size/mtime/SHA256 and integrity=ok. No protected DB write/launch.
No staging, commit, push, reset, clean or stash. Unrelated worktree preserved.

PRODUCT COMPLETION: NOT YET VERIFIED.
PRODUCT RELEASE AUTHORIZATION: NOT GRANTED.
Next action: final package/Browser journey, precise restart comparison and final matrices.

## 2026-09-08 final-package checkpoint — native authorization required

Bounded integration corrections additionally completed:
- Existing General delivery already excludes `meeting:` workflows; its read
  projection now uses the same filter. A legitimate isolated navigation Meeting
  no longer falsely blocks General readiness.
- Business summary reuses the existing scoped Workspace result projection:
  native Business and Workspace both show four existing result references.
  Result references include their existing artifact/evidence forms; this is not
  a count of four independently completed works.
- General pending execution now polls canonical progress without blocking pause/
  stop; synchronous duplicate submit is guarded. It never invents RUNNING.
- Existing role translations, P7 provenance wording, result summary disclosure,
  recruitment Escape, Employee details and avatar fallback are reconciled.

Final selected backend regression command: result-title/readiness, Business
Spine, General operating, Meeting productization, Shared Workspace, Insights,
Conversation/Attention, DB Safety, Conversation Usage, Employee Conversation and
Conversation productization: **58 PASS**. Frontend all: **89/95 PASS, 6 FAIL**;
same previously identified legacy assertions, not represented as a green suite.
New seven-area focused suite: **6 PASS**, including an executable deferred-
promise duplicate-submit/control-lock test. Scoped ESLint and Python AST compile
PASS; production/sidecars/Cargo/Tauri fresh package PASS; diff check PASS.

Browser at 1440×900 Light followed CEO → same persisted Conversation → Business
→ Workspace → explicit real Result → close → Knowledge → Insights → Organization
→ Employee directory → Talent → Meeting → P7 → CEO. Error/warn log query returned
[]. Screenshots in external root `seven-browser-*-1440.png`. Decision navigation
uses the labeled artificial fixture described above, not autonomous cloud proof.

Fresh native package showed corrected Business count 4, Workspace count 4,
General readiness READY, then created one explicitly artificial test Work
`work-f608a33a98c99ebe47d830ded6c1ef45` using the product form. Start processing
returned control; polling showed Runtime pending execution, with pause/stop
enabled. Real native click Pause persisted lifecycle PAUSED. No completed output
is claimed for this Work. At checkpoint Tasks=6, executions=4, artifacts=4,
Usage=5: no additional confirmed cloud usage from that pending request.

New package model recovery remains pending; SecurityAgent PID11975 is present.
Do not bypass native authorization. Earlier CEO authorization and real Employee
reply remain valid evidence; this new pending attempt is not another verified
cloud completion. Main app PID11898; external root unchanged. Current app stays
open for CEO authorization. Final stop/restart verification of this newest
pending Work is not yet complete.

Native evidence: `seven-final-native-business.png`,
`seven-final-native-running-controls.png`, `seven-final-native-paused.png`,
`seven-final-restart-conversation.png`. Package absolute path above; main SHA
unchanged, freshly regenerated resources are required to identify this build.

An intervening full restart comparison of all Task fields returned no changes;
earlier first-restart Task hash delta is not claimed byte-identical. Existing
conversation/viewed events, usage, executions and artifacts retained hashes.

All three protected DB size/mtime/SHA still exactly match intake, integrity=ok.
External SQLite integrity=ok. Staged=0; all unrelated dirty/untracked preserved.
No commit/push. **Final whole-product acceptance remains IN PROGRESS**, not
PRODUCT COMPLETE; next gate is native authorization followed by remaining final
Desktop/restart/matrix registration. No new architecture or release approval.
