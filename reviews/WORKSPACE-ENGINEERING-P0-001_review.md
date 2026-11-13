# WORKSPACE-ENGINEERING-P0-001 Review

**Status:** Review
**Record Type:** Formal Acceptance Record
**Date:** 2026-08-16
**Issue:** `issues/WORKSPACE-ENGINEERING-P0-001.md`
**Decision:** `IMPLEMENTED / ACCEPTED`

## Acceptance decision

`com.curis.sample.customer-feedback-office@0.1.0` was absent when the packaged Curis Desktop was built, was created only after the build, and was then installed and operated without modifying source, rebuilding or reinstalling the App.

The real packaged Desktop proved dynamic navigation, declarative Main / Context / Utility rendering, UI creation of a persisted `CustomerFeedback`, full Desktop restart recovery, fail-closed action handling, uninstall navigation removal and read-only business-data/provenance retention.

**WORKSPACE ENGINEERING P0 ACCEPTED**

## Gate result

| Gate | Result | Evidence |
| --- | --- | --- |
| Build before Package | PASS | App executable mtime/hash precede Package file mtime; build/source/bundle scans had zero sample terms |
| Install / provenance | PASS | packaged Runtime installed exact package/version/digest from the post-build external directory |
| Failure truth | PASS | invalid path and unknown action failed closed without Registry/object residue |
| Dynamic navigation | PASS | Registry-driven navigation appeared after install and disappeared after uninstall |
| Declarative surfaces | PASS | one generic host rendered declared Main, Context and Utility components |
| Business persistence | PASS | one scoped `CustomerFeedback` plus Core activity persisted to isolated SQLite |
| Desktop restart | PASS | complete stop/start of the same App binary recovered Registry, Workspace, object and activity |
| Uninstall / retention | PASS | active files removed; Package uninstalled; instance/Workspace archived; object/activity/provenance retained read-only |
| Desktop evidence | PASS | seven screenshots plus packaged gateway/API/SQLite evidence chain |
| No regression | PASS | backend `25 passed`; frontend `11 passed`; pre-Package production/Desktop build passed |
| Active SQLite guard | PASS WITH RECORDED INCIDENT | bounded logical repair verified; current hash stable during acceptance; original byte hash not restored |

## Actual architecture

- strict JSON Package validator and local immutable Package Store;
- tenant/company/workspace-scoped installed Package Registry in existing SQLite;
- materialization into existing Workspace identity;
- one generic Package domain-object/activity projection;
- finite P0 Core action allowlist containing only `core.domain-object.create`;
- Registry-driven existing sidebar navigation;
- one generic installed Workspace route reusing `WorkspacePaneShell`.

No second Employee, Responsibility, Capability, Decision, Evidence or Computer Access system was introduced. Permission requirements remain declarations and are not grants.

## Shared Core impact

Only two bounded integration seams changed:

- existing FastAPI app registers the Package router;
- existing Terra sidebar projects active Package Registry items under Workspace navigation.

XHS, RD and TTK business logic/routes/data were not migrated, refactored or converted. Their accepted focused slices passed no-regression checks.

The bounded commit contains only this Issue's files and the two integration hunks. It intentionally does not absorb the Preserved Development Baseline. Consequently it is an ordered integration commit, not a standalone cherry-pick onto clean historical HEAD: the reused `workspaces` schema is supplied by that preserved Shared Runtime baseline and must be integrated first. The accepted Desktop was built and tested against the recorded full baseline.

## Evidence root

`docs/reviews/workspace-engineering-p0-2026-08-16/README.md`

## Remaining boundary

Package update/migration/rollback, signing/Marketplace trust, arbitrary extensions, Workspace migrations and Workspace Engineering product/UX remain unimplemented and require new bounded Issues.
