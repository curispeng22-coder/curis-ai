# 系统架构

Status: Deprecated

## 当前架构

Curis Workspace Tool System v1.8 is a FastAPI + SQLite + Next.js implementation.

Final product target: AI Company System.

Current launch scope: AI Task Executor MVP.

The current stage must build the execution framework without prematurely implementing future company or economy layers.

## 全局分层架构

```text
L6 经济层: ROI / 成本 / 优化
L5 公司层: 组织 / 部门 / 职责
L4 工作流层: 任务拆解 / 编排 / 状态流转
L3 工具层: 工具注册 / 路由 / 执行 / fallback
L2 员工层: AI执行角色 / 员工能力 / 角色偏好
L1 执行层: Task / Run / Status / History / Result
L0 产品层: 用户界面 / 操作台 / 可视化
```

Current implemented framework:

- L0: unified task console and selected-task visualization.
- L1: task create, run, status, history, result.
- L2: minimal AI Employee coordinator for execution only.
- L3: tool registry, routing, execution, fallback.
- L4: workflow generation, workflow trace, stateful execution.

Future gated layers:

- L5: company organization, departments, ownership, and responsibility system.
- L6: ROI, cost, optimization, and economic decisioning.

Current execution loop:

```text
Task -> Orchestrator -> Auto Workflow Generator -> Employee -> Tool Router -> Tool Executor -> Result -> Development Learning -> Meta Development -> Evolution Governor -> Storage
```

## AI 员工运行时工作流原则

- Orchestrator owns final user-facing task closeout.
- Auto Workflow Generator produces compact step packages, not long role prompts.
- AI Employee receives only the current step, required tool, expected output, accumulated minimal context, and unusual constraints.
- AI Employee returns structured output, trace data, blocker if any, and next-step readiness.
- Tool Router and Tool Executor stay responsible for tool selection, fallback, chaining, and execution.
- Result Store persists step result, workflow trace, next step, blocker, and final summary evidence.
- Extra context is added only for permission boundary, safety boundary, user decision, or evolution-governor evaluation.
- This is not an Employee CRUD system, multi-agent system, or agent abstraction layer.

## 后端模块

- `backend/app/main.py`: FastAPI app, task APIs, tool APIs, trace/workflow APIs.
- `backend/app/orchestrator.py`: stateful task orchestration, workflow generation, execution learning, autonomous development loop.
- `backend/app/employee.py`: AI Employee coordinator for step execution.
- `backend/app/orchestrator.py`: v1.6 meta-development report generation after development learning.
- `backend/app/evolution_governor.py`: v1.8 controlled evolution evaluation, stability-first policy, proposal gating, architecture lock checks, simulation records, risk analysis, decision records, and rollback records.
- `backend/app/tool_router.py`: tool selection and fallback order.
- `backend/app/tool_executor.py`: tool dispatch, async execution, chaining, fallback.
- `backend/app/tool_registry.py`: tool registration and lookup.
- `backend/app/prompt_builder.py`: task-to-prompt conversion.
- `backend/app/model_gateway.py`: New API OpenAI-compatible model gateway adapter for all default runtime model calls.
- `backend/app/codex_executor.py`: backward-compatible executor name that delegates to `ModelGatewayAdapter`.
- `backend/app/result_store.py`: persistence access layer.
- `backend/app/database.py`: SQLite connection management and schema initialization.

## 前端模块

- `frontend/app/page.js`: minimal task submission, run action, result display, and task history.
- `frontend/app/globals.css`: global styles.

## Sprint 1 Visualization Boundary

- Sprint 1 visualization is a read-only observability layer over accepted v1.8 execution records.
- First slice should keep the existing compact task history plus selected task detail shape.
- Frontend may display task status/result, workflow timeline, tool trace/fallback evidence, learning evidence, meta-development report, and evolution decision evidence.
- Backend additions are limited to read-only aggregation endpoints or adapters over existing persisted records.
- Derived operating labels must come from existing task, workflow, trace, learning, meta-development, and evolution records.
- Sprint 1 must not introduce new orchestration, routing, execution, learning, meta-development, evolution-governor, persistence, or product-domain behavior.

## Sprint 2 Unified Task Console Boundary

- Sprint 2 is a frontend composition boundary over existing task creation, run, history, status, and accepted Sprint 1 selected-task detail evidence.
- First implementation slice is existing task composer, compact task history, existing run action, selected detail, and minimal review signals derived from existing state.
- Backend changes are not part of the first slice because existing APIs cover the required task, workflow, trace, meta-development, and evolution-decision records.
- Rerun, if shown, must call the existing Run API only; it is not a retry engine.
- Review signals must be derived from existing task, workflow, trace, meta-development, and evolution-decision records.
- Status filters and local presentation preferences are deferred unless they remain purely local UI state and do not create complex UI.
- Sprint 2 must not introduce new orchestration, routing, execution, learning, meta-development, evolution-governor, persistence, product-domain behavior, or unapproved read models.

## Project Memory Foundation Boundary

- Project Memory is a deterministic project-fact read model over existing source-of-truth files and execution summary memory.
- Allowed sources are `knowledge/`, `PROJECT_STATUS.md`, `TASKS.md`, `docs/decisions/`, `issues/`, `reviews/`, and existing execution summary memory from Result Store.
- Project Memory may structure and summarize facts with source references, but it does not own or replace the source-of-truth files.
- First implementation should be documentation-backed or a local deterministic helper unless a separate read-model gap is approved.
- Project Memory must not introduce backend persistence, vector database, embeddings, external memory service, agent memory, Employee memory, multi-agent coordination, L5 company organization, L6 ROI/economy, execution behavior, or automatic evolution behavior.
- Refresh may happen after issue completion, quality verification, product acceptance, or sprint status changes, but refresh output must be deterministic and reviewable.

## Sprint 3 Lightweight Role Boundary

- Sprint 3 lightweight roles are deterministic source-controlled execution guidance profiles.
- A role profile may include role intent, responsibility boundary, minimal context references, expected output shape, escalation triggers, and source references.
- The first implementation should define role profiles only.
- Role profiles may reference Project Memory to reduce repeated context, but they must not replace Project Memory or other source-of-truth files.
- Runtime prompt integration, task evidence attachment, task records, UI, backend metadata, and persistence are deferred unless a separate approved issue documents the gap.
- Sprint 3 must not introduce Employee CRUD, employee expansion, company organization, departments, reporting lines, staffing, multi-agent routing, agent abstraction, ROI/economy, role dashboard, backend persistence, external services, new execution behavior, or automatic evolution behavior.

## Sprint 3 Role Context Runtime Reference Boundary

- Runtime prompt integration remains blocked. — **Superseded in scope by ADR-0018** for ADR-0016 Sub-decision A (Runtime Role Wiring) only; all other constraints in this section (line 115–121) remain in force.
- A future role-context runtime reference may only be read-only prompt/context guidance from a stable profile id in `knowledge/ROLE_PROFILES.md`.
- The first future runtime slice should use an explicit issue-declared profile id, not an implicit default profile.
- If no profile id is declared, runtime must proceed without role context unless a separate product decision approves defaulting.
- Role context must not select tools, route work, create or select agents, mutate workflows, change task state, trigger tasks, alter learning/meta/evolution behavior, change API semantics, or change storage behavior.
- No task evidence attachment, UI selector/dashboard, backend metadata, persistence, new tables, or task-role association is approved.
- Future runtime implementation requires a separate approved issue with deterministic lookup, compact context excerpt, context-size reduction, fallback behavior, and forbidden-scope scan evidence.
- First implementation slice `backend/app/role_context.py` is a read-only helper for explicit profile id `curis.role.system-delivery.v1`; it is not wired into APIs, prompt execution, task evidence, persistence, routing, workflow generation, task state, learning, meta-development, evolution governor, or storage behavior.

## Sprint 4 Multi-Entry And Advanced UI Boundary

- Sprint 4 is a bounded operational UI composition layer inside the existing AI Task Executor product shell.
- Multi-entry means multiple UI affordances for the same existing task workflow, not new task semantics.
- Future UI may improve task composer ergonomics, compact task-entry affordances, selected-task detail navigation, status visibility, and review-signal clarity using existing data.
- First implementation should be frontend-only unless a separate approved API or read-model gap exists.
- First implementation slice adds local task-entry starters that prefill ordinary composer content only and submit through the existing Task API payload `{ content }`.
- Sprint 4 must not add external entry channels, complex UI, dashboards, business modules, ROI/economy behavior, Employee CRUD, company organization, multi-agent routing, agent abstraction, new execution behavior, API semantic changes, persistence, task-role association, task evidence attachment, or automatic evolution behavior.
- Runtime prompt integration remains limited to separately approved role-context helper behavior and must not be expanded by Sprint 4 UI work.

## AI Task Executor MVP Readiness Review Boundary

- MVP readiness review is gate-only planning and gap classification over existing accepted AI Task Executor MVP capabilities.
- The review may inspect task entry, run action, task history, selected detail, execution evidence, Project Memory, role guidance, Sprint 4 entry affordances, source-of-truth alignment, and verification coverage.
- The review may classify gaps as blocker, stabilization, verification, documentation, or future product scope.
- The review must not implement features, change APIs, add persistence, change execution behavior, add task types, add task-role association, attach task evidence, expand runtime prompt integration, add complex UI/dashboard, or expand into future L5/L6 scope.
- Any follow-up implementation requires a separately approved issue after classification and routing.

## AI Task Executor MVP Release-Candidate Boundary

- Release-candidate work is stabilization, verification command standardization, startup/deployment documentation, release checklist, rollback notes, local/demo deployment instructions, and regression verification planning only.
- The release-candidate baseline preserves the Chinese operation console, Task API payload `{ content }`, accepted readiness review, Project Memory, Role Profiles, Role Context, Sprint 4 frontend-only boundary, and Tool System v1.8 loop.
- Release-candidate planning may define exact stabilization/documentation outputs but must not implement them until a separate issue is approved.
- Release-candidate work must not add new product features, change backend/frontend behavior, change API semantics, add persistence, add execution behavior, introduce external services/channels, create complex dashboard UI, or expand into future L5/L6 scope.

## Workspace Model Gateway Adapter Boundary

- Default AI Task Executor model calls route through `ModelGatewayAdapter`.
- The first gateway surface is New API's OpenAI-compatible `/v1/chat/completions` API.
- Gateway configuration is environment-based and must not persist credentials.
- Default runtime tool selection uses provider-neutral `model_gateway_tool`; legacy provider-named tools remain compatibility labels for existing tests and historical routing behavior only.
- UsageEvent payloads for task execution include `tenant_id`, `task_id`, `model_gateway_id`, `model_name`, `token`, `estimated_cost`, and `status`.
- This boundary must not add Admin Platform pages, billing, ROI, tenant packages, platform governance, marketplace, private credential storage, connector credentials, or provider-specific direct model calls.

## Workspace Official Model Catalog Boundary

- `GET /api/catalog/models` exposes active `source=official` model catalog metadata to Workspace.
- The catalog stores shape metadata only: `provider_id`, `display_name`, `supported_models`, `auth_type`, `source`, `gateway_ref`, and `status`.
- The catalog must not store API keys, secrets, passwords, gateway tokens, or provider credentials.
- The first seed row represents the configured New API gateway model for local/demo continuity until Admin Platform model CRUD is separately delivered.
- Admin writes, model enable/disable management, marketplace, tenant-private models, billing, ROI, and governance remain out of this Workspace slice.

## Workspace Official Tool Catalog Boundary

- `GET /api/catalog/tools` exposes active official tool metadata to Workspace.
- The catalog projects existing `tools` registry rows as `source=official` and `status=active`.
- The endpoint is read-only and must not mutate tool registry rows or execution routing behavior.
- The catalog must not expose API keys, secrets, passwords, connector credentials, marketplace tools, or tenant-private tool credentials.
- Admin writes, official tool CRUD, marketplace, tenant-private tools, billing, ROI, and governance remain out of this Workspace slice.

## Workspace Tenant Model Preference Foundation Boundary

- Tenant model preference is a metadata-only Workspace state over active `source=official` model catalog entries.
- Admin Platform remains the owner of official model and gateway metadata; Workspace may store only tenant default-model references derived from that approved metadata.
- First implementation should be backend-only and may expose tenant-scoped preference read/write APIs plus deterministic runtime preference resolution.
- Allowed persisted fields are limited to `tenant_id`, `model_key`, `gateway_ref`, `model_name`, `source`, and `updated_at`; no credential values or secret-bearing references are approved.
- Runtime resolution must revalidate the stored preference against active official catalog metadata before use.
- Runtime model execution must remain constrained to `ModelGatewayAdapter`; the preference layer may choose adapter metadata but must not call New API directly, call provider SDKs, add provider-specific execution paths, mutate tool routing, or change the Tool System v1.8 loop.
- Admin UI, Workspace complex UI, billing, ROI, tenant package, secret storage, provider SDK, New API source changes, New API internal DB dependency, marketplace, automatic model optimization, per-department/per-employee model policy, credential persistence/exposure, direct provider calls, and execution path drift remain blocked.

## Workspace Company Foundation Boundary

- Workspace Company Foundation is a bounded local/demo company shell over accepted Workspace state, not a full L5 organization system.
- The foundation may frame tenant/workspace context, minimal company identity, existing department catalog/types and department instances, accepted model preference, accepted task console state, Project Memory references, and local/demo release status.
- It must not add Employee CRUD, employee expansion, staffing, permissions, reporting lines, org charts, complex company organization, business modules, ROI/economy, billing, packages, marketplace, hosted production, Admin Platform implementation, secret handling, provider SDK/direct provider calls, New API internal dependency, Task API payload changes, tool routing changes, workflow mutation, execution-loop changes, runtime behavior changes, or automatic evolution behavior changes.
- First implementation must be separately approved and should remain a minimal local/demo Workspace company frame. If company identity or department summaries require a new backend read model, 系统交付席 must document the read-model gap and route back for approval before implementation.

## 持久化

SQLite stores:

- tasks
- tools
- executions
- tool traces
- workflows
- auto workflows
- workflow traces
- execution patterns
- failure logs
- tool performance
- workflow metrics
- execution scores
- development strategies
- system evolution log
- meta development records
- evolution decisions
- architecture locks
- evolution simulations
- rollback records

## 架构边界

- No ROI system in current AI Task Executor MVP.
- No Employee CRUD or employee expansion in current AI Task Executor MVP.
- No multi-agent system in current AI Task Executor MVP.
- No business modules in current AI Task Executor MVP.
- No agent abstraction layer in current AI Task Executor MVP.
- No complex UI or advanced dashboard customization in current AI Task Executor MVP.
- No simulation mode or mock data.
- No uncontrolled architecture changes.
- No automatic code self-modification without approval.

## Architecture Decision Records

- `docs/decisions/ADR-0002-sprint-1-company-visualization-architecture-boundaries.md`
- `docs/decisions/ADR-0003-sprint-2-unified-task-console-architecture-boundaries.md`
- `docs/decisions/ADR-0004-project-memory-foundation-architecture-boundaries.md`
- `docs/decisions/ADR-0005-sprint-3-lightweight-role-responsibility-boundaries.md`
- `docs/decisions/ADR-0006-role-context-runtime-reference-boundaries.md`
- `docs/decisions/ADR-0007-sprint-4-multi-entry-advanced-ui-boundaries.md`
- `docs/decisions/ADR-0008-ai-task-executor-mvp-readiness-boundaries.md`
- `docs/decisions/ADR-0009-ai-task-executor-mvp-release-candidate-boundaries.md`
- `docs/decisions/ADR-0031-workspace-company-foundation-boundaries.md`
