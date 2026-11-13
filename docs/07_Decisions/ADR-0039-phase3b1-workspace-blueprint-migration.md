# ADR-0039: Phase 3-B1 Workspace Blueprint Migration

Status: Frozen

Baseline:
main @ 4a8a0debbf8654c5c0dfd0fa20829406305213e4

Updated:
2026-07-30

Module: Documentation Governance

## Decision

Move the 17 Deprecated, non-ADR Markdown files in
`curis_workspace_blueprint/` to
`docs/99_Archive/curis_workspace_blueprint/`, preserving their internal
directory structure.

Keep the two files in `curis_workspace_blueprint/ADR/` at their original paths.
They are historical Decision Records and are outside the Phase 3-B1 migration
scope.

## Preconditions Confirmed

- No AGENTS reference points to the 17 files.
- No script, test, CI or configuration reference points to the 17 files.
- All repository Markdown references to the moved paths are known and updated.
- Every moved file was already marked `Status: Deprecated`.

## Boundaries

- Markdown only
- No deletion
- No business-code, product-logic, database or runtime change
- No migration of CURRENT_STATE, Frozen domain entries, Decision Records,
  Change Log, Issue records or Review evidence

## Consequences

- Archived blueprint content remains searchable and traceable under
  `docs/99_Archive/`.
- Frozen entry documents may cite the archive for history, but archived content
  has no current authority.
- Further migrations require a separate reference audit and confirmation.
