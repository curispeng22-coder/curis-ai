# V1-P0-003 — macOS Keychain Credential Persistence

Status: IMPLEMENTED / PARTIAL

Owner: Main Development Session — Security + Desktop Runtime

## Goal

Persist a credential in the macOS Keychain, close the packaged Desktop, restart it, recover Health and complete one minimal real provider call without exposing the secret in SQLite, logs or API responses.

## Current truth

`CredentialVaultService` owns both the existing explicit development backend and a native
`MacOSKeychainCredentialBackend`. Packaged Desktop explicitly selects Keychain and rejects
process-memory fallback. With a CEO-entered legal DeepSeek test credential, the fresh package
proved native save, real Health, dynamic discovery, one minimal real call, full process exit,
restart recovery without re-entry, deletion and restart fail-closed against an isolated
application-data directory. Final acceptance remains partial because the current model-preference
contract only accepts official catalog models (the discovered tenant-private DeepSeek model cannot
be set as the tenant default), and the post-restart minimal call returned a truthful Provider 503.

## Allowed Files

- `backend/app/credential_vault.py`
- `backend/app/ai_capability_registry.py` — provider-bound resolve and restart recovery route only
- `backend/tests/test_v1_p0_003_keychain.py`
- `frontend/lib/v1FrontendApi.js` — recovery call only
- `frontend/components/v1/ModelManagement.js` — secret lifecycle / restart recovery seam only; no redesign
- `frontend/components/v1/SharedConversation.js` — AI Ready must consume real provider revalidation
- `frontend/tests/v1FrontendBatch1.test.mjs` — focused credential/revalidation contract assertions
- `desktop/src/lib.rs` — packaged backend selection and explicit isolated acceptance data root only
- `issues/V1-P0-003-MACOS-KEYCHAIN-CREDENTIAL-PERSISTENCE.md`
- `docs/reviews/CURIS_V1_P0_003_KEYCHAIN_IMPLEMENTATION_REVIEW.md`

`backend/app/main.py` is explicitly excluded: it is mixed-source and the existing
Vault/router registration is sufficient.

## Pre-change evidence

- HEAD: `c797db840bad285d7e9f1962d06eac61aa28508b`
- `backend/app/credential_vault.py`: `7f7a6878f9b2582e6cff9bbc78f7933c2eb88cc13e288d58dfd73037cea7df48`
- `backend/app/ai_capability_registry.py`: `27dc7984ba833fe21559cd05e4af9d69520872b75acdc8e52bb19192ccefed70` (accepted untracked baseline)
- `frontend/lib/v1FrontendApi.js`: `5f15ae7c883e0b307fa62a6eff5c3e8718242fbc897e8880763783ac8f8c258b` (accepted untracked baseline)
- `frontend/components/v1/ModelManagement.js`: `c58db1bb9f4d25acfcd693e1944caeba0a93b6554192b3bb5ff7eeb81145d774` (accepted untracked baseline)
- `frontend/components/v1/SharedConversation.js`: `170c868eda0719cac2a2f7522fddefe87f32214cff56104cf0a4cc728475fcf4` (accepted untracked baseline)
- `frontend/tests/v1FrontendBatch1.test.mjs`: `81c8e7c82e7b72ada8eef26d8b74a013d9ec139a99ea335108bec4cb850c54ce` (accepted untracked baseline)
- `desktop/src/lib.rs`: `d2ada1540eb173f567c9396481ed66424646928a663b96adb7021f8476fcc56d`
- Active DB fingerprints are recorded in the implementation Review; both started at
  `integrity_check=ok` and may not change.

## Security invariants

- macOS Keychain is the only durable production secret authority.
- Packaged Runtime selects Keychain explicitly and never falls back to memory,
  environment, SQLite, command arguments or plaintext files.
- Keychain identifiers contain only deterministic non-secret scope/reference data.
- API responses, logs, usage, evidence, URLs and frontend persistence never contain
  the secret.
- Keychain presence is not Provider Health; restart must perform a real provider
  revalidation before reporting connected.
- Provider and tenant scope are checked before a credential is resolved.

## Test matrix

- Native backend: save/read/overwrite/delete/missing/recreation/availability.
- Vault: stable `vault://` reference, tenant/provider isolation, unavailable backend,
  packaged no-fallback, metadata-only API response.
- Provider: Vault-backed Health/discovery, restart recovery, wrong-provider rejection,
  failure remains not healthy.
- Frontend: submitted secret is cleared; recovered reference can revalidate without
  re-entering the Key; no browser persistence.
- Desktop: packaged sidecar explicitly selects `macos-keychain`.
- Regression: credential vault, Provider Registry, model preference, App Entry,
  General Workspace, RD/XHS, DB safety, frontend build and fresh package.

## Stop gates

- Stop on any plaintext fallback, secret persistence/leak, active DB mutation or need
  for a second credential truth.
- Missing legal cloud test credential may leave only real-cloud acceptance blocked;
  it does not authorize a fake call.
- Native Keychain denial is recorded exactly and is never bypassed.

## Explicit Exclusions

- No environment-variable, plaintext file, SQLite or command-line-argument fallback.
- No process-memory implementation presented as restart persistence.
- No secret in logs, screenshots, API payloads or tests.
- No temporary security architecture invented inside the delivery Epic.

## Acceptance Gate

Verify a fresh packaged `Curis.app` performs save → Health → close → restart →
Keychain recovery → real Health → one minimal cloud call, with delete/fail-closed and
active-DB safety evidence. Without a legal cloud credential the maximum verdict is
`IMPLEMENTED / PARTIAL`.

## Final disposition

- Native Keychain backend and Credential Vault integration: implemented.
- Packaged save/read/restart/delete and fail-closed behavior: verified.
- Secret leakage scan over isolated SQLite/logs/generated app data: no match.
- Provider Health with a deliberately invalid packaged test credential: correctly failed closed.
- Real DeepSeek Health and dynamic discovery: verified before and after packaged restart.
- Minimal real DeepSeek call before restart: verified with `deepseek-v4-pro`; no sensitive business
  data was submitted.
- Tenant default selection: not verified; the existing official-only preference contract rejected
  the tenant-private capability before any default was written.
- Post-restart minimal real call: attempted through the same Keychain-backed Runtime and returned a
  truthful 503 after the existing bounded retry behavior; no success was fabricated.
- Credential deletion and a subsequent packaged restart: verified; Provider recovery returned
  `credential is not active` and the CEO Desk projected no connected model.
- Formal evidence: `docs/reviews/CURIS_V1_P0_003_KEYCHAIN_IMPLEMENTATION_REVIEW.md`.
