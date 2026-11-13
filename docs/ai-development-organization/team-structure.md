# Team Structure

## Purpose

This document defines the current Curis Workspace operating model.

## Structure

```text
总控决策席
  产品规划席
  系统交付席
  质量运行席
  安全边界席
```

## Operating Model

Each seat is a responsibility boundary, not necessarily a separate person or AI thread.

Daily work should route to one seat at a time. Legacy standalone roles remain historical context only and should not be used as dispatch targets.

## Seat Responsibilities

- 总控决策席 owns gate decisions, scope conflict, and sprint advancement.
- 产品规划席 owns product intent, PRD, backlog, acceptance criteria, and source-of-truth hygiene.
- 系统交付席 owns architecture boundaries, technical design, backend/frontend implementation, review, and commits.
- 质量运行席 owns verification, commands, environment reliability, and completion evidence.
- 安全边界席 owns secrets, external services, data handling, privacy, and security blockers.

## Team Rules

- Every work item has one accountable seat.
- Every cross-seat decision has a named approver.
- A seat may delegate execution, but not accountability.
- If a task crosses the current gate, 总控决策席 decides.
- If a task crosses product scope, 产品规划席 reframes it before engineering work.
- If completion evidence is missing, 质量运行席 blocks the completion claim.
- If data, secrets, external services, or privacy are affected, 安全边界席 must review.

## Minimum Review Quorum

Sprint advancement requires:

- 产品规划席 acceptance.
- 质量运行席 evidence.
- 总控决策席 approval.

系统交付席 and 安全边界席 review are required when their domains are affected.
