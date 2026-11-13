# Curis V1 — Whole-App Live AI Acceptance

Status: Review

Authority Class: EVIDENCE

Disposition: PARTIAL / PRODUCT GAP

Date: 2026-08-30

Owner: Main Development Session

Issue: `issues/CURIS-V1-WHOLE-APP-LIVE-AI-ACCEPTANCE-001.md`

## 1. Final verdict

`WHOLE-APP LIVE AI ACCEPTANCE: PARTIAL / PRODUCT GAP`

The exact packaged application completes fresh entry, local CEO/Company creation, real DeepSeek
setup, canonical Business/Workspace creation, employee recruitment and restart recovery. The
ordinary-user journey then breaks before the first Work: a recruited Company employee cannot be
joined to the generated Workspace/department and cannot receive its Responsibility through the
current UI. Curis truthfully blocks execution instead of inventing an employee or result.

## 2. Packaged bundle identity

- App: `/Users/yy/Documents/Curis AI Workspace/desktop/target/release/bundle/macos/Curis.app`
- Executable: `/Users/yy/Documents/Curis AI Workspace/desktop/target/release/bundle/macos/Curis.app/Contents/MacOS/curis-desktop`
- Executable SHA-256: `cabc9d9be89ec65af2511c3670ace505a6668979d542ca7c062d0b2c943c5f5a`
- Bundle id: `com.curis.desktop`
- Version: `0.1.0`
- Evidence targeted the absolute path. An unrelated same-name app from worktree `d126` remained
  excluded from all acceptance steps.

## 3. Isolated state and interaction method

- Root: `/tmp/curis-v1-whole-app-live-ai-20260830-01`
- SQLite: `/tmp/curis-v1-whole-app-live-ai-20260830-01/data/curis.sqlite`
- Interaction: path-specific packaged Desktop through `@oai/sky`; the CEO performed the only secret
  action by entering the DeepSeek key in the native product UI.
- Native mouse actions intermittently returned `native pipe closed before response`; keyboard and
  the CEO's manual credential action were used. This was not classified as a Curis product failure.
- No API or fixture created Company, Business, Workspace, employee or operating objects.

## 4. Journey evidence

| Step | Result | Actual evidence |
| --- | --- | --- |
| Launch | PASS | Exact packaged binary opened against a fresh external root. |
| Welcome | PASS | Fresh `/welcome` contained no Company, Business or Workspace. |
| CEO identity | PASS | UI created `Whole App CEO`; optional avatar safely used fallback. |
| Company | PASS | UI created `Whole App Acceptance Company`. |
| CEO Assistant presence | PASS | One canonical CEO Assistant appeared. |
| Cloud AI setup | PASS | CEO entered the DeepSeek key in product UI; real Health and model discovery returned three models; `deepseek-v4-pro` became tenant default. |
| CEO AI conversation | PARTIAL | The visible CEO Desk conversation is a read-only projection with disabled Send; no direct model call was possible and no response was fabricated. |
| Create Business | PASS | CEO intent produced a readable proposal and UI confirmation created canonical `Create a small customer`. |
| General Workspace | PASS | The first Workspace `workspace-first-7f979f2781d4f536644695af` was created and reopened through the Business directory. |
| Team | BLOCKED | UI recruited `Product Manager` as a Company employee, but the only generated department is `business.general`; the recruit flow rejects the template/department type and provides no later join/assignment action. |
| Responsibility | BLOCKED | Workspace continued to show zero responsible employees and `尚未形成唯一的团队责任安排`. |
| Work | BLOCKED | `交给负责员工` remained disabled; no legitimate Work was created. |
| Execution | BLOCKED | No Work/Responsibility existed, so no employee or cloud execution was launched. |
| Result | BLOCKED | No execution occurred; no fake Result was generated. |
| Evidence | BLOCKED | No execution occurred; no fake Evidence was generated. |
| Handoff | NOT APPLICABLE | No legal Work existed and no Handoff was forced. |
| P7 Decision | BLOCKED | No legal Work could produce a Decision Packet; none was fabricated. |
| CEO Desk | PASS / PARTIAL | It truthfully showed one Workspace, one AI employee, no result, no decision and no proven next responsibility. |
| Restart | PASS | Exact app exited; its 3010/8002/8080 sidecars exited; the same package/root reopened. |
| Restart recovery | PASS | CEO identity, Company, Assistant, Business, Workspace, employee and default model recovered without duplicate objects. Stored Keychain credential performed real Health/model rediscovery without re-entry. |
| Post-restart AI | BLOCKED | Direct CEO conversation has no submit path and Workspace execution remains responsibility-blocked. No API call was used as a substitute. |

## 5. Real Cloud AI truth

- Real Cloud Health: PASS before and after restart.
- Model discovery: PASS before and after restart.
- Discovered model names: `deepseek-v4-pro`, `deepseek-v4-flash-vision-exp`,
  `deepseek-v4-flash`.
- Tenant default: `deepseek-v4-pro`.
- Keychain recovery: PASS; post-restart Health/discovery succeeded with the API Key field left empty.
- Real inference call in this whole-app journey: NOT PROVED. `ai_usage_records=0`; neither the CEO
  Desk nor the responsibility-blocked Workspace offered a legal submit path.
- Cloud Health is therefore not misreported as employee execution.

## 6. Runtime and no-fake-data evidence

Final isolated database counts:

- Company: 1
- canonical Business: 1
- Workspace: 1
- employee: 1
- Task: 0
- AI usage: 0
- Decision: 0
- Artifact: 0

The UI and persistence agree: employee recruitment succeeded, while Work/Execution/Result/Decision
did not occur. No static fixture, mock answer, fake Health, fake Employee, fake Result, fake Evidence
or fake Decision was used.

## 7. Restart and persistence

After full app close and same-root reopen:

- CEO and Company identity were unchanged;
- canonical Business and Workspace were unchanged;
- recruited employee remained present;
- the Workspace remained correctly blocked on responsibility rather than claiming a running agent;
- default model remained `deepseek-v4-pro`;
- real Health/model discovery succeeded again using the saved Keychain reference;
- no canonical object was duplicated.

Evidence files:

- `/tmp/curis-v1-whole-app-live-ai-20260830-01/organization-assistant-summary.png`
- `/tmp/curis-v1-whole-app-live-ai-20260830-01/post-restart-model-revalidation.png`
- `/tmp/curis-v1-whole-app-live-ai-20260830-01/post-restart-workspace-responsibility-gap.png`

## 8. Secret safety

- Full credential was never read, copied, printed, logged in this Review or supplied through chat,
  environment, CLI, fixture or SQLite.
- Structural scan of the isolated SQLite/logs/artifacts found zero files matching long `sk-` keys,
  bearer tokens or URL key/token/secret parameters.
- UI and SQLite exposed only a `vault://.../credential/...` reference where applicable.
- Credential cleanup was not executed because deleting a native Keychain item is destructive and the
  CEO did not choose retain versus delete in this acceptance turn. State: `PRESERVED PENDING CEO CHOICE`.

## 9. Active database safety

| Path | Pre size | Final size | Pre/final mtime | Pre/final SHA-256 | integrity |
| --- | ---: | ---: | --- | --- | --- |
| `data/curis.sqlite` | 1232896 | 1232896 | 1786873339 | `2ea2506f90f764e834d47d8f6bae3cb41c22d457757e0e9216c0ae8c39a39ec6` | ok |
| `backend/data/curis.sqlite` | 1277952 | 1277952 | 1786783659 | `a9d96a9536a5bce3b3b30f912e86a37f61d28527a8eb2d35af7a5857d29414e4` | ok |

Both repository active databases remained byte-identical. All acceptance writes went to the external
isolated SQLite, whose final `integrity_check` was `ok`.

## 10. Product gaps

### P0 — ordinary-user operating chain break

`Talent recruitment → Department/Workspace membership → Responsibility` is not assembled for a
fresh General Workspace. The generated department reports `business.general` while its template is
the RD template; the recruit UI can create a Company employee but cannot attach that employee to the
department/Workspace. There is no subsequent responsibility-assignment action. This blocks Work,
Execution, Result/Evidence and P7 Decision in the required whole-app journey.

### P1 — direct CEO AI conversation

The CEO Desk renders a conversation surface but passes a fixed empty value, no-op change handler and
no submit handler. It must not be described as a working direct AI conversation.

### P1 — model revalidation projection

After restart, the Provider can perform real Health/model discovery from Keychain without key
re-entry, while previously saved model rows continue to display `等待重新验证` until that check runs.
This is truthful but the post-check status projection should be reviewed separately; it did not block
the responsibility failure above.

## 11. Remaining release gate

`RELEASE DISTRIBUTION & RECOVERY` does not start. First close the bounded product assembly gap:

`recruited Employee → Workspace membership → Responsibility → legal Work submit`.

Then rerun this same fresh packaged journey to obtain real inference, Result/Evidence, P7 Decision
and post-restart AI evidence. Signing/notarization remains a later initiative.

## 12. Decision

The package is not a fake-data failure: every unavailable downstream capability remained blocked and
truthful. It is nevertheless not a continuous operable V1 journey because the first Workspace cannot
turn its recruited employee into a responsible executor.

`WHOLE-APP LIVE AI ACCEPTANCE: PARTIAL / PRODUCT GAP`

`STOP FOR CEO / CHATGPT WHOLE-APP ACCEPTANCE REVIEW`

---

## Current correction — Product Gap Closure (2026-08-30)

The historical `PARTIAL / PRODUCT GAP` verdict above accurately records the first packaged run. The
bounded closure Issue subsequently implemented and re-ran the missing chain. Current scoped verdict:

`WHOLE-APP LIVE AI ACCEPTANCE: PASS WITH RECORDED P1`

`PRODUCT GAP CLOSED`

Now proven in the same isolated packaged journey:

- recruited Employee → Workspace Responsibility Assignment;
- legal Work → real DeepSeek execution → Result/Evidence/Artifact;
- canonical retry after a real failed attempt;
- CEO Assistant real submit and persisted response;
- exactly one high-risk P7 Decision Packet with provenance;
- CEO choice → same packet `APPLIED` → automatic responsibility resume → completed Work;
- full app/sidecar stop and exact-package restart;
- Keychain recovery without re-entry and post-restart real AI response;
- zero secret hits in isolated evidence and Issue-owned files;
- both repository active SQLite files byte-identical with `integrity_check=ok`.

Formal evidence and remaining P1 boundaries are recorded in:

`docs/reviews/CURIS_V1_WHOLE_APP_PRODUCT_GAP_CLOSURE_REVIEW.md`
