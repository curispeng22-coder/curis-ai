# MVP Phase 3 / S4 — Project Review

Date: 2026-07-29

Status: PASS

Issue: `issues/20260729_mvp_phase3_s4_project.md`

## Conclusion

T009 / T010 的真实项目创建、项目中心分组与统一项目工作台均通过，本 Issue 关闭。

## Implemented

- 从真实 Company、Department 和 AI Employee 创建项目，保存名称、目标、说明、部门、负责人和状态。
- 创建成功后直接进入真实项目工作台；项目中心按真实部门分组展示。
- 项目卡片与工作台不再展示示例项目、本地草稿、模拟进度、硬编码部门或团队。
- 工作台提供概览、任务、资料、成果和数据五个视图。
- 任务视图读取当前项目真实 Task；资料、成果和经营数据没有独立持久化事实时保持明确空状态。
- 未新增依赖、数据库表、Workspace/Admin、第二套项目服务或 affiliation 依赖。

## Passed Evidence

- `.venv/bin/python -m unittest discover -s tests -p 'test_mvp_phase3_s4_project.py'`：2 passed。
- `pnpm lint`：PASS。
- `pnpm build`：PASS，26 个静态页面生成成功。
- `git diff --check`：PASS。
- Desktop browser（隔离临时库）：
  - 从真实研发部与“技术负责人”创建“Curis MVP 交付”；
  - 项目目标、说明、部门、负责人和规划中状态写入并显示；
  - 创建后自动进入项目工作台；
  - 概览、任务、资料、成果、数据五个视图均可切换；
  - 项目中心同步显示研发部 1 个真实项目；
  - 注入一条真实 Project Task 后，任务视图显示真实内容、执行者和 `INIT` 状态。
- Mobile browser（390×844）：
  - 项目中心和项目工作台均为 `scrollWidth = clientWidth = 390`；
  - 项目卡片、创建入口、搜索入口与五个工作台视图可见。

## Full Regression

在 `1dd5b0b3` 干净提交树应用本 Issue 暂存差异后执行：

```bash
backend/.venv/bin/python -m pytest -q backend/tests
```

结果：`1116 passed, 3 skipped, 0 failed`。

## Boundaries

- S4 仅包含 T009 / T010。
- T011 任务管理与 T012 异步执行记录属于 S5，未在本 Issue 提前实现。
- Artifact、Knowledge、Memory、Business Template 自动生成和经营指标保持后续 Sprint 边界。

Handoff: sent to main thread
