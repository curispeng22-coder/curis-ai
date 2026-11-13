# Decision Authority Matrix

## Purpose

This matrix defines who can decide, approve, block, or escalate Curis operating decisions.

Legend:

- D: Decides
- A: Approves
- B: Can block
- C: Consulted
- I: Informed

## Matrix

| Decision Type | 总控决策席 | 产品规划席 | 系统交付席 | 质量运行席 | 安全边界席 |
| --- | --- | --- | --- | --- | --- |
| Enter or close a sprint | D/A/B | C | C | C | C |
| Change current gate | D/A/B | C | C | C | C |
| Change product scope | A/B | D/R | C | C | C |
| Change collaboration flow | A | D/R | C | C | I |
| Change context boundary | A | D/R | C | C | C |
| Create or change PRD slice | C | D/A/R | C | C | C |
| Create executable issue | C | D/R | C | C | C |
| Approve technical plan | C | C | D/A/R | C | C |
| Change architecture boundary | A when contested | C | D/A/R | C | C |
| Mark work accepted | A when sprint-level | D/A | C | B | C |
| Mark verification sufficient | I | C | C | D/A/B | C |
| Add external service integration | A/B | C | R | C | D/A/B |
| Add secret or sensitive data handling | A/B | C | C | C | D/A/B |

## Authority Rules

- A decision with `D` must have a named decision owner.
- A decision with `A` is not active until approved.
- A decision with `B` can stop execution immediately.
- Consulted seats must be included before approval when their domain is affected.
- Informed seats receive the final decision and rationale.

## Prohibited Delegation

总控决策席 cannot delegate final sprint advancement approval.

质量运行席 cannot delegate a block caused by missing verification evidence.

安全边界席 cannot delegate a block caused by sensitive data, secrets, or external integrations.
