# Token Optimization Strategy

## Purpose

This strategy keeps AI-assisted development efficient, focused, and reviewable without sacrificing correctness.

## Principles

- Read source-of-truth files before broad exploration.
- Prefer targeted searches over full-repository scans.
- Keep task scope narrow.
- Avoid repeating stable context unless it changed.
- Summarize decisions once and link to the source document.
- Preserve verification evidence in concise form.

## Context Loading Order

Use this order before expanding context:

1. `AGENTS.md`
2. Current Sprint document
3. Relevant organization or standards document
4. Relevant ADR
5. Target files
6. Related files found through focused search

## Prompt And Work Item Hygiene

Every task should include:

- Phase
- Scope
- Owner role
- Desired output
- Explicit blockers
- Files or docs to update when known

Avoid mixing unrelated work in one prompt. Split governance, planning, architecture, and implementation into separate tasks.

## File Reading Rules

- Start with indexes and README files.
- Use `rg` for targeted lookup.
- Read only files needed for the current decision.
- Re-open files after edits only when verification requires it.
- Do not load generated or dependency files unless they are the target.

## Documentation Rules

- Keep durable rules in stable source-of-truth documents.
- Keep Sprint-specific status in Sprint files.
- Link instead of duplicating long policy text.
- Remove stale summaries when they no longer add decision value.

## Agent Handoff Rules

Handoffs should include:

- Current phase and gate
- What changed
- What was verified
- What is blocked
- Next allowed action

Do not include long historical recaps unless the receiver lacks required context.

## Completion Compression

Final updates should be short and evidence-based:

- Changed files
- Verification
- Gate status

Detailed reasoning belongs in docs, ADRs, or review notes, not repeated chat output.
