# Low-Token Workflow V2 Decision

Date: 2026-07-12
Status: Adopted for Curis Workspace collaboration documents

## Problem

Automatic instructions and active source-of-truth files had accumulated full role contracts, capability inventories, and completed phase history. A task recovery therefore consumed large context before any issue work began, and repeated handoffs duplicated the same rules and verification evidence.

## Decision

- `AGENTS.md` keeps only shared boundaries, routing, verification ownership, and red lines.
- `knowledge/NOW.md` becomes the default current-state entry.
- Active status files contain current facts only.
- Completed chronology is archived, not deleted.
- Handoffs use four fields and link to evidence.
- Full verification runs once under 质量运行席; other seats do not repeat it without changed evidence.
- The main thread receives final evidence or user decision blockers only.

## Targets

- Recovery context: under about 2,000 tokens before Issue-specific files.
- Handoff: under 200 tokens.
- Final CEO report: short conclusion, reason, and next action.
- Active file limits: `AGENTS.md` 140 lines, `NOW.md` 60 lines, `CURRENT_CONTEXT.md` 100 lines, `PROJECT_STATUS.md` 80 lines, `TASKS.md` 70 lines.

## Non-Goals

- No product scope, runtime, API, or architecture change.
- No deletion of historical evidence.
- No change to gate authority or seat responsibility.
- No relaxation of independent quality or security review.

## Migration

The 2026-07-12 active documents were compacted. Their prior contents are preserved in:

- `knowledge/archive/CURRENT_CONTEXT_HISTORY_2026-07-12.md`
- `docs/pmo/archive/PROJECT_STATUS_HISTORY_2026-07-12.md`
- `docs/pmo/archive/TASKS_HISTORY_2026-07-12.md`

Future updates must keep completed history out of active entry files.
