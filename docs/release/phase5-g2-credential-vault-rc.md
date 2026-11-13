# Phase-5 G2 Credential Vault RC

Date: 2026-07-09

Status: RC verified, pending product acceptance.

Issue: `issues/phase5_g2_credential_vault_gate.md`

Implementation report: `docs/release/phase5-g2-credential-vault-implementation-report.md`

## Product Progress

Curis Workspace can now use resolver-managed `credential_ref` for tenant_private private capabilities in local/demo, while keeping plaintext credentials out of database rows, frontend responses, usage_event, audit_event, and Admin read projections.

## Implemented Scope Under RC

- Credential metadata persistence without plaintext secret storage.
- Workspace credential create / list / update / test / disable / delete APIs.
- `local-dev://tenant/{tenant_id}/credential/{credential_id}` local/demo credential_ref generation.
- Production-reserved `vault://tenant/{tenant_id}/credential/{credential_id}` and `kms://tenant/{tenant_id}/credential/{credential_id}` formats.
- Resolver service with tenant, status, and environment validation.
- Local/demo credential backend with server-side in-memory plaintext only.
- Vault/KMS adapter interface stubs.
- tenant_private model/tool/connector credential binding and unbinding.
- tenant_private private model execution through resolver-backed Model Gateway Adapter.
- Redacted credential attribution in usage_event.
- Redacted credential audit events.

## Acceptance Flow

1. Create credential through Workspace API.
2. Confirm API response contains only safe metadata and no plaintext secret.
3. Confirm database file does not contain plaintext secret.
4. Confirm generated credential_ref uses `local-dev://tenant/{tenant_id}/credential/{credential_id}`.
5. Confirm same tenant can test/resolve credential.
6. Confirm another tenant cannot test/resolve credential.
7. Disable credential and confirm resolver rejects it.
8. Set production environment and confirm `local-dev://` cannot resolve.
9. Bind credential_ref to private model, private tool, and private connector.
10. Execute selected tenant_private private model path.
11. Confirm runtime uses resolver-provided secret only on server side.
12. Confirm usage_event records `credential_id` and `credential_ref_digest`, not plaintext.
13. Confirm audit_event records allowlisted credential metadata only.
14. Confirm Workspace runtime does not call `/api/platform/*`.
15. Confirm Admin can only observe redacted attribution and audit data.

## Security Boundary Results

- Plaintext API key / token / secret did not enter the database.
- Plaintext did not return in API responses.
- Plaintext did not appear in resolver error responses.
- Plaintext did not appear in usage_event.
- Plaintext did not appear in audit_event.
- Plaintext did not appear in focused test output.
- Admin usage/audit reads did not expose tenant_private plaintext.
- tenant_private credential metadata remained tenant-scoped.
- Cross-tenant credential access was rejected.
- Disabled credentials were rejected.
- Production `local-dev://` resolution was rejected.

## credential_ref Format

Allowed local/demo format:

```text
local-dev://tenant/{tenant_id}/credential/{credential_id}
```

Production-reserved formats:

```text
vault://tenant/{tenant_id}/credential/{credential_id}
kms://tenant/{tenant_id}/credential/{credential_id}
```

Forbidden:

- `plaintext://`
- `raw_api_key`
- production credential_ref without tenant id
- cross-tenant credential_ref
- `local-dev://` in production

## Resolver RC Result

Validated:

- Same tenant credential test/resolve succeeds.
- Cross-tenant credential test returns not found / unavailable.
- Disabled credential test fails.
- Production environment rejects `local-dev://`.
- Resolver error messages do not include the plaintext credential.
- Resolver output is used only server-side and is not returned to frontend.

Known local/demo behavior:

- The local backend holds plaintext only in app process memory.
- Restarting the process clears local plaintext memory; credential metadata remains but the credential must be updated before local/demo resolution can succeed again.

## Private Capability Binding Result

Validated:

- private model can bind resolver-managed credential_ref.
- private tool can bind resolver-managed credential_ref.
- private connector can bind resolver-managed credential_ref.
- tenant_private private model execution uses resolver-managed secret through Model Gateway Adapter.
- usage_event preserves capability attribution and credential digest attribution.

## usage_event Redaction Result

Allowed fields observed:

- `tenant_id`
- `task_id`
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

- API key
- token
- secret
- credential value
- Authorization header
- raw provider sensitive response
- prompt or raw model output

## audit_event Redaction Result

Allowed payload keys verified:

- `tenant_id`
- `credential_id`
- `credential_ref_digest`
- `actor_id`
- `action`
- `status`
- `reason`
- `timestamp`

Forbidden values not observed:

- API key
- token
- secret
- plaintext credential value
- restorable secret configuration

## Tenant Isolation Result

- Tenant A credential could be tested and used by Tenant A.
- Tenant B could not test Tenant A credential.
- Tenant B could not read Tenant A employee/capability credential binding through Workspace-scoped APIs.
- Admin usage query remained tenant_id-scoped and returned only redacted attribution.

## Test Commands And Results

Focused secret and resolver tests:

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
cd backend && .venv/bin/python -m unittest tests.test_phase5_credential_vault 2>&1 | tee /tmp/phase5_g2_rc_test_output.txt
! rg -n "phase5[-]secret[-]value|Authorization: Bearer" /tmp/phase5_g2_rc_test_output.txt
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
git diff --check -- backend/app/credential_vault.py backend/app/runtime_capability_context.py backend/app/database.py backend/app/main.py backend/app/orchestrator.py backend/app/result_store.py backend/app/evolution_event_log.py backend/app/tool_executor.py backend/tests/test_phase5_credential_vault.py backend/tests/test_model_gateway_adapter.py issues/phase5_g2_credential_vault_gate.md knowledge/CURRENT_CONTEXT.md docs/release/phase5-g2-credential-vault-implementation-report.md docs/release/phase5-g2-credential-vault-rc.md
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
! rg -n "phase5[-]secret[-]value|sk-[A-Za-z0-9]{16,}|BEGIN (RSA|OPENSSH|EC|PRIVATE)|AKIA[0-9A-Z]{16}" backend/app/credential_vault.py backend/app/runtime_capability_context.py backend/app/database.py backend/app/main.py backend/app/orchestrator.py backend/app/result_store.py backend/app/evolution_event_log.py backend/app/tool_executor.py issues/phase5_g2_credential_vault_gate.md knowledge/CURRENT_CONTEXT.md docs/release/phase5-g2-credential-vault-implementation-report.md docs/release/phase5-g2-credential-vault-rc.md
```

Result:

```text
PASS
```

## Known Limits

- Local/demo credential backend is process memory only; restart requires credential update before local resolution works again.
- Vault/KMS adapters are interfaces/stubs; no real external Vault/KMS integration is active.
- No frontend credential-management UI was added.
- private tool and private connector can bind credential_ref, but deeper provider-specific runtime use remains future-gated.
- This is not Billing, Marketplace, ROI, Workflow, or production credential governance.

## RC Decision

Phase-5 G2 Credential Vault minimum safety loop can enter Phase-5 Demo Freeze after product acceptance.
