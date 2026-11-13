# Project Runtime Page

## Objective

让用户从 Project 视角提交目标、查看计划和运行状态、启动运行、处理待决策，并查看成果；Task、DAG、能力降级只作为运行证据，不再作为首页产品入口。

## Scope

- 新增或复用一个 Project Runtime 路由：`/projects/{project_id}`。
- 复用现有 Project、`/api/pipeline/*`、现有结果/trace 数据；仅在确有必要时增加一个薄的 Project Runtime 后端聚合/映射，优先复用 `projects.progress_json`，不得新建通用任务平台或第二套状态机。
- 页面只提供：目标输入、计划/DAG、启动/继续、待决策 approve/reject/rework、状态/降级链/成果（diff、测试、返工原因）查看。
- 页面必须有加载、空、失败、无可操作动作四种明确状态；操作反馈可恢复，不能把失败显示为完成。

## Product Rules

- 用户第一层只看到 Company / Project / 目标 / 运行；Task ID、节点 ID、能力路由只在“运行证据”内渐进展开。
- 每页仅一个主动作：pending 时“启动运行”；review 时“处理决策”；终态时“查看成果”。
- 使用现有 Next.js/Tailwind 和现有 API；不新增依赖，不重做全站，不做视觉方案探索。
- 运行页必须深链接到具体 `project_id`，刷新后仍能恢复该项目的可读状态；若底层 Pipeline 仅为进程态，页面必须明确显示而非伪造持久化。

## Non-goals

- 不启用模型、密钥、外网、Billing、Tenant、Marketplace、Secret Vault 或外部 Agent。
- 不重做 CEO Office、组织管理、员工配置、平台 Admin 或现有任务控制台。
- 不要求真实模型成功作为本 Issue 的完成条件。

## Acceptance

1. 用户能打开一个 Project Runtime URL，看到项目目标、当前运行状态和最近一次运行证据。
2. 用户可从页面提交目标并得到计划/DAG；可启动/继续当前运行；当状态允许时可 approve/reject/rework。
3. 运行中和终态均显示：状态、节点进度、降级/trace、测试/结果/返工信息；缺失数据以空态呈现。
4. 页面不直接暴露任务编辑器、员工能力/模型/私有能力配置作为主流程。
5. 系统交付只做 focused tests；质量运行席独立完成一次 API + 浏览器验收和一次全量回归，记录 Review。

## Browser Gate

浏览器验收是**硬门槛**：质量席在本地 URL 预检中最多等待 60 秒。权限弹窗、`networkidle` 超时、无响应或客户端拦截时立即停止浏览器步骤，标记 `PLATFORM_BLOCKED` 并提交停点汇报；不得用 API/测试证据替代“用户能看到并操作页面”的验收。

## Full Regression Attribution

全量回归出现的 11 项失败只做一次归因：在 `9165f41f^`（`d47cac5b`）的临时干净 worktree 复跑同一批失败测试，主工作树不动。

- 结果相同：记录为既有失败，本 Issue 状态为 `PASS_WITH_EXISTING_FAILURES`。
- 结果不同：仅修复由本 Issue 新增的回归，再由质量席复跑。
- 不修未知失败，不扩大本 Issue。

## Route

单主执行线程：系统交付席连续完成最小实现、focused 验证和本地修复；质量运行席只在里程碑/最终做独立验收。安全边界不介入，除非范围触及密钥、外网、跨租户、隐私或不可逆数据。

## Closure

- Status: `CLOSED — PASS_WITH_EXISTING_FAILURES`。
- Delivery SHA: `9165f41f`。
- Quality: API focused 45 passed、前端 view-model 3 passed、浏览器硬门槛 PASS；全量 `1065 passed / 11 failed / 2 skipped`。
- Attribution: 父 SHA `d47cac5b` 的临时干净 worktree 定向复跑确认 11 项失败均非本 Issue 引入；不修未知/并行失败，不扩大页面范围。详见 `reviews/20260722_project_runtime_page_review.md`。

## Local Operability Boundary

- Status: `BLOCKED_L2`（不改变本页交付验收结论）。
- 当前本地运行中，Gateway 对 Project API 强制 JWT；前端未具备已批准的可信 token 获取/交换路径，因此真实提交、启动与决策请求 fail-closed。
- 总控已关闭临时实现路径：禁止 BFF 自签、默认 token、伪造身份 Header、磁盘私钥、直连 8002 或关闭 Gateway。真正可操作性待产品级可信 OIDC/issuer 入口作为独立范围处理。
