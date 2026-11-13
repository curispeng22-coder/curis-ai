# Curis Workspace Project Handoff

Authority Class: HISTORY
Disposition: HISTORICAL / NOT A CURRENT ENTRYPOINT
Navigation updated: 2026-10-25

**以下是原阶段历史记录。** 旧“Current / Active / Next / Read this first”只描述当时状态。
当前请从 [AGENTS](<../../../../AGENTS.md>) → [现有入口](<../../../00_Context/CURIS_CURRENT_ENTRYPOINT.md>)查询；进度只看 [既有执行看板](<../../../../artifacts/tasks/CURIS-V1-BUSINESS-CATALOG-TEAM-20261008/DELIVERY_PROGRESS_AND_BATCH_PLAN_20261013.md>)。
[本轮维护决定](<../../../07_Decisions/DECISION-2026-10-25-development-baseline-doc-maintenance.md>)保留原文、原 Status 和历史日期；物理归档尚未执行。候选见 [精确归档清单](<../../../../artifacts/tasks/CURIS-V1-DEV-BASELINE-CONSOLIDATION-20261025/PLACEMENT_REVIEW.md>)。

Status: Deprecated

Last updated: 2026-07-08

Purpose: let a temporary team take over with minimal token usage, then let the original Codex flow resume later without rereading the full repository.

Read order for any incoming team:

1. Read this file first.
2. Read `AGENTS.md` for operating rules.
3. Read `shared/pmo/PROJECT_SPACE_MAP.md` for Admin Platform / Workspace / Shared file ownership.
4. Read `TASKS.md` active task and `knowledge/CURRENT_CONTEXT.md` current constraints.
5. If continuing the next decision, read only `issues/048_adr0016_gate_submission_package.md`, `issues/044_execution_substance_phase_gate.md`, and `docs/decisions/ADR-0016-execution-substance-initiative.md`.
6. Do not scan the whole repo unless the active issue explicitly requires it.

## 项目当前状态

- Current product state: AI Task Executor MVP v0.1 local/demo version has been closed and accepted.
- Current project node: next bounded phase selection after Project Memory Execution Summary.
- Active task in `TASKS.md`: `T-137 Decide next bounded phase after execution summary memory`.
- Current owner seat: `产品规划席`, but the next actual route is a gate/scope decision for `总控决策席`.
- Current implementation gate: Tool System v1.8.
- Current launch scope: AI Task Executor MVP, preserving compatibility with the future AI Company System.
- Current accepted product capability: local/demo task executor with Chinese operation console, task creation/run/history/detail, execution evidence, reliability evidence, local API smoke helper, Project Memory, Role Profiles, read-only role-context helper, release notes, and execution summary memory.
- Important handoff caveat: several new planning files are currently untracked in git. Treat them as proposed handoff material, not merged source-of-truth, until explicitly staged/committed.

Untracked proposed handoff/planning files currently visible:

- `docs/architecture/redesign-v2-architecture-and-roadmap.md`
- `docs/decisions/ADR-0016-execution-substance-initiative.md`
- `docs/decisions/ADR-0017-multitenant-department-catalog.md`
- `issues/044_execution_substance_phase_gate.md`
- `issues/045_runtime_role_wiring_first_slice.md`
- `issues/046_evolution_governor_sandbox_first_slice.md`
- `issues/047_append_only_evolution_log_first_slice.md`
- `issues/048_adr0016_gate_submission_package.md`
- `reviews/037_redesign_v2_architecture_review_decision.md`

## 项目目标

Final product goal: Curis is a commercial multi-tenant AI Company System composed of Curis Admin Platform and Curis Workspace.

Near-term launch product: AI Task Executor MVP.

The current product strategy is:

- Build the AI Task Executor foundation first.
- Preserve the future L0-L6 AI Company System frame.
- Keep Admin Platform and Workspace development separated by project space.
- Put cross-product contracts, role rules, and PMO maps in `shared/`.
- Do not prematurely implement company organization, ROI/economy, Employee CRUD, business modules, external platform integrations, multi-agent routing, or complex dashboards.
- Move only through approved gates with evidence.

Canonical product layers:

```text
L6 经济层: ROI / 成本 / 优化
L5 公司层: 组织 / 部门 / 职责
L4 工作流层: 任务拆解 / 编排 / 状态流转
L3 工具层: 工具注册 / 路由 / 执行 / fallback
L2 员工层: AI执行角色 / 员工能力 / 角色偏好
L1 执行层: Task / Run / Status / History / Result
L0 产品层: 用户界面 / 操作台 / 可视化
```

Important: do not renumber L0-L6. The v2 redesign has been corrected to keep this canonical numbering. `D 数据底座` may be discussed as a cross-cutting layer that does not consume an L number.

## 已完成模块

Accepted and verified modules/capabilities:

- Sprint 0: AI company execution kernel foundation.
- Tool System v1.6: Meta Development System.
- Tool System v1.8: Controlled Self-Evolution Kernel with Stability > Optimization > Evolution policy.
- Sprint 1: company operation visualization first slice and CEO-readable polish.
- Sprint 2: unified task console.
- Sprint 2 Project Memory Foundation: `knowledge/PROJECT_MEMORY.md`.
- Sprint 3 Role Profiles: `knowledge/ROLE_PROFILES.md`.
- Sprint 3 Role Context helper: `backend/app/role_context.py`, read-only and not wired into prompt/runtime behavior.
- Sprint 4: bounded multi-entry UI first slice.
- AI Task Executor MVP readiness review.
- Chinese operation console localization.
- Release-candidate stabilization/documentation package.
- First local/demo release verification using real local FastAPI app.
- AI Task Executor MVP v0.1 release record.
- Post-v0.1 Execution Reliability phase:
  - Run Evidence Reliability.
  - Workflow Error/Fallback Evidence Map.
  - Evolution Decision Evidence Map.
  - Phase closeout review.
- Local/Demo Operator Release Notes package.
- Local/Demo API Smoke Helper: `tools/local_demo_api_smoke.py`.
- Project Memory Execution Summary: `knowledge/EXECUTION_SUMMARY_MEMORY.md`.

## 当前架构

Runtime stack:

- Backend: FastAPI + SQLite.
- Frontend: Next.js.
- Persistence: SQLite tables for tasks, tools, executions, tool traces, workflows, auto workflows, workflow traces, execution patterns, failure logs, tool performance, workflow metrics, execution scores, development strategies, system evolution log, meta development records, evolution decisions, architecture locks, evolution simulations, rollback records.

Protected execution loop:

```text
Task -> Orchestrator -> Auto Workflow Generator -> Employee -> Tool Router -> Tool Executor -> Result -> Development Learning -> Meta Development -> Evolution Governor -> Storage
```

Current implemented frame:

- L0: Chinese task console, task entry, history, selected task detail, bounded multi-entry affordances.
- L1: task create, run, status, history, result.
- L2: minimal AI Employee coordinator required for execution only.
- L3: tool registry, router, executor, fallback.
- L4: workflow generation, workflow trace, stateful execution.
- L5/L6: future gated layers only.

Current v2 redesign status:

- `docs/architecture/redesign-v2-architecture-and-roadmap.md` is a Proposed future blueprint.
- It should not replace `knowledge/002_Product_Vision.md` or `knowledge/003_Architecture.md`.
- Its latest corrected direction:
  - Keep canonical L0-L6.
  - Express `D 数据底座` as cross-cutting, no L number.
  - Treat statistics/analytics as L6 economy measurement capability, future gate.
  - Treat department catalog and multi-tenant CEO as L5 company layer, future gate.
  - Treat Employee CRUD/HR capabilities as future L2/L5 scope, not current MVP.

## 技术决策

Key accepted decisions:

- Use strict role seats: `总控决策席`, `产品规划席`, `系统交付席`, `质量运行席`, `安全边界席`.
- Use issue -> review -> acceptance flow; no large ungated implementation.
- Keep handoffs compact to reduce token use.
- Keep Project Memory deterministic and source-referenced; it does not replace source files.
- Keep Role Profiles source-controlled and deterministic.
- Keep current `role_context.py` read-only unless a new gate explicitly unlocks runtime prompt integration.
- Keep AI Task Executor as the current product surface until future L5/L6 gates are approved.
- Preserve Task API payload `{ content }`.
- Preserve human approval for production mutation and automatic code self-modification.

Current proposed decisions not yet approved:

- ADR-0016 Execution Substance Initiative:
  - D1 Runtime Role Wiring.
  - D2 Evolution Governor Sandbox.
  - D3 Append-Only Evolution Event Log.
- ADR-0017 Multi-tenant CEO + Department Catalog.
- v2 architecture roadmap as future blueprint.

## 为什么采用这个方案：

- It separates final product vision from current approved implementation scope.
- It lets the project progress toward a real AI Company System without breaking the AI Task Executor MVP gate.
- It avoids token waste by maintaining `PROJECT_HANDOFF.md`, `PROJECT_STATUS.md`, `TASKS.md`, `knowledge/CURRENT_CONTEXT.md`, and Project Memory as low-context entry points.
- It keeps L0-L6 stable, preventing role confusion and document drift.
- It treats self-evolution as controlled, auditable, and reversible rather than automatic.
- It keeps future company/economy features gated so the team does not accidentally build ROI, departments, Employee CRUD, external platform integrations, or business modules inside the current MVP.

## 未完成任务

Active:

- `T-137 Decide next bounded phase after execution summary memory`.

Recommended next decision path:

1. Route `issues/048_adr0016_gate_submission_package.md` to `总控决策席`.
2. Decide whether to approve ADR-0016 gate.
3. Explicitly decide D1 conflict:
   - Option A: approve D1 and consciously supersede the Sprint 3 Role Context boundary only for explicit role-context prompt guidance.
   - Option B: defer D1 and proceed with D3 + D2 only.
   - Option C: reject D1 from ADR-0016.
4. If approved, open per-slice boundary work:
   - `issues/045_runtime_role_wiring_first_slice.md`
   - `issues/047_append_only_evolution_log_first_slice.md`
   - `issues/046_evolution_governor_sandbox_first_slice.md`

Important order:

- Preferred ADR-0016 order if D1 is approved: Role wiring -> Append-only event log -> Governor sandbox.
- If D1 is deferred: Append-only event log -> Governor sandbox; leave role wiring for a separate gate.

Future but not current:

- Statistics/analytics capability for L6.
- Department catalog and multi-tenant CEO model for L5.
- HR/Employee CRUD and skill assignment.
- External platform connectors and credential store.
- ROI/economy loop and BI dashboards.
- Media pipeline and long-running async worker infrastructure.

## 当前Bug

No confirmed blocker bug is currently recorded for the accepted v0.1 local/demo product.

Known issues/gaps:

- FastAPI Python 3.14 warning was triaged as `defer-known-gap`; no fix has been approved.
- `AGENTS.md` current sprint text appears stale (`Sprint 4 - Multi-Entry And Advanced UI`) compared with `PROJECT_STATUS.md` / `TASKS.md`, which say the current node is next bounded phase selection after Project Memory Execution Summary. Treat `TASKS.md` and `knowledge/CURRENT_CONTEXT.md` as more current for task routing.
- ADR-0016/0017, v2 roadmap, issues/044-048, and review/037 are untracked proposed materials. Do not assume they are committed.
- `role_context.py` exists but is not wired into runtime prompt execution; this is intentional under the current accepted boundary.
- Project Memory and Current Context may lag when untracked proposed files are edited; update source-of-truth only after gate decisions.

## 团队角色分工和角色要求

New team must use the existing Curis operating seats from `AGENTS.md`. Do not create new standalone roles unless the user explicitly approves a workflow redesign.

| Seat | 中文名称 | Responsibility | Must not do |
| --- | --- | --- | --- |
| Gate | 总控决策席 | Gate decisions, scope conflict裁决, sprint/phase advancement, final direction approval | Write implementation code; silently approve scope expansion |
| Product | 产品规划席 | Product scope, PRD, roadmap, acceptance criteria, backlog priority, source-of-truth hygiene | Implement code; redesign architecture alone |
| Delivery | 系统交付席 | Architecture boundaries, implementation plan, backend/frontend delivery, technical review, commits | Change product scope; bypass gate; self-approve quality |
| Quality | 质量运行席 | Verification, commands, regression evidence, environment reliability, completion evidence | Add product features; accept product scope alone |
| Security | 安全边界席 | Secrets, external services, data handling, privacy, credential and compliance blockers | Approve unrelated product or architecture scope |

Role requirements:

- Every seat reads only the minimum context needed for its task.
- Every seat starts from `PROJECT_HANDOFF.md`, `AGENTS.md`, `TASKS.md`, `knowledge/CURRENT_CONTEXT.md`, and the active issue/review only.
- Every seat must respect the current gate before acting.
- Any gate decision, phase advancement, or scope conflict routes to `总控决策席`.
- Any external service, credential, secret, privacy, or data-handling risk routes to `安全边界席`.
- Any product ambiguity routes to `产品规划席`.
- Any architecture ambiguity found during verification routes back to `系统交付席`.
- No seat may silently treat Proposed files as accepted SoT.
- No seat may implement future L5/L6 capabilities without an explicit approved gate.

Required workflow:

```text
产品规划席 -> 系统交付席 -> 质量运行席 -> 产品规划席 -> main thread closeout
```

Exception routes:

```text
Gate/scope conflict -> 总控决策席
Secrets/external/data risk -> 安全边界席
Product ambiguity -> 产品规划席
Architecture ambiguity -> 系统交付席
```

Compact handoff format:

```text
Issue:
Objective:
Special Constraints:
Next Seat:
```

Completion evidence format:

```text
Product Progress:
Completed:
Verification:
Known Gap:
Next:
Handoff:
```

New team working rule:

- Do not continuously scan role conversations.
- The completing seat must route to the next seat directly when possible.
- If direct routing is unavailable, write `Handoff: HANDOFF_REQUIRED` plus the compact payload.
- A task is not complete until handoff status is `sent`, `final closeout`, or `HANDOFF_REQUIRED`.
- After each accepted issue, update `knowledge/CURRENT_CONTEXT.md`.
- After phase/sprint status changes, update `PROJECT_STATUS.md` and `TASKS.md`.
- Final user-facing reports must start with one sentence: `Product Progress: ...`

## 下一步开发计划

Immediate next handoff:

```text
Issue: issues/048_adr0016_gate_submission_package.md
Objective: Approve or reject ADR-0016 gate; explicitly裁决 D1 runtime role wiring vs Sprint 3 Role Context boundary.
Special Constraints: v2 is blueprint only, not SoT. Do not approve whole v2 as implementation. Preserve canonical L0-L6. D1 is behavior change and needs explicit gate解禁. D3 is additive schema. D2 must write only to throwaway sandbox paths.
Next Seat: 总控决策席
```

If `总控决策席` approves ADR-0016:

1. `系统交付席` defines per-slice architecture boundaries.
2. `质量运行席` verifies boundary plans.
3. `产品规划席` accepts or revises.
4. Implementation proceeds one slice at a time.
5. After each issue: update `knowledge/CURRENT_CONTEXT.md`.
6. After phase/sprint change: update `PROJECT_STATUS.md` and `TASKS.md`.

If `总控决策席` rejects or defers ADR-0016:

- Keep v2 as blueprint only.
- Return to `产品规划席` for another bounded phase selection.

Resume rule when Codex quota returns:

- Read only this file, `TASKS.md`, `knowledge/CURRENT_CONTEXT.md`, and the active issue/review.
- Do not reread full history.
- Continue from the last accepted seat handoff.
- If no direct seat handoff exists, use the immediate next handoff above.

## 禁止修改区域

Do not modify or implement without explicit gate approval:

- ROI/economy system.
- Company organization, departments, reporting lines, staffing.
- Employee CRUD or employee expansion.
- Multi-agent system, agent abstraction layer, or agent routing.
- Business modules.
- External platform connectors, external channels, secrets, credential stores, or payment/notification services.
- Complex UI/dashboard.
- Vector database, embeddings, external memory service, hidden memory store, agent memory, or Employee memory.
- Runtime prompt integration beyond separately approved role-context guidance.
- Task-role association or task evidence attachment.
- API semantic changes beyond explicitly approved additive endpoints.
- Persistence/schema changes except explicitly approved slices.
- Automatic code self-modification or production mutation without human approval.
- Architecture lock bypass, uncontrolled architecture changes, or Evolution Governor policy weakening.
- Mock data or simulation substitution for release verification.

Do not treat these as active SoT unless approved/committed:

- `docs/architecture/redesign-v2-architecture-and-roadmap.md`
- `docs/decisions/ADR-0016-execution-substance-initiative.md`
- `docs/decisions/ADR-0017-multitenant-department-catalog.md`
- `issues/044_execution_substance_phase_gate.md`
- `issues/045_runtime_role_wiring_first_slice.md`
- `issues/046_evolution_governor_sandbox_first_slice.md`
- `issues/047_append_only_evolution_log_first_slice.md`
- `issues/048_adr0016_gate_submission_package.md`
- `reviews/037_redesign_v2_architecture_review_decision.md`

## Team Switch Rules

- Temporary team should treat this as a handoff package, not as permission to expand scope.
- Temporary team must not silently resolve gate conflicts.
- Temporary team must record any decision in `issues/`, `reviews/`, `docs/decisions/`, `PROJECT_STATUS.md`, `TASKS.md`, or `knowledge/CURRENT_CONTEXT.md`.
- Temporary team must leave a compact closeout note with changed files, verification, known gaps, and next seat.
- When original Codex flow resumes, it should start from this file and the latest changed issue/review only.
