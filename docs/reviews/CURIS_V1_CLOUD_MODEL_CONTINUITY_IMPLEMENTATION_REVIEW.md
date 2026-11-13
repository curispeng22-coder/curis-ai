# Curis V1 — Cloud Model Continuity Implementation Review

Status: Review

Authority Class: EVIDENCE

Verdict: **IMPLEMENTED / ACCEPTED CANDIDATE**

Issue: `issues/CURIS-V1-CLOUD-MODEL-CONTINUITY-001.md`

## 1. Scope and root causes

This bounded change closes model discovery → eligibility → preference → execution → restart →
recovery → re-execution. It does not modify native Keychain persistence.

The HTTP 422 came from `TenantModelPreferenceResolver`: it treated active official models as the
only legal preference candidates, even when the current tenant had a real Provider-discovered and
verified model capability.

The post-restart HTTP 503 came from a transport/runtime wait mismatch. The packaged Gateway stopped
waiting after 60 seconds while Workbench still owned a bounded second Provider attempt. Recorded
evidence showed the first attempt as `network_error` and the second as successful after the Gateway
had already returned 503. It was not a Keychain recovery failure.

## 2. Eligibility and preference correction

The existing preference contract now accepts either:

- an active official model; or
- an active current-tenant discovered model whose capability id is deterministic for its Provider
  discovery record, whose `discovery_verification` is verified, whose Provider/model metadata is
  coherent, and whose required credential metadata is active and Provider-matched.

Wrong tenant, wrong Provider, unknown, fabricated, stale, unavailable, disabled and missing-
credential candidates fail closed. Curated/local behavior remains governed by existing source and
Health rules. No DeepSeek-specific eligibility branch or new model taxonomy was introduced.

Preference remains user intent only. It does not manufacture Provider Health, capability readiness
or AI Ready. Restart restores preference metadata, then requires credential recovery, Health and
model rediscovery before presenting the model as usable.

Resolution order remains explicit conversation selection → employee/role binding when applicable
→ tenant default → No Model.

## 3. Runtime correction

Workbench resolves the eligible tenant-private preference before the official fallback and records
safe Provider/model/stage diagnostics without credential or prompt content. The packaged Gateway
default upstream wait is now 135 seconds (environment-overridable), covering the existing bounded
two-attempt Runtime window without adding a queue, router or retry system.

The model-management refresh also keeps the just-discovered selection stable by depending on the
selected Provider id and endpoint values rather than the replaced Provider object identity. This
prevents a successful discovery refresh from clearing the choice before default selection.

## 4. Real packaged DeepSeek acceptance

All writes used the repository-external root
`/tmp/curis-cloud-continuity-acceptance-20260830-01` and its isolated SQLite.

1. CEO entered the DeepSeek credential in the packaged Curis UI; the assistant never read, copied
   or typed the plaintext.
2. Native Keychain save, real Health and dynamic discovery passed. The returned models were
   `deepseek-v4-flash`, `deepseek-v4-pro` and `deepseek-v4-flash-vision-exp`.
3. `deepseek-v4-pro` became the tenant default with source `tenant_private`; the former 422 did not
   recur.
4. First minimal real call passed using DeepSeek / `deepseek-v4-pro`; guide session
   `gs-7defc290-3a43-4ceb-99ad-0082b1d0c7f5` returned HTTP 200.
5. The packaged app and its Desktop/Workspace/Gateway/Guardian/frontend processes fully exited.
6. The same freshly built package reopened with the same isolated root. Without re-entering the
   credential, Keychain recovery, Health, discovery and the same default model passed.
7. Second minimal real call passed using DeepSeek / `deepseek-v4-pro`; guide session
   `gs-4e499ab4-ea38-4248-ab91-0362ec7b1676` returned HTTP 200. The former false 503 did not recur.
8. The credential was deleted through the legal credential API. Recovery immediately returned
   HTTP 422 `credential is not active`, and the validated preference became `None`.
9. After a second full close/restart, the exact packaged app displayed `尚未连接模型` and
   `添加 AI 模型`. Backend recovery remained 422 and no default preference manufactured Ready.

Desktop evidence:
`/tmp/curis-cloud-continuity-acceptance-20260830-01/post-delete-restart-not-connected.png`.

An older Curis app from another worktree was also running under the same display name. Targeting
that window initially produced an ambiguous stale-looking observation. Process-path audit and
path-specific Computer Use identified the current package; the current package, its API and its
isolated database all agree on not connected after deletion.

## 5. Secret and database safety

A structural scan of all eight files under the isolated app-data root (SQLite and Runtime logs
included) found:

- DeepSeek/API-key-shaped values: 0
- bearer-token-shaped values: 0
- secret-assignment-shaped values: 0

Frontend persistence stores only Provider/model/capability metadata; it does not persist the API
Key. No plaintext secret entered source, Git diff, URL, Review or test artifacts.

Both repository active databases are byte-identical to preflight and healthy:

| Path | Size | mtime | SHA-256 | integrity_check |
| --- | ---: | ---: | --- | --- |
| `data/curis.sqlite` | 1232896 | 1786873339 | `2ea2506f90f764e834d47d8f6bae3cb41c22d457757e0e9216c0ae8c39a39ec6` | ok |
| `backend/data/curis.sqlite` | 1277952 | 1786783659 | `a9d96a9536a5bce3b3b30f912e86a37f61d28527a8eb2d35af7a5857d29414e4` | ok |

## 6. Tests and build

- backend continuity/Keychain/Provider/App Entry/General Workspace/RD/usage/DB-safety:
  `54 passed, 1 skipped`
- frontend Node regression: `5 passed`
- focused ESLint: PASS
- Python compile: PASS
- `git diff --check`: PASS
- current-source frontend/sidecar/Cargo/Tauri fresh packaged build used by the real acceptance:
  PASS

A redundant final `next build` retry after acceptance was blocked before compilation by the host's
connection reset while fetching Inter from `fonts.gstatic.com`. It did not change source or the
already fresh package used above; it is recorded as an external build-environment observation, not
as a Cloud continuity failure.

## 7. Changed files

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
- the bounded Issue and Reviews

No commit or push was created. Unrelated preserved worktree content was not staged or cleaned.

## 8. Final disposition

**CLOUD MODEL CONTINUITY: IMPLEMENTED / ACCEPTED CANDIDATE**

The full required chain passed: discovery, set default, first real call, full close, restart,
Keychain recover, same default, second real call, disconnect, and restart not connected.

Recommended V1-P0-003 status: **IMPLEMENTED / ACCEPTED CANDIDATE**. Its native Keychain safety
evidence remains owned by the original Review; this Review supplies the previously missing model-
selection and post-restart execution evidence.
