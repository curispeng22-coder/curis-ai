# MVP Phase 6 / S12 — 体验优化与最终收敛

Status: CLOSED — PASS

Owner seat: 系统交付席

Approval date: 2026-07-29

Expected review: `reviews/20260729_mvp_phase6_s12_experience_convergence_review.md`

## Objective

按接管 Migration Plan M5 与 MVP Execution Plan S12 完成 Curis v1.0 MVP 收尾：统一错误/加载体验，验证核心浏览器闭环稳定可用，迁移仍需保留的旧库数据后清理旧数据库与旧目录。

## Product Boundary

- 不重新设计产品，不改变 Curis v1.0 架构，不新建 Workspace/Admin。
- 只修复最终 MVP 主路径中经验证存在的体验、稳定性或错误处理缺口；不新增功能、状态管理框架或依赖。
- `frontend/`、`data/curis.sqlite` 与现有启动链保持唯一入口。
- 旧数据库先做只读审计、可恢复备份和幂等迁移；迁移及完整性验证通过后才清理。
- 核心对象保留并按主库现有 schema 合并；主库已有同 ID 记录优先，不覆盖当前数据。
- 历史/重复数据库文件不进入默认运行链；清理必须可恢复并记录精确目标。
- 不触碰当前 Issue 之外的实验代码或用户未提交改动。

## Tasks

- T026：补齐唯一 App 的统一加载与未捕获错误恢复界面，复用 Terra 视觉语言。
- T027：验证并修复核心 MVP 浏览器链路中的实际稳定性、错误态与响应式缺口。
- T028：提供并验证旧 SQLite 幂等迁移工具，备份主库，迁移缺失核心记录并运行完整性检查。
- T029：清理根 `curis.sqlite`、`data/admin.sqlite`、`data/workspace.sqlite` 与 `.pre-split` 历史库；确认旧前端/旧目录和运行引用为零。
- T030：执行聚焦测试、完整回归、Frontend lint/build、唯一启动链和 Desktop/Mobile 最终浏览器验收。

## Allowed Files

- `issues/20260729_mvp_phase6_s12_experience_convergence.md`
- `reviews/20260729_mvp_phase6_s12_experience_convergence_review.md`
- `frontend/app/error.js`
- `frontend/app/loading.js`
- `frontend/app/ceo-office/execution/tasks/[id]/page.js`
- `frontend/app/ceo-office/execution/page.js`
- `frontend/app/ceo-office/organization/departments/[id]/page.js`
- `frontend/app/ceo-office/projects/[id]/TaskFormDrawer.js`
- `frontend/app/ceo-office/projects/[id]/page.js`
- `frontend/tests/mvp-s12-experience.test.mjs`
- `tools/migrations/converge_legacy_sqlite.py`
- `backend/app/identity_membership.py`
- `backend/app/orchestrator.py`
- `backend/tests/test_mvp_phase6_s12_legacy_convergence.py`
- `backend/tests/test_mvp_phase6_s12_runtime_stability.py`
- `backend/tests/test_workspace_startup_entry.py`
- `deploy/curis/release-checklist.md`
- `deploy/curis/rollback-local.sh`
- `deploy/curis/start-local.sh`
- `deploy/curis/admin.env.example`（删除）
- `deploy/curis/run-admin-backend.sh`（删除）
- `curis.sqlite`（删除）
- `data/admin.sqlite`（迁移后清理）
- `data/workspace.sqlite`（迁移后清理）
- `data/*.pre-split` / `data/*.pre-r2-orphan`（迁移后清理）
- `knowledge/NOW.md`
- `knowledge/CURRENT_CONTEXT.md`
- `PROJECT_STATUS.md`
- `TASKS.md`

## Acceptance

1. 唯一 App 在加载和未捕获异常时展示统一、可恢复、无虚假事实的界面。
2. `创建公司 → 部门 → 员工 → 项目 → 配置能力 → 执行业务 → 获得成果 → 沉淀经验 → 下一任务复用` 可由真实用户在浏览器完成。
3. 核心页面错误时保留可理解原因和重试路径；Desktop/Mobile 无横向溢出。
4. 迁移工具只接受明确旧库与主库路径，迁移前备份主库，事务失败完整回滚，重复执行不产生重复数据。
5. 旧库中需保留且主库缺失的核心对象迁入 `data/curis.sqlite`；主库现有记录不被覆盖；SQLite `integrity_check` 与 `foreign_key_check` 通过。
6. 根旧库、Admin/Workspace 旧库、`.pre-split`/`.pre-r2-orphan` 与旧前端源码清理完成，默认启动/CI/发布无残留引用。
7. `data/curis.sqlite` 仍是唯一活动主库；实验服务仍不进入默认启动链。
8. 不新增依赖、产品入口、Workspace/Admin、自动架构或无证据优化。
9. 聚焦测试、Frontend lint/build、完整后端回归、启动检查与 Desktop/Mobile 浏览器 E2E 通过。
