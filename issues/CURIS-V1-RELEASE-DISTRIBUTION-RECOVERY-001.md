# CURIS-V1-RELEASE-DISTRIBUTION-RECOVERY-001

Status: Implemented / Partial — Blocked at Signing / Notarization

Authority Class: CURRENT / IMPLEMENTATION ISSUE

Owner: Main Development Session

## Goal

Turn the accepted local packaged Curis app into the narrowest recoverable macOS release candidate:
offline-repeatable source build, one DMG distribution path, versioned SQLite backup/restore with
failure atomicity, exact package identity evidence, and—only when legal Apple credentials exist—
Developer ID signing and notarization.

## Current release truth

- Product: `Curis`, bundle id `com.curis.desktop`, version `0.1.0`.
- Current app is ad-hoc/linker signed, has no TeamIdentifier or sealed resources, and fails strict
  `codesign`/`spctl` verification.
- No `Developer ID Application` identity is available. The only listed identity is
  `ClaudeCN Signing`, which is not accepted as Apple distribution authority.
- No notarytool Keychain profile was found. `notarytool`, `stapler` and `hdiutil` are installed.
- Five local app copies share `com.curis.desktop`; none may be deleted by this Issue.
- Release build now uses local/system font fallbacks, reuses an explicit local PyInstaller cache,
  refuses implicit network bootstrap, and excludes backend tests/virtualenv files from the bundle.

## Allowed Files

- `frontend/app/layout.js` — remove release-time remote font download only
- `frontend/app/globals.css` — system/local font fallback wording only
- `desktop/scripts/build-runtime.sh` — offline/dependency-safe build seam and recovery binary bundle
- `desktop/runtime/recovery.py` — versioned backup/restore utility
- `desktop/tests/test_release_recovery.py` — isolated recovery regression
- `desktop/scripts/build-manual-dmg.sh` — bounded deterministic staging cleanup only if required
- `desktop/tauri.conf.json` — signing/notarization configuration only after legal identity exists
- this Issue
- `docs/reviews/CURIS_V1_RELEASE_DISTRIBUTION_RECOVERY_REVIEW.md`

Pre-change SHA-256:

- `frontend/app/layout.js`: `96ed21fd4ed234e9934970dfd41899011d7d76a9be298cd90f34ff92154a545c`
- `frontend/app/globals.css`: `399d08d6b02fe4544135ef95c6db25f0399789d78857538f5543023e1d3fb845`
- `desktop/scripts/build-runtime.sh`: `0de2f22e65024be2e953d4e38fbda3a304f4acd2e30bc70560399e6790262651`
- `desktop/scripts/build-manual-dmg.sh`: `69035998bc82b608382ad2fa318e06191f2f902d2263a5c4421509f25522e20d`
- `desktop/tauri.conf.json`: `ec2f3ea29d5b2f564a12699ab8196ad54a8cf3f9645d4a40dff2ebd964045da2`

`desktop/src/lib.rs` is mixed-source and explicitly excluded from modification.

## Durable data and recovery contract

- Current durable app data is the app-data SQLite at `data/curis.sqlite`.
- Logs and the instance lock are not durable user data.
- Referenced external files remain references; the release backup does not silently copy arbitrary
  filesystem content.
- Keychain secrets are excluded. Restore may recover credential references but never a secret; a
  missing Keychain item requires reauthorization.
- Backup uses SQLite online backup, records schema/version/hash metadata, and produces one versioned
  archive.
- Restore requires the app-data lock, verifies archive shape/hash/SQLite integrity, keeps a local
  pre-restore DB copy, and atomically replaces the DB. Invalid input leaves the original untouched.

## Distribution, signing and notarization

- One V1 artifact: DMG.
- Signing must use a legal `Developer ID Application` identity and the same identity for nested
  executables/sidecars and outer app.
- Notarization must use an existing legal notarytool profile; secrets are never accepted through chat
  or written to the repository.
- Until those credentials exist, verdict cannot exceed `BLOCKED AT SIGNING / NOTARIZATION`.

## Test matrix

1. Offline frontend production build performs no Google Fonts fetch.
2. Runtime build does not silently fetch Python build dependencies.
3. Backup from an isolated live SQLite is consistent and versioned.
4. Restore into a clean root recovers all SQLite state.
5. Restore over an existing root creates a pre-restore safety copy.
6. Corrupt archive/hash/SQLite fails before target mutation.
7. Restore while Curis holds the app-data lock fails closed.
8. Keychain material is absent from backup and logs.
9. Two isolated builds complete from declared/local dependencies.
10. DMG install launches without repository/node_modules/dev server dependencies.
11. Existing-install data and Keychain continuity survive a signed candidate upgrade when signing
    authority becomes available.
12. Repository active SQLite fingerprints remain byte-identical.

## Stop gates

- Developer ID signing: `WAITING FOR CEO APPLE DEVELOPER SIGNING AUTHORITY`.
- Notarization: `NOTARIZATION CREDENTIAL REQUIRED`.
- Any restore design that would copy Keychain secrets or arbitrary external files.
- Active database mutation, destructive migration, mixed-source ownership collision or Frozen
  Authority conflict.

## Explicit exclusions

No new Product feature, Provider, Runtime architecture, database system, updater service, UI
redesign, old-app deletion, active DB write, commit or push.

## Implementation result

- Local DMG candidate: `desktop/target/release/bundle/dmg/Curis_0.1.0_manual_aarch64.dmg`
  (`SHA-256 6c0b4d9ba9bebd0e4d66b4a0f274d9aed30648214cbe12ad7a637d65c2037f9c`).
- Fresh DMG copy launches with isolated app data and starts packaged Frontend, Gateway and Workspace
  Runtime without repository services.
- `curis.release-backup/v1` backup/restore, running-app lock, pre-restore safety copy and corrupt-input
  fail-closed behavior are implemented and packaged.
- Keychain secrets are excluded from file backup. Signed-build Keychain continuity remains untested.
- The app remains ad-hoc signed (`TeamIdentifier=not set`) and fails strict codesign/Gatekeeper;
  therefore it is not an external release candidate.
- Developer ID and notary credentials are the exact remaining external gates. No secret was requested,
  read, exported or stored by this Issue.
