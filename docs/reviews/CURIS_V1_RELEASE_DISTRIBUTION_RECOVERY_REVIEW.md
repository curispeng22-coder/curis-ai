# CURIS V1 Release Distribution & Recovery Review

Status: Review

Authority Class: REVIEW / EVIDENCE

Issue: `CURIS-V1-RELEASE-DISTRIBUTION-RECOVERY-001`

Verdict: **GITHUB BETA DISTRIBUTION: IN PROGRESS / NOT BLOCKED BY APPLE MEMBERSHIP**

## 0. 2026-08-31 Distribution Strategy Registration

CEO has split macOS distribution into two stages. This Review remains the evidence
record for the local DMG, ad-hoc identity, Gatekeeper limitation and recovery checks;
its former single “blocked at signing/notarization” conclusion is now the deferred
Stage B conclusion, not a blocker for Stage A GitHub Beta.

- **Stage A — GitHub Beta Distribution:** current target; DMG, version, SHA-256,
  install/Open Anyway guidance, known limitations and backup/restore/upgrade
  documentation must close the beta gate.
- **Stage B — Trusted macOS Distribution:** deferred by CEO; Developer ID Application,
  stable signing identity, notarization and stapling are required only when this stage
  is opened.
- The beta package is ad-hoc signed and not notarized. Gatekeeper rejection on first
  open is an expected beta limitation; users must use Apple's per-application “Open
  Anyway” flow and must not disable global security.
- Rebuilding or upgrading to another ad-hoc package may change macOS code identity and
  trigger Keychain authorization again. The exact final package close → restart
  continuity remains verified.
- Next gate: **CURIS V1 GITHUB BETA DISTRIBUTION CLOSURE**.

## 1. Release identity

- App: `Curis`
- Bundle id: `com.curis.desktop`
- Version: `0.1.0`
- Executable: `curis-desktop`
- Source HEAD: `c797db840bad285d7e9f1962d06eac61aa28508b`
- Local candidate DMG: `/Users/yy/Documents/Curis AI Workspace/desktop/target/release/bundle/dmg/Curis_0.1.0_manual_aarch64.dmg`
- DMG SHA-256: `6c0b4d9ba9bebd0e4d66b4a0f274d9aed30648214cbe12ad7a637d65c2037f9c`
- DMG size: `221034025` bytes
- This artifact is a local development candidate, not the final V1 RC.

## 2. Duplicate app audit

No copy was deleted. Five known local bundles share the same bundle id/version:

| Path | Signature | Team |
|---|---|---|
| `/Users/yy/.codex/worktrees/aeb0/Curis AI Workspace/desktop/target/release/bundle/macos/Curis.app` | ad-hoc | not set |
| `/Users/yy/.codex/worktrees/d126/Curis AI Workspace/desktop/target/release/bundle/macos/Curis.app` | ad-hoc | not set |
| `/Users/yy/.codex/worktrees/ttk-shared-runtime-20260813/Curis AI Workspace/desktop/target/release/bundle/macos/Curis.app` | ad-hoc | not set |
| `/Users/yy/Documents/Curis AI Workspace/desktop/target/release/bundle/macos/Curis.app` | ad-hoc | not set |
| `/Users/yy/Documents/Curis AI Workspace/desktop/target/release/bundle/macos/CurisCopy.app` | local `ClaudeCN Signing` | not set |

Acceptance evidence in this Review refers only to the absolute DMG path above.

## 3. Developer ID and signing

- `security find-identity -v -p codesigning` exposes only `ClaudeCN Signing`.
- No `Developer ID Application` identity or Apple TeamIdentifier is available.
- Current app is ad-hoc signed: `Signature=adhoc`, `TeamIdentifier=not set`, `Info.plist=not bound`,
  `Sealed Resources=none`.
- `codesign --verify --deep --strict` fails because the bundle has no valid sealed-resource signature.
- Nested sidecars therefore also have no legal external distribution identity.

Gate (Stage B — deferred): `WAITING FOR CEO APPLE DEVELOPER SIGNING AUTHORITY`.

## 4. Notarization

- `notarytool 1.1.2`, `stapler` and `hdiutil` are available.
- No configured notarytool Keychain profile was found.
- No submission was attempted and no submission id exists.
- Stapling and Gatekeeper acceptance cannot be performed before legal signing/notary authority exists.

Gate (Stage B — deferred): `NOTARIZATION CREDENTIAL REQUIRED`.

## 5. Distribution and fresh local install

- One V1 format was retained: DMG.
- Final image passes `hdiutil verify`.
- A copy mounted from the final DMG was launched from
  `/tmp/curis-final-install.tTamLC/Curis.app` with isolated app data.
- Packaged Frontend `/ceo-office`, Gateway `/health`, and Workspace Foundation API all returned `200`.
- The isolated SQLite returned `integrity_check=ok`.
- The packaged backend no longer contains `backend/tests` or `backend/.venv`.
- Launch did not use repository dev servers, `node_modules`, or Python from the repository.
- Trusted external Gatekeeper acceptance is **not passed**: `spctl` rejects the ad-hoc
  app. This is a Stage B limitation; Stage A uses Apple's per-application Open Anyway
  flow and does not claim trusted distribution.

## 6. Build reliability

- Removed the release-time Google Fonts fetch; Inter is used only when locally available, otherwise
  platform system fonts are used.
- Runtime build reuses explicit local build tools and refuses an implicit network install unless
  `CURIS_ALLOW_BUILD_NETWORK=1` is deliberately set for bootstrap.
- Runtime skip mode now requires the packaged recovery binary as well as all sidecars.
- Multiple consecutive Runtime builds and final Tauri/DMG builds completed from local dependencies.
- The first security scan exposed an entire-backend data copy; the root build input was removed and
  the final bundle contains zero backend test and virtualenv files.

## 7. Backup, restore and failure recovery

- Added the packaged stdlib-only `curis-recovery` tool.
- Format: `curis.release-backup/v1`.
- Archive entries are exactly `manifest.json` and `data/curis.sqlite`.
- Manifest records UTC creation time, schema version, database hash and
  `credentials=EXCLUDED_MACOS_KEYCHAIN`.
- Backup uses SQLite online backup and verifies integrity.
- Restore requires the app lock, validates archive shape/hash/schema/integrity, creates a uniquely
  named pre-restore copy, then atomically replaces the DB.
- Isolated source and restored databases had the same SQL dump hash
  `b09f8512d5a099283d9261254151a476e14ca5e374002ee964d8fe33c70a1b01`,
  `103` tables, `269` rows and `integrity_check=ok`.
- The restored app-data directory relaunched successfully with Frontend/Gateway `200`.
- A corrupt archive returned `restore failed: backup archive has unexpected entries`; exit was
  non-zero and the target DB hash stayed unchanged.
- Restore while Curis owns the app lock is rejected.

Keychain secrets are intentionally outside file backup. A missing Keychain item after machine/user
transfer requires reauthorization; backup does not claim to migrate credentials.

## 8. Upgrade and Keychain continuity

- Same-bundle local reinstall and restored-state launch are proven.
- A previous **signed** V1 candidate does not exist, so signed old-to-new upgrade is not proven.
- Stable designated-requirement Keychain continuity across signed builds is not proven.
- The earlier accepted ad-hoc cloud continuity remains historical evidence; it is not promoted into
  signed-release evidence here.

## 9. Secret safety

- Issue diff, isolated SQLite, backup archive and isolated logs: zero credential-pattern hits.
- Final mounted artifact contains no Curis backend tests or virtualenv files.
- Remaining scanner matches are confined to vendored Next/Node binaries; inspection found a Node
  binary `AKIA...` test/embedded literal, not a user credential. No private key, API key or notary
  credential was read, printed, exported or written by this Issue.

## 10. Tests

- `python3 -m unittest desktop.tests.test_release_recovery -v`: 3 passed.
- `python3 -m py_compile desktop/runtime/recovery.py`: passed.
- `bash -n desktop/scripts/build-runtime.sh desktop/scripts/build-manual-dmg.sh`: passed.
- `pnpm exec eslint app/layout.js`: passed.
- Frontend production build: passed offline with no Google Fonts fetch.
- Repeated Runtime builds: passed.
- Fresh Tauri app build and DMG build: passed.
- `hdiutil verify`: passed.
- `git diff --check`: passed.

## 11. Active database safety

Both active SQLite files are byte-identical to preflight and return `integrity_check=ok`:

| Path | Size | mtime | SHA-256 |
|---|---:|---:|---|
| `data/curis.sqlite` | 1232896 | 1786873339 | `2ea2506f90f764e834d47d8f6bae3cb41c22d457757e0e9216c0ae8c39a39ec6` |
| `backend/data/curis.sqlite` | 1277952 | 1786783659 | `a9d96a9536a5bce3b3b30f912e86a37f61d28527a8eb2d35af7a5857d29414e4` |

## 12. Remaining Stage A / Stage B work

### Stage A — GitHub Beta closure

1. Publish a versioned DMG with SHA-256 and the install/Open Anyway instructions.
2. Document the ad-hoc code-identity/Keychain limitation, one-install-location rule,
   backup/restore guidance, upgrade limitation and known issues.
3. Complete fresh-install, Whole-App smoke, backup/restore and beta upgrade checks.

### Stage B — Deferred trusted distribution

The following are intentionally deferred until CEO opens Trusted macOS Distribution:

1. Install a legal Developer ID Application identity without exporting its private key.
2. Configure a legal notarytool credential in Keychain without sending it through chat.
3. Sign nested binaries and outer app with one stable identity; strict codesign must pass.
4. Submit, accept and staple notarization; Gatekeeper must pass on a quarantined fresh install.
5. Re-run signed upgrade and Keychain continuity with two signed candidates.
6. Run final whole-app RC regression on the signed/notarized artifact.

P1 remains outside this Release P0: product wording/attention polish already recorded by whole-app
acceptance.

## 13. Final decision

Recovery and local packaging are implemented. The produced DMG is reproducible enough for local
development acceptance and is recoverable, but it is not legally signed, notarized or Gatekeeper
accepted. Therefore no artifact is designated `Curis V1 RC`.

**GITHUB BETA DISTRIBUTION: IN PROGRESS / NOT BLOCKED BY APPLE MEMBERSHIP**

**TRUSTED MACOS DISTRIBUTION: DEFERRED — REQUIRES DEVELOPER ID / NOTARIZATION**
