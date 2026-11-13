# Phase-5 G2 Credential Vault Implementation Report

Date: 2026-07-09

Status: implemented, pending RC acceptance.

Issue: `issues/phase5_g2_credential_vault_gate.md`

## Product Progress

Curis Workspace can now create tenant-scoped credential metadata, resolve local/demo credential_ref values through a server-side resolver, bind credentials to tenant_private capabilities, execute a private model through the resolver, and write redacted credential attribution into usage_event and audit_event.

## Implementation Scope

- Added credential metadata persistence without plaintext secret storage.
- Added tenant-scoped Workspace credential APIs.
- Added local/demo credential backend.
- Added Vault/KMS adapter interface stubs.
- Added Credential Resolver Service.
- Added credential binding/unbinding for tenant_private model/tool/connector capabilities.
- Integrated tenant_private model execution with resolver-backed Model Gateway Adapter configuration.
- Added credential attribution to usage_event.
- Added credential audit events.
- Added redaction and boundary tests.

## Not Implemented

- No real Vault/KMS provider integration.
- No hosted production credential backend.
- No Workflow MVP.
- No Billing.
- No ROI.
- No capability marketplace.
- No Admin Platform tenant_private secret access.
- No complex employee-system expansion.
- No provider SDK or direct provider calls.

## Security Boundary

- Database stores only credential metadata:
  - `credential_id`
  - `tenant_id`
  - `name`
  - `provider`
  - `credential_type`
  - `credential_ref`
  - `status`
  - `encrypted_metadata`
  - `created_at`
  - `updated_at`
  - `disabled_at`
- Plaintext secret is held only in local/demo in-memory backend during the app process lifetime.
- Plaintext secret is never returned by API responses.
- Plaintext secret is never written to `usage_event`.
- Plaintext secret is never written to `audit_event`.
- Plaintext secret is never written to the database.
- `local-dev://` creation and resolution are blocked when `CURIS_ENV=production` or `CURIS_ENV=prod`.
- Resolver validates tenant_id in credential_ref before resolving.
- Cross-tenant credential resolution is rejected.

## API List

Workspace credential APIs:

- `GET /api/workspace/credentials`
- `POST /api/workspace/credentials`
- `PUT /api/workspace/credentials/{credential_id}`
- `POST /api/workspace/credentials/{credential_id}/test`
- `POST /api/workspace/credentials/{credential_id}/disable`
- `DELETE /api/workspace/credentials/{credential_id}`

Workspace private capability binding APIs:

- `PUT /api/workspace/private-capabilities/{capability_type}/{capability_id}/credential`
- `DELETE /api/workspace/private-capabilities/{capability_type}/{capability_id}/credential`

No Workspace runtime `/api/platform/*` call was added.

## Data Model

Table: `credential_metadata`

| Field | Purpose |
| --- | --- |
| `credential_id` | Stable credential id. |
| `tenant_id` | Tenant ownership and isolation boundary. |
| `name` | CEO-facing display name. |
| `provider` | Provider or gateway family, for example `newapi`. |
| `credential_type` | Shape label such as `api_key`. |
| `credential_ref` | Opaque resolver reference. |
| `status` | `active`, `disabled`, or `deleted`. |
| `encrypted_metadata` | Non-reversible metadata such as backend and digest. |
| `created_at` | Creation timestamp. |
| `updated_at` | Last update timestamp. |
| `disabled_at` | Disable/delete timestamp. |

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
- production `credential_ref` without tenant_id
- cross-tenant `credential_ref`
- `local-dev://` in production

## Resolver Behavior

Resolver steps:

1. Parse `credential_ref`.
2. Validate allowed scheme.
3. Validate `tenant_id` matches `TenantContext`.
4. Reject `local-dev://` in production.
5. Load credential metadata by current tenant and credential id.
6. Reject disabled/deleted credentials.
7. Resolve plaintext only from backend memory/adapters.
8. Return plaintext only to the server-side runtime caller.
9. Emit redacted audit event.
10. Discard plaintext after runtime call completes.

## AuditEvent

Credential audit events are allowlisted under `credential.*`:

- `credential.created`
- `credential.updated`
- `credential.disabled`
- `credential.deleted`
- `credential.tested`
- `credential.bound`
- `credential.unbound`
- `credential.resolved`
- `credential.resolve_failed`

Payload contains only:

- `tenant_id`
- `credential_id`
- `credential_ref_digest`
- `actor_id`
- `action`
- `status`
- `reason`
- `timestamp`

## usage_event

usage_event now may include:

- `credential_id`
- `credential_ref_digest`

It still includes existing tenant/task/employee/capability/model attribution and excludes plaintext secrets, raw provider bodies, Authorization headers, prompts, and outputs.

## Test Commands And Results

Focused Phase-5 tests:

```bash
cd backend && .venv/bin/python -m unittest tests.test_phase5_credential_vault
```

Result:

```text
Ran 4 tests in 0.190s
OK
```

Backend regression:

```bash
cd backend && .venv/bin/python -m unittest discover tests
```

Result:

```text
Ran 310 tests in 8.955s
OK
```

Frontend tests:

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

Additional verification:

- `git diff --check`: passed.
- Workspace runtime `/api/platform/*` scan: passed.
- Secret scan over changed production/docs files for actual secret patterns: passed.

## Known Limits

- Local/demo backend keeps plaintext in process memory only; restarting the app loses the local secret until the credential is updated.
- Vault/KMS adapters are interfaces/stubs only.
- Production credential storage remains blocked until a real backend is selected.
- Tool/connector credential_ref binding is supported, but deep provider-specific runtime behavior remains future-gated.
- No frontend credential-management UI was added in this phase.

## RC Recommendation

Phase-5 G2 Credential Vault minimum safety loop can enter RC verification after final scope scans pass.
