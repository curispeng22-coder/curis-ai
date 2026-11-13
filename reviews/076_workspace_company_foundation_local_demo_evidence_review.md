# Review 076: Workspace Company Foundation Local Demo Evidence

Date: 2026-07-08
Owner: 质量运行席
Issue: `issues/079_workspace_company_foundation_local_demo_evidence_gate.md`
Status: ACCEPTED_BY_PRODUCT

## Product Progress

Curis Workspace can now show and verify the accepted local/demo company workspace frame in a real browser runtime without changing task execution, APIs, model routing, or runtime behavior.

## Scope

- Verification-only local/demo evidence for the accepted Workspace Company Foundation first slice.
- Local backend and local frontend runtime smoke.
- Browser-visible evidence for the existing operation console company frame.
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
reviews/076_workspace_company_foundation_local_demo_evidence.png
```

Browser-visible checks:

```json
{
  "url": "http://127.0.0.1:3010/",
  "title": "Curis 工作台",
  "hasCompanyFrame": true,
  "hasCompanyName": true,
  "hasLocalDemo": true,
  "hasModelPref": true,
  "hasTaskSummary": true,
  "hasSourceLinks": true,
  "hasSecretLike": false
}
```

Visible company-frame text included:

```text
公司工作区
Curis 本地演示公司
本地演示 · 默认工作区
模型网关本地首版已收口
默认模型：未设置默认模型
任务台：1 个任务，0 个已完成
公司基础边界
项目记忆
首版收口记录
```

Visible source links:

```text
/docs/decisions/ADR-0031-workspace-company-foundation-boundaries.md
/knowledge/PROJECT_MEMORY.md
/docs/release/model-gateway-local-demo-first-version-release-record.md
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

Frontend view-model tests:

```text
cd frontend && node --test app/taskViewModel.test.mjs
```

Result:

```text
tests 16
pass 16
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
rg -n "sk-[A-Za-z0-9_-]{16,}|api[_-]?key|authorization|bearer|credential|secret" frontend/app/page.js frontend/app/taskViewModel.mjs reviews/076_workspace_company_foundation_local_demo_evidence.png
```

Result: no matches.

## Quality Result

Quality Result: PASS.

Commands: backend health, frontend runtime smoke, browser-visible company-frame evidence, screenshot capture, frontend tests, frontend lint, frontend build, task payload boundary check, and secret-like metadata scan.

Evidence: `reviews/076_workspace_company_foundation_local_demo_evidence.png` captures the company frame in the local/demo browser runtime; browser-visible checks confirmed company frame, company name, local/demo status, model preference summary, task summary, source links, and no secret-like metadata.

Risks: The local task history contains existing local data; this evidence issue did not create or mutate tasks.

Blocked / Pass: Pass; no blockers found.

## Product Acceptance

Product Decision: ACCEPTED.

Priority: Close local/demo evidence for the accepted Workspace Company Foundation first slice.

Scope: Accept verification-only evidence for the visible local/demo company frame.

Acceptance Criteria:

- Browser-visible company frame evidence is captured.
- Company identity, local/demo status, model preference summary, task summary, and source links are visible.
- No secret-like metadata is visible or matched by scan.
- Task API payload remains `{ content }`.
- No implementation or behavior change was made for this evidence issue.

Source Of Truth Updates: `issues/079_workspace_company_foundation_local_demo_evidence_gate.md`, `TASKS.md`, `PROJECT_STATUS.md`, `knowledge/CURRENT_CONTEXT.md`, and `knowledge/PROJECT_MEMORY.md` mark local/demo evidence accepted.

Next Seat: main thread closeout.

Open Questions: None.

Handoff: final closeout
