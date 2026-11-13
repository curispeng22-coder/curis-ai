# Phase-7 Demo Polish + Commercial Readiness

Date: 2026-07-09

Status: demo polish and commercial-readiness preparation complete, pending product acceptance.

Scope: Workspace line. No Marketplace, no complex Workflow Plus, no formal Billing, no ROI, no new business modules, no Credential Vault security-boundary change.

## Product Progress

Curis Workspace now has a repeatable local/demo package for the AI company story: CEO creates a Software R&D requirement, R&D employees execute an ordered SOP workflow, tenant_private capability uses credential_ref through resolver, and Admin observes only redacted usage_event / audit_event attribution.

## Deliverables

- Demo seed: `docs/demo/phase7-demo-seed.json`
- Environment check script: `tools/phase7_check_local_demo_env.py`
- One-command starter: `tools/phase7_start_local_demo.sh`
- Stable demo E2E script: `tools/phase7_stable_demo_e2e.py`
- Stable demo script: `docs/demo/phase7-stable-demo-script.md`
- Billing readiness issue: `issues/phase7_billing_readiness.md`

## 1. Demonstrable Capability

The current stable demo covers:

1. CEO creates a Software R&D requirement.
2. CEO starts Software R&D SOP Workflow.
3. Tech Lead receives and decomposes.
4. Product Manager supplements requirements.
5. Architect outputs technical plan.
6. Frontend Engineer performs frontend step.
7. Backend Engineer performs backend step.
8. QA Engineer verifies.
9. Tech Lead aggregates final result.
10. CEO views final report.
11. Employee uses bound capability.
12. tenant_private capability uses credential_ref / resolver.
13. usage_event records workflow / step / employee / capability redacted attribution.
14. audit_event records workflow state changes.
15. Admin observes attribution but cannot see tenant_private plaintext credential.

## 2. Demo Seed

Seed source:

```text
docs/demo/phase7-demo-seed.json
```

Seed includes:

- `tenant_id`
- `ceo_id`
- demo company id
- Software R&D department template
- fake local/demo credential metadata
- tenant_private private model metadata
- six R&D employee roles
- official Software R&D workflow template id
- demo requirement content

The seed contains no real external provider secret.

## 3. Startup Steps

Environment check:

```bash
cd "/Users/yy/Documents/Curis AI Workspace"
backend/.venv/bin/python tools/phase7_check_local_demo_env.py
```

One-command local starter:

```bash
cd "/Users/yy/Documents/Curis AI Workspace"
tools/phase7_start_local_demo.sh
```

The starter launches:

- local demo model gateway
- backend
- frontend

## 4. E2E Verification Result

Command:

```bash
cd "/Users/yy/Documents/Curis AI Workspace"
backend/.venv/bin/python tools/phase7_stable_demo_e2e.py
```

Result:

```text
status: PASS
step_count: 7
step_result_count: 7
usage_model_call_count: 7
audit_completed_count: 1
tenant_isolation: PASS
secret_leakage: PASS
admin_plaintext_visibility: BLOCKED
```

Coverage:

- Demo seed is usable from a clean local database.
- Software R&D workflow runs all seven ordered steps.
- Every step produces StepResult.
- usage_event records workflow / step / employee / capability attribution.
- audit_event records workflow completion.
- tenant isolation rejects cross-tenant WorkflowRun read.
- tenant_private secret is not present in public response payloads.
- resolver supplies credential only to the server-side model gateway call.

## 5. Browser Demo Chain

Manual browser path is documented in:

```text
docs/demo/phase7-stable-demo-script.md
```

Browser coverage:

- Open Workspace.
- View R&D employees.
- View capability binding.
- View tenant_private credential_ref binding.
- Create Software R&D requirement.
- Start Software R&D SOP workflow.
- View WorkflowRun detail.
- View WorkflowStep status.
- View StepResult output.
- View Tech Lead final report.
- View Admin usage_event and audit_event evidence.

## 6. usage_event / audit_event Display

usage_event is sufficient for product analytics and early billing-readiness analysis because it includes:

- tenant
- task
- workflow run
- workflow step
- employee
- capability source/type/id
- model gateway and model
- token fields
- estimated cost
- credential digest attribution
- status
- timestamp

audit_event is sufficient for operational audit of workflow state changes and credential operations.

Both event streams remain redacted and do not expose plaintext credentials.

## 7. Billing Readiness Conclusion

Current usage_event is strong enough for usage analytics and billing input mapping.

It is not enough for authoritative billing settlement because:

- `estimated_cost` is estimate-level.
- Provider settlement cost is not normalized.
- No billing ledger exists.
- No plan/quota/invoice lifecycle exists.
- No invoice line-item state exists.
- No payment or subscription lifecycle exists.

Recommendation:

- Add a Billing Readiness / Contract phase before Billing MVP implementation.
- Admin Platform owns billing authority.
- Workspace preserves usage_event/audit_event attribution and does not implement invoices.
- Introduce `billing_event` or an Admin-owned billing ledger only after contract approval.

Issue prepared:

```text
issues/phase7_billing_readiness.md
```

## 8. Known Limits

- Local/demo only.
- No hosted production hardening.
- No production Vault/KMS backend.
- No formal Billing.
- No Marketplace.
- No ROI.
- Sequential Workflow only.
- `run-next-step` remains operator-triggered.
- Browser path is documented; automated script validates the full backend/API demo chain.
- Screenshot capture remains checklist-based.

## 9. Commercial Readiness Boundary

Commercial readiness is split:

- Workspace: usage attribution, employee/workflow/capability execution evidence, local/demo repeatability.
- Admin Platform: tenant management, official catalog, usage aggregation, future billing/invoice authority.
- Security boundary: production credential custody must pass a separate Vault/KMS gate.

Workspace must not:

- implement invoices,
- collect payment,
- store real production secrets in local/demo backend,
- let Admin read tenant_private plaintext credentials,
- call `/api/platform/*` from Workspace runtime.

## 10. Test Commands And Results

Environment check:

```bash
backend/.venv/bin/python tools/phase7_check_local_demo_env.py
```

Result:

```text
ok: true
```

Stable demo E2E:

```bash
backend/.venv/bin/python tools/phase7_stable_demo_e2e.py
```

Result:

```text
status: PASS
step_count: 7
step_result_count: 7
usage_model_call_count: 7
audit_completed_count: 1
tenant_isolation: PASS
secret_leakage: PASS
```

Backend full regression:

```bash
cd backend && .venv/bin/python -m unittest discover tests
```

Result:

```text
Ran 313 tests in 10.822s
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

Runtime `/api/platform/*` scan:

```bash
! rg -n "/api/platform/" frontend/app/page.js backend/app/workflow_runtime.py backend/app/result_store.py backend/app/evolution_event_log.py
```

Result:

```text
PASS
```

Scoped secret scan:

```bash
! rg -n "sk-[A-Za-z0-9]{16,}|BEGIN (RSA|OPENSSH|EC|PRIVATE)|AKIA[0-9A-Z]{16}|xox[baprs]-[A-Za-z0-9-]{10,}|ghp_[A-Za-z0-9]{36}" docs/demo/phase7-demo-seed.json docs/demo/phase7-stable-demo-script.md docs/release/phase7-demo-polish-commercial-readiness.md issues/phase7_billing_readiness.md tools/phase7_check_local_demo_env.py tools/phase7_stable_demo_e2e.py tools/phase7_start_local_demo.sh
```

Result:

```text
PASS
```

Diff check:

```bash
git diff --check -- docs/demo/phase7-demo-seed.json docs/demo/phase7-stable-demo-script.md docs/release/phase7-demo-polish-commercial-readiness.md issues/phase7_billing_readiness.md tools/phase7_check_local_demo_env.py tools/phase7_stable_demo_e2e.py tools/phase7_start_local_demo.sh knowledge/CURRENT_CONTEXT.md
```

Result:

```text
PASS
```

## 11. External Demo Readiness

Curis Workspace can enter external-demo preparation after product acceptance of this package.

Recommended next step:

- Use Phase-7 stable demo for controlled demos.
- Keep Billing implementation blocked until `issues/phase7_billing_readiness.md` is reviewed and accepted.
- Keep production credentials blocked until the production Vault/KMS gate is approved.
