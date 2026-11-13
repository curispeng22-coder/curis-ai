# Review 071: Workspace Model Preference Local E2E Evidence

Date: 2026-07-08

Issue: `issues/074_workspace_model_preference_local_e2e_evidence.md`

## Product Progress

Curis Workspace can now prove locally that the operation console reads, saves, and resets the tenant default model preference against the real backend while preserving ordinary task creation.

## Result

PASS.

## Environment

- Backend: `http://127.0.0.1:8010`
- Backend database: temporary SQLite `/tmp/curis_074_e2e.sqlite`
- Frontend: `http://127.0.0.1:3010`
- Frontend API base: `NEXT_PUBLIC_API_BASE=http://127.0.0.1:8010`
- CORS note: backend was started with `CURIS_ALLOWED_ORIGINS` including `http://127.0.0.1:3010`.

## Runtime Commands

Backend:

```bash
cd backend
CURIS_DB=/tmp/curis_074_e2e.sqlite \
CURIS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000,http://127.0.0.1:3010 \
./.venv/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 8010
```

Frontend:

```bash
cd frontend
NEXT_PUBLIC_API_BASE=http://127.0.0.1:8010 npm run dev -- --hostname 127.0.0.1 --port 3010
```

## API Evidence

Backend health:

```bash
curl -s http://127.0.0.1:8010/health
```

Observed:

```json
{"status":"ok"}
```

Initial preference read:

```bash
curl -s -H 'X-Tenant-Id: tenant-e2e' http://127.0.0.1:8010/api/workspace/model-preference
```

Observed:

```json
{"preference":null,"available_models":[{"model_key":"official.newapi.default","provider_id":"newapi","display_name":"New API Default Model","gateway_ref":"newapi","model_name":"newapi-default","source":"official","status":"active"}]}
```

Preference save:

```bash
curl -s -H 'Content-Type: application/json' -H 'X-Tenant-Id: tenant-e2e' \
  -X PUT http://127.0.0.1:8010/api/workspace/model-preference \
  -d '{"model_key":"official.newapi.default"}'
```

Observed:

```json
{"preference":{"tenant_id":"tenant-e2e","model_key":"official.newapi.default","gateway_ref":"newapi","model_name":"newapi-default","source":"official"}}
```

Task creation payload boundary:

```bash
curl -s -H 'Content-Type: application/json' \
  -X POST http://127.0.0.1:8010/api/task \
  -d '{"content":"074 UI 后任务载荷边界验证"}'
```

Observed:

```json
{"status":"created"}
```

Task history confirmed the created record stores ordinary `content` with tenant `default`; no model preference fields are part of the Task API payload.

## Browser Evidence

Browser runtime loaded `http://127.0.0.1:3010`.

Visible selector state after CORS-correct reload:

- Page showed `默认模型`.
- Official option was visible: `New API Default Model - newapi / newapi-default`.
- Page did not show `Failed to fetch`.
- Page did not render secret-like words matched by `api_key|credential_ref|Authorization|Bearer|secret|password|token`.

Save interaction:

- Selected `official.newapi.default`.
- Clicked `保存模型`.
- Page showed current default model as `New API Default Model` with detail `newapi / newapi-default`.
- Backend read returned preference for tenant `default` with `model_key=official.newapi.default`, `gateway_ref=newapi`, `model_name=newapi-default`, and `source=official`.

Reset interaction:

- Clicked `重置默认`.
- Page showed `未设置默认模型` and `将使用系统当前默认模型`.
- Backend read returned `"preference": null`.

Task creation interaction:

- Entered `074 浏览器端任务载荷边界验证` in the operation console task editor.
- Clicked `创建任务`.
- Page showed `任务已创建` and the created task in history.
- Backend history showed the task content as `074 浏览器端任务载荷边界验证` with no preference fields in the task record.

## Verification Commands

```bash
cd frontend
node --test app/taskViewModel.test.mjs
npm run lint
npm run build
```

Evidence:

- Frontend view-model tests: 14 tests passed.
- Frontend lint: passed.
- Frontend build: passed.

UI secret/scope scan:

```bash
rg -n "api_key|credential_ref|Authorization|Bearer|secret|password|billing|ROI|tenant package|marketplace|optimization|provider SDK|New API|department|employee|prompt|output|raw|credential|token" frontend/app/page.js frontend/app/taskViewModel.mjs frontend/app/taskViewModel.test.mjs
```

Observed:

- No rendered UI secret exposure was found.
- Matches were limited to existing task output terminology and the negative test fixture proving `credential_ref` is not rendered.

## Scope Check

- No product feature was added in this issue.
- No backend semantic change was made for this issue.
- No frontend design expansion was made for this issue.
- Working tree already contains unrelated prior implementation changes; this issue only added local E2E evidence/status updates.
- ADR-0030, ADR-0029, runtime secret guardrails, official model catalog metadata boundary, current Task API payloads, and `ModelGatewayAdapter`-only execution remain preserved.

## Known Gaps

- The local dev backend must include the active frontend origin in `CURIS_ALLOWED_ORIGINS` when the frontend runs on a non-default port such as `3010`.

Quality Result: PASS; no blockers found.

## Handoff

Issue: `issues/074_workspace_model_preference_local_e2e_evidence.md`
Objective: Accept Workspace Model Preference local E2E evidence.
Special Constraints: Verification-only issue; no implementation changes approved. Local backend/frontend E2E passed for read/save/reset and Task API payload boundary.
Next Seat: main thread closeout

Handoff: final closeout
