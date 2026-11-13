# CURIS V1 — Cloud Model Selection + Restart Execution Continuity

Status: IMPLEMENTED / ACCEPTED CANDIDATE

Owner: Main Development Session

## Goal

Close the existing cloud-model continuity gap without changing Keychain: a tenant-scoped model
that was discovered through a healthy registered Provider can be selected as the tenant default,
revalidated after packaged restart, resolved for the existing Workbench execution path, and used
again without converting preference metadata into Health or AI Ready.

## Authority and inputs

- `issues/V1-P0-003-MACOS-KEYCHAIN-CREDENTIAL-PERSISTENCE.md`
- `docs/reviews/CURIS_V1_P0_003_KEYCHAIN_IMPLEMENTATION_REVIEW.md`
- current Provider Registry / discovery / recovery implementation
- current tenant model preference and conversation selector implementation
- current Model Gateway / Workbench Guide execution implementation
- current canonical Usage Attribution and Runtime truth

## Current gaps

1. `TenantModelPreferenceResolver` only accepts active `official_models`; a real current-tenant
   DeepSeek discovery row in `tenant_private_capabilities` is rejected with HTTP 422.
2. The packaged Gateway waits synchronously for at most 60 seconds. The recorded post-restart
   call used the recovered Keychain credential, logged one `network_error`, then a successful
   second Provider attempt, but the Gateway had already returned 503 before the Workspace Runtime
   could return its final response.

## Eligibility contract

- Existing official active models remain eligible exactly as before.
- A tenant-private model is eligible only when it belongs to the current tenant, is active, was
  produced by the existing registered Provider discovery path, has coherent Provider/model/
  credential metadata, and its discovery verification is available.
- Preference expresses user selection only. It never upgrades credential, Provider Health,
  capability availability or AI Ready.
- Restart may restore preference metadata, but Provider recovery must revalidate Health and model
  discovery before Runtime/UI presents the model as ready.
- Missing, disabled, wrong-tenant, unknown-provider, stale/unavailable or fabricated model refs
  fail closed.

## Exact Allowed Files

- `backend/app/model_preferences.py`
- `backend/app/ai_capability_registry.py`
- `backend/app/workbench_guide.py`
- `backend/tests/test_tenant_model_preference.py`
- `backend/tests/test_ai_capability_registry.py`
- `backend/tests/test_workbench_guide_backend.py`
- `desktop/runtime/gateway.py`
- `backend/tests/test_desktop_gateway_continuity.py`
- `frontend/components/v1/ModelManagement.js`
- `frontend/components/v1/SharedConversation.js`
- `frontend/tests/v1FrontendBatch1.test.mjs`
- `issues/CURIS-V1-CLOUD-MODEL-CONTINUITY-001.md`
- `docs/reviews/CURIS_V1_CLOUD_MODEL_CONTINUITY_IMPLEMENTATION_REVIEW.md`
- `docs/reviews/CURIS_V1_P0_003_KEYCHAIN_IMPLEMENTATION_REVIEW.md` (cross-reference only)

## Pre-change hashes

- HEAD: `c0e1855f446a55aa3a384006cfcfed9877130338`
- `backend/app/model_preferences.py`: `9d1ad3751ee0bdc41d45bf28e403f662cc93b328b81cb402887f2a680189dc3f`
- `backend/app/ai_capability_registry.py`: `39fbb433fc3236a06521b76814e754ccbd1d0b169afc794cd6c4d917e35dce19`
- `backend/app/workbench_guide.py`: `d801b2d294d36a2668391e011de222b9f4149c29fe3d72d8f9f808c2384b45dc`
- `backend/tests/test_tenant_model_preference.py`: `7c84f9e466ca2b81cee79753cc4acba94152455a0a6a1f8d28ba9744cfd7cda2`
- `frontend/components/v1/ModelManagement.js`: `4be7d4fbc962805f64e8680df1918d3a72c91491e89f1a2ae80377c74b9eb4ae`
- `frontend/components/v1/SharedConversation.js`: `498764f05a0ed31a196d43239f6aa6f2f766f7b2f37634bb49638cdd5206c9cd`
- `frontend/tests/v1FrontendBatch1.test.mjs`: `6c9f8405b37b2ee505aebc55a8d8a8f1571d209a2f649aec3e27974e51ec95bc`

## Active database preflight

| Path | Size | mtime | SHA-256 | integrity_check |
| --- | ---: | ---: | --- | --- |
| `data/curis.sqlite` | 1232896 | 1786873339 | `2ea2506f90f764e834d47d8f6bae3cb41c22d457757e0e9216c0ae8c39a39ec6` | ok |
| `backend/data/curis.sqlite` | 1277952 | 1786783659 | `a9d96a9536a5bce3b3b30f912e86a37f61d28527a8eb2d35af7a5857d29414e4` | ok |

All tests and Runtime evidence must use repository-external isolated SQLite.

## Acceptance

- official and eligible discovered models can be selected; tenant/provider/model isolation fails
  closed;
- model disappearance, disabled capability, missing credential and unavailable recovery never
  manufacture AI Ready;
- preference survives restart-like reconstruction as metadata and is revalidated before use;
- explicit selection remains ahead of employee binding, tenant default and No Model;
- Workbench resolver uses the selected eligible tenant-private model without exposing its key;
- packaged Gateway does not report a Runtime-owned bounded retry as a false business 503;
- real packaged DeepSeek sequence passes save, Health, discovery, set default, first call, full
  close, restart, recovery, same default, second call, delete and restart-unconnected;
- secret scan is zero and both active databases remain byte-identical;
- credential, Provider, model preference/selector, CEO Assistant, General Workspace, RD, usage,
  App Entry and DB-safety regressions pass.

## Explicit exclusions

- no Keychain backend, account/service naming or Credential Vault persistence changes;
- no new Provider, model catalog, schema, Model Router, conversation system or UI redesign;
- no Professional Workspace, signing/notarization, legacy cleanup, commit or push.

## Stop conditions

Stop for review on a Keychain/security defect, need for a new schema/Authority, active database
mutation, or any required edit outside the exact Allowed Files.

## Acceptance result

The bounded continuity chain is closed in
`docs/reviews/CURIS_V1_CLOUD_MODEL_CONTINUITY_IMPLEMENTATION_REVIEW.md`:

- a verified current-tenant discovered model can be selected without becoming official;
- preference metadata is revalidated against credential, Provider recovery and discovery;
- the packaged Gateway no longer turns the Runtime-owned retry window into a false 503;
- real DeepSeek calls succeeded before and after full packaged restart with the same model;
- credential deletion and restart returned the exact packaged app to not connected;
- structural secret scan returned zero hits and both active SQLite files remained byte-identical.

No Keychain implementation, schema, Provider catalog, model router or product Authority changed.
