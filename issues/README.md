# Issues

This folder contains executable project issues.

Issues are the main handoff format for approved work across Curis operating seats.

## Issue Rules

- One issue should describe one bounded slice.
- Every issue must name the owner seat.
- Every issue must state allowed files.
- Every issue must state non-goals.
- Every issue must include acceptance criteria.
- Every issue must include verification commands or manual verification expectations.
- Do not use issues to bypass the active gate in `AGENTS.md`.

## Suggested Template

```markdown
# Issue: <short title>

## Owner

产品规划席 | 系统交付席 | 质量运行席 | 安全边界席 | 总控决策席

## Context

Minimal context needed to execute this issue.

## Scope

Allowed work.

## Non-Goals

Out-of-scope work.

## Allowed Files

- `path/to/file`

## Acceptance Criteria

- [ ] Criterion

## Verification

- Command or manual verification.

## Completion Notes

Filled after completion.
```
