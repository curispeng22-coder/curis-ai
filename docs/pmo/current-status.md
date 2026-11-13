# Curis Seat Status

Status: Deprecated

Updated: 2026-07-23 (项目负责人工作台第一纵向切片 PASS)

## Current Work

- 最近完成：项目负责人工作台第一纵向切片。
- 收口 Issue：`issues/20260723_project_owner_workbench_product_flow.md`，状态 `CLOSED — PASS / USER_FLOW_PASS`。
- 验收：`9165f41f`，API 45 passed、前端 3 passed、浏览器硬门槛 PASS；全量 `1065 passed / 11 failed / 2 skipped`，父 SHA 定向归因确认非本 Issue 引入。
- 当前产品主目标：无活动实施 Issue。
- 本地可操作性：`PASS / LOCAL_ONLY`。用户可通过本机 Google 登录进入项目负责人工作台，使用聊天式目标或结构化任务入口，看到同一结构化确认单，确认生成计划，启动运行，查看结果解释，批准成果并继续修改目标。
- 验收证据：SHA `b349b4367e2002f3702ffd788162c477015a2c4f`，独立 Chrome 真链完成，`7 passed` / `exit0` / `round1`，trace `local.project_runtime.focused success`。Task `task-5506d18e` / Graph `graph-6396d4a85b2e` 仅在折叠证据区；成本未知显示“未记录”，员工未分配如实显示。
- 外部配置：Google OAuth Client 已创建，`CLIENT_CREATED_SECRET_NOT_INJECTED`；仅在实施完成后回传一条隐藏输入命令与成功标志。
- 工作方式：系统交付单主线程连续实现；质量仅最终独立验收；无敏感边界变化不新增 Gate。

## 不再使用的手势

- ❌ D1 E2E BLOCKED_L2 — 已不适用。研发闭环已跑通，不再受 D1 冻结约束。
- ❌ PAUSED_FOR_QUOTA_HANDOFF — 额度切换已结束，当前无阻塞。

## Seat Task IDs

| Seat | Task ID |
| --- | --- |
| 总控决策席 | `019f6c51-6fc8-7642-927b-bd4f15828669` |
| 产品规划席 | `019f4d17-fca0-71a2-aff3-ec965e1e695b` |
| 系统交付席 | `019f6c48-8999-7ac1-aade-119ac71b483d` |
| 质量运行席 | `019f6cb7-3e8d-7313-91d9-95b226c9ed2e` |
| 安全边界席 | `019f6c48-bca4-7be3-8ff0-dccaf3ea5b93` |

## Route

`产品规划席 -> 系统交付席 -> 质量运行席 -> 产品规划席 -> main thread`
