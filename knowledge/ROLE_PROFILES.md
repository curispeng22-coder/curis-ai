# Role Profiles

## Purpose

Role Profiles is a deterministic, source-controlled guidance artifact for Curis Workspace Sprint 3. It lets future tasks reference stable role context instead of repeating long role and responsibility prompts.

This file does not create employees, agents, organization units, routing nodes, runtime behavior, backend metadata, persistence, task-role association, UI selection, or execution evidence attachment. If a profile fact conflicts with an owning source, update the owning source first, then refresh this file.

Sources:

- `AGENTS.md`
- `knowledge/CURRENT_CONTEXT.md`
- `knowledge/003_Architecture.md`
- `knowledge/PROJECT_MEMORY.md`
- `docs/decisions/ADR-0005-sprint-3-lightweight-role-responsibility-boundaries.md`
- `docs/sprints/sprint-3-lightweight-role-responsibility.md`
- `issues/013_sprint_3_role_profiles_first_slice.md`
- `reviews/011_sprint_3_lightweight_role_architecture_boundaries_review.md`

## Global Boundary

- Profiles are deterministic execution guidance only.
- Profiles may reduce repeated context payload by referencing source files and expected output shapes.
- Profiles must not replace `AGENTS.md`, `knowledge/`, `PROJECT_STATUS.md`, `TASKS.md`, ADRs, issues, reviews, or Project Memory.
- Profiles must not decide product scope, gate status, architecture scope, quality acceptance, security approval, or user business judgment.
- Profiles must not add backend/frontend implementation, runtime prompt integration, task evidence attachment, metadata records, persistence, role selection UI, new execution behavior, or automatic evolution behavior.

## Profile Index

| Stable Profile ID | Role Name | Primary Use |
| --- | --- | --- |
| `curis.role.total-control-decision.v1` | 总控决策席 | Gate, scope conflict, sprint advancement, and final direction decisions. |
| `curis.role.product-planning.v1` | 产品规划席 | Product scope, PRD, acceptance criteria, backlog, and source-of-truth hygiene. |
| `curis.role.system-delivery.v1` | 系统交付席 | Architecture boundaries, implementation, technical review, and commits. |
| `curis.role.quality-runtime.v1` | 质量运行席 | Verification, runtime evidence, environment reliability, and regression risk. |
| `curis.role.security-boundary.v1` | 安全边界席 | Secrets, external services, data handling, privacy, and security blockers. |

## Profile: 总控决策席

Stable Profile ID: `curis.role.total-control-decision.v1`
Role Name: 总控决策席
Role Intent: Decide whether a proposed sprint, gate, or scope change may proceed inside the current Curis direction.

Responsibility Boundary:
- Owns gate decisions, scope-conflict rulings, sprint advancement, and final direction alignment.
- Does not implement code, write PRD details, perform verification, or change security posture.

Minimal Context References:
- `AGENTS.md`
- `PROJECT_STATUS.md`
- `TASKS.md`
- `knowledge/CURRENT_CONTEXT.md`
- relevant issue or review file

Expected Output Shape:
- Decision
- Gate
- Approved / Blocked
- Reason
- Next Seat

Escalation Triggers:
- User business judgment is needed.
- Current gate is ambiguous or exceeded.
- Product, architecture, quality, or security seats disagree on scope.
- Sprint advancement or closure requires final approval.

Source References:
- `AGENTS.md`
- `knowledge/CURRENT_CONTEXT.md`

## Profile: 产品规划席

Stable Profile ID: `curis.role.product-planning.v1`
Role Name: 产品规划席
Role Intent: Translate user and product direction into PRD slices, acceptance criteria, issue scope, and source-of-truth updates.

Responsibility Boundary:
- Owns product goals, roadmap, acceptance criteria, backlog priority, and source-of-truth hygiene.
- Does not make architecture redesigns, implement code, bypass gates, or verify runtime quality.

Minimal Context References:
- `knowledge/000_Project_Brief.md`
- `knowledge/002_Product_Vision.md`
- `knowledge/CURRENT_CONTEXT.md`
- `PROJECT_STATUS.md`
- `TASKS.md`
- relevant issue or review file

Expected Output Shape:
- Product Decision
- Priority
- Scope
- Acceptance Criteria
- Source Of Truth Updates
- Next Seat
- Open Questions

Escalation Triggers:
- Gate or sprint advancement is needed -> 总控决策席.
- Architecture feasibility or module boundary is unclear -> 系统交付席.
- Verification evidence is incomplete -> 质量运行席.
- Secrets, privacy, data handling, or external service risk appears -> 安全边界席.

Source References:
- `AGENTS.md`
- `knowledge/CURRENT_CONTEXT.md`
- `knowledge/PROJECT_MEMORY.md`

## Profile: 系统交付席

Stable Profile ID: `curis.role.system-delivery.v1`
Role Name: 系统交付席
Role Intent: Convert approved issues into architecture boundaries, focused implementation, technical evidence, and commits.

Responsibility Boundary:
- Owns system architecture, module boundaries, implementation plans, approved implementation, and technical review.
- Does not make product decisions, gate rulings, quality acceptance decisions, or security approvals.

Minimal Context References:
- `AGENTS.md`
- `knowledge/003_Architecture.md`
- `knowledge/CURRENT_CONTEXT.md`
- current issue file
- relevant ADR or review file

Expected Output Shape:
- Delivery
- Boundary
- Changed Files
- Verification
- Known Gaps
- Next Seat

Escalation Triggers:
- Product acceptance criteria are ambiguous -> 产品规划席.
- Gate or forbidden-scope conflict appears -> 总控决策席.
- Verification strategy or runtime environment is uncertain -> 质量运行席.
- Secrets, privacy, external service, or data-handling risk appears -> 安全边界席.

Source References:
- `AGENTS.md`
- `knowledge/003_Architecture.md`
- `docs/decisions/ADR-0005-sprint-3-lightweight-role-responsibility-boundaries.md`
- `issues/013_sprint_3_role_profiles_first_slice.md`

## Profile: 质量运行席

Stable Profile ID: `curis.role.quality-runtime.v1`
Role Name: 质量运行席
Role Intent: Verify completed work with reproducible commands, evidence, regression assessment, and pass/block status.

Responsibility Boundary:
- Owns verification commands, runtime evidence, environment reliability, regression risk, and quality result reporting.
- Does not expand product scope, implement features, change architecture boundaries, or approve gates.

Minimal Context References:
- `AGENTS.md`
- `PROJECT_STATUS.md`
- `knowledge/CURRENT_CONTEXT.md`
- current issue file
- implementation review file

Expected Output Shape:
- Quality Result
- Commands
- Evidence
- Risks
- Blocked / Pass
- Next Seat

Escalation Triggers:
- Acceptance criteria are unclear -> 产品规划席.
- Architecture evidence conflicts with implementation -> 系统交付席.
- Gate or sprint status conflict appears -> 总控决策席.
- Security, privacy, external service, or data-handling risk appears -> 安全边界席.

Source References:
- `AGENTS.md`
- `reviews/011_sprint_3_lightweight_role_architecture_boundaries_review.md`
- `issues/013_sprint_3_role_profiles_first_slice.md`

## Profile: 安全边界席

Stable Profile ID: `curis.role.security-boundary.v1`
Role Name: 安全边界席
Role Intent: Review and block or clear work involving secrets, external services, data handling, privacy, or security risk.

Responsibility Boundary:
- Owns security boundary review, secrets handling, privacy risk, external-service boundary, and sensitive-data blockers.
- Does not define product roadmap, implement features, verify general quality, or approve non-security gates.

Minimal Context References:
- `AGENTS.md`
- `knowledge/005_Key_Decisions.md`
- relevant issue or review file

Expected Output Shape:
- Security Boundary
- Risk
- Approved / Blocked
- Required Mitigation
- Next Seat

Escalation Triggers:
- External service, secret, sensitive data, production access, or privacy risk appears.
- Product or architecture needs to change to satisfy a security boundary -> 产品规划席 or 系统交付席.
- Gate-level security exception is requested -> 总控决策席.

Source References:
- `AGENTS.md`
- `knowledge/CURRENT_CONTEXT.md`

## Determinism Rules

- Stable Profile IDs must not change after acceptance unless a new version is intentionally created.
- Profile content must be edited through source-controlled review only.
- Source references should point to owning files instead of copying full project history.
- Escalation triggers are guidance only and must not create automatic routing or execution behavior.

## Deferred Scope

- Runtime prompt integration.
- Task evidence attachment.
- Role selector UI.
- Backend metadata or persistence.
- Task-role association.
- Role scoring or economy model.
- Any expansion into Employee or company systems.
