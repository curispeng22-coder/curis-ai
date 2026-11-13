# Curis V1 — Whole-App Live AI Acceptance

Status: ACCEPTANCE COMPLETE — PARTIAL / PRODUCT GAP

Owner: Main Development Session

## Goal

Verify one continuous ordinary-user journey in one exact freshly packaged development `Curis.app`:

`Launch → Welcome → CEO identity → Company → CEO Assistant → Model setup → Business proposal → General Workspace → Team/Responsibility → Work/Execution → Result/Evidence → P7 Decision → CEO Desk → full restart → recovery → post-restart real AI`.

This is an Acceptance Issue, not a feature or design initiative.

## Packaged app identity

- App: `/Users/yy/Documents/Curis AI Workspace/desktop/target/release/bundle/macos/Curis.app`
- Executable: `/Users/yy/Documents/Curis AI Workspace/desktop/target/release/bundle/macos/Curis.app/Contents/MacOS/curis-desktop`
- Executable SHA-256: `cabc9d9be89ec65af2511c3670ace505a6668979d542ca7c062d0b2c943c5f5a`
- Bundle id: `com.curis.desktop`
- Version: `0.1.0`

All Desktop evidence must target this absolute path, not a display-name match.

## Isolated acceptance state

- Root: `/tmp/curis-v1-whole-app-live-ai-20260830-01`
- SQLite: `/tmp/curis-v1-whole-app-live-ai-20260830-01/data/curis.sqlite`
- CEO display name: `Whole App CEO`
- Company: `Whole App Acceptance Company`
- Business intent: a small non-sensitive general business used only to prove the current product chain
- Credential: CEO-entered DeepSeek test credential through packaged Model Management only

The journey starts with zero Company, Business and Workspace records. No API fixture or direct
backend materialization may replace the product UI.

## Interaction and evidence

- Primary: packaged Tauri window through path-specific native Computer Use.
- Manual native interaction is allowed where the CEO must enter a credential or where the native
  automation bridge cannot perform a real click.
- Browser/API/SQLite may support diagnosis but cannot replace Desktop product evidence.
- Screenshots, safe object identifiers, Runtime status and restart/process evidence are stored only
  under the isolated acceptance root or this Review.

## Exact acceptance journey

1. launch exact package into fresh isolated state;
2. complete Welcome, CEO identity/avatar and Company creation through UI;
3. confirm one canonical CEO Assistant;
4. configure DeepSeek through Model Management, pass real Health/discovery and set a default;
5. exercise direct CEO AI conversation only if it exists; otherwise record the precise P1 gap;
6. create a canonical General Business and first General Workspace through the product flow;
7. observe truthful Team/Responsibility/Employee state without inventing missing staff;
8. create and execute one minimal safe Work through UI using the actual selected capability;
9. read Result/Evidence/owner/source/responsibility through UI;
10. observe a legitimate Handoff only if the chosen Work creates one;
11. complete one real P7 Decision Packet round-trip and verify CEO Desk Attention;
12. fully close the exact app and sidecars, then reopen the same package/root;
13. recover identity, Company, Assistant, Provider/Model, Business, Workspace, Work, Result/Evidence
    and Decision without duplicates or credential re-entry;
14. execute one minimal post-restart real AI call;
15. retain or delete the test credential only according to the CEO's choice.

## Stop gates

- `WAITING FOR CEO CREDENTIAL INPUT` at the exact packaged API Key field;
- any fake Health, Employee, Result, Evidence, Decision or AI answer;
- active database mutation;
- need for a Product Contract, schema or feature change;
- inability to distinguish the exact package from another same-name Curis process;
- secret exposure in logs, files, URL, persistence, evidence or Git diff.

## Database safety preflight

| Path | Size | mtime | SHA-256 | integrity_check |
| --- | ---: | ---: | --- | --- |
| `data/curis.sqlite` | 1232896 | 1786873339 | `2ea2506f90f764e834d47d8f6bae3cb41c22d457757e0e9216c0ae8c39a39ec6` | ok |
| `backend/data/curis.sqlite` | 1277952 | 1786783659 | `a9d96a9536a5bce3b3b30f912e86a37f61d28527a8eb2d35af7a5857d29414e4` | ok |

## Explicit exclusions

No feature development, Figma, Product redesign, Provider/Keychain changes, schema changes,
signing/notarization, active database access, commit or push.

## Delivery

The final evidence record is
`docs/reviews/CURIS_V1_WHOLE_APP_LIVE_AI_ACCEPTANCE.md` with a step-by-step matrix and one of:
PASS, PASS WITH RECORDED P1 GAPS, PARTIAL / PRODUCT GAP, or FAIL.

## Acceptance result

- Final verdict: `PARTIAL / PRODUCT GAP`.
- Passed: exact packaged launch, fresh Welcome/identity/Company, canonical CEO Assistant,
  CEO-entered DeepSeek credential, real Health/model discovery/default model, General Business and
  first Workspace creation, truthful missing-team state, employee recruitment, full process exit,
  same-root restart, Keychain-backed Health/model rediscovery without credential re-entry, and
  active-database/secret safety.
- Product break: the recruited Company employee cannot be assigned to the generated
  `business.general` department/Workspace through the current product UI. The Workspace therefore
  remains at zero responsible employees, and `交给负责员工` remains disabled.
- Consequence: no legitimate Work, Provider execution, Result/Evidence, Handoff, P7 Decision or
  post-restart AI execution could be produced. No fixture or direct API materialization was used to
  bypass the break.
- Direct CEO AI conversation is also not implemented: the visible CEO Desk conversation is a
  read-only projection (`value=""`, no-op change handler, no submit handler), so its Send action is
  correctly disabled rather than fabricating a response.
- Test credential was not deleted because no destructive cleanup authorization was given; it remains
  in the local native Keychain pending the CEO's explicit retain/delete choice.
- Formal record: `docs/reviews/CURIS_V1_WHOLE_APP_LIVE_AI_ACCEPTANCE.md`.
