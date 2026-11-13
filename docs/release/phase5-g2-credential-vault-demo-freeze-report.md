# Phase-5 G2 Credential Vault Demo Freeze Report

Date: 2026-07-09

Status: demo freeze verified, pending product acceptance.

Demo script: `docs/demo/phase5-g2-credential-vault-demo-script.md`

RC evidence: `docs/release/phase5-g2-credential-vault-rc.md`

## Product Progress

Curis Workspace can now demonstrate tenant_private credential_ref creation, resolver-backed private capability execution, and redacted credential attribution in usage_event and audit_event without exposing plaintext credentials to database rows, frontend responses, Admin reads, or logs.

## Current Demo Capability

- Create tenant_private credential metadata through Workspace API.
- Generate `local-dev://tenant/{tenant_id}/credential/{credential_id}` credential_ref.
- Confirm API responses do not return plaintext.
- Bind credential_ref to tenant_private private model.
- Bind credential_ref to tenant_private private tool.
- Bind credential_ref to tenant_private private connector.
- Create/select R&D employee.
- Bind employee to tenant_private private model capability.
- Execute employee task through resolver-backed private model.
- View task result.
- View usage_event with `credential_id` and `credential_ref_digest`.
- View audit_event with credential action and digest.
- Confirm Admin cannot see tenant_private plaintext credential.

## Frozen Scope

- Credential metadata only in SQLite.
- Local/demo in-memory credential backend.
- Resolver tenant/status/environment validation.
- tenant_private private capability credential binding.
- tenant_private private model runtime through resolver.
- Redacted usage_event and audit_event.
- Documentation and demo script.

## Out Of Scope

- Workflow MVP.
- Billing MVP.
- Marketplace.
- ROI.
- New business modules.
- Complex employee-system expansion.
- Admin tenant_private plaintext access.
- Workspace runtime `/api/platform/*` calls.
- Plaintext secret persistence.
- Production Vault/KMS integration.
- Credential management frontend UI.

## credential_ref Format

Local/demo:

```text
local-dev://tenant/{tenant_id}/credential/{credential_id}
```

Production-reserved:

```text
vault://tenant/{tenant_id}/credential/{credential_id}
kms://tenant/{tenant_id}/credential/{credential_id}
```

Forbidden:

- `plaintext://`
- `raw_api_key`
- production reference without tenant id
- cross-tenant reference
- `local-dev://` in production

## Resolver Summary

Resolver behavior:

1. Parse credential_ref.
2. Validate allowed scheme.
3. Validate ref tenant matches current tenant.
4. Reject `local-dev://` under production env.
5. Load tenant-owned credential metadata.
6. Reject disabled/deleted credential.
7. Resolve plaintext only from server-side backend memory/adapters.
8. Pass plaintext only to runtime adapter.
9. Record redacted audit metadata.
10. Do not return plaintext to frontend, usage_event, audit_event, logs, or Admin.

## usage_event Redaction Result

usage_event can show:

- `tenant_id`
- `task_id`
- `employee_id`
- `employee_role`
- `capability_source`
- `capability_type`
- `capability_id`
- `credential_id`
- `credential_ref_digest`
- `status`
- `created_at`

usage_event must not show:

- API key
- token
- secret
- credential value
- Authorization header
- raw sensitive provider response

RC result: passed.

## audit_event Redaction Result

audit_event can show:

- `tenant_id`
- `credential_id`
- `credential_ref_digest`
- `actor_id`
- `action`
- `status`
- `reason`
- `timestamp`

audit_event must not show:

- API key
- token
- secret
- plaintext credential value
- restorable secret configuration

RC result: passed.

## Tenant Isolation Result

- Same-tenant credential resolve/test passed.
- Cross-tenant credential resolve/test rejected.
- Disabled credential resolve/test rejected.
- Admin usage/audit reads stayed redacted.
- tenant_private credential did not leak to another tenant through Workspace scoped APIs.

RC result: passed.

## Admin / Workspace Boundary

- Workspace owns tenant_private credential metadata and private capability binding.
- Workspace runtime does not call `/api/platform/*`.
- Admin can observe redacted usage_event and audit_event.
- Admin cannot read tenant_private plaintext credential.
- Admin does not manage Workspace employee instances or tenant_private private capability configuration.

## Screenshot Checklist

Capture these demo artifacts:

- tenant_private credential creation API response or future credential page.
- credential_ref display or binding response.
- private model / tool / connector credential_ref binding response.
- Employee private capability binding in Workspace.
- Employee task execution in Workspace.
- Task result page.
- Admin usage_event redacted credential attribution.
- Admin audit_event redacted credential audit.

## Stability Verification

Focused resolver / leakage tests:

```bash
cd backend && .venv/bin/python -m unittest tests.test_phase5_credential_vault
```

Result:

```text
Ran 4 tests in 0.192s
OK
```

Focused test-output leakage check:

```bash
cd backend && .venv/bin/python -m unittest tests.test_phase5_credential_vault 2>&1 | tee /tmp/phase5_g2_demo_freeze_test_output.txt
! rg -n "phase5[-]secret[-]value|Authorization: Bearer" /tmp/phase5_g2_demo_freeze_test_output.txt
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
Ran 310 tests in 8.774s
OK
```

Frontend unit tests:

```bash
cd frontend && node --test app/taskViewModel.test.mjs
```

Result:

```text
tests 30
pass 30
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

Diff check:

```bash
git diff --check -- backend/app/credential_vault.py backend/app/runtime_capability_context.py backend/app/database.py backend/app/main.py backend/app/orchestrator.py backend/app/result_store.py backend/app/evolution_event_log.py backend/app/tool_executor.py backend/tests/test_phase5_credential_vault.py backend/tests/test_model_gateway_adapter.py issues/phase5_g2_credential_vault_gate.md knowledge/CURRENT_CONTEXT.md docs/release/phase5-g2-credential-vault-implementation-report.md docs/release/phase5-g2-credential-vault-rc.md docs/demo/phase5-g2-credential-vault-demo-script.md docs/release/phase5-g2-credential-vault-demo-freeze-report.md
```

Result:

```text
PASS
```

Workspace runtime `/api/platform/*` scan:

```bash
! rg -n "/api/platform/" frontend/app/page.js backend/app/credential_vault.py backend/app/runtime_capability_context.py backend/app/orchestrator.py backend/app/result_store.py backend/app/tool_executor.py backend/app/model_gateway.py
```

Result:

```text
PASS
```

Changed production/docs secret scan:

```bash
! rg -n "phase5[-]secret[-]value|sk-[A-Za-z0-9]{16,}|BEGIN (RSA|OPENSSH|EC|PRIVATE)|AKIA[0-9A-Z]{16}" backend/app/credential_vault.py backend/app/runtime_capability_context.py backend/app/database.py backend/app/main.py backend/app/orchestrator.py backend/app/result_store.py backend/app/evolution_event_log.py backend/app/tool_executor.py issues/phase5_g2_credential_vault_gate.md knowledge/CURRENT_CONTEXT.md docs/release/phase5-g2-credential-vault-implementation-report.md docs/release/phase5-g2-credential-vault-rc.md docs/demo/phase5-g2-credential-vault-demo-script.md docs/release/phase5-g2-credential-vault-demo-freeze-report.md
```

Result:

```text
PASS
```

## Known Limits

- This is local/demo only.
- Local/demo plaintext lives only in app process memory; restarting backend requires updating credential before resolution works again.
- Vault/KMS adapters are stubs/interfaces.
- No credential-management frontend UI exists yet; the demo uses API commands for credential creation and binding.
- private tool/connector credential binding is visible and persisted as reference metadata, but deeper provider-specific runtime behavior remains future-gated.
- Not a Workflow, Billing, Marketplace, ROI, or production credential governance release.

## Freeze Decision

Phase-5 G2 Credential Vault can be frozen as the local/demo version after product acceptance.

Next recommended step: capture the eight screenshots/artifacts listed above from a clean `/tmp/curis_phase5_g2_demo.sqlite` database.
