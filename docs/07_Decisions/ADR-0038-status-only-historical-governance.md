# ADR-0038: Status-Only Historical Governance

Status: Frozen

Baseline:
main @ 8ac3b814

Updated:
2026-07-30

Module: Documentation Governance

## Decision

Phase 3-A applies `Status: Deprecated` only to clearly superseded Markdown
documents. Existing paths and historical content remain unchanged.

The approved categories are:

- old UI proposals
- the fixed CEO Office secretary architecture
- old Workspace/Admin architecture
- superseded development workflows
- historical Prototype/Demo documentation

`docs/99_Archive/README.md` becomes the Frozen Archive governance and query
index. It does not authorize moving files into Archive.

## Boundaries

- No file movement, rename or deletion
- No business-code or product-logic change
- No status injection into HTML, images, design sources, CSS or JavaScript
- No change to Release Evidence or WorkBuddy Memory without a separate review
- Historical lifecycle text is preserved as `Historical Status` when needed

## Consequences

- Deprecated documents cannot override Current State or a Frozen domain entry.
- Agents read them only for history, provenance or migration analysis.
- Phase 3-B requires explicit confirmation and a reference audit.
