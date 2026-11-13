# Phase-6 Workflow MVP Implementation Report

Date: 2026-07-09

Status: implementation complete; ready for Phase-6 RC verification.

## Product Progress

Curis Workspace can now run a minimal Software R&D SOP workflow where multiple R&D employees execute ordered steps, reuse their own capability bindings, and write workflow/step/employee attribution into usage_event and audit_event.

## Implemented Scope

- Official sequential Software R&D WorkflowTemplate.
- Tenant-scoped WorkflowInstance and WorkflowRun.
- Ordered WorkflowStep records.
- StepAssignment per workflow step.
- StepResult per executed step.
- `run-next-step` bounded sequential execution.
- Employee assignment by R&D role:
  - Tech Lead
  - Product Manager
  - Architect
  - Frontend Engineer
  - Backend Engineer
  - QA Engineer
  - Tech Lead final report
- EmployeeCapabilityBinding reuse.
- tenant_private private model execution through existing Credential Resolver and Model Gateway Adapter.
- usage_event workflow attribution.
- audit_event workflow state attribution.
- Minimal Workspace Workflow UI inside the existing operation console.

## Not Implemented

- Complex DAG.
- Visual workflow editor.
- Cross-department workflow.
- Content operations / investment / ecommerce workflows.
- Automatic employee recruiting.
- Billing.
- Marketplace.
- ROI.
- Production queue scheduler.
- Admin workflow ownership or editing.
- Credential Vault security-boundary change.

## Data Model

Added Phase-6 runtime tables:

- `workflow_templates`
- `workflow_instances`
- `workflow_runs`
- `workflow_steps`
- `step_assignments`
- `step_results`

WorkflowTemplate is seeded as:

- `official.workflow.software_rnd_sop`
- source: `official`
- department_type: `software_rnd`
- process_type: `sequential`
- status: `active`

## API List

Workspace APIs:

- `GET /api/workspace/workflow-templates`
- `GET /api/workspace/workflows`
- `POST /api/workspace/workflows`
- `GET /api/workspace/workflows/{workflow_run_id}`
- `POST /api/workspace/workflows/{workflow_run_id}/run-next-step`

Existing Task APIs remain backward-compatible.

## UI Pages

Workspace operation console now includes a minimal `研发 SOP Workflow` section:

- official workflow template selection.
- department selection.
- CEO requirement input.
- WorkflowRun creation.
- WorkflowRun list.
- selected WorkflowRun detail.
- ordered step status.
- assigned employee role / employee id.
- step output and final report.
- run-next-step action.

No workflow canvas, drag/drop editor, DAG view, marketplace picker, or multi-department dashboard was added.

## State Machine

WorkflowRun status:

```text
pending -> running -> succeeded
                  |-> failed
                  |-> cancelled
```

WorkflowStep status:

```text
pending -> running -> succeeded
                  |-> failed
                  |-> skipped
```

Phase-6 executes one next pending step at a time. A failed step marks the WorkflowRun failed.

## Employee / Capability Reuse

- Step assignment selects an enabled employee in the same tenant and department by required `employee_role`.
- Step execution uses the assigned employee's highest-priority enabled EmployeeCapabilityBinding.
- official tool bindings execute through the existing tool executor.
- tenant_private model bindings execute through RuntimeCapabilityContext, Credential Resolver, and Model Gateway Adapter.
- Marketplace remains reserved only.

## Credential Vault Reuse

No Credential Vault boundary was changed.

For tenant_private model steps:

```text
WorkflowStep
-> assigned EmployeeCapabilityBinding
-> RuntimeCapabilityContext
-> Credential Resolver
-> Model Gateway Adapter
-> StepResult
```

Plaintext credentials remain server-side only and do not enter frontend, logs, usage_event, or audit_event.

## usage_event Extension

usage_event now supports workflow attribution when present:

- `workflow_run_id`
- `workflow_step_id`
- `employee_id`
- `employee_role`
- `employee_name`
- `capability_source`
- `capability_type`
- `capability_id`
- `credential_id`
- `credential_ref_digest`
- `status`

Non-workflow task usage_event payload shape remains allowlisted and backward-compatible.

## audit_event Extension

Audit allowlist now includes `workflow.*`.

Implemented events:

- `workflow.run.created`
- `workflow.run.started`
- `workflow.run.completed`
- `workflow.run.failed`
- `workflow.step.assigned`
- `workflow.step.started`
- `workflow.step.completed`
- `workflow.step.failed`

Audit payload is redacted and contains workflow/task/employee/status metadata only.

## Test Commands And Results

Focused Phase-6 backend tests:

```bash
cd backend && .venv/bin/python -m unittest tests.test_phase6_workflow_mvp
```

Result:

```text
Ran 3 tests ... OK
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

Secret leakage test output check:

```bash
cd backend && .venv/bin/python -m unittest tests.test_phase6_workflow_mvp 2>&1 | tee /tmp/phase6_workflow_test_output.txt
! rg -n "phase6[-]secret[-]value|Authorization: Bearer" /tmp/phase6_workflow_test_output.txt
```

Result: pass.

Workspace runtime platform-call scan:

```bash
! rg -n "/api/platform/" frontend/app/page.js backend/app/workflow_runtime.py backend/app/result_store.py backend/app/evolution_event_log.py
```

Result: pass.

Scoped production/docs secret scan:

```bash
! rg -n "phase6[-]secret[-]value|sk-[A-Za-z0-9]{16,}|BEGIN (RSA|OPENSSH|EC|PRIVATE)|AKIA[0-9A-Z]{16}" backend/app/workflow_runtime.py backend/app/database.py backend/app/result_store.py backend/app/evolution_event_log.py frontend/app/page.js frontend/app/taskViewModel.mjs docs/release/phase6-workflow-mvp-implementation-report.md
```

Result: pass.

Diff check:

```bash
git diff --check -- backend/app/database.py backend/app/evolution_event_log.py backend/app/main.py backend/app/result_store.py backend/app/workflow_runtime.py backend/tests/test_phase6_workflow_mvp.py frontend/app/page.js frontend/app/taskViewModel.mjs frontend/app/taskViewModel.test.mjs docs/release/phase6-workflow-mvp-implementation-report.md knowledge/CURRENT_CONTEXT.md
```

Result: pass.

## Known Limits

- Phase-6 MVP is sequential only.
- `run-next-step` is user-triggered; no production queue scheduler.
- The step plan is fixed to the official Software R&D SOP.
- Step assignment uses deterministic first enabled employee by role.
- Final report is simple text aggregation.
- private tool / connector deeper runtime remains future-gated.
- Workflow templates from tenant_private / marketplace remain reserved only.

## RC Readiness

Phase-6 Workflow MVP is ready to enter RC verification.
