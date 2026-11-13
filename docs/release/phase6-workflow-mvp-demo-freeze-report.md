# Phase-6 Workflow MVP Demo Freeze Report

Date: 2026-07-09

Status: demo freeze verified, pending product acceptance.

Demo script: `docs/demo/phase6-workflow-mvp-demo-script.md`

RC evidence: `docs/release/phase6-workflow-mvp-rc.md`

## Product Progress

Curis Workspace can now demonstrate a local Software R&D SOP workflow where R&D AI employees execute ordered steps, reuse their own official or tenant_private capability bindings, preserve Credential Vault boundaries, and write redacted workflow / step / employee / capability attribution to usage_event and audit_event.

## Current Demo Capability

- View R&D employee templates and employee instances.
- View employee capability bindings.
- View tenant_private credential_ref binding on private capability metadata.
- Create a Software R&D requirement.
- Start the official Software R&D SOP WorkflowRun.
- Execute WorkflowSteps in order.
- View each employee StepResult.
- View the Tech Lead final summary report.
- View usage_event workflow / step / employee / capability redacted attribution.
- View audit_event workflow state changes.
- Confirm Admin cannot see tenant_private plaintext credential.

## Demo Chain Confirmation

The Phase-6 local/demo chain is confirmed:

1. CEO creates a Software R&D requirement.
2. CEO starts the Software R&D SOP Workflow.
3. Tech Lead receives and decomposes the task.
4. Product Manager supplements requirements.
5. Architect outputs the technical plan.
6. Frontend Engineer performs frontend work.
7. Backend Engineer performs backend work.
8. QA Engineer verifies the work.
9. Tech Lead aggregates the final result.
10. CEO views the final report.
11. usage_event records workflow / step / employee / capability redacted attribution.
12. audit_event records workflow state changes and redacted audit data.
13. tenant_private capability continues to use credentials through credential_ref and resolver.
14. Admin cannot see tenant_private plaintext credential.
15. Workspace runtime does not call `/api/platform/*`.

## Frozen Scope

- Official Software R&D sequential WorkflowTemplate.
- Tenant-scoped WorkflowInstance and WorkflowRun.
- Ordered WorkflowStep execution through `run-next-step`.
- StepAssignment by expected employee role.
- StepResult persistence.
- Tech Lead final report aggregation.
- EmployeeCapabilityBinding reuse.
- Credential Vault resolver reuse for tenant_private private model execution.
- usage_event workflow / step / employee / capability attribution.
- audit_event workflow state attribution.
- Minimal Workspace UI and local/demo script.

## Out Of Scope

- Complex DAG.
- Visual workflow editor.
- Billing.
- Marketplace.
- ROI.
- New business modules.
- Content operations / investment / ecommerce workflows.
- Complex approval workflow.
- Credential Vault security-boundary changes.
- Admin tenant_private plaintext access.
- Workspace runtime `/api/platform/*` calls.
- Plaintext secret persistence in database, logs, frontend, usage_event, or audit_event.

## Workflow SOP Chain

The frozen demo uses this ordered SOP:

1. Tech Lead 接收并拆解。
2. Product Manager 补充需求。
3. Architect 输出技术方案。
4. Frontend Engineer 执行前端任务。
5. Backend Engineer 执行后端任务。
6. QA Engineer 验收。
7. Tech Lead 汇总结果。

Expected demo result:

- WorkflowRun reaches `succeeded`.
- Every WorkflowStep reaches `succeeded`.
- Every WorkflowStep has one StepResult.
- The final report is produced by Tech Lead from step outputs.

## Employee / Capability Reuse

- Each step resolves an enabled employee in the same tenant and department.
- Step role assignment uses the R&D employee role required by the SOP.
- Each employee uses its own EmployeeCapabilityBinding.
- official and tenant_private capability sources remain visible and distinct.
- tenant_private capability execution continues through the existing private model path and resolver.

## Credential Vault Reuse

- tenant_private private model uses resolver-managed `credential_ref`.
- Plaintext credential is resolved server-side only for the model gateway call.
- Plaintext credential is not returned to frontend.
- Plaintext credential is not written to usage_event or audit_event.
- Plaintext credential is not exposed to Admin.
- Disabled and cross-tenant credential boundaries remain covered by focused resolver tests.

## usage_event Redacted Attribution Result

usage_event can show:

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
- `status`
- `created_at`

usage_event must not show:

- API key
- token
- secret
- credential value
- Authorization header
- raw sensitive provider response

Demo freeze result: passed.

## audit_event Redacted Attribution Result

Validated workflow audit events:

- `workflow.run.created`
- `workflow.run.started`
- `workflow.run.completed`
- `workflow.run.failed`
- `workflow.step.started`
- `workflow.step.completed`
- `workflow.step.failed`
- `workflow.step.assigned`

audit_event can show:

- `tenant_id`
- `workflow_run_id`
- `workflow_step_id`
- `task_id`
- `employee_id`
- `employee_role`
- `actor_id`
- `action`
- `status`
- `reason`
- `timestamp`

audit_event must not show:

- plaintext credential
- token
- secret
- restorable credential configuration

Demo freeze result: passed.

## Admin / Workspace Boundary

- Workspace owns WorkflowRun and WorkflowStep execution.
- Workspace runtime does not call `/api/platform/*`.
- Admin does not create, edit, own, or run WorkflowRun.
- Admin only observes redacted usage_event and audit_event.
- Admin cannot read tenant_private plaintext credential.

Demo freeze result: passed.

## Tenant Isolation Result

- Tenant A can create and run its WorkflowRun.
- Tenant B cannot read Tenant A WorkflowRun through Workspace API.
- Employee assignment is constrained to the current tenant and department.
- tenant_private credential resolution remains tenant-scoped.
- Admin usage/audit observability remains redacted.

Demo freeze result: passed.

## Screenshot Checklist

Capture these demo artifacts:

- 研发部员工列表。
- 员工 capability binding。
- tenant_private credential_ref 绑定。
- 创建研发需求。
- 启动研发 SOP workflow。
- WorkflowRun 详情。
- WorkflowStep 状态列表。
- StepResult 结果页。
- Tech Lead 汇总报告。
- Admin usage_event 脱敏归因。
- audit_event 脱敏审计。

## Stability Verification

Workflow runtime and event attribution tests:

```bash
cd backend && .venv/bin/python -m unittest tests.test_phase6_workflow_mvp
```

Result:

```text
Ran 3 tests in 0.278s
OK
```

Workflow test-output leakage check:

```bash
cd backend && .venv/bin/python -m unittest tests.test_phase6_workflow_mvp 2>&1 | tee /tmp/phase6_workflow_demo_freeze_test_output.txt
! rg -n "phase6[-]secret[-]value|Authorization: Bearer" /tmp/phase6_workflow_demo_freeze_test_output.txt
```

Result:

```text
PASS
```

Credential resolver boundary tests:

```bash
cd backend && .venv/bin/python -m unittest tests.test_phase5_credential_vault
```

Result:

```text
Ran 4 tests in 0.216s
OK
```

Credential test-output leakage check:

```bash
cd backend && .venv/bin/python -m unittest tests.test_phase5_credential_vault 2>&1 | tee /tmp/phase6_credential_demo_freeze_test_output.txt
! rg -n "phase5[-]secret[-]value|Authorization: Bearer" /tmp/phase6_credential_demo_freeze_test_output.txt
```

Result:

```text
PASS
```

Backend full regression:

```bash
cd backend && .venv/bin/python -m unittest discover tests
```

Result:

```text
Ran 313 tests in 10.609s
OK
```

Frontend unit tests:

```bash
cd frontend && node --test app/taskViewModel.test.mjs
```

Result:

```text
tests 32
pass 32
fail 0
```

Frontend lint:

```bash
cd frontend && npm run lint
```

Result:

```text
PASS
```

Frontend build:

```bash
cd frontend && npm run build
```

Result:

```text
Compiled successfully
```

Workspace runtime `/api/platform/*` scan:

```bash
! rg -n "/api/platform/" frontend/app/page.js backend/app/workflow_runtime.py backend/app/result_store.py backend/app/evolution_event_log.py
```

Result:

```text
PASS
```

Scoped secret scan:

```bash
! rg -n "phase6[-]secret[-]value|phase5[-]secret[-]value|sk-[A-Za-z0-9]{16,}|BEGIN (RSA|OPENSSH|EC|PRIVATE)|AKIA[0-9A-Z]{16}" backend/app/workflow_runtime.py backend/app/database.py backend/app/main.py backend/app/result_store.py backend/app/evolution_event_log.py frontend/app/page.js frontend/app/taskViewModel.mjs frontend/app/taskViewModel.test.mjs docs/demo/phase6-workflow-mvp-demo-script.md docs/release/phase6-workflow-mvp-implementation-report.md docs/release/phase6-workflow-mvp-rc.md docs/release/phase6-workflow-mvp-demo-freeze-report.md
```

Result:

```text
PASS
```

Diff check:

```bash
git diff --check -- backend/app/database.py backend/app/evolution_event_log.py backend/app/main.py backend/app/result_store.py backend/app/workflow_runtime.py backend/tests/test_phase6_workflow_mvp.py frontend/app/page.js frontend/app/taskViewModel.mjs frontend/app/taskViewModel.test.mjs docs/release/phase6-workflow-mvp-implementation-report.md docs/release/phase6-workflow-mvp-rc.md docs/demo/phase6-workflow-mvp-demo-script.md docs/release/phase6-workflow-mvp-demo-freeze-report.md knowledge/CURRENT_CONTEXT.md
```

Result:

```text
PASS
```

## Known Limits

- Sequential workflow only.
- No complex DAG.
- No visual workflow editor.
- No cross-department workflow.
- No content operations / investment / ecommerce workflows.
- `run-next-step` is user-triggered; no production scheduler.
- Step assignment uses deterministic first enabled employee by role.
- Final report is simple text aggregation.
- Workflow templates from tenant_private / marketplace remain reserved only.
- private tool / connector deeper runtime remains future-gated.

## Demo Freeze Decision

Phase-6 Workflow MVP can freeze as a local/demo version after product acceptance.
