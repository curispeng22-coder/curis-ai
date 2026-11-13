# Phase-6 Workflow MVP RC

Date: 2026-07-09

Status: RC verified, pending product acceptance.

Issue: `issues/phase6_workflow_mvp.md`

Implementation report: `docs/release/phase6-workflow-mvp-implementation-report.md`

## Product Progress

Curis Workspace can now demonstrate a bounded Software R&D SOP workflow where R&D AI employees execute ordered steps, reuse their own capability bindings, and write redacted workflow / step / employee / capability attribution to usage_event and audit_event.

## Implemented Scope Under RC

- Official Software R&D sequential WorkflowTemplate.
- Tenant-scoped WorkflowInstance and WorkflowRun.
- Ordered WorkflowStep records.
- StepAssignment per step.
- StepResult per completed step.
- `run-next-step` bounded sequential execution.
- Role-based assignment for:
  - Tech Lead
  - Product Manager
  - Architect
  - Frontend Engineer
  - Backend Engineer
  - QA Engineer
  - Tech Lead final report
- EmployeeCapabilityBinding reuse.
- tenant_private private model execution through existing Credential Resolver and Model Gateway Adapter.
- usage_event workflow / step / employee attribution.
- audit_event workflow state attribution.
- Minimal Workflow UI inside the existing Workspace operation console.

## Acceptance Flow

1. Create Software R&D department instance.
2. Create the six R&D employee instances.
3. Bind each employee to an enabled capability.
4. Create tenant_private private model backed by resolver-managed credential_ref.
5. Create WorkflowRun from the official R&D SOP template.
6. Execute `run-next-step` seven times.
7. Confirm steps execute by `step_order`.
8. Confirm each step is assigned to the expected employee role.
9. Confirm every step writes StepResult.
10. Confirm Tech Lead final report is produced.
11. Confirm usage_event includes workflow_run_id / workflow_step_id / employee / capability / credential attribution.
12. Confirm audit_event includes workflow run and step state changes.
13. Confirm tenant isolation by rejecting cross-tenant WorkflowRun reads.
14. Confirm Credential Vault boundaries remain intact.
15. Confirm Workspace runtime does not call `/api/platform/*`.

## Workflow SOP Chain Result

Validated:

- CEO requirement can create WorkflowRun.
- Official R&D SOP template is source `official`, process_type `sequential`, status `active`.
- WorkflowStep executes in this order:
  1. Tech Lead 接收并拆解
  2. Product Manager 补充需求
  3. Architect 输出技术方案
  4. Frontend Engineer 执行前端任务
  5. Backend Engineer 执行后端任务
  6. QA Engineer 验收
  7. Tech Lead 汇总结果
- Every executed step produces StepResult.
- WorkflowRun reaches `succeeded`.
- CEO-readable final report is produced from step results.

RC result: passed.

## Employee / Capability Reuse Result

Validated:

- Tech Lead can execute breakdown and final-report steps.
- Product Manager can execute requirement clarification.
- Architect can execute architecture design.
- Frontend Engineer can execute frontend step.
- Backend Engineer can execute backend step.
- QA Engineer can execute verification step.
- Each step resolves an enabled employee in the same tenant and department.
- Each step uses the assigned employee's own EmployeeCapabilityBinding.
- A workflow step fails when the underlying tool execution fails.

RC result: passed.

## Credential Vault Reuse Result

Validated:

- tenant_private model capability continues through RuntimeCapabilityContext.
- Runtime uses Credential Resolver for resolver-managed credential_ref.
- Runtime does not bypass credential_ref.
- Plaintext credential is used only server-side during the model gateway call.
- Disabled credential and cross-tenant credential boundaries remain covered by Phase-5 resolver tests.
- No Credential Vault security-boundary change was introduced.

RC result: passed.

## usage_event Redacted Attribution Result

Observed workflow usage_event fields:

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

Forbidden values not observed:

- plaintext API key
- token
- secret
- credential value
- Authorization header
- raw sensitive provider response

RC result: passed.

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

Allowed audit payload fields:

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

Forbidden values not observed:

- plaintext credential
- token
- secret
- restorable credential configuration

RC result: passed.

## Tenant Isolation Result

- Tenant A can create and run its WorkflowRun.
- Tenant B cannot read Tenant A WorkflowRun through Workspace API.
- Employee assignment uses employees from the current tenant and department.
- tenant_private credential resolution remains tenant-scoped.
- Admin usage/audit reads stay redacted and observational.

RC result: passed.

## Admin / Workspace Boundary Result

- Workspace runtime does not call `/api/platform/*`.
- Admin does not create, edit, own, or run WorkflowRun.
- Admin does not edit tenant_private workflow state.
- Admin observes only redacted usage_event and audit_event.
- Admin cannot read tenant_private plaintext credential.

RC result: passed.

## Test Commands And Results

Workflow runtime and event attribution tests:

```bash
cd backend && .venv/bin/python -m unittest tests.test_phase6_workflow_mvp
```

Result:

```text
Ran 3 tests ... OK
```

Credential resolver boundary tests:

```bash
cd backend && .venv/bin/python -m unittest tests.test_phase5_credential_vault
```

Result:

```text
Ran 4 tests ... OK
```

Backend full regression:

```bash
cd backend && .venv/bin/python -m unittest discover tests
```

Result:

```text
Ran 313 tests ... OK
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

Result: pass.

Frontend build:

```bash
cd frontend && npm run build
```

Result: compiled successfully.

Workflow test-output leakage check:

```bash
cd backend && .venv/bin/python -m unittest tests.test_phase6_workflow_mvp 2>&1 | tee /tmp/phase6_workflow_rc_test_output.txt
! rg -n "phase6[-]secret[-]value|Authorization: Bearer" /tmp/phase6_workflow_rc_test_output.txt
```

Result: pass.

Credential resolver test-output leakage check:

```bash
cd backend && .venv/bin/python -m unittest tests.test_phase5_credential_vault 2>&1 | tee /tmp/phase6_credential_boundary_test_output.txt
! rg -n "phase5[-]secret[-]value|Authorization: Bearer" /tmp/phase6_credential_boundary_test_output.txt
```

Result: pass.

Workspace runtime `/api/platform/*` scan:

```bash
! rg -n "/api/platform/" frontend/app/page.js backend/app/workflow_runtime.py backend/app/result_store.py backend/app/evolution_event_log.py
```

Result: pass.

Scoped secret scan:

```bash
! rg -n "phase6[-]secret[-]value|phase5[-]secret[-]value|sk-[A-Za-z0-9]{16,}|BEGIN (RSA|OPENSSH|EC|PRIVATE)|AKIA[0-9A-Z]{16}" backend/app/workflow_runtime.py backend/app/database.py backend/app/main.py backend/app/result_store.py backend/app/evolution_event_log.py frontend/app/page.js frontend/app/taskViewModel.mjs frontend/app/taskViewModel.test.mjs docs/release/phase6-workflow-mvp-implementation-report.md docs/release/phase6-workflow-mvp-rc.md
```

Result: pass.

Diff check:

```bash
git diff --check -- backend/app/database.py backend/app/evolution_event_log.py backend/app/main.py backend/app/result_store.py backend/app/workflow_runtime.py backend/tests/test_phase6_workflow_mvp.py frontend/app/page.js frontend/app/taskViewModel.mjs frontend/app/taskViewModel.test.mjs docs/release/phase6-workflow-mvp-implementation-report.md docs/release/phase6-workflow-mvp-rc.md knowledge/CURRENT_CONTEXT.md
```

Result: pass.

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

## Demo Freeze Readiness

Phase-6 Workflow MVP can enter Demo Freeze after product acceptance.
