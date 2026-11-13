# Append-Only Evolution Event Log

Date: 2026-07-07

Owner seat: 系统交付席

Status: Implementation accepted by 产品规划席 on 2026-07-07 (质量运行席 verification PASS, 57 tests). D3 slice CLOSED. Next per ADR-0016 order D1→D3→D2: D2 Evolution Governor Sandbox (issues/046).

Source gate: `issues/044_execution_substance_phase_gate.md`

Boundary ADR: `docs/decisions/ADR-0016-execution-substance-initiative.md`

## Objective

Introduce an append-only event log that records every evolution proposal, simulation, decision, lock, and rollback as immutable events with a correlation id. The log becomes the system of record for audit; existing mutable tables may remain for query convenience.

## Allowed Scope

- Add a new append-only `evolution_events` table (or dedicated append-only store) with event type, payload, correlation id, and timestamp.
- Write events from the existing Evolution Governor paths (proposal, simulation, decision, lock, rollback).
- Add read-only endpoints/helpers over the log.
- Keep mutable tables for query; no UPDATE/DELETE path on the event log.
- Backend tests asserting insert-only behavior and correlation-id linkage.

## Required Preservation

- AI Task Executor MVP v0.1 local/demo release.
- Tool System v1.8 loop.
- Stability > Optimization > Evolution policy.
- Chinese operation console.
- Task API payload `{ content }`.
- Existing API semantics (except additive read/event endpoints).
- Existing execution behavior.
- Existing Evolution Governor decision policy.
- Human-approval gate for production mutation.
- Role Profiles / Role Context semantics.
- Existing source-of-truth files (the log supplements, does not replace them).

## Forbidden Scope

- Dropping or mutating existing persistence tables in this phase.
- UPDATE / DELETE paths on the event log.
- Replacing `CURRENT_CONTEXT.md`, `PROJECT_STATUS.md`, or other source-of-truth files with the log.
- Employee CRUD / employee expansion, multi-agent, agent abstraction.
- Complex UI / dashboard beyond minimal evidence display.
- API semantic changes beyond additive read/event endpoints.
- ROI / economy, business modules, company organization.
- Runtime prompt integration beyond role-context guidance.
- Task-role association, task evidence attachment.
- Vector database, embeddings, external memory service, hidden memory store.
- Automatic evolution behavior changes / automatic code self-modification.
- Future-layer implementation.

## Acceptance Criteria

- `evolution_events` exists and is written by the existing Evolution Governor paths.
- Every event carries a correlation id linking proposal/simulation/decision/lock/rollback.
- No UPDATE/DELETE path exists for the event log (asserted by test + code review).
- Read-only endpoints/helpers return events by correlation id.
- Backend regression passes; new focused tests cover insert-only and linkage.
- `git diff --check` passes; forbidden-scope scan passes.

## Verification

质量运行席 verifies with diff guard, `git diff --check`, forbidden-scope scan, and focused tests asserting insert-only behavior and correlation-id linkage across events.

## Handoff

Handoff: sent to 质量运行席 (after implementation).

Target seat: 质量运行席.

Compact payload:

- Issue: `issues/047_append_only_evolution_log_first_slice.md`
- Objective: Add an append-only evolution event log with correlation id as the audit system of record.
- Preserve: AI Task Executor MVP v0.1 local/demo release, Tool System v1.8 loop, Stability > Optimization > Evolution policy, Chinese operation console, Task API `{ content }`, existing API semantics (except additive read/event endpoints), existing execution behavior, Evolution Governor decision policy, human-approval gate, Role Profiles, Role Context, existing source-of-truth files.
- Allow: new append-only `evolution_events` table/store; events from governor paths; read-only endpoints/helpers; keep mutable tables for query; backend tests for insert-only and linkage.
- Forbid: dropping/mutating existing tables; UPDATE/DELETE on the event log; replacing source-of-truth files; Employee CRUD/expansion, multi-agent, agent abstraction; complex UI/dashboard; API semantic changes beyond additive endpoints; ROI/economy, business modules, company organization; runtime prompt integration beyond role-context guidance; task-role association; task evidence attachment; vector/embeddings/external/hidden memory; automatic evolution behavior changes / automatic code self-modification; future-layer scope.
