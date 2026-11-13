# CURIS V1-P0-003 — Keychain Implementation Review

Status: Review

Authority Class: REVIEW

Verdict: IMPLEMENTED / PARTIAL

Owner: Main Development Session — Security + Desktop Runtime

## 1. Scope and verdict

The bounded Keychain implementation is complete. Native macOS Keychain persistence, packaged
backend selection, API secrecy, real DeepSeek Health/discovery, one minimal real cloud call,
restart recovery and delete/fail-closed behavior are verified. Final acceptance remains partial:
the discovered tenant-private DeepSeek model cannot be written through the existing official-only
tenant model-preference contract, and the post-restart minimal real call returned a truthful
Provider 503. Neither result was converted into success.

## 2. Keychain backend design

- Existing `CredentialVaultService` remains the only Runtime credential authority.
- `MacOSKeychainCredentialBackend` uses macOS Security.framework generic-password APIs directly;
  no encrypted-file substitute or new credential system was added.
- Stable service: `com.curis.desktop.credentials.v1`.
- Account identity is deterministic from tenant plus canonical credential id using SHA-256; it
  contains no secret, provider token or display-name authority.
- Supported operations: save, read, safe overwrite, delete, missing-item handling and backend
  availability.

## 3. Vault and packaged selection

- Packaged Workspace sidecar sets `CURIS_PACKAGED_RUNTIME=1` and
  `CURIS_CREDENTIAL_BACKEND=macos-keychain`.
- Packaged mode rejects `memory` / `local-dev`; Keychain failure produces credential unavailable
  and does not fall back to SQLite, environment variables or plaintext files.
- Tests inject isolated fake backends explicitly.
- `CURIS_DESKTOP_DATA_ROOT` only provides an explicit isolated acceptance root; when absent,
  normal Tauri `app_data_dir()` behavior is unchanged.

## 4. API and frontend boundary

- Credential create/update returns only safe metadata plus `vault://...` reference.
- Provider resolution validates the stored provider before returning the in-memory secret.
- Model Management clears the submitted secret after the request, never re-echoes it and does not
  use localStorage, sessionStorage or IndexedDB.
- A saved default model does not make AI Ready. Shared Conversation calls Provider recovery and
  requires real Health before projecting readiness.
- Provider recovery reuses existing private-model metadata and the existing Health/discovery path;
  Keychain item existence alone never means healthy.

## 5. Native and API evidence

Native Security.framework smoke, using a generated disposable item:

- save: PASS
- read: PASS
- overwrite: PASS
- delete: PASS
- missing after delete: `CredentialError`

Credential API → Vault → native Keychain, with repository-external SQLite:

- create HTTP 201
- returned storage `macos_keychain`
- returned reference scheme `vault`
- recreated `create_app()` then credential test HTTP 200
- overwrite HTTP 200
- delete then recreated `create_app()` produced HTTP 422
- isolated SQLite contained no submitted plaintext

## 6. Fresh packaged Desktop evidence

Built from current source on 2026-08-30:

`desktop/target/release/bundle/macos/Curis.app`

Build chain:

- frontend standalone production build: PASS
- fresh Workspace sidecar: PASS
- fresh Gateway sidecar: PASS
- fresh Guardian sidecar: PASS
- Cargo/Tauri release build: PASS
- fresh `Curis.app`: PASS

The first build attempt was stopped by a transient Google Fonts fetch error. A retry through the
same declared build path succeeded; no source workaround was added.

Native UI, using an explicit `/tmp` app-data root:

1. fresh app opened the Welcome screen;
2. an isolated company was created and Model Management opened;
3. UI explicitly stated that packaged credentials are held by macOS Keychain;
4. a dedicated fake credential was submitted;
5. real DeepSeek Health rejected it and UI remained unconnected;
6. app fully quit and sidecars exited;
7. the same fresh package reopened with the same isolated root;
8. credential metadata remained `active`, storage remained `macos_keychain`, and the API could
   read it from the recreated Vault (`restart_vault_test=ok`) without re-entry;
9. disconnect disabled metadata and deleted the Keychain item;
10. after another full quit/restart, credential test returned HTTP 422,
    `credential is not active`.

The deliberately invalid credential correctly did not create model discovery, default-model or
AI Ready success.

### Legal DeepSeek packaged acceptance (2026-08-30)

The CEO entered one legal, limited DeepSeek test credential directly in the packaged Model
Management secure field. The key was not sent to chat, read by the development agent, printed or
copied into evidence.

1. Native Keychain save returned only credential metadata and a `vault://` reference.
2. Real Provider recovery returned `health=healthy`, `available=true`, `saved=true`.
3. Dynamic discovery returned `deepseek-v4-flash`, `deepseek-v4-pro` and
   `deepseek-v4-flash-vision-exp`.
4. A minimal non-sensitive Workbench Guide call completed with source `tenant_private`, Provider
   `deepseek`, model `deepseek-v4-pro`, and persisted the same guide session as `READY`.
5. Curis fully quit; all packaged Desktop, Workspace, Gateway, Guardian and frontend processes
   exited.
6. The same package reopened with the same isolated app-data root. Without credential re-entry,
   Provider recovery again returned healthy and the same discovered model set.
7. A second minimal real call used the same Keychain-backed path but returned a redacted 503 after
   the existing retry boundary. Its guide session remained `COLLECTING`; no result or success was
   fabricated.
8. Delete removed the native Keychain item. Recovery immediately returned HTTP 422
   `credential is not active`.
9. After another full quit/restart, DeepSeek had no active credential, recovery remained 422, and
   CEO Desk displayed `尚未连接模型`.

Default-model selection was separately attempted with the discovered tenant-private capability.
The existing endpoint returned HTTP 422 because it only accepts an active official model key.
No preference row was forged and no source was changed for this security acceptance.

## 7. Secret leakage audit

The submitted packaged test value was searched after shutdown and after restart across the
isolated app-data tree, including SQLite and logs. Result: zero matching files.

For the legal CEO-entered DeepSeek credential, the agent never read the plaintext. A structural
scan across all eight isolated app-data files (SQLite and Runtime logs included) found zero
secret-like API-key or bearer-token values. API responses contained metadata/reference only;
frontend code retains no Key in browser persistence.

The API integration separately asserted that its generated secret was absent from API responses
and SQLite bytes. No real credential entered source, tests, Git, URLs, logs or evidence.

## 8. Tests

- credential / Provider focused backend: `18 passed, 1 skipped`
- General Workspace / RD / XHS / frontend projection / DB safety no-regression: `15 passed`
- frontend Node tests: `7 passed`
- focused ESLint: PASS
- Python compile: PASS
- Cargo check: PASS
- frontend production build: PASS
- fresh packaged build: PASS
- `git diff --check`: PASS

The opt-in native Keychain test passed separately. One broad harness run initially used the wrong
admin-token value and produced two platform-admin 401 failures; rerun with the test's declared
token passed. Existing `test_tenant_model_preference.py` assumptions target older seeded model
names and were not changed by this security Issue.

## 9. Active database safety

Both repository active databases are byte-for-byte unchanged from preflight and remain healthy:

| Path | Size | mtime | SHA-256 | integrity_check |
| --- | ---: | ---: | --- | --- |
| `data/curis.sqlite` | 1232896 | 1786873339 | `2ea2506f90f764e834d47d8f6bae3cb41c22d457757e0e9216c0ae8c39a39ec6` | ok |
| `backend/data/curis.sqlite` | 1277952 | 1786783659 | `a9d96a9536a5bce3b3b30f912e86a37f61d28527a8eb2d35af7a5857d29414e4` | ok |

All Runtime and packaged acceptance writes used repository-external isolated SQLite.

## 10. Changed files

- `backend/app/credential_vault.py`
- `backend/app/ai_capability_registry.py`
- `backend/tests/test_v1_p0_003_keychain.py`
- `frontend/lib/v1FrontendApi.js`
- `frontend/components/v1/ModelManagement.js`
- `frontend/components/v1/SharedConversation.js`
- `frontend/tests/v1FrontendBatch1.test.mjs`
- `desktop/src/lib.rs`
- `issues/V1-P0-003-MACOS-KEYCHAIN-CREDENTIAL-PERSISTENCE.md`
- this Review

No commit or push was created. Unrelated preserved worktree content was not staged or cleaned.

## 11. Remaining acceptance gates

1. **Tenant-private default model integration:** discovered DeepSeek capabilities are valid for
   Provider recovery and direct Runtime use, but `TenantModelPreferenceResolver` accepts only
   `source=official`. Fixing this requires a separately bounded model-preference/runtime integration
   decision; it is outside this Keychain Issue's Allowed Files and `backend/app/main.py` is
   explicitly excluded.
2. **Post-restart real call:** Keychain recovery and Provider Health passed, but the second minimal
   real call returned the product's redacted 503. This is a real external/runtime-call failure, not
   a credential persistence failure. A future acceptance retry may use a legal credential, but
   this Review does not spend further quota or alter retry/error handling.

## 12. Final P0 disposition

V1-P0-003: **IMPLEMENTED / PARTIAL**.

- Native durable credential persistence: implemented and packaged-verified.
- Fail-closed and deletion: implemented and packaged-verified.
- Real Health/discovery after restart: verified.
- One real cloud call before restart: verified.
- Default model and successful post-restart cloud call: not verified; no success was simulated.
- Native credential deletion and restart-unconnected truth: verified.

## 13. Cloud continuity cross-reference

The separately bounded `CURIS-V1-CLOUD-MODEL-CONTINUITY-001` closed both remaining integration
gates without changing Keychain. See
`docs/reviews/CURIS_V1_CLOUD_MODEL_CONTINUITY_IMPLEMENTATION_REVIEW.md`.

That Review verifies tenant-private DeepSeek default selection, a successful real call before and
after full packaged restart, Keychain-backed recovery without credential re-entry, legal deletion,
and restart-unconnected truth. Recommended aggregate V1-P0-003 status is therefore
**IMPLEMENTED / ACCEPTED CANDIDATE**.
