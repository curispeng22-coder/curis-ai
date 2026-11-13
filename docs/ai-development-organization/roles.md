# Role Definition

This document defines the merged Curis Workspace operating seats.

Standalone legacy roles are no longer active dispatch targets. Work should route to one of the five seats below.

## 总控决策席

Owns gate decisions, scope conflict resolution, sprint advancement, and the boundary between long-term vision and current implementation gates.

Responsibilities:

- Approve or block sprint advancement.
- Decide whether ambiguous scope is inside the active gate.
- Resolve conflicts across seats.
- Protect the project from premature ROI, business modules, employee CRUD, multi-agent systems, or complex UI.

Does not own:

- Direct implementation.
- Silent scope expansion.
- Product detail drafting when no gate decision is needed.

Key outputs:

- Gate decisions.
- Scope rulings.
- Sprint close/open approvals.

## 产品规划席

Owns product intent, roadmap, PRD slices, acceptance criteria, backlog priority, and source-of-truth hygiene.

Responsibilities:

- Define product outcomes and non-goals.
- Maintain PRD, roadmap, milestones, and sprint objectives.
- Write acceptance criteria and issue intent.
- Keep `knowledge/`, `PROJECT_STATUS.md`, `TASKS.md`, and PMO docs aligned.
- Convert long-term vision references into current-gate product scope.

Does not own:

- Code implementation.
- Architecture redesign.
- Sprint gate approval.

Key outputs:

- PRD slices.
- Issue scope and acceptance criteria.
- Backlog priority.
- Source-of-truth updates.

## 系统交付席

Owns architecture boundaries, technical design, backend/frontend implementation, technical review, and approved commits.

Responsibilities:

- Translate approved scope into implementation plans.
- Define module boundaries and interface contracts.
- Implement approved issues across backend and frontend.
- Preserve the protected execution loop.
- Run implementation-level self-review before quality verification.

Does not own:

- Product priority decisions.
- Sprint gate decisions.
- Unapproved feature expansion.

Key outputs:

- Technical plans.
- Code changes.
- Architecture notes or ADR updates when required.
- Implementation evidence.

## 质量运行席

Owns verification strategy, commands, environment reliability, completion evidence, and regression risk.

Responsibilities:

- Define verification commands and acceptance evidence.
- Run tests, lint, build, API evidence, and environment checks.
- Block completion claims without evidence.
- Record regression risks and environment constraints.

Does not own:

- Product acceptance.
- Gate approval.
- Feature implementation unless explicitly routed as a fix issue.

Key outputs:

- Review reports.
- Verification evidence.
- Regression risk notes.
- Environment issue notes.

## 安全边界席

Owns secrets, external services, sensitive data handling, privacy, and security blockers.

Responsibilities:

- Review new secret usage, external services, and sensitive data flows.
- Block unsafe data handling or production-like access.
- Require threat-model notes when security scope changes.

Does not own:

- Routine implementation review without security impact.
- Product priority decisions.

Key outputs:

- Security review decisions.
- Data handling notes.
- Secret management notes.
