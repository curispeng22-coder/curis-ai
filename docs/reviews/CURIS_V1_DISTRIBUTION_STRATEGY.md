# CURIS V1 Distribution Strategy

Status: Frozen

Authority Class: FROZEN / PRODUCT STRATEGY RECORD

Disposition: CEO ACCEPTED — TWO-STAGE MACOS DISTRIBUTION

Date: 2026-08-31

## Stage A — GitHub Beta Distribution (current)

The current release target is a GitHub Beta DMG. Apple Developer Program membership,
Developer ID Application signing, notarization and stapling are not prerequisites for
this gate. A beta user may install the DMG and use Apple's per-application “Open
Anyway” flow when Gatekeeper blocks first launch. Curis must never ask users to disable
Gatekeeper or weaken global macOS security.

The Beta closure gate covers a versioned DMG, SHA-256, install and Open Anyway
instructions, known limitations, backup/restore guidance, upgrade guidance and known
issues. The beta package is ad-hoc signed and not notarized; rebuilding or upgrading
to another ad-hoc package may change macOS code identity and trigger Keychain
authorization again. The final package's close → restart continuity remains verified.

Only one installed Curis should be used, preferably `/Applications/Curis.app`.
Users should close the old Curis before upgrading and should not run copies from
Downloads, worktrees or old test bundles with the same Bundle ID.

## Stage B — Trusted macOS Distribution (deferred)

Developer ID Application, stable signing identity, notarization, stapling and trusted
Gatekeeper distribution are deferred by CEO. They are not a current Product or GitHub
Beta blocker. When this stage is opened, it must also re-test signed upgrade and
Keychain continuity across two signed candidates.

## Current release truth

- GitHub Beta Distribution: `IN PROGRESS / NOT BLOCKED BY APPLE MEMBERSHIP`.
- Trusted macOS Distribution: `DEFERRED — REQUIRES DEVELOPER ID / NOTARIZATION`.
- Next gate: `CURIS V1 GITHUB BETA DISTRIBUTION CLOSURE`.
- Whole-App Live AI, Cloud AI continuity and Keychain remain accepted within their
  recorded scope; this strategy does not reopen product acceptance.
