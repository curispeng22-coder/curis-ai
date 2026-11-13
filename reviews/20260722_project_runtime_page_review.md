# Project Runtime Page 质量 Review

- Issue：`issues/20260722_project_runtime_page.md`
- 交付 SHA：`9165f41fb80cf125c8e06a701d258a9b6454e4ff`
- 质量结论：`PASS_WITH_EXISTING_FAILURES`
- 功能里程碑：`API_PASS / BROWSER_PASS`

## 独立证据

### 范围

- `git show 9165f41f` 仅含薄聚合 API、Scheduler 回调透传、Project Runtime 页面/视图模型/测试和 Issue，共 7 文件；未新增依赖。
- 当前 HEAD 精确为交付 SHA；工作区另有既存脏改动，未归入本 Issue。

### API 与前端聚焦

- `cd backend && ../backend/.venv/bin/python -m pytest -q tests/test_project_runtime_page.py tests/test_issue_pipeline.py`：`45 passed`。
- 覆盖 Project→Task/Graph 关联、`progress_json` 来源快照、进程态丢失不伪造进度、auto-run→review→approve、重复活跃运行 409，以及 Project/Task/Graph 跨租户 404。
- `node frontend-workspace/app/projects/[project_id]/projectRuntimeViewModel.test.mjs`：`3 passed`。
- 目标页面与视图模型 ESLint：PASS。
- 隔离本地 API 实证：提交后返回 `pending`、2 节点、0%、`available_actions=["auto_run"]`；服务重启后返回 `graph.available=false`、`progress=null`、两节点 `unknown`、`available_actions=[]`、`blocked_reason=pipeline_process_state_unavailable`。

### 浏览器

- 本地深链 `/projects/project-2c38dcd5-e871-48b7-8e56-4efb3bdd343c` 可打开，空态显示项目目标、空计划、空成果和“生成计划”。
- 通过页面提交目标后，显示成功反馈、2 节点 DAG、0% 真实进度、唯一主动作“启动运行”，Task/Graph 仅位于运行证据区。
- 重启后刷新同一深链，页面明确显示“当前无可执行动作”“计划快照仍在但节点运行态无法恢复”“不会显示推测进度”，节点均为“状态不可恢复”。
- 总控已撤销临时 `PLATFORM_BLOCKED` 判断；浏览器证据有效，未重开、未等待弹窗、未使用 `networkidle`，本项不构成阻塞。

### 一次全量回归

- 正确工作区根目录命令：`backend/.venv/bin/python -m pytest -q backend/tests`。
- 结果：`1065 passed / 11 failed / 2 skipped`，耗时 `135.81s`。
- 11 项失败分属：Budget/B-layer 顶层导入守卫 2、CEO evidence 并行脏改动 4、既有 PipelineRuntime fake resolver 接口漂移 4、MCP stdio 权限 1。
- Project Runtime 新增测试全部通过；11 项均不位于 `9165f41f` 的实现文件。
- 首次从 `backend/` 直接运行时因 4 个现有测试使用 `backend.*` 导入而在收集阶段退出；随后按当前根目录导入约定完成上述唯一有效全量，保留该命令归因但不计为产品失败。

### 父 SHA 归因

- 在父 SHA `d47cac5b58540252518a1502d935da3afa4aaaad` 的 detached 干净 worktree，仅复跑上述 11 个失败 node ID；其中 8 项存在，结果为 `3 passed / 5 failed`。
- 5 项复现失败与当前全量相同：4 个 PipelineRuntime fake resolver 不接受 `employee_id` 的 `TypeError`，以及 1 个 MCP stdio `PermissionError`，确认属于既有失败。
- 父 SHA 通过的 3 项为 2 个 `budget_guard` 与 1 个 `ceo_evidence` 顶层导入守卫；另 3 个 `ceo_runtime_evidence` node ID 在父 SHA 不存在，当前对应实现/测试文件为并行 untracked 工作。
- `d47cac5b..9165f41f` 对上述实现与测试路径 `diff=0`，因此未复现/新增节点均不是本 Issue 引入的回归。临时 worktree 已移除，主工作树未因归因复跑而改动。

## 结论

Project Runtime 的薄聚合 API、租户边界、深链页面、空/失败/无动作态、目标→计划及进程态降级里程碑均通过；浏览器不是阻塞。全量 11 项失败已通过父 SHA 定向复跑确认不由本 Issue 引入，故本 Issue 按 `PASS_WITH_EXISTING_FAILURES` 交产品规划席验收；不修复这 11 项，不扩大页面 Issue，不重放历史 sentinel。

Next Seat：产品规划席

Handoff: sent to 产品规划席
