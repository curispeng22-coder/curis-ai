# Phase-5 G2 Credential Vault Gate

Status: RC verified pending product acceptance

Gate Decision: APPROVED_WITH_CONDITIONS by 总控决策席.

Security Sign-off: APPROVED_FOR_IMPLEMENTATION by 安全边界席 after this contract update.

Owner Seat: 总控决策席 for gate decision; 安全边界席 for security boundary; 系统交付席 only after approval.

## Background

Phase-4 made tenant_private private model/tool/connector metadata configurable in Workspace, but `credential_ref` and `config_ref` remain `scheme:reference` placeholders. This keeps demos safe, but it prevents Workspace self-extension from becoming production-usable for real private integrations.

## Goal

Define the G2 security and architecture gate for real credential_ref / config_ref secret custody and runtime resolution.

The outcome of this issue is a gate decision and boundary definition only. Implementation must be opened separately after approval.

## Non-Goals

- Do not implement credential vault storage in this issue.
- Do not store raw secrets in Workspace tables.
- Do not expose secrets in Workspace UI, Admin UI, logs, traces, usage_event, or audit payloads.
- Do not implement billing.
- Do not implement ROI.
- Do not implement marketplace.
- Do not modify New API source.
- Do not depend on New API internal database.
- Do not change Task Execution semantics.
- Do not add provider SDK or direct provider calls.

## Data Model Impact

Allowed for boundary planning:

- Define a future `CredentialReference` contract:
  - `credential_ref`
  - `tenant_id`
  - `owner_scope`
  - `capability_type`
  - `capability_id`
  - `secret_backend`
  - `status`
  - `created_at`
  - `rotated_at`
  - `last_used_at`
- Define whether the source of truth lives in Admin Platform, external secret manager, or shared contract.

Blocked in this issue:

- No table creation.
- No secret persistence.
- No migration.
- No runtime secret read.

## API Impact

Allowed for boundary planning:

- Define future Workspace read/write behavior for opaque references.
- Define future runtime resolution contract for Model Gateway Adapter / tool execution.
- Define future Admin/security audit visibility.

Blocked in this issue:

- No new API implementation.
- No `/api/platform/*` calls from Workspace runtime.
- No secret read/write endpoint implementation.

## UI Impact

Allowed for boundary planning:

- Define safe UI requirements:
  - secret entry must not echo values after save.
  - display only reference id, status, and last verification state.
  - never show raw key.

Blocked in this issue:

- No UI implementation.
- No real key input field.

## Security Boundary

This issue must be reviewed by 安全边界席 before any implementation issue opens.

Security decisions required:

- Secret owner and storage backend.
- Tenant isolation rule.
- Runtime access rule.
- Secret redaction rule.
- Rotation/revocation rule.
- Audit event allowlist.
- Failure mode when secret is missing or revoked.

## Credential Ownership

- `official` credentials are owned by Admin Platform as platform-managed credentials.
- `tenant_private` credentials are owned by the Workspace tenant.
- `marketplace` credentials are future-reserved only and are not approved for Phase-5 G2 implementation.
- Admin Platform may manage official credential policy, platform-managed credential policy, audit policy, and credential risk/disable policy.
- Admin Platform must not read tenant_private credential plaintext.
- Admin Platform must not modify tenant_private private capability configuration content.
- Admin Platform must not take over Workspace employee instances.
- Admin Platform must not bypass Workspace to manage tenant-private credentials.
- Workspace may manage and use only credentials that belong to its own tenant.
- Shared credential service owns credential storage, resolver, encryption/decryption, runtime secret access, redaction, and audit emission.

## credential_ref / config_ref Contract

Allowed local development format:

- `local-dev://tenant/{tenant_id}/credential/{credential_id}`

Allowed production formats:

- `vault://tenant/{tenant_id}/credential/{credential_id}`
- `kms://tenant/{tenant_id}/credential/{credential_id}`

Forbidden formats:

- `plaintext://`
- `env://tenant_private`
- `raw_api_key`
- Any production `credential_ref` without `tenant_id`.
- Any cross-tenant `credential_ref`.
- Any unregistered or non-allowlisted credential scheme.

Production rule:

- `local-dev://` is allowed only in local/demo environments and is forbidden in production.
- Production credential references must include `tenant_id` and must resolve only through the credential resolver.
- `config_ref` follows the same tenant isolation, resolver-only, no-plaintext, and environment allowlist rules as `credential_ref`.

## Storage Contract

Production-preferred storage:

- Vault.
- KMS-backed Secret Manager.

Database may store only:

- `credential_id`
- `tenant_id`
- `credential_ref`
- `provider`
- `type`
- `name`
- `status`
- `encrypted_metadata`
- `created_at`
- `updated_at`
- `disabled_at`
- audit fields

Database must not store:

- Plaintext API key.
- Plaintext token.
- Plaintext secret.
- Reversible plaintext config.
- Any frontend-replayable secret value.

Allowed encryption form:

- KMS envelope encrypted ciphertext is allowed.

Plaintext handling rule:

- Plaintext may exist only in short-lived server-side resolver memory.
- Plaintext must not enter logs, error messages, `usage_event`, `audit_event`, traces, frontend responses, persisted task results, or persisted execution records.
- Plaintext must be discarded immediately after the runtime call completes.

## API Boundary

Workspace may expose tenant-scoped APIs to:

- Create tenant_private credential.
- Update tenant_private credential.
- Delete or disable tenant_private credential.
- Test tenant_private credential.
- Bind `credential_ref` to private model/tool/connector.
- Unbind `credential_ref`.

Workspace API constraints:

- Workspace APIs may accept a secret only on create/update/test paths.
- Workspace APIs must never return the secret value after submission.
- Workspace APIs must return only safe metadata such as `credential_id`, `credential_ref`, status, provider/type/name, verification state, timestamps, and redacted error codes.
- Workspace runtime must not call `/api/platform/*` to resolve, read, or bypass credential boundaries.

Admin Platform may expose APIs for:

- Official credential policy.
- Platform-managed credential policy.
- Audit policy.
- Credential risk status / disable policy.

Admin Platform must not expose APIs that:

- Read tenant_private credential plaintext.
- Modify tenant_private private capability configuration content.
- Take over Workspace employee instances.
- Bypass Workspace tenant-private credential management.

Shared service responsibilities:

- Credential storage.
- Credential resolver.
- Encryption/decryption.
- Runtime secret access.
- Redaction.
- Audit emit.

Runtime requirements:

- Runtime must use secrets only through the `credential_ref` resolver.
- Runtime must not return secrets.
- Runtime must not record secrets.
- Runtime must not write secrets to `usage_event` or `audit_event`.
- Runtime must discard plaintext immediately after the call completes.

## AuditEvent Allowlist

Allowed credential audit actions:

- `credential.created`
- `credential.updated`
- `credential.disabled`
- `credential.deleted`
- `credential.tested`
- `credential.bound`
- `credential.unbound`
- `credential.resolved`
- `credential.resolve_failed`

`audit_event` may record only:

- `tenant_id`
- `credential_id`
- `credential_ref` hash or digest
- `actor_id`
- `action`
- `status`
- `reason`
- `timestamp`

`audit_event` must not record:

- API key.
- Token.
- Secret.
- Plaintext credential value.
- Any configuration that can restore the secret.

## usage_event Credential Rules

`usage_event` may record:

- `tenant_id`
- `task_id`
- `employee_id` / `employee_role`
- `capability_source`
- `capability_type`
- `capability_id`
- `credential_id`
- `credential_ref` hash or digest
- `status`
- `error_code`
- `created_at`

`usage_event` must not record:

- Plaintext API key.
- Token.
- Secret.
- Credential value.
- Raw sensitive external provider response.

## Security Red Lines

- No plaintext secret in database.
- No plaintext secret in logs.
- No plaintext secret returned to frontend.
- No plaintext secret in `usage_event`.
- No plaintext secret in `audit_event`.
- No cross-tenant credential reads.
- No Workspace call to `/api/platform/*` to bypass boundaries.
- No Admin plaintext read of tenant_private secrets.
- No `local-dev://` credential reference in production.
- No direct use of `credential_ref` without resolver.
- No production `credential_ref` without `tenant_id`.
- No raw provider secret in traces, errors, task outputs, execution records, prompt context, or model output.

## Phase-5 Minimal Implementation Scope

Approved implementation scope:

- Credential metadata model.
- `credential_ref` generation.
- Local-dev credential backend for local/demo.
- Vault/KMS adapter interface.
- Resolver service.
- Private model/tool/connector credential binding.
- Runtime resolve-and-use flow.
- Redaction.
- `audit_event`.
- `usage_event` credential attribution.
- Tenant isolation tests.
- Secret leakage tests.
- Resolver error handling tests.
- Audit allowlist tests.

Not approved in this gate:

- Workflow MVP.
- Billing MVP.
- Marketplace.
- ROI.
- Multi-business modules.
- Complex employee system expansion.
- Admin takeover of Workspace private capabilities.
- Complex secret rotation automation.
- Full multi-cloud KMS adapter coverage.
- Provider SDK/direct provider calls beyond the existing approved runtime boundary.
- Hosted production deployment.

## Sign-off

Gate condition checklist:

| Condition | Status |
| --- | --- |
| Credential ownership defined | PASS |
| `credential_ref` / `config_ref` formats defined | PASS |
| Local-dev vs production schemes separated | PASS |
| Storage contract defined | PASS |
| Plaintext persistence forbidden | PASS |
| Frontend echo forbidden | PASS |
| Log/event secret leakage forbidden | PASS |
| API boundary defined | PASS |
| Runtime resolver-only rule defined | PASS |
| AuditEvent allowlist defined | PASS |
| usage_event field rules defined | PASS |
| Security red lines defined | PASS |
| Phase-5 minimal scope defined | PASS |
| Future/non-goal scope blocked | PASS |

安全边界席 Sign-off: APPROVED_FOR_IMPLEMENTATION.

总控决策席 Conclusion: Phase-5 G2 may proceed only as the minimal credential vault safety loop described above.

Next Seat: 系统交付席.

## Test Requirements

Boundary verification must include:

- No implementation files changed.
- No raw secret examples added.
- No `/api/platform/*` Workspace runtime calls introduced.
- No new persistence created.
- Secret scan passes.
- Contract explicitly forbids raw secret exposure.

## Acceptance Criteria

- 总控决策席 approves or rejects the G2 gate.
- 安全边界席 signs off on boundary conditions.
- Secret ownership is defined.
- Workspace/Admin boundary is defined.
- Runtime resolution path is defined without implementation.
- Follow-up implementation issue can be created with precise allowed files and tests.

## Recommended Priority

P0.

Reason: real tenant_private model/tool/connector usability depends on this gate.

## Implementation Notes

Implemented on 2026-07-09:

- Credential metadata table without plaintext secret storage.
- Workspace tenant-scoped credential APIs.
- Local/demo in-memory credential backend.
- Vault/KMS adapter interface stubs.
- Credential resolver with tenant and environment validation.
- tenant_private model/tool/connector credential binding and unbinding.
- Private model execution through resolver-backed Model Gateway Adapter configuration.
- Redacted credential attribution in usage_event.
- Redacted credential audit_event allowlist.
- Boundary and redaction tests.

Implementation report: `docs/release/phase5-g2-credential-vault-implementation-report.md`.

RC report: `docs/release/phase5-g2-credential-vault-rc.md`.
