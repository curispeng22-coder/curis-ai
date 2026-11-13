# CURIS V1 Frontend Batch 1 — Implementation Review

**Status:** Review  
**Authority Class:** REVIEW / IMPLEMENTATION EVIDENCE  
**Date:** 2026-08-29  
**Issue:** `CURIS-V1-FRONTEND-BATCH-1`  
**Verdict:** IMPLEMENTED / CEO REVIEW REQUIRED

## 1. Delivered vertical slice

Fresh Curis now supports this real sequence:

`Welcome → optional Skip → Empty Curis → minimal CEO/Company setup → real Company + Runtime CEO Assistant → attention-first CEO Desk → provider directory → first-business proposal → canonical Business + first General Workspace → restart reread`.

Skip persists only presentation state and creates no Company. Company setup creates no Business. The first Business is materialized only after proposal confirmation and reuses the canonical Business Spine atomic transaction.

## 2. Runtime truth

- Company, Runtime CEO Assistant, FoundingRun, Business and Workspace are persisted Runtime objects.
- CEO Desk attention is a deterministic read projection over existing Decision, Handoff, Result, Evidence, Responsibility and Work truth; an empty projection renders a quiet state.
- The provider directory and model preference use the existing APIs. All unverified entries remain `未连接`.
- No model credential was entered during acceptance. No AI response, provider Health, Result, Decision, Handoff or Current Executor was fabricated.
- M3 native Keychain remains `SECURITY BLOCKED`; current-process credential entry is explicitly not restart-safe and never writes the key to SQLite.

## 3. Browser evidence

Repository-external DB: `/tmp/curis-v1-batch1-browser.iOTZUt/curis.sqlite`.

- Welcome, 1440 Light: `/tmp/curis-v1-batch1-evidence/01-welcome-1440-light.png`
- Empty Curis, 1024 Light: `/tmp/curis-v1-batch1-evidence/02-empty-curis-1024-light.png`
- CEO Desk empty, 1024 Light: `/tmp/curis-v1-batch1-evidence/03-ceo-desk-empty-1024-light.png`
- CEO Desk empty, 1440 Dark: `/tmp/curis-v1-batch1-evidence/04-ceo-desk-empty-1440-dark.png`
- Provider directory, 1440 Dark: `/tmp/curis-v1-batch1-evidence/05-model-directory-1440-dark.png`
- First canonical Workspace: `/tmp/curis-v1-batch1-evidence/06-first-workspace-1440-dark.png`
- CEO Desk after Business: `/tmp/curis-v1-batch1-evidence/07-ceo-desk-with-business-1440-dark.png`

The Browser console contained no warning or error. Backend restart preserved the proposal and the created Workspace.

## 4. Fresh Packaged Desktop evidence

Built from current source:

`/Users/yy/Documents/Curis AI Workspace/desktop/target/release/bundle/macos/Curis.app`

Build regenerated the standalone frontend, Workspace/Gateway/Guardian sidecars and Tauri app. Because `fonts.googleapis.com` was unreachable, the build used official `@fontsource/inter@5.3.0` files through Next's documented test-response environment hook; no font or product source was changed.

Isolated app-data:

`/tmp/curis-v1-batch1-desktop-home/Library/Application Support/com.curis.desktop`

The packaged app completed Welcome, Skip, Company/Assistant creation, real provider-directory read, proposal confirmation and canonical first Workspace creation. After full app close/reopen, CEO Desk reread one Workspace from the same SQLite.

- First Workspace: `/tmp/curis-v1-batch1-evidence/08-packaged-first-workspace.png`
- Restart reread: `/tmp/curis-v1-batch1-evidence/09-packaged-restart.png`

Packaged logs contained zero `error`, `exception`, traceback or HTTP 5xx matches. Isolated DB `integrity_check=ok`; counts were Company `1`, Runtime entities `3`, canonical Business `1`, Workspace `1`.

## 5. Tests and build

- Backend focused + RD/XHS no-regression: `19 passed`.
- Frontend source tests: `12 passed`.
- Scoped ESLint: PASS.
- Python compile: PASS.
- `git diff --check`: PASS for Issue-owned paths.
- Next production build: PASS, `46` routes.
- Fresh PyInstaller sidecars + Cargo/Tauri `Curis.app`: PASS.

## 6. Active DB safety

Both repository active databases were read-only and unchanged from preflight:

| Path | Size | mtime | SHA-256 | integrity |
| --- | ---: | ---: | --- | --- |
| `data/curis.sqlite` | 1232896 | 1786873339 | `2ea2506f90f764e834d47d8f6bae3cb41c22d457757e0e9216c0ae8c39a39ec6` | ok |
| `backend/data/curis.sqlite` | 1277952 | 1786783659 | `a9d96a9536a5bce3b3b30f912e86a37f61d28527a8eb2d35af7a5857d29414e4` | ok |

## 7. Remaining boundaries

- Durable native Keychain and packaged credential recovery are not implemented.
- No real cloud model was connected and no AI execution was accepted in this Batch.
- The first General Workspace entry exists; the complete General operating office remains P1.
- Professional Workspace auto-match/materialization is not implemented.
- The pre-existing floating `GlobalAssistant` still reads its legacy identity projection and can show an unnamed identity; Batch 1's main CEO Desk conversation reads the Runtime CEO Assistant and does not create a second identity.
- Signing/notarization is a later distribution gate.

No commit or push was performed.
