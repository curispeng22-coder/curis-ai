# CURIS V1 — Whole-App Product Gap Closure Review

Status: Review

Authority Class: EVIDENCE / FORMAL ACCEPTANCE RECORD

Issue: `CURIS-V1-WHOLE-APP-PRODUCT-GAP-CLOSURE-001`

Date: 2026-08-30

## Verdict

`WHOLE-APP LIVE AI ACCEPTANCE: PASS WITH RECORDED P1`

`PRODUCT GAP CLOSED`

This verdict is scoped to the accepted fresh packaged journey. It does not claim all Providers,
external publishing, distribution signing/notarization, or every Curis module is accepted.

## Packaged identity and isolated state

- App: `/Users/yy/Documents/Curis AI Workspace/desktop/target/release/bundle/macos/Curis.app`
- Executable SHA-256: `cabc9d9be89ec65af2511c3670ace505a6668979d542ca7c062d0b2c943c5f5a`
- Isolated root: `/tmp/curis-v1-whole-app-live-ai-20260830-01`
- Isolated SQLite integrity: `ok`
- Native surface: packaged Tauri WebView operated through macOS accessibility/Computer Use

## Accepted vertical chain

1. A real recruited `Product Manager` Employee was selected in the General Workspace.
2. One canonical Role, Employee bridge, Responsibility Assignment and Responsibility Workflow were
   persisted for the same Company/Business/Workspace.
3. A legal Work was created from the Workspace and routed to that Employee.
4. CEO Assistant composer called the selected `deepseek-v4-flash` model and persisted the real CEO
   and Assistant messages.
5. Work execution called the real DeepSeek Provider. No fixture or local fallback supplied results.
6. The completed Work exposed real Result, Evidence and Artifact references. Conversation retained
   only a readable summary and references.
7. A failed retry exposed a real canonical attribution defect; the shared resolver was corrected to
   identify the current Task/Execution among multiple attempts for one Work. The next retry completed.
8. A second legitimate Work created exactly one high-risk `DECISION_PACKET` from the real prior
   Result/Evidence. No Handoff was fabricated because responsibility did not transfer.
9. Banner, Workspace package and detail all referenced
   `decision_packet-ab813d9b-33c3-48e4-839f-cb1cecce8eea`.
10. Layer 0 showed only `查看方案` and `暂缓`. Layer 1 retained FACT/EVIDENCE/EST/UNK provenance.
11. CEO chose `COLLECT_MORE`; the same packet transitioned `WAITING_CEO → APPLIED`, the original
    responsibility resumed automatically, and real execution completed without a manual next-step
    button or second Decision Packet.
12. CEO Desk received the canonical attention projection and the Workspace remained directly
    reachable from it.

## Runtime evidence

- Company: `company-a0460ff7-3510-458a-a35e-06687fcca9f9`
- Workspace: `workspace-first-7f979f2781d4f536644695af`
- Employee: `emp-f1ca6bd6-171c-4c87-b175-b98904418cea`
- Initial Work: `work-04cdfc5d60ada178f1fbc4ea09182467`
- Decision Work: `work-5ef9b134c27eb697ed5aec2e8d720b61`
- Decision Packet count: 1; final state: `APPLIED`
- Runtime counts: 1 Employee, 1 Assistant, 2 Cycles, 2 Works, 1 Responsibility Assignment,
  1 Responsibility Workflow, 1 Role Slot and 1 Decision Packet.
- Task outcomes: 3 `COMPLETED`, 1 `FAILED`.
- Canonical AI usage records: 3. Failed pre-Provider attribution did not fabricate Provider usage.
- Final decision Work: holder retained, Current Executor empty, real Result/Evidence/Artifact present.

## Restart and Keychain truth

The final packaged app and all of its sidecars were stopped, then the same absolute package and same
isolated root were reopened.

- No `SecurityAgent` prompt appeared.
- The saved native Keychain credential recovered without re-entry.
- Model status returned to `AI 已准备`; `deepseek-v4-flash` remained available.
- Both Works remained completed with the same persisted references.
- The Decision Packet remained `APPLIED`; no duplicate packet, Work or Employee was created.
- CEO Assistant conversation remained present and a post-restart real call returned
  `重启后已恢复。`

Repeated credential prompts observed earlier were caused by launching newly rebuilt, ad-hoc signed
packages with changed macOS code identity. They were not credential loss. A duplicate old Curis app
with the same Bundle ID also caused LaunchServices to activate the wrong package once; the final
acceptance explicitly registered and launched the exact package above.

Evidence images:

- `/tmp/curis-v1-whole-app-live-ai-20260830-01/p7-decision-applied-completed.png`
- `/tmp/curis-v1-whole-app-live-ai-20260830-01/post-p7-restart-workspace.png`
- `/tmp/curis-v1-whole-app-live-ai-20260830-01/post-restart-model-revalidation.png`

## Tests and build

- Backend focused/no-regression: `37 passed`.
- Canonical attribution focused suite after the retry correction: included and passing.
- Frontend focused tests: `7 passed`.
- ESLint: PASS.
- Python compile: PASS.
- `git diff --check`: PASS.
- Production frontend and fresh Tauri package build: PASS.
- Packaged native Work, P7, restart and post-restart paths: PASS.

The regression scope included General Workspace P1, canonical usage attribution, Employee identity,
Team Operating real Employee execution, RD real execution and XHS Calendar/Note Runtime.

## Secret and database safety

- Isolated state/log/artifact secret-pattern hits: 0.
- Issue-owned source/test/document secret-pattern hits: 0.
- The API Key was never read, copied, printed, placed in chat, environment, SQLite or source.
- Credential remains in native Keychain by CEO choice; it was not deleted.

| Active SQLite | Size | mtime | SHA-256 | integrity |
| --- | ---: | ---: | --- | --- |
| `data/curis.sqlite` | 1232896 | 1786873339 | `2ea2506f90f764e834d47d8f6bae3cb41c22d457757e0e9216c0ae8c39a39ec6` | ok |
| `backend/data/curis.sqlite` | 1277952 | 1786783659 | `a9d96a9536a5bce3b3b30f912e86a37f61d28527a8eb2d35af7a5857d29414e4` | ok |

Both repository active databases remained byte-identical. All acceptance writes used the external
isolated SQLite.

## Recorded P1 / later gates

1. CEO Desk still exposes Employee refs and internal statuses such as `PLANNED` and
   `RESPONSIBILITY_ASSIGNMENT`; these should be translated to ordinary-user language.
2. An `APPLIED` Decision remains in low-rank continuous attention instead of moving to a compact
   history/result presentation.
3. Stable Developer ID signing/notarization is required before distribution so rebuilt packages have
   stable macOS Keychain identity and LaunchServices selection.
4. External publishing/connectors and broad release acceptance were outside this Issue.

No P0 gap remains in the scoped chain. No commit or push was created.

`STOP FOR CEO / CHATGPT WHOLE-APP PRODUCT GAP REVIEW`
