---
name: curis-development-organization
description: Use when working in Curis Workspace to enforce the AI Development Organization, role boundaries, governance docs, standards, and Sprint gates before business development.
---

# Curis Development Organization

Use this skill for Curis Workspace governance, planning, review, and implementation-readiness checks.

## Current Gate

Sprint 1 is open only for the MVP minimal working loop.

Allowed Sprint 1 work is limited to:

- Company CRUD
- Employee CRUD
- Task CRUD
- LLM execution through GPT-4o, Claude, DeepSeek, or local fallback
- ROI calculation
- SQLite persistence
- Next.js and Tailwind frontend
- FastAPI backend
- Documentation updates needed to reflect Sprint 1 status

Do not add advanced agent systems, multi-company systems, autonomy systems, new AI Development OS architecture, or complex business automation.

## Required Context

Read the relevant source-of-truth documents before acting:

- `AGENTS.md`
- `docs/ai-development-organization/README.md`
- `docs/ai-development-organization/team-structure.md`
- `docs/ai-development-organization/roles.md`
- `docs/ai-development-organization/responsibility-matrix.md`
- `docs/ai-development-organization/collaboration-protocol.md`
- `docs/ai-development-organization/token-optimization-strategy.md`
- `docs/ai-development-organization/task-execution-system.md`
- `docs/ai-development-organization/context-boundary-system.md`
- `docs/ai-development-organization/decision-authority-matrix.md`
- `docs/ai-development-organization/system-state-machine.md`
- `docs/ai-development-organization/sprint-gate-system.md`
- `docs/ai-development-organization/task-runtime-engine.md`
- `docs/ai-development-organization/agent-execution-loop.md`
- `docs/ai-development-organization/system-feedback-loop.md`
- `docs/ai-development-organization/token-governance-layer.md`
- `docs/ai-development-organization/runtime-state-observer.md`
- `docs/ai-development-organization/mvp-execution-loop.md`
- `docs/ai-development-organization/standard-task-template.md`
- `docs/ai-development-organization/bootstrap-sequence.md`
- `docs/standards/directory-structure.md`
- `docs/standards/documentation-standard.md`
- `docs/standards/coding-standard.md`
- `docs/sprints/sprint-workflow.md`
- `docs/sprints/sprint-0-organization-review.md`
- `docs/sprints/sprint-1-company-dashboard.md`
- `docs/sprints/mvp-implementation.md`

## Operating Protocol

1. Identify the request scope.
2. Check whether the current phase allows that scope.
3. Check the current system state and Sprint gate.
4. If blocked, state the gate and stop before implementation.
5. If allowed, make a narrow, reviewable change.
6. Verify with the strongest practical evidence.
7. Report changed files, verification, and remaining gaps.

## Role Routing

- CTO: organization, gates, standards, cross-role conflicts
- Product Lead: product outcomes and priority after Sprint 1 opens
- Engineering Lead: implementation planning and execution quality
- Architecture Lead: system boundaries and ADRs
- QA Lead: verification and acceptance evidence
- Documentation Lead: documentation structure and quality
- DevOps Lead: environments, automation, CI/CD
- Security And Compliance Lead: data, privacy, secrets, external services

## Completion Rule

Do not claim MVP scope is complete unless Company CRUD, Employee CRUD, Task CRUD, LLM execution, ROI calculation, and UI display are verified.
