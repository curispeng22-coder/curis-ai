# ADR-0029: Model Gateway Production Security Boundary

Date: 2026-07-08

Status: Accepted by Security Boundary Seat

Issue: `issues/069_model_gateway_production_security_boundary.md`

## Context

Curis Workspace has locally verified the New API + DeepSeek path:

```text
Workspace -> ModelGatewayAdapter -> New API OpenAI-compatible API -> upstream model provider
```

This introduces external-service and secret-handling risk. The production boundary must be explicit before broader Workspace/Admin development relies on the model gateway path.

## Decision

New API is approved only as a model gateway. It is not a Curis primary system, not a Curis database dependency, and not an Admin or Workspace source-code dependency. Curis must call it only through its OpenAI-compatible HTTP surface and only from the Workspace runtime adapter path.

Workspace model execution remains constrained to `ModelGatewayAdapter`. Direct provider SDK calls, direct New API database reads, New API source modification, and provider-specific execution paths are blocked unless a later issue is approved by 总控决策席 and 安全边界席.

Curis production systems must never persist secret values in the Curis SQLite database. Admin/Workspace records may store non-secret metadata and opaque credential references only.

## Credential Boundary

| Credential | Local | Test/CI | Production |
| --- | --- | --- | --- |
| New API admin/root credentials | Local password manager or ignored local files only. Rotate if shared. | Not required for normal regression. If used, inject through CI secret store only. | Secret manager or password manager only. Never in Git, docs, logs, UsageEvent, or Curis DB. |
| Curis New API token | Runtime environment or ignored `deploy/new-api/.env` only. | Dummy value for unit tests; live smoke token only through CI secret store. | Runtime secret from secret manager/KMS/Vault/env injection. Never persisted in Curis DB. |
| Upstream provider API key, including DeepSeek | Stored only inside New API local configuration/data or local secret manager. | No live upstream key in normal regression. Live smoke requires explicit protected secret injection. | Owned by platform operations in New API or external secret manager. Never exposed to Workspace, UsageEvent, docs, logs, or Curis DB. |
| `credential_ref` | Optional non-secret reference such as `env:CURIS_MODEL_GATEWAY_API_KEY`. | Non-secret reference only. | Non-secret reference only; allowed schemes remain `env`, `kms`, or `vault`. Curis does not resolve secret values unless a future security-approved credential retrieval issue unlocks it. |

All real keys, tokens, admin passwords, session secrets, and provider credentials must stay out of Git, docs, logs, UsageEvent payloads, task results, prompts, outputs, traces, and Curis Workspace database tables.

## Admin Platform And Workspace Split

Admin Platform owns official gateway and model metadata:

- gateway id, display name, type, base URL, status, default model, and optional non-secret `credential_ref`;
- official model catalog metadata;
- enable/disable decisions and platform audit events;
- future production key custody only after a separate security gate.

Admin Platform must not:

- import or call `ModelGatewayAdapter`;
- proxy model inference;
- read New API internal database tables;
- store secret values in Curis DB;
- expose credentials through `/api/platform/*` or `/api/catalog/*`.

Workspace owns runtime consumption:

- select configured official model metadata;
- call New API only through `ModelGatewayAdapter`;
- emit usage metering after execution;
- fail closed when required tenant/CEO runtime context is missing.

Workspace must not:

- manage New API admin users, New API channels, or upstream provider keys;
- write Admin gateway configuration;
- persist gateway tokens or provider keys;
- log prompt/output content in UsageEvent.

## UsageEvent Logging Boundary

For model gateway metering, the approved UsageEvent model-meter fields are:

- `tenant_id`
- `task_id`
- `model_gateway_id`
- `model_name`
- `token`
- `estimated_cost`
- `status`

Existing non-secret audit envelope fields may remain when needed for tenant/CEO attribution and idempotency, but UsageEvent payloads must never contain:

- API keys, tokens, admin passwords, session secrets, or credential references that reveal secret material;
- Authorization headers or raw HTTP request/response bodies;
- prompts, user input text, model output text, task result content, or trace bodies;
- upstream provider account identifiers beyond approved non-secret gateway/model ids;
- New API internal row ids or database state.

## Runtime And Deployment Expectations

Local development may use ignored local env files and New API local data. Those files must stay ignored and must not be copied into docs, reviews, issue files, or test fixtures.

Automated regression should use deterministic dependency injection and dummy credentials. Live external smoke is opt-in and must use protected environment injection.

Production must use secret-manager-backed injection or equivalent platform controls. Production logs must redact Authorization headers and secret-like values. Network access to New API should be limited to the Curis runtime and Admin operations that are explicitly approved for metadata management.

## Rotation, Disable, And Incident Rules

Minimum controls before production use:

- Rotate the Curis New API token after local setup or whenever it is shared beyond the local operator.
- Disable the relevant model gateway or New API token immediately on suspected exposure.
- Disable or rotate the upstream provider key in New API or the upstream provider console after suspected exposure.
- Rotate New API admin credentials after setup, operator turnover, or suspected exposure.
- Record incident outcome as a security review note without secret values.
- Treat any secret in Git, docs, logs, UsageEvent, task payloads, traces, or Curis DB as a blocking incident.

## Follow-Up Implementation Boundary

No UI, billing, ROI, tenant package, New API source change, Curis DB credential persistence, or New API internal DB dependency is approved by this ADR.

Broader Workspace/Admin parallel development may proceed if it stays inside this boundary. Before production external-model operation, 系统交付席 should open and implement a bounded follow-up issue:

```text
issues/070_model_gateway_runtime_secret_guardrails.md
```

Proposed scope:

- startup validation for required model gateway env configuration;
- redaction guard tests for model gateway errors and UsageEvent payloads;
- regression guards that `model_gateways`, `official_models`, and UsageEvent do not expose secret values;
- no UI, no credential persistence, no New API source changes, no provider-specific SDK.

## Consequences

The local New API + DeepSeek verification is production-informative but not production credential approval. The accepted production boundary is env/secret-manager injection plus metadata-only Curis persistence. Any move from local token handling to managed production credential retrieval requires a separate 总控决策席 + 安全边界席 gate.
