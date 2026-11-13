# MVP Phase 6 / S11 — 基础 Memory 与 Context Package

Status: CLOSED — PASS

Owner seat: 系统交付席

Approval date: 2026-07-29

Expected review: `reviews/20260729_mvp_phase6_s11_basic_memory_context_review.md`

## Objective

按 Curis v1.0 既定边界完成“任务执行 → 用户确认沉淀经验 → 下一任务自动检索相关 Memory/Knowledge → 生成并实际使用 Context Package”的真实闭环。

## Product Boundary

- Memory 是 Curis 工作中形成的长期经验；Knowledge 是外部资料，二者不得混用。
- MVP 只实现用户 Memory、项目 Memory、员工基础 Memory；保留 Dev Spec 17 的分级语义。
- Memory 写入必须由用户明确确认；不自动总结执行结果，不实现自动进化、冲突裁决或 Knowledge Graph。
- Context Package 只包含当前 Task Goal、相关 Memory、相关 Knowledge、所需能力、约束和输出要求；不得加载整个历史。
- Context Package 在 Task 执行前生成、持久化并进入真实 Prompt；无相关资料时保持真实空列表，不伪造上下文。
- 不新增 Workspace/Admin、会议室运行时、向量数据库、Embedding、云服务、凭证或外部依赖。
- 所有读写保持 tenant、用户、项目和员工对象隔离。

## Implementation

- 新增标准 MemoryEntry 与 ContextPackage 持久化。
- 新增用户/项目/员工 Memory 的创建、读取、更新、检索 API。
- 新增 Context Engine：以当前 Task、Project、Employee 为范围做基础相关性检索并构建可追溯 Context Package。
- 将 Context Package 接入现有 Orchestrator Prompt，不创建第二套执行链。
- 新增 Memory 管理入口；Task 详情支持从终态执行结果确认沉淀经验，并展示本次执行使用的 Context Package。

## Allowed Files

- `issues/20260729_mvp_phase6_s11_basic_memory_context.md`
- `reviews/20260729_mvp_phase6_s11_basic_memory_context_review.md`
- `backend/app/database.py`
- `backend/app/main.py`
- `backend/app/memory_api.py`
- `backend/app/memory_service.py`
- `backend/app/context_service.py`
- `backend/app/orchestrator.py`
- `backend/app/prompt_builder.py`
- `backend/app/task_jobs.py`
- `backend/tests/test_mvp_phase6_s11_basic_memory_context.py`
- `frontend/components/terra/TerraNavData.js`
- `frontend/lib/memory.js`
- `frontend/app/ceo-office/knowledge/memory/page.js`
- `frontend/app/ceo-office/execution/tasks/[id]/page.js`
- `knowledge/NOW.md`
- `knowledge/CURRENT_CONTEXT.md`
- `PROJECT_STATUS.md`
- `TASKS.md`

## Acceptance

1. 用户可创建、查看、更新并检索用户/项目/员工 Memory；每条展示内容、来源、时间、使用次数与可信度。
2. Task 只有在 completed/failed 后才可作为 Memory 来源；来源 Task、Project、Employee 与租户必须一致。
3. 下一 Task 执行前自动生成 Context Package，优先当前 Task，再检索相关 Project Memory、Employee Memory、User Memory 与 Knowledge。
4. Context Package 真实持久化 Task Goal、Memory/Knowledge ID、所需能力、约束、输出要求、摘要和 SHA。
5. 实际执行 Prompt 包含该 Context Package；使用的 Memory 更新使用次数和最后使用时间。
6. 无 Memory/Knowledge、无项目、无员工或无能力时保持真实空列表/`未记录`，不阻断仅依赖 Task Goal 的执行。
7. 跨租户、跨用户、跨项目或跨员工的 Memory/Context 不可读取或写入。
8. 不新增依赖、Workspace/Admin、自动 Memory 进化、Knowledge Graph、Embedding、会议运行时或凭证。
9. 聚焦测试、Frontend lint/build、完整后端回归与 Desktop/Mobile 浏览器 E2E 通过。
