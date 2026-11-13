# MVP Phase 1 / S1 — App Shell 与 Terra Design System

Status: CLOSED — PASS

Owner seat: 系统交付席

Approval date: 2026-07-29

Expected review: `reviews/20260729_mvp_phase1_s1_app_shell_design_system_review.md`

## Objective

按 Curis v1.0 的既定信息架构与 UI 规范完成：

- T001：确认并收口现有 App Shell（Sidebar / TopBar / Main / AI Assistant Layer）。
- T002：复用现有 Terra 体系，补齐当前明确缺失的 Modal / Table / Input / Drawer 与 ProjectCard / EmployeeCard / CapabilityCard。

## Constraints

- 不重新设计导航、页面或产品流程。
- 不新增依赖、状态框架、第二套 Design System 或第二套前端。
- 已存在且符合规范的 Shell 直接复用，不重写。
- 组件使用真实字段与明确空状态，不引入 Mock 业务数据。
- 本 Issue 不修改后端、API、数据库或持久化。

## Required Context

- `docs/curis-takeover/01-Documentation-Index.md`
- `docs/curis-takeover/03-Migration-Plan.md`
- `docs/curis-takeover/04-MVP-Execution-Plan.md`
- Curis Dev Spec 46 / 47 / 48 / 60
- Curis Product Bible 24 / 25 / 26 / 27 / 28
- Curis Official 09 的前端章节

## Allowed Files

- `issues/20260729_mvp_phase1_s1_app_shell_design_system.md`
- `reviews/20260729_mvp_phase1_s1_app_shell_design_system_review.md`
- `frontend/components/terra/**`
- `frontend/app/ceo-office/organization/employees/**`
- `frontend/app/ceo-office/capabilities/**`
- `frontend/app/globals.css`
- `knowledge/NOW.md`
- `knowledge/CURRENT_CONTEXT.md`
- `PROJECT_STATUS.md`
- `TASKS.md`

## Acceptance

1. Shell 的 Sidebar / TopBar / Main / AI Assistant Layer 均由现有单一 Terra Shell 提供，页面不再各自复制壳层。
2. Modal / Table / Input / Drawer 具备键盘、焦点、标签、空状态和移动端基本可用性。
3. ProjectCard / EmployeeCard / CapabilityCard 仅展示传入事实；缺失值使用统一 `未记录/未分配` 口径。
4. 至少一个真实组织或能力页面使用新增原语，证明组件不是死代码。
5. Frontend lint/build 通过；浏览器验证 Desktop 与 Mobile 下导航及采用页面可达。
6. 不新增包，不修改 API，不引入 Mock 经营数据。

## Verification

```bash
pnpm --dir frontend lint
pnpm --dir frontend build
git diff --check
```

Browser hard gate: yes.
