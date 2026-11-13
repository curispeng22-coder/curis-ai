# Review 066: Model Gateway Production Security Boundary

Date: 2026-07-08

Issue: `issues/069_model_gateway_production_security_boundary.md`

## Security Result

PASS-WITH-GUARDRAILS.

The implementation boundary is accepted for continued 系统交付席 planning, provided production external-model operation is not enabled until runtime secret guardrails are implemented and verified.

## Boundary Defined

- New API remains a model gateway only, not a Curis primary system.
- Curis does not modify New API source code.
- Curis does not depend on New API internal database tables.
- Curis DB may store only gateway/model metadata and non-secret `credential_ref` values.
- Curis DB must not persist New API admin credentials, Curis New API tokens, upstream provider keys, Authorization headers, or secret values.
- Workspace model calls remain constrained to `ModelGatewayAdapter`.
- Admin Platform owns official gateway/model metadata and enable/disable decisions, but must not proxy model calls or store secret values.
- Workspace owns runtime consumption and UsageEvent metering, but must not manage New API channels or upstream provider keys.

## UsageEvent Boundary

Approved model-meter fields:

- `tenant_id`
- `task_id`
- `model_gateway_id`
- `model_name`
- `token`
- `estimated_cost`
- `status`

UsageEvent payloads must not include API keys, tokens, admin credentials, Authorization headers, prompts, user input text, model output text, raw HTTP payloads, New API internal ids, or provider account secrets.

## Secret Handling Decision

- Local: secrets may live only in ignored local env files, local password manager, New API local configuration, or New API local data.
- Test/CI: normal regression must not require live external keys; live smoke must use protected environment injection.
- Production: tokens and upstream keys must come from a secret manager/KMS/Vault/env injection path. Curis DB stores no secret values.

## Commands

```bash
git check-ignore -v deploy/new-api/.env deploy/new-api/data
git ls-files --cached --others --exclude-standard | rg -v '^(deploy/new-api/\.env|deploy/new-api/data/|backend/data/|backend/tests/data/)' | xargs rg -n -l --pcre2 '(^|[^A-Za-z])sk-(?!placeholder|your|test|example)[A-Za-z0-9_-]{32,}|sk-or-v1-[A-Za-z0-9_-]{32,}'
rg -n "ROI|billing|tenant package|tenant_package|New API source|calciumion/new-api|mock|simulation|Admin Platform UI|Employee CRUD|multi-agent" issues/069_model_gateway_production_security_boundary.md docs/deployment/new-api-local.md reviews/065_new_api_local_deployment_review.md
```

## Evidence

- `deploy/new-api/.env` and `deploy/new-api/data/` are ignored by `.gitignore`.
- Strict `sk-` / `sk-or-v1-` secret-pattern scan outside ignored New API local files and runtime/test data returned no matches.
- Existing deployment review confirms New API source code was not modified and Curis does not depend on New API internal database tables.
- Existing adapter review confirms default AI Task Executor model calls route through `ModelGatewayAdapter`.
- Existing schema comments and tests confirm `model_gateways` and `official_models` store metadata only and no API key/token/secret columns.

## Known Gaps

- Production secret-manager retrieval is not implemented.
- Runtime redaction guard tests are not yet implemented.
- Live external smoke still depends on local/operator-managed secrets.

## Required Follow-Up

Before production external-model operation, open and route this bounded implementation issue to 系统交付席:

```text
issues/070_model_gateway_runtime_secret_guardrails.md
```

Scope: startup env validation, redaction guard tests, UsageEvent allowlist regression, catalog/gateway no-secret regression. No UI, billing, ROI, tenant package, credential persistence, New API source change, provider SDK, or New API internal DB dependency.

## Handoff

Next Seat: 系统交付席

Handoff: sent to 系统交付席

Payload sent:

```text
Issue: issues/069_model_gateway_production_security_boundary.md
Objective: Implement only the accepted follow-up boundary if opened: issues/070_model_gateway_runtime_secret_guardrails.md for runtime env validation, log/UsageEvent redaction guards, and no-secret regression around model gateway metadata.
Special Constraints: External service + secret boundary. No UI, billing, ROI, tenant package, New API source change, Curis DB credential persistence, provider SDK, or New API internal DB dependency. Keep calls constrained to ModelGatewayAdapter.
Next Seat: 质量运行席 after implementation evidence.
```
