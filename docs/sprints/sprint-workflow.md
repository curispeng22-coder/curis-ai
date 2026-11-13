# Sprint Workflow

Status: Deprecated

## Sprint Lifecycle

1. Intake
2. Scope review
3. Planning
4. Implementation
5. Verification
6. Review
7. Retrospective

## Gate Dependency

Sprint workflow is controlled by `docs/ai-development-organization/sprint-gate-system.md` and `docs/ai-development-organization/system-state-machine.md`.

If the state machine and this workflow conflict, the stricter gate wins until the 总控决策席 resolves the conflict.

## Intake

Every Sprint item must include:

- Problem statement
- Owner role
- Scope boundary
- Acceptance criteria
- Verification expectation
- Dependencies and risks

## Scope Review

The 总控决策席 and relevant leads confirm whether the item is:

- In phase
- Owned
- Reviewable
- Testable
- Free of hidden business-code drift

## Planning

Approved items receive:

- Implementation plan
- File or module boundaries
- Test plan
- Review owner
- Completion evidence requirement

## Implementation

Implementation must stay inside the approved plan. Material scope changes return to scope review.

## Verification

Completion requires evidence:

- Automated test output when applicable
- Manual verification notes when applicable
- Known gaps if verification is incomplete

## Review

Review confirms:

- Acceptance criteria met
- Standards followed
- Docs updated
- Risks recorded
- No blocked gate bypassed

## Retrospective

Each Sprint closes with:

- What worked
- What changed
- What remains risky
- Process updates needed

## Sprint 1 Entry Gate

Sprint 1 may begin only when Sprint 0 organization review is approved.

Sprint 1 implementation may begin only after a separate Sprint 1 implementation gate is approved.
