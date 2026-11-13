# Phase-7 Stable Demo Script

Status: Deprecated

Date: 2026-07-09

Demo status: local/demo stable package.

## Product Progress

Curis Workspace can now demonstrate a repeatable local AI company workflow: CEO creates a Software R&D requirement, R&D employees execute an ordered SOP, tenant_private capability uses credential_ref through resolver, and Admin observes only redacted usage_event / audit_event attribution.

## Demo Package Paths

- Demo seed: `docs/demo/phase7-demo-seed.json`
- Environment check: `tools/phase7_check_local_demo_env.py`
- One-command local starter: `tools/phase7_start_local_demo.sh`
- Stable demo E2E: `tools/phase7_stable_demo_e2e.py`
- Phase-6 reference script: `docs/demo/phase6-workflow-mvp-demo-script.md`
- Phase-7 release report: `docs/release/phase7-demo-polish-commercial-readiness.md`

## 1. Environment Check

```bash
cd "/Users/yy/Documents/Curis AI Workspace"
backend/.venv/bin/python tools/phase7_check_local_demo_env.py
```

Expected result:

```text
"ok": true
```

## 2. One-Command Local Startup

```bash
cd "/Users/yy/Documents/Curis AI Workspace"
tools/phase7_start_local_demo.sh
```

The starter launches:

- Local OpenAI-compatible demo gateway at `http://127.0.0.1:18080`
- Backend at `http://127.0.0.1:8000`
- Frontend at `http://127.0.0.1:3000`

Logs:

```text
/tmp/curis_phase7_demo_logs/model-gateway.log
/tmp/curis_phase7_demo_logs/backend.log
/tmp/curis_phase7_demo_logs/frontend.log
```

Open Workspace:

```text
http://127.0.0.1:3000
```

Stop services using the command printed by the starter, for example:

```bash
kill <gateway_pid> <backend_pid> <frontend_pid>
```

## 3. Stable Demo E2E Verification

This command creates a clean local database through FastAPI TestClient and verifies the full Phase-4 + Phase-5 + Phase-6 demo chain without changing product runtime behavior:

```bash
cd "/Users/yy/Documents/Curis AI Workspace"
backend/.venv/bin/python tools/phase7_stable_demo_e2e.py
```

Expected result:

```text
"status": "PASS"
"step_count": 7
"step_result_count": 7
"usage_model_call_count": 7
"audit_completed_count": 1
"tenant_isolation": "PASS"
"secret_leakage": "PASS"
"admin_plaintext_visibility": "BLOCKED"
```

## 4. Browser Demo Path

After running `tools/phase7_start_local_demo.sh`, use the Workspace UI:

1. Open `http://127.0.0.1:3000`.
2. Confirm the company/workspace frame is visible.
3. Open the R&D employee area.
4. View the R&D employee list:
   - Tech Lead
   - Product Manager
   - Architect
   - Frontend Engineer
   - Backend Engineer
   - QA Engineer
5. View each employee capability binding.
6. View tenant_private credential_ref binding on the private model metadata.
7. Create a Software R&D requirement.
8. Start the Software R&D SOP workflow.
9. Open WorkflowRun detail.
10. Run the ordered workflow steps.
11. Confirm WorkflowStep status progression.
12. Confirm StepResult output for every employee step.
13. Confirm the Tech Lead final report is visible.
14. Query Admin redacted usage_event evidence.
15. Query Admin redacted audit_event evidence.
16. Confirm Admin never sees tenant_private plaintext credential.

## 5. Demo Chain

```text
CEO 创建研发需求
-> 启动研发 SOP Workflow
-> Tech Lead 接收并拆解
-> Product Manager 补充需求
-> Architect 输出技术方案
-> Frontend Engineer 执行前端任务
-> Backend Engineer 执行后端任务
-> QA Engineer 验收
-> Tech Lead 汇总最终结果
-> CEO 查看最终报告
-> usage_event / audit_event 展示脱敏归因
```

## 6. usage_event / audit_event Display

usage_event should show redacted attribution:

- `tenant_id`
- `task_id`
- `workflow_run_id`
- `workflow_step_id`
- `employee_id`
- `employee_role`
- `capability_source`
- `capability_type`
- `capability_id`
- `credential_id`
- `credential_ref_digest`
- `model_gateway_id`
- `model_name`
- token fields
- `estimated_cost`
- `status`
- `created_at`

audit_event should show workflow state changes:

- `workflow.run.created`
- `workflow.run.started`
- `workflow.run.completed`
- `workflow.run.failed`
- `workflow.step.started`
- `workflow.step.completed`
- `workflow.step.failed`
- `workflow.step.assigned`

Neither event stream may show plaintext credentials, API keys, tokens, Authorization headers, or raw sensitive provider responses.

## 7. Screenshot Checklist

Capture:

- Workspace company frame.
- R&D employee list.
- Employee capability binding.
- tenant_private credential_ref binding.
- Create Software R&D requirement.
- Start Software R&D SOP workflow.
- WorkflowRun detail.
- WorkflowStep status list.
- StepResult outputs.
- Tech Lead final report.
- Admin usage_event redacted attribution.
- Admin audit_event redacted audit.

## 8. Common Failure Scenarios And Recovery

### Port Already In Use

Symptom:

```text
address already in use
```

Recovery:

- Stop the old gateway/backend/frontend process.
- Or set `CURIS_DEMO_GATEWAY_PORT`, `CURIS_DEMO_BACKEND_PORT`, and `CURIS_DEMO_FRONTEND_PORT` before running the starter.

### Frontend Cannot Reach Backend

Symptom:

```text
fetch failed
```

Recovery:

- Confirm backend health at `http://127.0.0.1:8000/health`.
- Restart `tools/phase7_start_local_demo.sh`.
- Check `/tmp/curis_phase7_demo_logs/backend.log`.

### Demo Data Missing

Symptom:

```text
No R&D employees or workflow data visible.
```

Recovery:

- Re-run `backend/.venv/bin/python tools/phase7_stable_demo_e2e.py` for validation.
- Follow the seed steps in `docs/demo/phase6-workflow-mvp-demo-script.md` if browser-visible seed data is needed in the running server database.

### Credential Boundary Error

Symptom:

```text
credential cannot resolve
```

Recovery:

- Confirm `CURIS_ENV=local` for local/demo.
- Confirm credential_ref uses `local-dev://tenant/default/credential/{credential_id}`.
- Do not use production Vault/KMS references in the local demo unless the production credential gate is separately approved.

### Admin Usage Or Audit Query Empty

Symptom:

```text
usage_events: []
audit_events: []
```

Recovery:

- Complete all workflow steps first.
- Confirm the query uses `tenant_id=default`.
- Confirm Admin token is `platform-admin-dev` in local/demo.

## 9. Demo Narrative

Suggested talk track:

```text
Curis Workspace is no longer only a task executor. In this local demo, a CEO creates a software requirement, the R&D department runs a sequential SOP, each AI employee uses its own bound capability, private capability credentials are resolved server-side through credential_ref, and Admin can observe usage and audit attribution without seeing tenant-private secrets.
```

## 10. Strict Boundaries

- No Marketplace.
- No complex Workflow Plus.
- No formal Billing.
- No real charge collection.
- No ROI system.
- No new business modules.
- No Credential Vault security-boundary change.
- No Admin plaintext access to tenant_private credentials.
- No Workspace runtime call to `/api/platform/*`.
