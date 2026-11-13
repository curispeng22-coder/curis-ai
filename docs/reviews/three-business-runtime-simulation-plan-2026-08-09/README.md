# 三业务 Runtime Simulation Plan（2026-08-09）

Status: Review

Decision: `AUTHORIZED_BACKEND_SIMULATION_ONLY`

本计划把当前 Product Blueprint 与 Business Runtime 定义转换为可执行的业务验证。它不授权修改业务代码，也不把静态原型、fixture 或 AI 自报结果当成通过证据。

## 1. 目标与范围

验证同一个 Company OS / CEO Assistant / AI Organization / Evidence / Decision Runtime，能否同时承载：

1. 研发工作台：第一个任务“Curis 的自研发”（工作项名：完善 Curis）；
2. 小红书运营工作台：内容生产、授权发布、互动和结果反馈；
3. 抖音 / TikTok 运营工作台：视频生产、授权发布、互动、成交或手动结果反馈。

三条业务必须使用不同的 Workspace Blueprint 和外部结果路径，但不得复制三套 Company OS。

## 2. 统一 Simulation 前置条件

以下前置条件适用于 Company 创建完成后的三业务与共享 Runtime Simulation；`FIRST-ARRIVAL-*` 的起点恰恰是 Company 尚未建立，使用 §4 自己的前置条件。

| 前置 | 必须具备 | 失败即停止 |
| --- | --- | --- |
| Company / CEO | 一个真实 Company、一个真实 CEO、稳定 `companyId` 与身份边界 | 读取到跨 Company 或 fixture 数据 |
| Assistant | CEO Assistant 已有身份、责任契约、升级入口和 CEO Desk 回报 | 只存在聊天框或空身份 |
| AI 组织 | 专业 Agent 有 Role Contract、容量、能力授权和交接记录 | Agent 平级、无 Owner 或越权 |
| Workspace | CEO 创建 / 确认 Workspace，Blueprint 具备 Outcome、Stage、Owner、I/O、Evidence、失败出口 | 固定业务卡片或保存表单直接变成运行空间 |
| 外部结果 | API 授权状态或 CEO 手动 Evidence 窗口，来源、新鲜度、证据等级明确 | 示例指标直接进入 Verified |
| 审计 | `actor / at / reason / state / evidence / nextCheckAt` 可持久化 | 只存在页面内存或截图 |

## 3. Simulation 记录格式

每次运行必须生成一份 `SimulationRun`，至少包含：

```text
simulationRunId
companyId / ceoId / workspaceId / blueprintVersion
scenarioId / startedAt / finishedAt
participants[] / inputRefs[] / stateTransitions[]
handoffs[] / externalReceipts[] / evidenceRefs[]
failureEvents[] / ceoDecisions[] / finalState
passStatus / reviewer / reviewedAt / reviewNotes
```

每个关键业务对象必须能反查：

```text
Content: contentId → runId → outcomeId → decisionId
Interaction: interactionId → responseVersion → externalReceipt
R&D: intentId → cycleId → commit/build/test evidence → CEO acceptance
```

## 4. First Arrival / Company Formation Simulation

首次进入不是三业务运行前的旁支，而是 CEO 公司生命周期的起点。它必须先证明 Curis 能从空公司安全地产生 Company、CEO Assistant、第一条业务和首个 Cycle 候选，再进入三业务 Simulation。

| 场景 | 起点 | 必须验证 | 终态 |
|---|---|---|---|
| FIRST-ARRIVAL-001 正常创建 | 新 CEO 打开 Curis，Company 尚未建立 | 创建向导态介绍身份；CEO 表达意图；形成可恢复 `FoundingRun`；CEO 确认 Company；持久化 `companyId`、唯一 `assistantId`、Context v1；继续配置第一业务 | `foundingRunId → companyId → assistantId → businessId → workspaceId → cycleId` 候选完整 |
| FIRST-ARRIVAL-002 中途离开 / 恢复 | CEO 在 Founding Brief 或 Company Design 中退出 | 草案、未知项、假设和下一步持久化；不创建假 Company / Assistant / Business | 原 `FoundingRun` 恢复到正确阶段 |
| FIRST-ARRIVAL-003 CEO 拒绝草案 | CEO 拒绝 Company 或第一业务提案 | 保留版本、拒绝原因和影响预览；返回 `PROPOSED` / `CLARIFYING`，不覆盖旧草案 | CEO 修改后重新确认 |
| FIRST-ARRIVAL-004 创建失败 | Company 持久化或 Assistant 初始化失败 | UI 不显示创建成功；记录错误和恢复动作；不产生孤立 Company / Assistant | `WAITING_CEO` 或可重试的失败记录 |

通过条件：Pre-company Founding Guide 只能收集意图和形成草案；只有 CEO 确认并完成持久化后才生成 `CEOAssistant`。LocalStorage、页面内存、截图或手动编辑数据库均不能替代 First Arrival 证据。

## 5. AI Organization / Capability Simulation

First Arrival 产生 Company 后，不能直接把 Workspace 标记为“团队已就绪”。组织配置必须证明 CEO 如何接受 AI 员工责任、能力授权与容量边界。

| 场景 | 起点 | 必须验证 | 终态 |
|---|---|---|---|
| ORG-001 最小团队 | First Business 已有 Outcome 与失败出口 | CEO Assistant 提出 Role Slot；CEO 接受 / 修改；创建 AIEmployee、CapabilityBinding；完成权限、容量和模拟检查 | `AIEmployee=AVAILABLE`，Workspace 可生成首个 Cycle 候选 |
| ORG-002 能力缺失 | Role Slot 没有满足输入 / 输出的能力 | `AIEmployee.lifecycleStatus=DEGRADED`、`presenceState=BLOCKED`，RoleSlot 标记阻塞；Assistant 说明缺口并提供补能力、换责或暂停 | 不得进入 Operating |
| ORG-003 容量过载 | 多个业务同时占满共享 AI / Capability | 按业务隔离队列与优先级排队；不抢占其他 Workspace；超时升级 CEO | 责任保持未完成，记录 `overdueSince` |
| ORG-004 责任退回 / 换责 | AI 员工无法在授权、能力或输入范围内完成责任 | Handoff=`RETURNED`；记录原因、已尝试范围、缺口和建议 Owner；新 Owner 接手前不显示完成 | CEO 重新分配、补能力或暂停 |
| ORG-005 能力撤权 / 版本失配 | CapabilityBinding 被撤销或版本不匹配 | 高影响动作阻断；`CapabilityBinding=REVOKED / DEGRADED`，员工进入 `lifecycleStatus=SUSPENDED`、`presenceState=BLOCKED`；回写授权版本和恢复路径 | CEO 恢复、替换能力或重新模拟 |

通过条件：Role Slot、AIEmployee 和 CapabilityBinding 可分别查询；同一员工跨 Workspace 复用时责任、容量和授权范围不混淆；组织配置变更会使受影响 Blueprint 的 Simulation 失效。

## 6. 研发工作台 Simulation

| 场景 | 起点 | 必须验证 | 终态 |
| --- | --- | --- | --- |
| RD-001 正常交付 | CEO 提出“完善 Curis”意图 | 按研发工作台 `INTAKE → DESIGN → IMPLEMENT → VERIFY → ACCEPT → REVIEW` 运行；产品 / 研发 / QA AI 形成责任，真实代码、构建、测试和 CEO 验收产生证据 | Cycle 完成；CEO 决定继续下一周期 |
| RD-002 需求不清 | CEO 意图缺少验收标准 | Assistant 先澄清并生成 Decision 草案，不直接创建无限 Task | 等待 CEO 或形成有限 Scope |
| RD-003 工程失败 | 构建或真实用户流程失败 | 运行暂停、错误与责任人可见，Assistant 升级 CEO，不能报告完成 | `PAUSED` / 修复后重新验证 |
| RD-004 CEO 拒绝 | CEO 不接受软件增量 | 保留版本、证据和拒绝原因，回到修订周期 | 新 Cycle 或关闭 |
| RD-005 结果反馈 | CEO 真实使用增量 | 使用反馈进入 Insight，并形成下一轮产品 Decision | `VERIFIED` 或 `UNKNOWN`，不得 AI 自报 |

## 7. 小红书运营工作台 Simulation

| 场景 | 起点 | 必须验证 | 终态 |
| --- | --- | --- | --- |
| XHS-001 正常闭环 | CEO 确认本周期目标 | `IDEA → DRAFT → IN_REVIEW → APPROVED → PUBLISHED → AWAITING_FEEDBACK → REVIEWED`；图文 / 轮播变体、授权、回执和结果窗口完整 | Outcome `VERIFIED` 或 CEO 明确继续 / 调整 |
| XHS-002 未授权 | 账号权限缺失 | 发布按钮禁用；Assistant 提供授权或手动发布路径；手动结果标记 `UNVERIFIED` | 不得进入 Verified 或扩大 |
| XHS-003 发布失败 | 平台返回失败 / 超时 | `ScheduledRun=FAILED`；ContentItem 保持原 `lifecycleStatus`，`exceptionStatus=FAILED`，保留版本、错误、重试和责任 | CEO 重试、改期、退回或暂停 |
| XHS-004 数据延迟 / 冲突 | API 无数据或与 CEO 手动录入冲突 | ContentItem 保持 `AWAITING_FEEDBACK`，结果 / 异常分别标记 `STALE / ABNORMAL`，显示来源和时间窗，不能触发扩大 | 补证据、采用待验证数据或暂停 |
| XHS-005 CEO 拒绝 | CEO 拒绝标题、表达或素材 | 版本回 `DRAFT`，保留意见和 `versionId`，不得覆盖历史审核 | 创作 AI 重做并重新审核 |
| XHS-006 互动线索 | 评论、私信、咨询到达 | `InteractionItem` 分类，线索 / 投诉 / 敏感事项升级；回复策略和回执可追溯 | CEO 批准、模板自动回复或升级 |

## 8. 抖音 / TikTok 运营工作台 Simulation

| 场景 | 起点 | 必须验证 | 终态 |
| --- | --- | --- | --- |
| TTK-001 正常闭环 | CEO 确认视频结果目标 | 脚本 / 分镜 / 封面 / 时长 / 钩子独立版本，授权、发布回执、播放 / 完播 / 互动 / 涨粉 / 成交结果完整 | Outcome `VERIFIED` 或 CEO 明确继续 / 调整 |
| TTK-002 未授权 | 账号或发布权限缺失 | 发布执行 AI 停止，Assistant 升级，手动发布路径保留待验证状态 | 不得把“视频已准备”说成“已发布” |
| TTK-003 视频处理 / 发布失败 | 平台处理、权限或内容检查失败 | ContentItem 保持原生命周期，`exceptionStatus=FAILED`；失败原因、原素材、版本、重试和回退路径完整 | CEO 修复、重试、改期或退回脚本 |
| TTK-004 数据 / 成交归因异常 | 数据延迟或成交口径冲突 | 结果标记 `STALE / ABNORMAL`，禁止放量和预算扩大 | 补证据、手动待验证或暂停 |
| TTK-005 CEO 拒绝 | CEO 拒绝脚本、钩子或外部承诺 | 回到 `DRAFT`，意见绑定具体视频版本 | 创作 AI 重新生成并重新审核 |
| TTK-006 互动与订单意向 | 评论、私信、订单咨询到达 | 回复策略、风险、响应版本、平台回执和下一检查点完整 | CEO 批准、模板回复或升级 |

## 9. 共享 Assistant / Studio Simulation

| 场景 | 必须验证 |
| --- | --- |
| STUDIO-001 配置变化 | 修改 Stage、Agent、Connector、Evidence Rule 后，`simulationPassed=false`，运行版本不被静默修改 |
| STUDIO-002 模拟通过 | 正常、能力缺席、工具失败、外部延迟、CEO 拒绝均有记录；未通过不能提交审批 |
| STUDIO-003 审批回退 | CEO 选择“要求修改”后回到 `BLUEPRINTING`，草案、意见和影响范围保留 |
| ASSIST-001 主动汇报 | Assistant 只在审核、授权、异常、承诺风险、跨业务影响和日末收束时主动出现，并带证据与动作 |
| ASSIST-002 跨空间交接 | Assistant 能从研发、小红书、抖音三条工作台收回结果，形成同一 CEO Desk 的排序和 Decision |
| RUNTIME-001 AI 员工责任退回 | AI 员工发现能力、授权、容量或输入不足，Handoff 进入 `RETURNED`；记录原因、缺口、尝试范围和建议 Owner；原责任不能进入完成态 |
| RUNTIME-002 超时与暂停保护 | `WAITING_CEO` 按风险等级触发 2h / 4h / 24h 提醒；暂停 7 天生成复盘事项、30 天生成归档候选；系统不得自动批准或归档 |
| RUNTIME-003 证据置信度与公司脉搏 | 同一结果显示来源组成、置信度和六维脉搏等级；缺少关键证据显示 `UNKNOWN`，不得用模型自报数字填充 |

## 10. 通过标准

三业务 Simulation 只有同时满足以下条件才算通过：

1. 每个场景都从 CEO 入口开始，经过真实 Workspace / Agent 交接，并能回到 CEO Desk；
2. 每次状态转换都有持久化 Actor、时间、原因、证据和下一检查点；
3. 所有失败、未授权、延迟、冲突和 CEO 拒绝路径都不能被成功态覆盖；
4. `VERIFIED` 只由外部回执或 CEO 真实验收产生；
5. 平台批准版本与实际发布版本不一致时必须阻断并升级；
6. 互动和线索不能绕过 ReplyPolicy 直接对外回复；
7. 三条业务共享同一 Company OS，但 Workspace 差异由 Blueprint 配置表达；
8. 运行记录可重启后恢复，并可由 `companyId / workspaceId / scenarioId` 查询；
9. Review 记录包含浏览器证据、后端 / 数据证据、失败记录和 CEO 决策记录。

## 11. 当前执行状态

| 项目 | 状态 | 说明 |
| --- | --- | --- |
| 方案与契约 | 已完成 | Product Blueprint、Business Runtime、UI Shell 已定义 |
| Review | 进行中 | 见 `reviews/20260809_runtime_simulation_001_review.md` |
| Runtime Foundation | 已通过聚焦复核 | `PASS_WITH_BASELINE_BLOCKERS`；全量基线失败保持隔离 |
| Simulation Issue | 已授权 | `issues/20260809_runtime_simulation_001.md`，仅后端临时 SQLite 运行证据 |
| Backend Runtime Simulation | 已通过 | `PASS_BACKEND_SIMULATION_WITH_BASELINE_BLOCKERS`；RD / XHS / TTK 通过，未证明真实平台发布或 UI |

## 12. 执行准备度复核（2026-08-09）

本节把“可以开始 Simulation”与“当前代码已有的可复用运行能力”分开记录。它不是把后端现状当成通过证据，而是确定下一步是否存在可执行的真实入口。

### 12.1 已存在、可复用的运行基座

当前后端已存在以下可复用基座：

| 能力 | 当前证据 | 可用于 Simulation 的范围 |
| --- | --- | --- |
| Company / Business / Workspace / Outcome | `backend/app/runtime/models.py`；`business_directions`、`commitments`、`workspaces`、`outcomes`、`attributions` 表 | 可承载业务方向、工作空间、结果和归因的基础引用；尚未承载内容对象本身 |
| Workspace 状态机 | `backend/app/runtime/registry.py`：`DRAFT → BLUEPRINTING → SIMULATED → PENDING_APPROVAL → OPERATING` | 可验证工作空间装修与审批门禁的基础流转；仍缺运行版本与 Blueprint 版本关联 |
| Cadence / ScheduledRun | `backend/app/runtime/scheduler.py`；`cadences`、`scheduled_runs` 表 | 可验证排期、队列、等待 CEO、失败和重启恢复的通用基座 |
| 研发执行链 | `backend/app/rd_workflow_runtime.py`；`workflow_runs`、`workflow_steps` | 可作为 RD-001～RD-005 的执行入口；还需绑定真实代码 / 构建 / 测试 / CEO 验收证据 |
| 内容生成与发布包 | `backend/app/content_workflow_runtime.py`、`backend/app/content_publish_package.py`；`content_workflow_runs`、`content_publish_packages` 表 | 可作为内容生成、发布包和连接器回执的旧链路；不等于 ContentItem 生命周期 |
| 状态流转审计 | `backend/app/runtime/store.py`；`runtime_transition_log` 表 | 可复用 actor、时间、原因、上下文留痕；尚未形成 SimulationRun 的完整聚合记录 |

### 12.2 当前确认的缺口

在当前实际数据库 `backend/data/curis.sqlite` 上，相关运行表均为 0 条记录；预期活动数据库 `data/curis.sqlite` 当前不在工作树中。因此下面的缺口是“尚未有可执行的真实样本”，不是“已经通过”。

| Simulation 必需对象 / 证据 | 当前事实 | 结论 |
| --- | --- | --- |
| `SimulationRun` 聚合记录 | 未发现对应持久化表或服务；现有 `evolution_simulations` 是演化模拟旧表，字段不能覆盖本计划的参与者、交接、回执、CEO 决策和失败事件 | **缺失** |
| `ContentItem` / `InteractionItem` | 未发现对应表、状态机或服务；现有 `content_publish_packages` 只保存发布包快照，`content_workflow_runs` 只保存 running/completed/failed | **缺失** |
| 平台独立变体与版本审计 | `platforms_targeted`、`artifacts_json` 为 JSON 快照；没有 `platformVariant`、`versionId`、`publishedVersionId`、审核意见 / 批准人字段 | **缺失** |
| ReplyPolicy 与互动回执 | 未发现 ReplyPolicy / InteractionItem 持久化对象；不能证明自动回复、CEO 审批、禁止自动回复三种策略 | **缺失** |
| Studio 配置 → 模拟失效 | `workspaces` 只有 `blueprint_json` 与三个门禁布尔字段，未发现配置版本、变更影响或 `simulationPassed=false` 的自动失效记录 | **未证明** |
| 研发真实验收链 | `workflow_runs` / `workflow_steps` 存在，但当前数据库无运行记录；需要真实 commit、build、test、CEO acceptance 的证据引用 | **未执行** |
| 统一状态机迁移 | 旧内容 / 研发运行时存在直接写入 `content_workflow_runs.status`、`workflow_runs.status`、`workflow_steps.status` 的路径 | **未接入**；Runtime Foundation 必须建立迁移边界，不能把旧 `running/completed/failed` 当成 v1.6 的业务状态机 |

### 12.3 执行决定

当前可以开始 Backend Runtime Simulation，但不能把它描述成真实平台或 UI 完成：研发与内容各自有可复用的旧运行基座，Foundation 已提供统一 `SimulationRun`、证据和失效契约；下一步顺序固定为：

1. 执行 `issues/20260809_runtime_simulation_001.md` 的后端 Simulation Issue；
2. 记录 RD、XHS、TTK 的成功、CEO 等待 / 拒绝、失败、回执 / 手动反馈和重启证据；
3. Simulation 交付并通过独立 Review 后，再创建 Workspace Studio 与运行态 UI 的实现 Issue；
4. UI Browser Evidence 全部通过后，才进入 Desktop 接入与打包验收。

在第 2 步之前，不得把当前内容发布包、研发工作流或静态原型描述为“三业务已跑通”。

## 13. RUNTIME-SIMULATION-001 执行结果（2026-08-09）

`RUNTIME-SIMULATION-001` 已完成并通过独立 Backend Review：

- RD-001、XHS-001、TTK-001 在同一 Company / CEO Assistant / AI 组织下，三个独立 Workspace 生成独立 `SimulationRun`；
- 聚焦联合回归 `31 passed`，包含 4 项三业务 Simulation 与 27 项 Foundation / 状态 / schema 兼容测试；
- RD 覆盖 CEO 等待、Commit / Build / Test 非 fixture `VERIFIED` Evidence、Cycle 关闭与下一周期反查；
- XHS 覆盖 CEO 拒绝、平台回执、版本生命周期和 ReplyPolicy 失效；
- TTK 覆盖 CEO 手动 `UNVERIFIED` 反馈、未解决失败阻断、失败解除留痕和最终平台回执；
- 临时 SQLite fresh、重启、Company / Workspace / Scenario 查询和 Tenant / Company / Workspace fail-closed 通过；
- Backend 全量为 `1272 passed, 31 failed, 2 skipped`，失败数与既有基线一致，清单外问题未修复；
- 本结果是 Backend Runtime Simulation 证据，不是浏览器证据、真实平台发布证明、UI 完成或 Desktop 完成。

阶段结论：`PASS_BACKEND_SIMULATION_WITH_BASELINE_BLOCKERS`。下一步只能创建 UI / 导航 / CEO Assistant / Workspace 运行态迁移 Issue；该 Issue 必须先通过 UI Evidence Review，之后才进入 Tauri Desktop 接入与打包验收。
