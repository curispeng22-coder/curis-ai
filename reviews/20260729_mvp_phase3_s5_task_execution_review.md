# MVP Phase 3 / S5 — Task 与异步执行记录 Review

Date: 2026-07-29

Status: PASS

Issue: `issues/20260729_mvp_phase3_s5_task_execution.md`

## Conclusion

T011 / T012 的真实项目 Task 创建、AI Employee 指派、非阻塞启动与状态查询闭环通过，本 Issue 关闭。

## Implemented

- 用户可在真实 Project Workspace 创建 Task，并指定当前公司已启用 AI Employee。
- Task 继续使用既有 `tasks` / `executions`、ResultStore 和 Orchestrator，不新增表、依赖或第二套执行服务。
- 启动接口立即返回 `202`；`job_id` 复用持久化且租户隔离的 `task_id`。
- 既有状态机映射为 queued / running / completed / failed；后台执行显式恢复租户与身份上下文。
- Project Workspace 支持创建、执行、轮询和重试；执行工作台与 Task 详情全部改读真实 API。
- 无执行事实时结果、能力和成本保持 `未记录`；失败显示持久化真实原因。

## Passed Evidence

- `backend/.venv/bin/python -m pytest -q backend/tests/test_mvp_phase3_s5_task_execution.py`：2 passed。
- `npm run lint`：PASS。
- `npm run build`：PASS，26 个静态页面生成成功。
- `git diff --check`：PASS。
- Desktop browser（隔离临时库）：
  - 在“S5 任务执行验收”真实项目中创建“生成一份 S5 浏览器验收任务清单”；
  - Task 持久化项目与“S5 执行员工”，项目任务数由 0 更新为 1；
  - 点击执行后先显示“排队中”，确认 `202 + job_id` 非阻塞契约；
  - 无模型网关配置时状态转为“失败”，项目页和详情页均显示真实配置错误；
  - 详情页展示 INIT → PENDING → PARSED → RUNNING → FAILED 状态流，成本保持“未记录”；
  - 执行工作台聚合该真实 Task、项目、员工和失败状态。
- Mobile browser（390×844）：项目工作台标题、事实卡、五个视图和团队信息在单列布局中可读，无可见横向溢出。

## Full Regression

在 `b061bedc` 干净提交树应用本 Issue 暂存差异后执行：

```bash
backend/.venv/bin/python -m pytest -q backend/tests
```

结果：`1119 passed, 2 skipped, 0 failed`。

## Boundaries

- 浏览器验收环境未注入外部模型网关凭证，因此验证的是受控真实失败；成功执行路径由聚焦测试的真实 Orchestrator + 记录型执行器覆盖。
- 未新增暂停/恢复、自动拆解、定时任务、自适应执行、Artifact/Knowledge、外部凭证或持久队列。
- S6 仅按独立 Issue 进入 Capability Registry T013 / T014。

Handoff: sent to main thread
