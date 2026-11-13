# CURIS V1 — Talent & Capability Productization Review

Status: Review
Authority Class: REVIEW
Date: 2026-08-31
Issue: `CURIS-V1-TALENT-CAPABILITY-PRODUCTIZATION-001`
Owner: Main Development Session
Verdict: `IMPLEMENTED / ACCEPTED CANDIDATE`

## 1. Current product structure

The current user-facing product area is `人才与能力`, with exactly three views:

- `专家`: recruitable canonical Employee Templates and current Company Employees.
- `技能`: official Skill definitions, Company installation truth and explicit Employee binding.
- `连接器`: Connector definition plus current authorization/health boundary.

The page reuses the current Direction D shell and does not create a new IA, Marketplace, Provider surface or capability system.

## 2. Legacy reconciliation

### KEEP

- Existing `TerraShell`, navigation and page route.
- Canonical recruitment, Employee list, Skill install/binding and Connector list endpoints.
- Existing Employee Detail and Organization Center routes.

### REWIRE

- Catalog records are projected into ordinary-user product states instead of engineering maturity/source language.
- Current Employee detail is loaded from persisted Employee Skill and Capability bindings.
- Organization-origin and safe local `returnTo` context are preserved.

### SUPERSEDED ON CURRENT PATH

- `Candidate`, `MCP`, repository path, maturity, mock/runtime and catalog-internal terminology.
- Catalog existence as a proxy for recruitability, installability, connectivity or health.

Legacy routes/components were not deleted.

## 3. Experts

The Experts view distinguishes `可招聘与准备中` from `公司员工`.

- Active canonical Employee Templates are recruitable.
- Existing EmployeeInstances are shown from canonical persisted data.
- External candidates remain `正在准备 / 暂未开放招聘` and expose no recruitment action.
- Search works over name, role and description.

## 4. Recruitment

The packaged Desktop proof recruited `质量工程师小验` from `QA Engineer` into `人才产品桌面验收公司`.

The recruitment endpoint created:

- EmployeeInstance `emp-78675fdd-e201-431b-82b3-8ef40189061f`;
- company ownership `company-talent-desktop-accepted`;
- role `qa_engineer`;
- status `idle`;
- real default Skill `测试设计`;
- truthful missing-tool result, without promoting the Employee to fully ready.

## 5. Avatar

The existing first-character identity fallback is reused (`质`). Avatar upload, preset selection and persisted avatar authority remain unimplemented and are not presented as completed.

## 6. Skills / Capability

The page separates:

- Skill definition/catalog visibility;
- Company installation;
- Employee Skill binding;
- Employee execution-capability binding.

The current backend accepts only its existing Skill Runtime types. Unsupported catalog types such as `development` remain visible but render `暂不可用`; no 422 is disguised as product success.

## 7. Installation

`PRD 设计` was installed through the existing idempotent Company Skill endpoint. Repeated installation is covered by backend regression and resolves to the same installed definition rather than creating duplicate Company truth.

## 8. Employee binding

`PRD 设计` was explicitly bound to `质量工程师小验`. The binding helper first reads existing bindings, preserves them and appends only the missing Skill.

After packaged restart, the same Employee read:

- `测试设计`;
- `PRD 设计`;
- two persisted Skill bindings;
- zero execution-capability bindings.

No ability was inferred from the Employee name or role.

## 9. Connectors

The current Connector list exposes two definitions, `aitoearn` and `social_auto_upload`.

Both remain:

- authorization: not authorized;
- health: unknown;
- local/demo-only: true;
- user state: `未连接` and `暂不可用于真实业务`.

No OAuth, external publication or real platform write was attempted.

## 10. Health truth

Definition/catalog presence is never displayed as health. The UI shows `已连接` only for verified authorized/healthy truth; the current Connector evidence therefore remains unconnected. There is no invented health timestamp, account identity or recovery success.

## 11. Model / Provider boundary

This Issue did not modify Model Management, Provider discovery, Keychain, default model, Provider health or execution. Employee remains a business identity; Provider/model stays an execution capability behind the Employee.

## 12. Return context

Safe local paths under `/ceo-office` are accepted. Known Organization origin resolves to `/ceo-office/organization?tab=employees`. External, protocol-relative and malformed paths fail closed to the Talent page. Completion exposes an explicit return action and does not auto-navigate.

## 13. Organization continuity

The fresh Desktop canonical Organization projection read:

- Company: `人才产品桌面验收公司`;
- `0 部门 · 0 业务 · 1 员工`;
- Employee Directory: `质量工程师小验 · qa_engineer`;
- truthful direct-company membership;
- `当前没有可证明的 Business 责任分配`.

Talent did not create a parallel Organization or Employee record.

## 14. Restart

The packaged app was fully stopped, including Workspace, Gateway, Guardian and frontend sidecars, then relaunched with the same isolated app-data root:

`/tmp/curis-talent-desktop.Iv5Lv0`

After restart, the Talent page recovered:

- one Company Employee;
- one Company-installed Skill;
- the same Employee identity;
- both Employee Skill bindings;
- the same unconnected Connector truth.

Persistence did not imply external authorization or execution readiness.

## 15. Browser

Browser acceptance used fresh ports and a repository-external SQLite. Verified:

- Experts and current employees;
- recruitment;
- supported Skill install and explicit binding;
- unsupported Skill `暂不可用` boundary;
- Connector unconnected state;
- Talent → Organization return;
- backend stop → user-facing load error → same-root restart → retry recovery;
- fresh-tab console errors: `0`.

Evidence: `/tmp/curis-talent-browser-final.png`.

## 16. Packaged Desktop

Fresh package:

`/Users/yy/Documents/Curis AI Workspace/desktop/target/release/bundle/macos/Curis.app`

Binary:

- path: `Contents/MacOS/curis-desktop`;
- size: `5267408` bytes;
- SHA-256: `cabc9d9be89ec65af2511c3670ace505a6668979d542ca7c062d0b2c943c5f5a`;
- build manifest time: `2026-08-31T14:45:54Z`;
- source HEAD recorded by manifest: `c797db840bad285d7e9f1962d06eac61aa28508b`.

Native interaction verified Experts, recruitment, Skills, Employee binding, Connectors, Organization Directory, complete sidecar shutdown and same-root reopen. Frontend error log stayed empty. The evidence harness intentionally generated one fail-closed wrong-tenant audit while probing headers and one transport reset while forcibly stopping the process; neither altered product truth or produced a business failure.

Evidence:

- `/tmp/curis-talent-desktop-experts.png`
- `/tmp/curis-talent-desktop-recruited.png`
- `/tmp/curis-talent-desktop-connectors.png`
- `/tmp/curis-talent-desktop-organization.png`
- `/tmp/curis-talent-desktop-restart-employee.png`

## 17. Tests / build

- Backend focused + no-regression: `51 passed, 1 skipped`.
- Frontend focused + no-regression: `30 passed`.
- Talent-specific backend existing/new tests: `10 passed` in the earlier focused pass.
- Talent-specific frontend: `4 passed`.
- Scoped ESLint: pass.
- Python compile for the new backend test: pass.
- Frontend production build: pass.
- Fresh Workspace/Gateway/Guardian/Recovery sidecars and Tauri package build: pass, proven by the launched fresh package above.
- Scoped `git diff --check`: pass.

Regression coverage included App Entry/First Run, Organization, Employee, Talent, General Workspace, Responsibility/real Employee execution, Operating Intelligence, P7, Result/Evidence, Provider protocol, Keychain contract and Backend DB Safety.

## 18. Active DB safety

Both active SQLite files are byte-identical to preflight and pass `integrity_check`:

| Path | Size | mtime | SHA-256 | integrity |
|---|---:|---:|---|---|
| `data/curis.sqlite` | `1232896` | `1786873339` | `2ea2506f90f764e834d47d8f6bae3cb41c22d457757e0e9216c0ae8c39a39ec6` | `ok` |
| `backend/data/curis.sqlite` | `1277952` | `1786783659` | `a9d96a9536a5bce3b3b30f912e86a37f61d28527a8eb2d35af7a5857d29414e4` | `ok` |

All Browser/Desktop/tests used repository-external SQLite/app-data.

## 19. Remaining P1 / P2

- Real Connector authorization, account binding, health and external execution.
- Avatar upload/preset persistence.
- Catalog/runtime alignment for currently unsupported official Skill types.
- External Candidate conversion and acceptance evidence.
- Final visual-specific Talent design remains open under Product Completion governance.

These are not presented as implemented by this Issue.

## 20. Final verdict

`TALENT & CAPABILITY: IMPLEMENTED / ACCEPTED CANDIDATE`

The bounded productization is complete with real recruitment, installation, Employee binding, Organization continuity, failure/retry, Browser/Desktop and restart evidence. External Connector capability remains honestly unconnected. No commit or push was performed.

## P1 Employee Avatar Closure · 2026-09-01

Final avatar evidence is recorded in:

- `docs/reviews/CURIS_V1_EMPLOYEE_RECRUITMENT_AVATAR_CLOSURE_REVIEW.md`

Disposition: the previous `Avatar upload/preset persistence` gap is closed by one canonical Employee avatar reference with upload, bundled preset, and fallback. No Talent, Organization, Employee, Identity, Provider or Connector redesign was introduced.

Recommended combined status: `TALENT & CAPABILITY: IMPLEMENTED / ACCEPTED` after CEO review of the closure record.
