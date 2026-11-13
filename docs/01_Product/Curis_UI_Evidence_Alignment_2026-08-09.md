# Curis UI 证据与产品定义对照（2026-08-09）

Status: Review

本文件不是新的 UI Blueprint，也不是代码规范。它记录本轮从当前 `frontend/` 与
`curis-ui-prototype/` 中提取的必要产品链路，作为 Blueprint 5.0 的 UI 证据补充依据。

## 1. 对照规则

```text
Blueprint：定义为什么存在、谁负责、状态如何变化、什么算完成
UI：证明 CEO 如何进入、看到、操作、确认、返回和继续经营
Runtime：证明这些 UI 行为是否真的产生业务状态、证据和交接
```

三者必须闭合。UI 不能单独决定产品；Blueprint 也不能删除 UI 中完成经营闭环所必需的
进入、反馈和返回行为。

## 2. 前端中应保留的必要链路

| UI 证据 | 保留的产品行为 | 当前问题 | Blueprint 映射 |
| --- | --- | --- | --- |
| Onboarding 六步：欢迎、创业简报、公司设定、首个业务、AI 团队、启动检查 | CEO 从空公司逐步形成 Company、Business、AI Team 和首个运行入口 | 当前仍是表单式向导，Assistant 没有独立 Runtime | First Arrival、Company Lifecycle、Assistant Runtime |
| Assistant 代拟、填入示例、字段接受/跳过 | AI 提出可修改草案，CEO 保留确认权 | 结果尚未形成可追溯 Context 版本 | Assistant Context、Decision |
| 公司设定与公司卡预览 | CEO 在创建时看到公司边界和后果 | 法律/组织字段过早，需区分必须项与可延后信息 | Company Design |
| 首个业务目标、验收结果、最小责任、未知假设 | 创建业务时同时定义结果与验证条件 | 当前容易落成 Project 名称 | Business Runtime、Outcome |
| AI 团队与能力配置 | 让 CEO 知道谁承担责任、能力是否足够 | 当前是员工/能力 CRUD，没有汇报链 | AI Organization、Capacity |
| 启动检查 | 运行前发现责任、能力、授权、证据缺口 | 当前没有统一 Launch Gate | Workspace Runtime、Simulation |
| CEO Desk Brief、Matters、Pulse、Timeline、Handoffs、Closeout | Assistant 用经营日组织 CEO 注意力 | 当前数据范围与 Assistant Snapshot 不一致 | CEO Operating Day |
| 业务版图 | CEO 查看业务价值、真实结果和下一步 | 当前被 Project/graph 列表替代 | Business Runtime、Outcome |
| Workspace Portal / Studio / Runtime | 从业务结构进入部门办公室，再到运行现场 | 当前门户为空、Studio 只是创建表单 | Workspace Studio、Workspace Runtime |
| Decision / Evidence 回流 | 结果经过证据、验收后进入 CEO 决策 | 当前决策页为空，Meeting 为占位 | Evidence、Decision、Company Change |

## 3. 本轮明确不继承的 UI 结构

- 固定的 software / xhs / shortvideo 默认业务卡片
- Task、Project、Execution、Pipeline 作为 CEO 一级入口
- `graph-*`、`local-demo-company` 等演示事实
- 只展示状态但不能产生业务状态变化的装饰性 Dashboard
- 只显示“规划中”的 Meeting、Finance、Calendar 主路径入口
- 第二套 Assistant 抽屉任务系统

## 4. 三业务同步验证范围

三条业务同步推进，但不复制三套产品。共享内核统一使用 Company、CEO Assistant、AI Team、
Evidence、Decision 和 Change Runtime；业务差异只通过各自 Workspace 表达。

### 4.1 研发工作台：第一个任务是 Curis 的自研发（完善 Curis）

```text
研发工作台
→ 第一个任务：Curis 的自研发（工作项名：完善 Curis）
→ CEO 表达产品意图
→ Assistant 提炼结果、未知与影响
→ 产品 / 业务 AI 准备方案
→ 工程 AI 与 QA AI 接受责任
→ Workspace 运行 Curis 研发周期
→ 产生真实代码、构建、测试与运行证据
→ CEO 验收 / 退回 / 暂停 / 回滚
→ Assistant 收束并提出下一周期
```

### 4.2 小红书与抖音：同步设计和验证轨道

小红书与抖音不再延后到“Curis 的自研发”任务完成之后，而是与研发工作台同步完成各自业务 Workspace 设计和运行验证。
它们仍不能通过固定演示数据直接进入产品，必须完成：

1. Workspace 视觉与空间感重新设计；
2. 平台授权、API 回传和 CEO 手动录入的统一 Evidence 方案；
3. 内容生产、发布、数据回传、复盘和下一轮决策的 Runtime Simulation；
4. 与研发工作台共享内核的并行 Runtime Simulation 和独立业务评审；研发工作台内部的首个任务仍是“Curis 的自研发（完善 Curis）”。

三条轨道的推进关系：

```text
共享 Company OS / Assistant / AI Organization / Evidence / Decision
        ├── 研发工作台：第一个任务是 Curis 的自研发（完善 Curis）
        ├── 小红书运营工作台：并行 Workspace 设计与外部反馈验证
        └── 抖音 / TikTok 运营工作台：并行 Workspace 设计与外部反馈验证
```

### 4.3 内容发布参考转译后的当前 UI 差距（含 P0 门禁）

当前 `curis-ui-prototype/` 已证明内容工作台需要结果条、责任链、管道、CEO 决策队列和详情抽屉；但它仍是展示型原型，不能直接作为 Runtime 完成证据：

| 当前原型证据 | 已证明 | 仍缺什么 | 进入开发前的要求 |
| --- | --- | --- | --- |
| `workspace-runtime-xhs.html`：选题池 → 草稿 → 封面 → 待发布 → 已发布 | 小红书需要内容队列和 CEO 发布前确认 | 缺少显式 `APPROVED`、`SCHEDULED`、`AWAITING_FEEDBACK`、`REVIEWED` 状态；结果仍以示例数据呈现 | 以 `ContentItem` 状态机驱动，不允许拖拽绕过 CEO 门禁；发布回执和结果窗口必须有证据等级 |
| `workspace-runtime-shortvideo.html`：选题 → 制作 → 发布 → 数据 → 复盘 | 抖音需要脚本 / 视频制作与发布后数据 | 未授权、发布失败、数据冲突和 CEO 拒绝尚未成为可操作分支；部分界面仍使用英文角色名 | 增加失败出口、手动发布 / 补录入口、版本差异和中文责任名称；平台结果必须回到 `Outcome` |
| 两个页面的 JS 管道数据与拖拽 | 证明队列交互和键盘等价操作需要存在 | 状态只存在页面内存，无法证明 `contentId → runId → outcomeId` 追溯，也无法证明重启后状态保留 | UI 只能调用统一 Runtime 状态入口；每次变化显示 actor、时间、原因和下一检查点 |
| 结果条中的指标与“示例数据”徽标 | 证明平台指标必须有口径和可信状态 | 示例值不能参与业务扩大或复盘决策 | 未授权显示“待授权 / 待验证”；没有真实证据时不显示已验证价值 |
| 评论 / 私信 / 提及 / 订单咨询 | 证明内容结果不仅是指标，还会产生互动与线索 | 当前没有 `InteractionItem`、意图分流、回复版本、风险升级、`replyPolicy` 或外部回执 | 作为内容详情 / 结果面板 / Assistant 事项投影，不新增 CRM 一级导航；外部承诺必须 CEO 介入 |

因此，现有原型应被视为**布局与信息层级证据**，而不是 ContentItem 状态机或内容发布运行完成证据。Simulation 通过前，不能以现有看板、拖拽或静态数字宣称小红书 / 抖音工作台已跑通。

### 4.4 下一版必须补齐的屏幕证据

| 屏幕 / 状态 | 必须证明的行为 | 不能接受的表现 |
|---|---|---|
| 内容卡片 | 状态、负责人、证据等级、下一检查点和唯一主动作随状态变化 | 所有卡片都显示“移动至下一阶段” |
| CEO 审核抽屉 | CEO 能看版本差异、事实 / 未知、外部承诺影响，并批准或退回 | 只展示正文和一个绿色“通过”按钮 |
| 未授权发布 | 发布动作变为授权或手动发布；手动结果标记待验证 | 顶部显示 API 未授权，卡片仍可直接发布 |
| 发布失败 | 显示失败原因、重试 / 改期 / 退回路径，保留原版本 | 卡片移动到已发布或从队列消失 |
| 版本审核链 | 审核意见绑定 `versionId`，显示 Reviewer / CEO Approver，发布回执显示 `publishedVersionId` | 审核意见漂浮在聊天中，或批准 v2 却发布 v1 |
| 互动回流 | 显示来源、关联内容、意图、风险、回复策略、回复版本、处理状态和下一检查点 | 把评论数当价值，或直接生成无审计的外部回复 |
| 结果回流 | 显示时间窗口、原始指标、来源、新鲜度和证据等级 | 用示例数据填满结果条并允许放量 |
| Assistant 上下文 | 汇报为什么现在需要 CEO，并连接当前内容与历史决策 | 另建一套聊天任务系统或固定第三栏 |
| AI 团队状态带 | 显示岗位责任、`presenceState`、容量、最近交接和下一检查点 | 只显示一排 Agent 头像或把 Agent 做成平级聊天列表 |
| 平台变体卡片 | 小红书显示图文 / 轮播与收藏假设；抖音显示视频预览、钩子、时长与完播假设；各自绑定 `versionId` | 把一条通用内容直接复制到两个平台，或批准一个平台后自动批准另一个 |
| 内容 Workspace Studio | CEO / Business Engineering 能配置 Outcome、平台、Role Slot、Agent、ReplyPolicy、Evidence 和 Cadence，并运行模拟 | 只有“添加 Agent”表单，或保存配置后直接改变运行中的办公室 |

### 4.5 当前 Workspace Studio 的证据边界

当前 `curis-ui-prototype/workspace-studio.html` 已证明通用装修台需要“左侧资源 / 中间蓝图画布 /
右侧配置检查 / 底部版本与模拟操作”，这部分布局可以保留。但当前页面仍是混合短视频 / 小红书的
静态示例，不能作为 Blueprint 5.0 的 Content Workspace Studio 完成证据：

- 节点使用 `Research AI`、`Analysis AI`、`Script AI` 等英文演示名，未形成中文岗位和组织关系；
- 没有 `ContentIntent → platformVariant`、平台变体约束、`ReplyPolicy`、`InteractionItem` 和互动回流节点；
- 没有 `presenceState`、真实容量交接、版本审核意见或 `publishedVersionId`；
- “运行模拟”“提交审批”仍是展示型按钮，不能证明 Draft / Simulation / Approval / Runtime 的持久化流转；
- 画布把抖音拍摄 / 剪辑与小红书图文生产混在同一条固定链路中，不能体现两种平台变体的业务差异。

因此，Studio 的**画布形态可以继承，节点内容和运行契约必须重做**；在 Runtime Review 通过前，不把
当前 Studio 页面当成业务空间已经搭建完成。

Studio 的下一次验收必须执行 `docs/03_Design/Curis_Workspace_Shell.md §9.8` 的 DOM 与交互门禁：
验证 Outcome、平台变体、中文 Role Slot、在岗状态、ReplyPolicy、Evidence、模拟状态、版本持久化，
以及“未通过模拟不得提交审批”。当前原型尚未提供这些属性，不能用现有按钮或画布截图替代。

完整的 Runtime 逐项评审记录见 [`docs/reviews/content-workspace-runtime-review-2026-08-09/README.md`](../reviews/content-workspace-runtime-review-2026-08-09/README.md)。当前结论为 `BLOCKED_PENDING_RUNTIME_REVIEW`，不进入业务代码实现。

### 4.6 运行态布局迁移契约

Runtime Review 通过后，运行态页面必须从“管道看板”迁移为“运营办公室”。Studio 的装修画布不直接复用为运行页，运行页只读取已批准 Blueprint 和当前运行事实。

| 区域 | 运行态必须显示 | 主要交互 | 不能出现 |
|---|---|---|---|
| 顶部经营上下文 | 业务目标、当前周期、本周期承诺、Assistant 状态、同步时间 | 回到 CEO Desk、查看本周期影响 | 只显示“内容管理”或项目名称 |
| AI 团队状态带 | 每个岗位的中文名称、`presenceState`、当前责任、容量、最近交接、下一检查点 | 打开岗位上下文抽屉 | 平级 Agent 头像墙、第三栏聊天 |
| 主队列 | ContentItem 状态、平台变体、版本、负责人、证据等级、唯一主动作 | 提交审核、批准、排期、补录、复盘等状态动作 | 通用“移动至下一阶段”、自由拖拽改写事实 |
| Assistant 抽屉 | 当前内容、来源、事实 / 未知、权限、版本差异、为什么需要 CEO | 批准、退回、授权、升级、形成 Decision | 独立 Assistant 任务系统 |
| 结果区 | 发布回执、时间窗口、原始指标、来源、新鲜度、验证等级、复盘结论 | 补证据、标记待回流 / 来源冲突、进入下一轮决策 | 示例数字参与扩大业务 |

运行态首屏结构：

```text
业务目标 / 周期承诺 / Assistant 状态
→ AI 团队状态带
→ 内容运行队列（平台变体卡片）
→ 按需 Assistant 上下文抽屉
→ 发布回执 / 外部结果 / 复盘 / 下一轮 Decision
```

小红书与抖音共享这套布局骨架，但卡片主体必须分别呈现图文 / 轮播与视频 / 脚本；平台差异只进入
`platformVariant`，不能复制成两套 Company OS，也不能将两平台内容合并成一张“通用内容卡”。

### 4.7 研发工作台的 Cycle / Handoff / Acceptance 屏幕证据

Business Runtime v1.6 在 v1.5 的基础上补齐了 AI Employee / Role Slot / Capability Binding 的组织版本、岗位生命周期和员工 `lifecycleStatus / presenceState` 边界，并保留 First Arrival、CEO Assistant Runtime、Cycle 异常维度、证据新鲜度和 Simulation 复核状态。研发工作台不能只显示旧 Workflow 的步骤列表。运行页必须让 CEO 看见“一轮责任如何被接住、执行、验证并回到自己手里”：

| 屏幕区域 | 必须显示 | 交互与门禁 | 不能接受 |
|---|---|---|---|
| 顶部 Cycle 上下文 | Cycle 名称、序号、Outcome、Blueprint Version、当前 Stage、下一检查点 | 回到 CEO Desk；查看影响范围和历史版本 | 只显示 Project / Task 名称 |
| 研发 AI 团队状态带 | 产品 AI、工程 AI、QA AI、运行与反馈 AI 的责任、`presenceState`、容量和最近 Handoff | 打开责任上下文；可查看交接而非进入平级聊天 | 头像墙或“研发 AI 已完成” |
| Stage 运行队列 | 意图接收、方案设计、实现、验证、CEO 验收、复盘与改进 | 主动作由当前状态 / Owner 生成；失败进入异常抽屉 | 统一“下一步”或自由拖拽 |
| 工程证据区 | commit、build、test、真实用户流程、失败原因和来源 | 证据必须可展开、可回溯到 `cycleId`；没有关键证据不能提交验收 | 只显示代码提交或测试数量 |
| Handoff / Decision | 来源岗位、目标岗位、输入 / 输出、确认状态、CEO 待决策原因 | 交接未确认不能显示“已接手”；Decision 必须有选项、影响、回滚条件和 CEO 选择 | 把交接写成评论或复制文本 |
| Acceptance 抽屉 | 验收标准、证据、已知缺口、CEO 接受 / 拒绝 / 暂停 / 回滚 | 只有 CEO 产生 Acceptance；拒绝必须进入新 Cycle 或修订 | AI 自动写“已验收” |

状态投影必须同时显示：岗位是否可接手（`RoleSlot.status`）、员工身份生命周期（`AIEmployee.lifecycleStatus`）和当前在岗状态（`presenceState`）。`BLOCKED` 只能作为岗位 / 在岗阻塞原因，不得单独渲染成“员工已结束”。

研发工作台首屏建议固定为：

```text
当前 Cycle / Outcome / 承诺
→ AI 团队状态带
→ Stage 运行队列
→ 工程证据与异常
→ Handoff / CEO Decision / Acceptance
→ 复盘 Insight / 下一 Cycle
```

当前原型尚未提供上述 Cycle、Handoff、Acceptance 的持久化 UI 证据；它只能作为未来 UI 设计的要求，不能作为研发业务已跑通的证据。

## 5. 进入开发前的验收条件

只有以下证据全部存在，UI 证据才可以进入代码：

- Blueprint 已描述对应产品对象、Owner、Input/Output、状态、反馈和关闭；
- Runtime Simulation 已覆盖正常、失败、外部结果缺失和 CEO 拒绝；
- Runtime Simulation 已覆盖批准版本与实际发布版本不一致时的阻断与升级；
- UI 可从 CEO 入口走到下一阶段，并能回到 CEO Desk；
- API / 数据只读取当前 Company；
- 不依赖固定业务、测试项目或旧导航；
- 真实使用结果可以被 CEO 验收，并进入下一次 Decision。
