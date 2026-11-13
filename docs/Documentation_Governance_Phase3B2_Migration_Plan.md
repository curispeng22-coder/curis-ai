# Curis Documentation Governance Phase 3-B2 Migration Plan

Status: Review

Baseline:
main @ 75a9ce13e2653c8d94f8c9f8243c223d891577d7

Updated:
2026-07-30

---

## 1. Purpose

This plan converts the Phase 3-B2 asset analysis into explicit future movement
gates. It does not authorize or execute a move, deletion, code change or
configuration change.

The authoritative row-level inventory is
`docs/Documentation_Governance_Phase3B2_Asset_Report.md`.

## 2. Gate Definitions

### Safe Move

Requirements:

- Classification is `Archive`.
- No Markdown, script/config, AGENTS or internal asset reference was detected.
- The asset is not evidence, an Issue/Review record, a decision record,
  WorkBuddy Memory or protected runtime state.

Result: eligible for a future archive batch after explicit confirmation.

### Human Confirmation Required

Applied when:

- an Archive asset has a Markdown or internal-package reference;
- the asset is WorkBuddy Memory;
- the row is a Delete Candidate;
- the location is ignored/generated and has not been reviewed per child file;
- a coherent package move is safer than moving individual children.

Result: keep in place until the named owner confirms the treatment and the
reference update list.

### Forbidden Move

Applied when:

- the asset is Release Evidence, Issue evidence, Review evidence or decision
  provenance;
- a script/config or AGENTS consumer exists;
- the path is current runtime data, an active worktree, local environment state
  or sensitive generated gateway state.

Result: no movement or deletion under Documentation Governance.

## 3. Direct Archive Eligibility

Exactly 200 tracked assets are classified `Archive` and marked `安全移动` in
the Asset Report:

| Cohort | Count | Proposed Destination |
| --- | ---: | --- |
| Deprecated UI V2 | 172 | `docs/99_Archive/design/curis-ui-v2/` |
| CEO Office historical design | 17 | `docs/99_Archive/design/ceo-office/` |
| Historical diagram/prototype | 7 | `docs/99_Archive/prototypes/diagrams/` |
| Historical Handoff/governance | 4 | `docs/99_Archive/handoff/` |
| Total | 200 | Preserve original relative structure |

The exact file list is the complete Archive table in the Asset Report filtered
by `Gate = 安全移动`. No other file is directly eligible.

Recommended future batch order:

1. four unreferenced Handoff/governance files;
2. seven unreferenced standalone diagram prototypes;
3. the 16-file CEO Office `_archive/` cohort;
4. remaining unreferenced CEO Office assets;
5. UI V2 assets only after deciding whether to move the package as a whole.

Every future batch must run an exact `rg -n --fixed-strings` search for every
approved source path or directory, followed by `git diff --check`, and must
update Markdown, script/config and internal relative references before commit.

## 4. Human Confirmation Required

### 4.1 Tracked Assets — 184

| Cohort | Count | Reason |
| --- | ---: | --- |
| Deprecated UI V2 | 88 | Internal or Markdown reference, including 6 duplicate Delete Candidates |
| CEO Office historical design | 57 | Internal or Markdown reference |
| WorkBuddy Memory | 16 | Possible external tool-state consumer |
| Diagram prototypes | 9 | Markdown or internal reference |
| Demo | 6 | Release/demo provenance references |
| Handoff | 4 | Historical governance references |
| Static prototypes | 2 | Markdown references |
| CEO Evidence generated/source | 2 | Generated Delete Candidates |
| Total | 184 | Keep in place pending confirmation |

### 4.2 Ignored Locations — 34

- 33 regenerable cache, dependency, log or temporary locations are Delete
  Candidates.
- `deploy/curis/releases/` is an Archive candidate containing a historical
  local release bundle.

Ignored locations require an independent cleanup review. Documentation
Governance must not delete them.

### 4.3 Delete Candidates — 41 Records

Tracked:

- 6 byte-identical duplicate PNG exports
- `frontend/ceo-evidence/dist/index.html`
- `frontend/ceo-evidence/tsconfig.tsbuildinfo`

Ignored:

- 33 cache, dependency, log, build-output or temporary locations listed in the
  Asset Report

Required before any deletion:

1. explicit deletion authorization;
2. fresh exact-path and relative-reference audit;
3. regeneration command or duplicate hash evidence;
4. evidence-retention check;
5. Security review for any path that may contain secrets or runtime state;
6. a recoverable backup or reproducible source;
7. a dedicated deletion report.

## 5. Forbidden Processing

### 5.1 Tracked Assets — 41

- 29 Release Evidence files
- 9 Issue/Review/product-decision Handoff records
- 2 PNG Review evidence files
- `frontend/ceo-evidence/index.html`, referenced by
  `frontend/ceo-evidence/tailwind.config.ts`

### 5.2 Ignored Locations — 10

- `.worktrees/`
- `backend/data/`
- `backend/tests/data/`
- `data/b_layer_pending_decisions.sqlite`
- `data/curis.sqlite`
- `data/issue_pipeline.sqlite`
- `data/quality.sqlite`
- `deploy/curis/gateway/.generated/`
- `deploy/new-api/.env`
- `deploy/new-api/data/`

These paths are current, sensitive, evidentiary or externally consumed. They
are not historical cleanup targets.

## 6. Future Archive Procedure

For each separately approved cohort:

1. confirm the source list against the Asset Report;
2. rerun Git, Markdown, script/config and AGENTS reference searches;
3. verify no path has changed classification since baseline;
4. create the destination directory under `docs/99_Archive/`;
5. use `git mv` and preserve relative package structure;
6. update every direct, directory and internal relative reference;
7. update `DOCUMENT_INVENTORY.md`, Archive README and Change Log;
8. run `git diff --check`;
9. record moved count, old/new path map and remaining risks;
10. stop before the next cohort.

## 7. Phase 3-B2 Boundary

- No file movement
- No file deletion
- No code modification
- No configuration modification
- No product-logic change
- No automatic cleanup of ignored paths

Execution requires a separate confirmation after this plan is reviewed.
