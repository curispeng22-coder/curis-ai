# Workspace Engineering P0 Desktop Evidence

**Status:** Review
**Issue:** `WORKSPACE-ENGINEERING-P0-001`
**Decision:** `WORKSPACE ENGINEERING P0 ACCEPTED`
**Date:** 2026-08-16

## Build before Package

The packaged Desktop was built before the sample Package existed.

- App: `desktop/target/release/bundle/macos/Curis.app`
- App executable mtime: `2026-08-16T17:17:53+0800` (`1786871873`)
- App executable SHA-256: `1e73656fd32f3978b8a3b4b929d1ce1d25ffb694bb2a6a6ae766359328d74abf`
- packaged Workspace sidecar SHA-256: `5820d50199e39677ad925abe1fafe756fb1513a217aca654febaa82e86e4e6db`
- sample Package first file mtime: `2026-08-16T17:18:50+0800` (`1786871930`)
- post-build sample tree SHA-256: `d3a939412ca532c907990689ca48f2cf68ac353f11d7d20bed830d9a378dece3`
- Package manifest SHA-256: `a60860be270dd615ba895f24c1a0f20407204e80c0ce60d8263945eba40e283b`
- packaged App scan for the package ID, `CustomerFeedback` and `客户反馈办公室`: `0` matches
- packaged source-root scan for the same terms before Package creation: `0` matches

The Package was introduced only under `/tmp/curis-workspace-p0-acceptance-20260816/customer-feedback-office` after the App build. No source edit, rebuild or App reinstall occurred after its creation.

## Isolated Desktop Runtime

- HOME: `/tmp/curis-workspace-p0-desktop-home`
- SQLite: `/tmp/curis-workspace-p0-desktop-home/Library/Application Support/com.curis.desktop/data/curis.sqlite`
- Package Store: `/tmp/curis-workspace-p0-desktop-home/Library/Application Support/com.curis.desktop/data/workspace-packages`
- Company: `company-p0-desktop`
- Package: `com.curis.sample.customer-feedback-office@0.1.0`
- validated Runtime digest: `022b501bc2702be8eb17edce78e6bb07f8cba857d34277d11e3563b2e670cdc3`
- instance: `workspace-package-instance-93ad8850-24e8-4fe7-ae21-1a052ab7718c`
- Workspace: `workspace-package-f6eaf8a3-b268-40e5-958f-4abb2e023894`

An invalid source path first failed with HTTP `422` and left the Registry empty. The valid post-build Package then installed through the packaged Runtime API. Registry and navigation returned the package/version/digest and the dynamic route without any Package-specific compiled route or component.

## Desktop surfaces and business truth

Desktop Computer Use verified:

- dynamic second-level navigation: [desktop-dynamic-navigation.jpg](desktop-dynamic-navigation.jpg)
- declarative Main Surface: [desktop-main-surface.jpg](desktop-main-surface.jpg)
- declarative Utility Surface: [desktop-utility-surface.jpg](desktop-utility-surface.jpg)
- Main after UI-created object: [desktop-customer-feedback-created.jpg](desktop-customer-feedback-created.jpg)
- Context + Main + Utility together: [desktop-context-main-utility.jpg](desktop-context-main-utility.jpg)

The UI created one real object and one Core activity:

- object: `package-object-f2d820be-fdd5-4dc2-a5ec-15a45f607d77`
- object type: `CustomerFeedback`
- title: `导出结果难以定位`
- status: `NEW`
- channel: `INTERVIEW`
- responsibility: `employee:existing-owner`
- evidence reference: `evidence:interview-001`
- action: `core.domain-object.create`
- activity: `package-activity-a896e94c-528e-452d-947f-45492716cd9c`

An unknown action failed closed with HTTP `422` / `Core action is not allowed`; object and activity counts remained `1 / 1`.

## Restart and uninstall

The entire Desktop process and packaged gateway stopped. SQLite hash remained unchanged across shutdown. The exact same App executable was relaunched with the same isolated DB; its executable SHA-256 remained `1e73656f...`. Registry, navigation, object and activity recovered from SQLite, and Desktop displayed the same object: [desktop-restart-recovery.jpg](desktop-restart-recovery.jpg).

Uninstall then produced these facts:

- navigation API returned `[]` and Desktop second-level navigation disappeared;
- active Package Store directory was removed;
- direct active Workspace read returned HTTP `404`;
- Package status became `UNINSTALLED` and instance/Workspace status became `ARCHIVED`;
- archived manifest, schema, digest, provenance, the one business object and the one activity remained in SQLite read-only;
- Desktop showed the archived Workspace in the existing Workspace Portal without restoring dynamic navigation: [desktop-uninstall-navigation-removed.jpg](desktop-uninstall-navigation-removed.jpg).

Final isolated Desktop SQLite: `integrity_check = ok`, foreign-key violations `0`, objects `1`, activities `1`.

## Regression and active DB guard

- backend focused/shared regression: `25 passed` using an isolated DB with all of `CURIS_DB`, `CURIS_DB_PATH`, `CURIS_WORKSPACE_DB` set to the same `/tmp` path;
- frontend Package/RD/shared Workspace regression: `11 passed`;
- production frontend and packaged Desktop build: passed as part of the pre-Package build;
- XHS accepted Calendar/Note slice, RD real execution slice, Runtime Foundation persistence/isolation/Workspace and ADR-0046 Computer Access P0 truth checks passed;
- active `data/curis.sqlite` final SHA-256 stayed `c838f41deaf643b6a0ef55aa63b7467dbaaf9bb6d3a0e5a425e3d459f7ca53f0`, integrity remained `ok`, and the four Package tables remained absent.

The earlier guard violation is separately recorded in [ACTIVE_SQLITE_GUARD_REPAIR.md](ACTIVE_SQLITE_GUARD_REPAIR.md). Its original byte hash was not restored and is not claimed as restored; only bounded logical equivalence of all non-target schema/data was proven.

## Boundary

This accepts only the first controlled local declarative Package substrate. It does not accept arbitrary extensions, Package update/migration/rollback, Marketplace/signing infrastructure, XHS/RD/TTK migration, Full Computer Access or Workspace Engineering product/UX.
