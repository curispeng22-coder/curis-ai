# Review 078: Workspace Department Catalog Local Demo Evidence

Date: 2026-07-08
Owner: 质量运行席 / 产品规划席
Issue: `issues/081_workspace_department_catalog_local_demo_evidence_gate.md`
Status: ACCEPTED_BY_PRODUCT

## Product Progress

Curis Workspace can now show and verify the accepted read-only department catalog summary in a real local/demo browser runtime without enabling department management, employee management, new APIs, or runtime behavior changes.

## Scope

- Verification-only local/demo evidence for the accepted Workspace Company Department Catalog Summary slice.
- Local backend and local frontend runtime smoke.
- Browser-visible evidence for the existing operation console company frame and `部门目录` summary.
- Existing read-only department catalog API evidence.
- Secret-like metadata scan.
- Task API payload boundary verification.
- No implementation or behavior changes.

## Runtime Evidence

Local services:

```text
backend: http://127.0.0.1:8000
frontend: http://127.0.0.1:3010
```

Browser URL:

```text
http://127.0.0.1:3010/
```

Screenshot artifact:

```text
reviews/078_workspace_department_catalog_local_demo_evidence.png
```

Browser-visible checks:

```json
{
  "url": "http://127.0.0.1:3010/",
  "title": "Curis 工作台",
  "hasCompanyFrame": true,
  "hasDepartmentCatalog": true,
  "hasEnabledOfficialCount": true,
  "hasCategorySummary": true,
  "hasBusinessOrFunctionLabel": true,
  "hasSecretLike": false
}
```

Visible department summary text included:

```text
公司工作区
Curis 本地演示公司
本地演示 · 默认工作区
部门目录
已启用 4 个官方部门类型
类别：业务型 1 个，职能型 3 个
业务型 · business.general
职能型 · function.admin
职能型 · function.bi
职能型 · function.hr
```

Existing department catalog API returned active official types:

```text
business.general / 业务部 / official / enabled=1
function.admin / 行政部 / official / enabled=1
function.bi / BI 部 / official / enabled=1
function.hr / 人事部 / official / enabled=1
```

## Verification

Backend health:

```text
curl -sS http://127.0.0.1:8000/health
```

Result:

```json
{"status":"ok"}
```

Frontend runtime:

```text
curl -sS -I http://127.0.0.1:3010
```

Result:

```text
HTTP/1.1 200 OK
```

Department catalog API:

```text
curl -sS http://127.0.0.1:8000/api/catalog/department-types
```

Result: returned 4 active official department types.

Frontend view-model tests:

```text
cd frontend && node --test app/taskViewModel.test.mjs
```

Result:

```text
tests 18
pass 18
fail 0
```

Frontend lint:

```text
cd frontend && npm run lint
```

Result:

```text
eslint .
```

Exit code: 0.

Frontend build:

```text
cd frontend && npm run build
```

Result:

```text
Compiled successfully
Route (app)
┌ ○ /
├ ○ /_not-found
└ ○ /platform
```

Task API payload boundary:

```text
buildTaskPayload(content) -> { content }
```

No secret-like metadata scan:

```text
rg -n "sk-[A-Za-z0-9_-]{16,}|api[_-]?key|authorization|bearer|credential|secret" frontend/app/page.js frontend/app/taskViewModel.mjs reviews/078_workspace_department_catalog_local_demo_evidence.png
```

Result: no matches.

## Quality Result

Quality Result: PASS.

Commands: backend health, frontend runtime smoke, browser-visible department summary evidence, screenshot capture, department catalog API read, frontend tests, frontend lint, frontend build, task payload boundary check, and secret-like metadata scan.

Evidence: `reviews/078_workspace_department_catalog_local_demo_evidence.png` captures the accepted `部门目录` summary in the local/demo browser runtime; browser-visible checks confirmed company frame, department catalog summary, enabled official count, category summary, non-secret department labels, and no secret-like metadata.

Risks: The evidence pass uses current local data. This issue did not create or mutate departments, employees, tasks, workflows, model preferences, or runtime execution state.

Blocked / Pass: Pass; no blockers found.

## Product Acceptance

Product Decision: ACCEPTED.

Priority: Close local/demo evidence for the accepted Workspace Department Catalog Summary slice and continue to the next bounded Workspace Company Foundation step.

Scope: Accept verification-only evidence for the visible local/demo department catalog summary.

Acceptance Criteria:

- Browser-visible department catalog evidence is captured.
- Company frame and `部门目录` summary are visible.
- Active official department type count, category summary, and non-secret department labels are visible.
- No secret-like metadata is visible or matched by scan.
- Task API payload remains `{ content }`.
- No implementation or behavior change was made for this evidence issue.

Source Of Truth Updates: `issues/081_workspace_department_catalog_local_demo_evidence_gate.md`, `TASKS.md`, `PROJECT_STATUS.md`, `knowledge/CURRENT_CONTEXT.md`, and `knowledge/PROJECT_MEMORY.md` mark local/demo department catalog evidence accepted.

Next Seat: main thread closeout.

Open Questions: None.

Handoff: final closeout
