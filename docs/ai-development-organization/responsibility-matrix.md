# Responsibility Matrix

## Purpose

This matrix defines accountability for the merged Curis operating seats.

Legend:

- A: Accountable
- R: Responsible
- C: Consulted
- I: Informed
- B: Blocking authority

## Matrix

| Area | 总控决策席 | 产品规划席 | 系统交付席 | 质量运行席 | 安全边界席 |
| --- | --- | --- | --- | --- | --- |
| Sprint gate approval | A/B | C | C | C | C |
| Sprint scope | A/B | R | C | C | C |
| Product direction | C | A/R | I | I | C |
| Backlog priority | I | A/R | C | C | C |
| PRD and acceptance criteria | C | A/R | C | C | C |
| Source-of-truth hygiene | C | A/R | C | C | I |
| Implementation plan | C | C | A/R | C | C |
| Architecture boundaries | A when contested | C | A/R | C | C |
| Backend/frontend implementation | I | C | A/R | C | C |
| Coding standards | C | I | A/R | C | I |
| Verification evidence | I | C | R | A/R/B | C |
| Environment and commands | I | I | C | A/R | C |
| Security and privacy | A when contested | C | C | C | A/R/B |
| External integrations | A/B | C | R | C | A/R/B |
| Release readiness | A/B | A | R | A/R/B | C |
| Retrospective actions | A | R | R | R | C |

## Conflict Rules

- Scope or sprint conflict: 总控决策席 decides.
- Product conflict: 产品规划席 recommends, 总控决策席 decides if the gate is affected.
- Architecture or implementation conflict: 系统交付席 recommends, 总控决策席 decides if unresolved.
- Verification conflict: 质量运行席 can block completion.
- Security conflict: 安全边界席 can block integration or release.
