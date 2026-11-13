# Curis Workspace Shell — 统一工作台骨架设计规范

> **⚠️ Status: DEPRECATED（2026-08-17 设计文档整合）** — 本草案「5 槽位工作台骨架」已被 Frozen `Curis_Workspace_Shell_Contract_And_Shared_Patterns.md`（四独立 Pane + 7 Shared Pattern）**取代**。其「5 槽位（结果条 / 责任链 / 管道 / 侧栏 / CEO 队列）」概念属 Layer 4 的一种 Main 运营变体，**非 Shell Contract 本身**。新 Agent 请勿以本文件为权威；仅作历史参考。

> 配套文档：基础令牌、主题令牌和组件基类见 `Curis_Design_System.md`（单一真相源）。
> 本规范定义「域无关工作台外壳」——新业务接入 = 声明式填充槽位，而非重新造页面。

## 0. 状态与定位

- **状态**：设计系统交付物（草案，待 Frozen 验收）
- **定位**：一套可克隆的工作台骨架。任何新业务（软件研发、小红书、短视频、未来任意域）共用同一套 shell、令牌、导航与交互模型，仅填充领域语义。
- **参考原型**：`curis-ui-prototype/workspace-shell-reference.html`（基于冻结 `_system`，含全部 5 槽位与占位示例业务）

## 1. 设计目标与产品对齐

对齐 Curis 产品主轴（不可动摇）：

- **能力可替换不写死** → 骨架不绑定任何业务词，槽位由数据声明。
- **员工 = 动态调用能力的岗位** → 责任链槽位用「角色 → 可验收结果」表达，不固化具体 Agent。
- **新业务 = 新工作空间域** → 加一个业务 = 配置槽位，不是从零开发一套页面 + 重新踩设计系统违规的坑。

**价值**：统一视觉/导航/交互/无障碍；缩短新域从 0 到可用的时间；降低设计债务。

## 2. 不可违背的纪律（铁律）

1. **一套 shell、一套令牌、一个导航**：禁止页面私有 accent（历史违规：`#387bff`、`#32f08c`）。全部走 `--ui-*`。
2. **尺寸纪律**：顶栏 52px、侧栏 220px；所有颜色与主题令牌只来自冻结 `Curis_Design_System.md`。
3. **主题三态**（dark / light / system）由 `_system/theme.js` 统一接管，禁止页面自带主题逻辑。
4. **共享助理抽屉** `_system/assistant-drawer.*` 全局唯一，禁止每页自建悬浮卡（旧 `curis-companion` 已退役）。
5. **mock 数据必须带「示例数据」徽标**（`.mock-badge`），避免与真实数据混淆。
6. **主按钮纪律**：每页主按钮 ≤ 1；运行时动态生成的主按钮须降级为 `btn-secondary`。
7. **运营场景驱动（最高优先级）**：槽位内容必须源于该业务的真实日运营场景，禁止纯占位/通用词（如「示例工作项 A」直接上线）。重点约束：
   - **指标由域声明**：每个域的「结果条」指标卡**各不相同**——小红书看收藏率、短视频看完播率、研发看回归通过率，**禁止套通用指标模板**（如「指标 A / 值」）。每项指标须带口径说明（`note`），让「这个数到底量的是什么」一目了然。
   - 实例化前先产出「运营场景清单」（真实动线、每天看什么、卡在哪一步、CEO 在哪一刻介入、该域到底用什么指标衡量成败），再映射到 5 个槽位。详见 §8。

## 3. 骨架结构：5 个域无关槽位

每个槽位给出：作用 / 组成 / 状态 / 令牌 / 无障碍要点。

### 3.1 结果条（Result Bar）

- **作用**：顶部一眼看全局结果与数据可信度。
- **组成**：4–6 个指标卡（标签 / 值 / 趋势 + 口径 `note`）+ 数据可信徽标（已同步 / 同步中 / 未授权 / 示例数据）。**指标卡由域在 `metrics` 槽位声明，禁止通用占位（如「指标 A / 值」）——每个域的北极星与辅助指标不同，详见 §8 各域「指标定义」。**
- **状态**：`live` / `syncing` / `unauthorized` / `mock`。
- **令牌**：指标值 `--ui-text`；可信徽标 `--ui-success`（已同步）/ `--ui-warning`（同步中）/ `--ui-text-3`（未授权）；mock 用 `.mock-badge`。
- **无障碍**：指标卡用 `<dl>`；徽标 `aria-live="polite"`。

### 3.2 责任链（Responsibility Chain）

- **作用**：谁对哪个可验收结果负责，避免「已完成」式空话。
- **组成**：角色 chip（角色名 + 负责的可验收结果 + 状态点）。
- **状态**：待开始 / 执行中 / 验收中 / 已交付。
- **令牌**：状态点 `--ui-warning`（执行中）/ `--ui-success`（已交付）/ `--ui-text-3`（待开始）。
- **无障碍**：chip 列表 `role="list"`；状态点带 `aria-label`。

### 3.3 管道看板（Pipeline Board）

- **作用**：工作项流动的主操作区。
- **组成**：4–5 条**活跃泳道**（如 选题 → 生产 → 审核 → 发布）+ 一个**回顾区**（数据 / 复盘 / 归档，结果态只读派生）。
- **卡片**：标题 / 负责人 / 状态 / 证据链接 / 检查点。
- **交互**：生产态卡片可拖拽；结果态（已发布 / 归档）只读，由平台派生，不可手动回拖。
- **令牌**：泳道头 `--ui-surface-2`；卡片 `--ui-surface`；生产中边框 `--ui-accent`。
- **无障碍**：看板 `role="list"`；每个卡片的状态动作必须有键盘等价，按钮名称随状态变化（如「提交审核」「批准发布」「补录结果」），禁止用一个“移动至下一阶段”按钮代替所有动作。

### 3.4 侧栏面板（Context Panels）

- **作用**：上下文 / 明细 / 决策支撑。
- **组成**：3 块固定面板 —— ① 外部结果与验收 ② 价值与成本（含投入产出比口径说明）③ 洞察与下一步（含 CEO 待决策项）。
- **令牌**：面板容器 `--ui-surface`；标题 `--ui-text-2`。
- **无障碍**：面板使用 `aria-label`；用户界面不把 ROI / KPI 作为独立标签，统一显示“投入产出比 / 工作指标”，内部字段可保留英文。

### 3.5 CEO 决策队列（CEO Decision Queue）

- **作用**：把「待我确认」的事前置暴露，不沉在页底。
- **组成**：① 顶栏常驻徽标「待 CEO 决策：N」；② 洞察面板内的高亮队列项（可点击处理）。
- **状态**：待 CEO 确认 / 已确认 / 已退回。
- **令牌**：队列徽标 `--ui-warning`；高亮项左缘条 `--ui-accent`。
- **无障碍**：徽标 `aria-live`；队列项 `role="link"` 或 `button`。

## 4. 布局与响应式

- **桌面（≥1024）**：左导航 220 + 主区（结果条 / 责任链 / 管道 + 侧栏面板两栏）/ CEO 队列。
- **平板（640–1023）**：导航收为图标栏（仅图标）；管道横向滚动或堆叠。
- **移动（<640）**：导航抽屉化；管道纵向堆叠；结果条指标折行。
- **间距**：8px 基准栅格（`--ui-*` 间距令牌）。

## 5. 新业务实例化协议（接入 = 配置）

复制 `curis-ui-prototype/workspace-shell-reference.html`，声明以下槽位（JSON / HTML 注释均可）：

```js
{
  domainName: "示例业务",
  responsibilityChain: [{ role, deliverable, status }],
  pipelineColumns: [{ id, title, type: "active" | "review" }],
  metrics: [{ label, value, trend, note }],
  ceoDecisions: [{ title, status, link }]
}
```

其中 `metrics` 必须由域声明「**北极星指标 + 辅助指标**」，每项含 `label / value / trend / note（口径说明）`，禁止通用占位。例如小红书的北极星是「平均收藏率」而非「阅读量」；短视频是「完播率」而非「播放量」；研发是「回归通过率」而非「完成度%」。

未声明的槽位不得留空 UI 洞——用 `.empty-state` 占位（「暂无数据，配置后显示」）。

## 6. 反例（已发现违规，须整改）

- **短视频工作台**（`workspace-runtime-shortvideo.html`）：历史原型曾在冻结系统之外另立平行令牌、引入 CDN、拆分导航和自定义顶栏。它的后续改写只能作为布局证据，不能证明 Runtime 已实现。
- **研发 / 小红书运行现场**：历史原型曾尝试补齐管道看板和 CEO 决策队列，但状态主要存在页面内存。当前三域页面均只能证明信息层级与交互方向，不能据此宣称运行现场已合规或业务已跑通。

## 7. 参考原型

`curis-ui-prototype/workspace-shell-reference.html`：基于冻结 `_system`（tokens.css / shell.css / theme.js / assistant-drawer）的骨架演示，含全部 5 槽位与占位示例业务，可直接克隆接入新域。

## 8. 域实例：真实运营场景 → 槽位映射

> 骨架是「结构」，槽位内容必须源于该业务的真实日运营场景（铁律 #7）。以下为三个已落地业务的实例化参考，**禁止**用通用占位词替代。

### 8.1 软件研发
- **真实场景**：每日看 backlog → 进行中 → 评审 → 合并；CI 绿/红；待我 review 的 PR；阻塞项；开放缺陷。不是散文报告，是流动的工作项。
- **指标定义**（研发视角，北极星 = 可交付且可验收的版本节奏）：
  - **北极星**：回归通过率（QA 红线，目标 ≥ 95%）——比「功能做了多少」更能反映交付质量。
  - **辅助**：本周期版本号 / 提交数 / 开放缺陷数 / 阻塞项数 / 待 review PR 数 / 首次验收通过率。
  - **口径**：回归通过率 = 自动回归用例通过数 ÷ 总数；首次通过率 = 一次验收通过的工作项 ÷ 总交付工作项。**禁止用「完成度%」这种模糊通用卡**。
- **责任链**：产品 AI（范围）→ 研发 AI（实现）→ QA AI（验收）→ CEO（真实使用验收）。
- **管道看板**：需求池 → 实现中 → 评审 → 待发布 → 已发布（只读）。卡片含关联 commit/PR、CI 状态、检查点。
- **侧栏面板**：外部结果（真实路径跑通证据）/ 价值成本（模型·Skills·成本·首次通过率）/ 洞察（下一周期改进 + CEO 验收）。
- **CEO 决策**：验收通过 / 退回修改 / 请求现场演示。

### 8.2 小红书
- **真实场景**：收藏率（北极星，权重 > 赞）→ 内容日历 → 草稿队列 → 单篇数据 → 定时发布 → 强审核（品牌/敏感需 CEO 确认）→ 授权后真实指标。运营每天动线：打开 → 看发布队列 → 查草稿 → 发布 → 看实时数据 → 反应。
- **指标定义**（运营视角，北极星 = 收藏率）：
  - **北极星**：平均收藏率（小红书权重收藏 > 赞，直接决定分发）——比点赞更能反映内容价值。
  - **辅助**：本周发布/目标 / 新增粉丝 / 线索价值（¥）/ 投入产出比 / 平均互动率 / 私信咨询数（线索入口）/ 爆文率（单篇 ≥ 1k 收藏占比）。
  - **口径**：收藏率 = 收藏数 ÷ 曝光数；线索价值 = 私信转化估值（¥）；投入产出比 = 内容产出价值 ÷ 投入（模型+人工）。**禁止用「阅读量」当主指标**（小红书分发逻辑不认阅读量）。
- **责任链**：选题 AI → 内容 AI → 审核 AI（CEO 确认）→ 运营 AI（数据复盘）。
- **管道看板**：选题池 → 草稿 → 封面 → 审核（CEO）→ 定时发布 → 数据 → 复盘（只读）。卡片含封面缩略图、选题标签。
- **侧栏面板**：外部结果（平台回传）/ 价值成本（线索价值·投入产出比口径）/ 洞察（掉量笔记·选题池建议 + CEO 决策）。
- **CEO 决策**：待发布品牌/敏感表达确认；授权后是否放量。

### 8.3 短视频（抖音 / TikTok）
- **真实场景**：生产中 4–5 条泳道并行；发布后数据/复盘/归档由平台派生、只读；授权状态必须与其他域一致（当前三页割裂，须统一）。
- **指标定义**（抖音视角，北极星 = 完播率驱动的播放规模）：
  - **北极星**：5s 完播率 + 整体完播率（决定系统是否继续分发）——比播放量更前置、更可控。
  - **辅助**：播放量 / 互动率（赞+评+转 ÷ 播放）/ 涨粉 / 投入产出比（4.4x）/ 转发率 / 评论率 / 转化成交额（若带货）。
  - **口径**：完播率 = 播完用户 ÷ 播放用户；投入产出比 = 视频带来收益 ÷ 制作+投放成本。**短视频的「播放量」是结果而非原因，不能当北极星**——但须与其他域统一「同步中 / 已授权」的数据可信表达。
- **责任链**：选题 AI → 脚本 AI → 拍摄 AI → 剪辑 AI → 发布 AI → 运营 AI。
- **管道看板（收敛）**：选题 → 脚本/制作 → 发布 → 数据 → 复盘（只读）。拍摄+剪辑合并；数据/复盘/归档归回顾区，不可手动回拖。
- **侧栏面板**：外部结果（平台数据）/ 价值成本（投入产出比口径）/ 洞察（下一条选题 + CEO 待决策）。
- **CEO 决策**：选题方向确认；投放预算确认。

### 8.5 内容发布工作台的运行语义（对齐 Business Runtime v1.6）

小红书和抖音的工作台沿用同一套 Shell，但内容卡片必须表达 `ContentItem` 的真实运行状态，不能只表达“有一篇内容”：

| 卡片区域 | 必须显示 | 交互边界 |
|---|---|---|
| 身份 | 内容标题、平台、版本、所属业务周期 | 点击打开内容详情，不离开当前工作台上下文 |
| 责任 | 当前 Owner、责任 AI、下一检查点 | 可查看交接记录；不能在卡片上静默改责任 |
| 状态 | 选题 / 草稿 / 审核中 / 已批准 / 已排期 / 已发布 / 待反馈 / 已复盘 | 只能通过 Runtime 状态入口流转；不允许拖拽跳过 CEO 审核或发布回执 |
| 证据 | 来源、授权状态、发布回执、数据新鲜度、验证等级 | `待验证 / 待回流 / 来源冲突` 必须可见，不能用绿色成功态掩盖 |
| CEO 动作 | 审核、退回、手动发布、补录结果、确认复盘 | 高影响动作必须进入 CEO Assistant / Decision 记录 |

视觉上，生产中的泳道可以支持受限拖拽和键盘状态动作；`已批准`、`已发布`、`待反馈`和`已复盘`属于受门禁或平台派生的状态，只能通过明确动作推进。`APPROVED` 表示发布前审核通过，`ACCEPT` 表示外部结果验收通过，二者不能使用同一个“完成”标签。授权缺失、发布失败、数据延迟和结果冲突使用独立的 `exceptionStatus`（等待 CEO / 发布失败 / 待数据 / 结果异常）表达，不得把异常伪装成新的成功泳道。

### 8.6 内容卡片动作矩阵

内容卡片不再显示跨阶段通用的“移动至下一阶段”。按钮由状态与当前角色共同决定：

| 状态 | 卡片主动作 | 次动作 | 禁止显示 |
|---|---|---|---|
| 选题 | 接受选题 | 查看来源、退回补证据 | 发布、排期 |
| 草稿 | 提交审核 | 继续创作、查看版本 | 直接发布 |
| 审核中 | 批准发布 | 退回并填写原因、请求补证据 | AI 自动通过 |
| 已批准 | 排期 / 立即发布 | 修改版本、取消 | 未授权时显示“发布成功” |
| 已排期 | 查看排期 | 取消排期、处理失败 | 拖回草稿 |
| 已发布 | 查看发布回执 | 查看外部链接 | 手动改写平台结果 |
| 待反馈 | 补录结果 | 标记待回流 / 标记来源冲突 | 直接扩大业务 |
| 已复盘 | 形成下一轮决策 | 归档、复制为草案 | 覆盖历史证据 |

当账号未授权时，`已批准` 卡片只显示“授权账号”或“手动发布并录入证据”；CEO 手动发布后的卡片可以显示“已发布 · 待验证”，但不能显示“已验证价值”。

审核意见必须绑定 `versionId`，显示意见者、时间、事实 / 观点 / 品牌 / 风险分类和解决状态。已批准版本只读；任何正文、素材、平台适配或外部承诺变化都创建新版本并重新进入审核。发布回执必须显示实际发布的 `publishedVersionId`，防止批准版本与上线版本不一致。

Business Runtime v1.6 的运行态投影还必须表达三类跨业务事实：

- **责任退回**：Handoff 进入 `RETURNED` 时，责任卡显示退回原因、缺少的能力 / 输入、已尝试范围和建议 Owner；不得显示“已完成”，也不得静默换人。
- **升级超时**：`WAITING_CEO` 超过 2h / 4h / 24h 后只提高 Assistant 提醒等级并显示 `overdueSince`，不改变批准结果；风险动作同时进入暂停态。
- **脉搏与置信度**：公司脉搏显示等级与触发证据，置信度展开显示来源组成；`UNKNOWN / STALE / CONFLICT` 不能被绿色成功样式覆盖。

首屏布局固定为“业务目标与周期 → 内容运行队列 → 按需 Assistant 上下文 → 外部结果与下一轮”，日历只作为节奏视图。小红书在内容详情中优先展示图文 / 轮播、收藏与线索反馈；抖音 / TikTok 优先展示脚本 / 视频版本、钩子、完播与成交反馈。平台差异只改变槽位内容，不改变 Shell、Assistant 抽屉和证据语法。

### 8.7 内容发布产品参考：借机制，不复制后台

外部产品只用于验证“内容团队如何工作”，不用于决定 Curis 的产品根。参考四类机制：

| 参考机制 | 可借鉴的经营事实 | Curis 的转译 | 明确不复制 |
|---|---|---|---|
| Buffer：平台适配创作、AI 辅助、审批 | 一条内容需要按平台改写，并在发布前由责任人确认 | `ContentItem` 维护平台版本；Assistant 生成审核包；CEO 在 `IN_REVIEW` 做最终门禁 | 不把 AI 文案生成器当成 Assistant，也不以“发送成功”替代外部结果 |
| Hootsuite：Yeti Agent 趋势 / 监听 / 带引用 AI 建议 | 选题来自外部信号，信号需要来源、时间和置信度，建议必须能转成行动 | 结果条上方先放信号摘要；研究 AI 只提交带证据的候选选题和下一动作 | 不做以热点数量、互动量堆叠为主的 Dashboard |
| Predis：内容日历、队列、审批状态 | 日历能表达节奏、排期和批量观察 | 日历是 Cadence 投影；主界面仍是状态队列，排期动作必须经过授权 / CEO 门禁 | 不让拖拽改写 Runtime 状态，不允许日历直接发布 |
| Later：可视规划、团队审核、媒体预览 | CEO 需要在发布前看到最终视觉、版本和审核意见 | 详情抽屉提供图文 / 视频预览、版本差异、意见和发布回执 | 不引入多真实员工协作模型，不把媒体库变成产品入口 |

#### 8.7.1 Curis 内容办公室的屏幕顺序

```text
业务目标 / 当前周期 / 本周期承诺
→ 外部信号摘要（来源、新鲜度、置信度）
→ 内容运行队列（按 ContentItem 状态与下一动作）
→ CEO 审核抽屉（版本、事实 / 未知、承诺影响、授权）
→ 发布回执与结果窗口（API / 手动、证据等级、新鲜度）
→ 复盘与下一轮 Decision
```

这意味着小红书 / 抖音工作台都应有一个“运营办公室”首屏，而不是“内容管理后台”首屏：
CEO 首先看到本周期要创造的结果，其次看到 AI 团队正在推进的内容，最后才看到素材、日历
和指标细节。Assistant 只在审核、权限、异常或决策点主动出现；其余时间把准备好的上下文
安静地留在内容卡片和抽屉中。

#### 8.7.2 Agent 机制与布局的对应关系

| Agent 角色 | 默认出现位置 | 主动触发 | 交付给下一环节 |
|---|---|---|---|
| CEO Assistant | CEO Desk、内容详情抽屉 | 审核窗口、授权缺失、结果异常、日末收束 | 审核包 / Decision / Handoff |
| 选题研究 AI | 信号摘要、选题池 | 新信号或结果复盘形成新假设 | 带来源的 `IDEA` |
| 内容创作 AI | `DRAFT` 卡片、版本比较 | 选题被接受或 CEO 退回 | 平台适配版本 |
| 发布执行 AI | `APPROVED` / `SCHEDULED` 卡片 | 审核通过、排期到点 | 授权检查、发布回执或失败 |
| 数据复盘 AI | 结果窗口、复盘面板 | `PUBLISHED + 24h / 72h` | `verificationStatus=VERIFIED / UNVERIFIED / ABNORMAL` + `evidenceCondition=FRESH / STALE / CONFLICT` 结果与下一轮建议 |
| 互动回收 / 分流 AI | 互动回流面板、Assistant 事项 | 新评论、私信、提及、咨询或 API 异常 | `CLASSIFIED` 互动、风险标签、线索或回复草案 |
| 回复准备 AI | 互动详情抽屉 | 低风险互动或 CEO 退回修改 | 绑定 `responseVersion` 的平台回复草案 |

运营办公室在内容队列上方增加一条“AI 团队状态带”，不增加第三栏：

```text
Assistant：准备汇报 · 选题研究 AI：监听信号 · 内容创作 AI：制作 v3
发布执行 AI：等待授权 · 数据复盘 AI：等待结果 · 显示容量、最近交接、下一检查点
```

每个岗位状态使用 `AVAILABLE / RUNNING / WAITING_CEO / BLOCKED / PAUSED`，必须同时显示
当前责任和容量。点击岗位只打开上下文抽屉，不进入聊天列表；CEO 处理的是责任、证据、交接
和容量，不是逐个阅读 Agent 的对话。

互动回流面板的主动作也必须随状态和 `replyPolicy` 变化：

| 状态 | 主动作 | 门禁 |
|---|---|---|
| `CAPTURED` | 分类互动 | 来源缺失或重复时先补证据 |
| `CLASSIFIED` | 生成回复草案 / 标记无须回复 | 低置信度、敏感或潜在线索转 CEO Assistant |
| `DRAFTED` | 按策略自动回复 / 提交 CEO 审核 | `AUTO_APPROVED_TEMPLATE` 只能使用批准模板；其他策略禁止直接发送 |
| `WAITING_CEO` | 批准并发送 / 修改 / 升级 | CEO 决策与 `responseVersion` 必须留痕 |
| `RESPONDED` | 查看平台回执 / 跟进结果 | 无外部回执只能显示“待验证” |
| `OUTCOME_TRACKING` | 记录线索、成交或关闭原因 | 不得从互动数量估算收入 |

外部参考的共同结论是“内容生产需要队列、审批、排期和结果”，Curis 的差异在于：这些都
必须挂在 CEO 的经营结果、AI 员工责任、Evidence 和 Decision 上，而不是形成另一套社交媒体后台。

#### 8.7.3 平台变体的卡片布局

两个平台共享卡片外壳，但卡片主体必须呈现不同的工作对象：

| 区域 | 小红书变体 | 抖音 / TikTok 变体 | 共享规则 |
|---|---|---|---|
| 预览 | 封面、标题、图文 / 轮播缩略图 | 视频首帧 / 播放预览、时长、比例 | 预览必须对应当前 `versionId` |
| 创作上下文 | 搜索表达、选题标签、收藏价值假设 | 钩子、脚本版本、节奏、完播假设 | 来源、事实 / 未知和平台约束可展开 |
| 结果 | 收藏率、评论、关注、线索 | 完播率、互动、涨粉、成交 | API / 手动来源、新鲜度和证据等级始终可见 |
| 主动作 | 提交审核 / 批准发布 / 补录互动 | 提交审核 / 检查发布权限 / 补录结果 | 由状态、角色和 `replyPolicy` 生成，不使用通用移动 |

平台差异只改变变体内容，不改变 CEO Assistant、Evidence、Decision、状态门禁和回到 CEO Desk 的路径。

#### 8.7.4 内容运营 Workspace Studio 布局

```text
┌ 运营 Workspace Studio · 草稿 vN · 模拟状态 · 提交审批 ────────────────────┐
│ 左：Outcome / 受众 / 平台 / 约束 │ 中：阶段与输入输出画布 │ 右：岗位 / Agent / 能力 │
│                                  │                      │                    │
│                                  │ 研究 → 创作 → 审核    │ 发布 / 互动 / 复盘   │
├──────────────────────────────────────────────────────────────────────────┤
│ 底部：缺口检查 · 授权状态 · ReplyPolicy · Evidence Route · Simulation 结果 │
└──────────────────────────────────────────────────────────────────────────┘
```

Studio 中拖入的不是“一个 Agent 卡片”，而是带有责任、输入、输出、能力、权限和失败出口的
Role Slot。保存草稿不会改变 Runtime；只有模拟通过并经 CEO 批准后，才生成新的运行版本。

### 8.8 研发工作台运行态：Cycle Office 而不是 Workflow 列表

研发工作台沿用统一 Shell，但运行页必须以 `Cycle` 为主语义。`Project / Task / Workflow` 只在 Cycle 内部证据区出现，不得成为 CEO 首屏的导航或主标题。

```text
┌ 研发工作台 · Cycle N · Outcome · Blueprint Version · Assistant 状态 ┐
│ AI 团队状态带：产品 AI · 工程 AI · QA AI · 运行与反馈 AI             │
├───────────────────────────────────────────────────────────────────┤
│ Stage 队列：意图接收 → 方案设计 → 实现 → 验证 → CEO 验收 → 复盘      │
│ 当前责任卡：Owner / Handoff / 下一检查点 / exceptionStatus          │
├───────────────────────────────┬───────────────────────────────────┤
│ 工程证据：commit / build / test │ CEO Acceptance / Decision 抽屉      │
│ 真实用户流程 / 失败与恢复       │ 接受 / 拒绝 / 暂停 / 回滚             │
└───────────────────────────────┴───────────────────────────────────┘
```

| 区域 | 视觉和交互要求 | 运行事实来源 |
|---|---|---|
| Cycle Header | 显示 Outcome、周期序号、Blueprint Version、当前阶段和下一检查点 | `Cycle` |
| AI 团队状态带 | 中文岗位、`presenceState`、当前责任、容量、最近 Handoff；点击开上下文抽屉 | `Role Slot / Handoff` |
| Stage 队列 | 只显示当前合法主动作；不能用通用“移动至下一阶段” | Cycle / Stage 状态机 |
| 工程证据区 | commit、build、test、真实用户流程、错误和恢复命令可展开 | `executionRef / Evidence` |
| CEO 抽屉 | 版本差异、验收标准、未知、影响、回滚条件和 CEO 选择 | `Acceptance / DecisionPacket` |
| 复盘区 | Insight、下一 Cycle、能力缺口和公司变更建议 | `Insight / Decision` |

CEO 完成验收后，界面必须回到 CEO Desk 的 Operating Day 上下文；不得停留在“任务完成”页，也不得让 AI 直接把 `Acceptance` 写成成功。研发工作台和内容工作台共享“周期 → 交接 → 验收 → 决策”路径，但各自只呈现自己的 Stage 与证据。

### 8.9 部门办公室（跨工作空间聚合视图）
- **真实场景**：部门承接 CEO 目标后，把它拆成若干「责任项」，再分派给下属工作空间（小红书 / 短视频 / 软件工作室…）执行；部门本身不直接生产内容/代码，而是跨空间回收结果、验收、复盘。卡片实体不是作品，而是**责任项**。
- **指标定义**（部门视角，北极星 = 责任是否按时交付并被 CEO 验收）：
  - **北极星**：责任按期交付率——比「下属空间发了多少内容/写了多少代码」更能反映部门整体履约质量。
  - **辅助**：在办责任项 / 一次验收通过率 / 验收周期中位数 / 跨空间复用率 / 部门投入产出比。
  - **口径**：责任按期交付率 = CEO 验收通过且未超期的责任项 ÷ 本季全部已到期责任项（中途暂停计为未达成）；一次验收通过率 = 首次提交即通过 ÷ 总提交次数；跨空间复用率 = 被 ≥2 个空间复用的成果 ÷ 成果总数（部门层独有指标）。
- **责任链**：业务工程 AI（拆解 + 验收标准）→ 执行调度 AI（跨空间分派与进度回收）→ 反馈 AI（外部结果与异常回收）→ CEO（验收 / 调整 / 暂停）。
- **管道看板**：责任承接 → 路径拆解 → 分派执行 → 待验收（CEO）→ 已结项（只读）。卡片须带**所属工作空间**标签（复用 `.ci-tag`，如「小红书」「短视频」「财务」），方便一眼识别跨空间分布。
- **侧栏面板**：外部结果与验收（跨空间汇总）/ 价值成本（含部门投入产出比与复用成果口径）/ 洞察（下一季改进 + CEO 决策）。
- **CEO 决策**：授权上线双端共用能力、确认成本口径重定义、批准/暂停责任项。

## 9. 前端实现规格（组件级骨架）

> 本节能让前端直接落地。所有 class / data 属性 / 交互均取自已通过深·浅 DOM 断言的四个运行现场（`workspace-runtime-software.html` / `workspace-runtime-shortvideo.html` / `workspace-runtime-xhs.html` / `workspace-runtime-department.html`），可照抄。

### 9.1 文件结构与依赖（每页头部固定）

```html
<html lang="zh-CN" data-theme="dark">
<head>
  <link rel="stylesheet" href="_system/tokens.css">   <!-- 冻结令牌，唯一来源 -->
  <link rel="stylesheet" href="_system/shell.css">      <!-- 冻结基础壳 -->
  <link rel="stylesheet" href="_system/assistant-drawer.css">
  <script src="_system/theme.js"></script>              <!-- 主题三态接管 -->
  <meta charset="UTF-8">
</head>
<body data-assistant-context="<域>运行现场">            <!-- 助理抽屉上下文 -->
```

- 禁止引入 Tailwind CDN、页面内私有 `@keyframes`/私有 `--accent` 定义。
- 页内 `<style>` 仅允许**结构布局类**（`.lane`/`.card`/`.panel` 等），颜色一律 `var(--ui-*)`。

### 9.2 槽位 HTML / class / data 速查表

| 槽位 | 容器 class | 关键子元素 | data / role 属性 |
|---|---|---|---|
| 侧栏导航 | `.sidebar > .nav` | `.nav-item`（`href` 跳各域页） | 当前页加 `.active`；分组用 `<p class="nav-label">` |
| 顶栏 | `.topbar` | `.crumbs` `.trust-pill` `.ceo-badge` `.theme-switch` | `trust-pill` 可选 `.live`；`ceo-badge` 带 `aria-live="polite"` |
| 结果条 | `.result-bar` | `.metric`（含 `span/strong/small/.caliber`） | `.caliber` 必填口径；加 `.mock-badge`「示例数据」 |
| 责任链 | `.chain` | `.role`（含 `.dot.run/.done/.wait`） | 容器 `role="list"`，子项 `role="listitem"` |
| 管道看板 | `.board` > `.lane`（`.stage-dropzone` 内 `.card`） | `.lane-head` `.card`（`.meta/.owner/.avatar/.evidence/.ci/.checkpoint/.move`） | 看板 `role="list"`；泳道 `data-stage`；卡片 `draggable` + `data-id`/`data-status`；`.ci-tag` 可承载 CI 状态、检查点、**跨空间域标签**（见 §8.9）；回顾区 `.lane.review` |
| 侧栏面板 | `.panels > .panel` | `.metrics-2` `.accept-item` `.insight` `.queue-item` | 面板 `aria-label`；`queue-item` `role="button" tabindex="0"` |
| 详情抽屉 | `.drawer-overlay` + `.drawer`（`.drawer-head/.drawer-body/.drawer-acts`） | `#drawerTitle/#drawerBody/#drawerClose` | 开关切 `.open` |

### 9.3 主题切换接入（theme.js 接管，页内零逻辑）

页内只需在 `.topbar` 末尾留一个空挂载点，由 `theme.js` 注入三态按钮：

```html
<div class="theme-switch" role="group" aria-label="主题切换"></div>
```

`theme.js` 已自动注入 `深色 / 浅色 / 系统` 三按钮（`data-curis-theme="dark|light|system"`）。页内**不得**再写主题切换代码。

### 9.4 mock 徽标注入点（铁律 #5）

结果条标题旁挂 `.mock-badge`：

```html
<h2 class="section-title">结果条<span class="mock-badge" style="margin-left:8px;">示例数据</span></h2>
```

`.mock-badge` 样式（页内或移入 shell.css）：

```css
.mock-badge{display:inline-flex;align-items:center;padding:2px 8px;border-radius:999px;border:1px solid var(--ui-line);background:var(--ui-surface-2);color:var(--ui-text-3);font-size:10px;font-weight:500;vertical-align:middle}
```

### 9.5 管道看板交互（拖拽 + 键盘等价 + 数据驱动）

- **数据驱动**：`stages` + `items` 两个数组 → `renderPipeline()` 注入泳道与卡片。
- **拖拽**（仅允许的内部流转）：卡片只有在当前角色有合法下一动作、且不跨越 CEO / 外部平台门禁时才可拖动；`drop` 必须调用统一 Runtime 状态入口，不能直接改 `v.stage`。`已批准`、`已排期`、`已发布`、`待反馈`、`已复盘`默认不可拖动。
- **键盘等价**（无障碍必需）：根据 `getActions(contentItem, currentRole)` 生成动作按钮，例如 `<button data-action="submit-review">提交审核</button>`、`<button data-action="approve-publish">批准发布</button>`；按钮执行同一 Runtime 状态入口，并显示禁用原因。
- **门禁反馈**：没有授权、证据或 CEO 审核时，主动作必须禁用并说明缺口；不能通过拖拽、键盘或详情抽屉绕过。
- **过滤**：`[data-filter="all|decision|attention"]` 切换 `currentFilter` 后重渲染（按 `v.status` 过滤）。
- **详情抽屉**：点击卡片 `openDrawer(v)`；`Escape` / 点遮罩 / 关闭按钮 `closeDrawer()`。

### 9.6 新业务克隆清单（Checklist）

1. 复制 `workspace-shell-reference.html` → 新文件 `workspace-runtime-<domain>.html`。
2. **导航**：15 个 `.nav-item` 全保留，仅把对应域页加 `.active`；不得删项、不得错标。
3. **顶栏**：52px 不动；`trust-pill`（数据可信态）、`ceo-badge`（待决策数）填该域真实值；保留空 `.theme-switch`。
4. **结果条**：写该域 `metrics`（北极星 + 辅助，每项带 `.caliber` 口径），挂 `.mock-badge`。
5. **责任链**：4 角色（含 CEO），用「角色 → 可验收结果」表达。
6. **管道**：4 活跃泳道 + 1 回顾区（`active:false`），命名贴合该域真实动线；卡片 `items` 写实内容（禁止「示例工作项 A」）。
7. **侧栏面板**：3 块固定（外部结果与验收 / 价值成本含投入产出比口径 / 洞察 + CEO 决策队列）。
8. **CEO 决策队列**：顶栏徽标 + 洞察面板内 `.queue-item`，与该域「CEO 在哪一刻介入」对齐。
9. 跑深/浅布局断言与内容状态动作断言（见 9.7）全绿；确认没有通用 `data-move`、没有示例数据触发外部动作，再提交。

### 9.7 DOM 断言校验（验收脚本指标）

Puppeteer 深·浅各跑一次，断言须全过：

```js
const checks = await page.evaluate(() => ({
  topbarH: Math.round(document.querySelector('.topbar').getBoundingClientRect().height), // 62
  navItems: document.querySelectorAll('.sidebar .nav-item').length,                       // 15
  lanes: document.querySelectorAll('.lane').length,                                        // 5
  panels: document.querySelectorAll('.panels .panel').length,                             // 3
  ceo: !!document.querySelector('.ceo-badge'),                                            // true
  mock: !!document.querySelector('.mock-badge'),                                          // true
  genericMove: document.querySelectorAll('[data-move]').length,                           // 内容工作台必须=0
  stateActions: document.querySelectorAll('[data-action]').length,                        // 内容工作台 >0
  activeNavText: document.querySelector('.sidebar .nav-item.active').textContent.trim(),  // 须=本域
  caliber: document.querySelectorAll('.metric .caliber').length,                          // 5
  polarText: document.querySelector('.metric span').textContent.trim()                    // 须=本域北极星
}));
```

- `accent` 计算值深= `#32f08c`、浅= `#1a1c1f`（冻结 tokens.css 官方值，非私有残留）。
- 内容发布工作台额外断言：`genericMove === 0`；每张卡片由状态与角色生成至少一个 `[data-action]`；审核、发布和结果回流动作必须能从 DOM 读出禁用原因或证据等级。
- 标杆示例：软件页 `activeNavText="⌨软件工作室"`、北极星「回归通过率」；小红书页 `activeNavText="✎小红书"`、北极星「平均收藏率」；短视频页 `activeNavText="▶短视频"`、北极星「完播率」；部门页 `activeNavText="▤部门"`、北极星「责任按期交付率」。

### 9.8 Content Workspace Studio DOM 与交互门禁

Studio 不能只证明“有画布和按钮”，必须证明它正在搭建一间可运行的业务空间。实现或原型验收时，
在深色、浅色和刷新后各执行一次以下断言；选择平台后，`platformVariant` 数量应与已选平台一致，
不允许用固定的抖音 / 小红书混合链路冒充通用配置。

```js
const studioChecks = await page.evaluate(() => ({
  studio: !!document.querySelector('[data-workspace-studio]'),
  mode: document.querySelector('[data-studio-mode]')?.textContent.trim(),
  outcome: !!document.querySelector('[data-studio-outcome]'),
  platformVariants: document.querySelectorAll('[data-platform-variant]').length,
  roleSlots: document.querySelectorAll('[data-role-slot]').length,
  presence: document.querySelectorAll('[data-presence-state]').length,
  replyPolicies: document.querySelectorAll('[data-reply-policy]').length,
  evidenceRules: document.querySelectorAll('[data-evidence-rule]').length,
  simulationStatus: document.querySelector('[data-simulation-status]')?.dataset.status,
  blueprintVersion: document.querySelector('[data-blueprint-version]')?.textContent.trim(),
  submitDisabled: document.querySelector('[data-studio-action="submit-approval"]')?.disabled,
  genericMove: document.querySelectorAll('[data-move]').length,
  englishRoleLabels: [...document.querySelectorAll('[data-role-slot]')]
    .filter((el) => /Research AI|Analysis AI|Script AI|Data AI|Review AI/.test(el.textContent)).length
}));
```

必须满足：

- `studio=true`，`mode` 为 `BLUEPRINTING` 或 `DRAFT`；保存草稿不改变运行版本；
- `outcome=true`，且至少有一个平台变体、五类责任槽位（研究 / 创作 / 发布 / 互动 / 复盘）和对应的 AI 在岗状态；
- `replyPolicies>0`、`evidenceRules>0`，并能在界面看到自动回复边界、外部回执和手动补录口径；
- `simulationStatus` 必须可读；不是 `PASS` 时，`submitDisabled=true`，且页面显示未通过原因；
- `genericMove=0`；Studio 的画布动作必须调用配置 / 模拟 / 审批 Runtime，不能直接推动 ContentItem 或运行版本；
- `englishRoleLabels=0`；用户可见岗位必须为中文，英文仅可作为内部标识；
- 刷新后 `mode`、版本号、模拟状态和缺口保持一致；若不能持久化，必须明确显示“仅为设计草稿”，不得伪装成已交付办公室。

以下证据仍不足以通过门禁：静态节点、按钮点击后跳转到决策室、只显示“未通过 3 项”、或仅凭一张画布截图。
通过门禁还必须有至少一条正常、一条未授权、一条平台变体不合法、一条 CEO 拒绝和一条模拟失败后的恢复记录。

---

**UI Designer**：UI Designer
**规范日期**：2026-08-04（2026-08-05 增补第四域实例与 §9.2 扩展说明）
**实现事实**：四域运行现场已证明统一 Shell、指标、责任链和管道布局；内容发布 Runtime 门禁、ContentItem 状态动作和真实外部结果仍未通过验收。
**QA**：旧版深 / 浅主题 DOM 断言只证明布局骨架；新的内容状态动作断言待原型修正后执行，不能把旧版全绿作为业务完成证据。
