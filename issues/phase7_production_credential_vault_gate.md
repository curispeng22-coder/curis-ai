# Phase-7 Production Credential Vault/KMS Gate

Status: Draft for future security gate review

Owner Seat: 安全边界席 for security scope; 总控决策席 for gate approval; 系统交付席 only after approval.

Source review: `docs/release/phase65-post-workflow-roadmap-review.md`

## Background

Phase-5 G2 delivered a local/demo Credential Vault safety loop. tenant_private capability execution can use `credential_ref` through the server-side resolver, and plaintext credentials do not enter database rows, frontend responses, usage_event, audit_event, or Admin reads.

Production customer use still requires a real Vault/KMS backend. `local-dev://` is not acceptable for production.

## Goal

Define the production credential custody boundary before implementing real customer private credential storage.

## Non-Goals

- Do not implement production Vault/KMS in this gate.
- Do not change Workflow runtime behavior.
- Do not implement Billing.
- Do not implement Marketplace.
- Do not implement ROI.
- Do not let Admin read tenant_private plaintext secrets.
- Do not let Workspace runtime call `/api/platform/*`.

## Data Model Impact

To be defined by 安全边界席 and 系统交付席 after gate approval.

Expected boundary areas:

- Production credential metadata.
- `vault://tenant/{tenant_id}/credential/{credential_id}` or `kms://tenant/{tenant_id}/credential/{credential_id}`.
- Rotation/disable/delete metadata.
- Redacted audit metadata.

## API Impact

To be defined after gate approval.

Expected constraints:

- Workspace APIs must never return plaintext credentials.
- Resolver output must remain server-side only.
- Admin APIs must observe only redacted audit and attribution.

## UI Impact

No UI is approved by this gate.

Future UI, if approved separately, must not display plaintext after create/test operations unless a separate security decision explicitly permits a one-time write-only input flow.

## Security Boundary

- Production must reject `local-dev://`.
- Production must reject plaintext credential_ref formats.
- Tenant id must be present in production credential_ref.
- Cross-tenant credential resolution must fail.
- AuditEvent and usage_event must remain redacted.
- Logs, errors, tests, and API responses must not leak plaintext.

## Test Requirements

- Production rejects `local-dev://`.
- Same-tenant production credential can resolve through approved adapter.
- Cross-tenant credential cannot resolve.
- Disabled/deleted credential cannot resolve.
- Logs/API/errors/usage_event/audit_event contain no plaintext.
- Workspace runtime `/api/platform/*` scan passes.
- Secret scan passes.

## Acceptance Criteria

- 安全边界席 accepts the production custody model.
- 总控决策席 approves or rejects production implementation entry.
- No implementation occurs before the gate is accepted.

## Recommended Priority

P1.

Reason: required before hosted customer use of tenant_private real credentials, but not required to improve the current local/demo package.
