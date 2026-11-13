# Curis UI Blueprint 升级审计工作稿

**Status: Review · READY FOR DESIGN**  
**日期：2026-08-14**  
**性质：唯一 UI Blueprint 的升级审计输入；不是第二份 Blueprint、不是 Product Blueprint、不是正式业务代码规范。**

## 1. 依据与边界

本审计只服务于原位更新 `docs/01_Product/Curis_Product_UI_Blueprint.html`。该文件已收敛为当前唯一 UI Blueprint；不新建 Shell / Talent Market / Workspace Blueprint。

当前 Consolidation 的上位依据：

1. `docs/01_Product/Curis_Product_Blueprint.html`（5.1，Status: Review）
2. 当前唯一 `Curis_Product_UI_Blueprint.html`
3. `Curis_RD_Workspace_Design_Brief.md`（Review state: `READY FOR DESIGN REVIEW`）与 `Curis_RD_Workspace_Reference_Synthesis.md`
4. `Curis_UI_Reference_Map.md`、`Curis_UI_Reference_Gap_Audit.md`
5. `docs/03_Design/Curis_Design_System.md`（Frozen）与 `AI_Capability_UI_Contract.md`（Review）

本稿 §§1–11 保留先前升级过程的审计记录；§12 是当前生效的 Design Preflight Consolidation，覆盖其中关于 Prototype 设计权威、Employee Workstation 首版行为和研发首版范围的旧表述。

本轮不修改 Product Blueprint、Master Map、Page Map、Runtime、数据库、接口或正式前端业务代码。原型中的内容均是**Curis 产品示例快照**，不代表运行事实、招募完成、连接已授权或业务已验收。

## 2. 结论先行

旧蓝图的“安静 CEO 工作空间、中文用语、按需详情抽屉、Workspace 可以是专业工作面”仍可复用；但其导航和页面树已不能表达 Product Blueprint 5.1。最小正确动作不是在旧“经营 / 公司 / 能力中心”外继续加页面，而是把现有文件原位收敛为六个冻结一级区域与统一的空间原语系统。

## 3. 旧 UI Blueprint 审计

| 旧内容 | 与 5.1 的关系 | 处理 | 理由 |
| --- | --- | --- | --- |
| CEO 工作台、公司简报、待处理、当前运行、结果入口 | 符合 | 保留并重写成首页首屏骨架 | 仍以 CEO 的“今天发生什么、要决定什么、去哪做事”为主，不做指标大屏。 |
| “经营 / 业务 / 公司 / 工作空间”五项一级导航 | 过时 | 移除为一级导航 | 5.1 已冻结：首页、业务空间、组织中心、人才市场、资料库、会议。 |
| “能力中心”作为一级或高可见中心 | 过时 | 退出一级 | Skill / Connector 在人才市场发现，在组织、设置和 Workspace 内按上下文配置；不能成为面向 CEO 的产品中心。 |
| 公司资源 / 成果库 / 知识库并列 | 部分过时 | 收敛为资料库 | 资料库承接本地、外部、公司产生、引用、权限和使用关系。 |
| AI 组织控制面、Runtime、Gate、Studio 等页面组织词 | 过度工程化 | 仅留给内部实现/Review，不作为用户导航 | 用户看到的是员工、责任、工作、结果和需要处理的事项。 |
| Meeting / Decision 作为上下文模式 | 部分符合 | 会议升级为冻结一级区域；决定保留为待处理与结果内的上下文 | 5.1 已将会议定为一级区域，不能再隐藏。 |
| Employee Detail Drawer、对象详情不打断工作 | 部分符合 | 保留“关闭后回到原工作”的返回原则，改为按任务选择 Inspector / Focus View / Full Workspace | 只有必须保持当前现场的局部信息才适合 Inspector；员工协作和完整专家介绍不应被压进右栏。 |
| Calm Executive Workspace、中文词表、低对比边界、单一主动作 | 符合 | 直接复用 Frozen Design System | 不再发明第二套视觉语言。 |
| Workspace 可用不同工作面、研发可有对话/文件/Diff/终端/测试/Review | 符合 | 保留为“Workspace 大画布”状态 | Workspace 不被统一 Dashboard 或后台面板限制。 |
| 创建公司引导 | 仍符合但不属本轮首屏 | 保留为后续状态，不占本阶段六区首屏 | 当前任务只交付 Desktop Shell 与六区首屏骨架。 |

## 4. 当前前端仅作现状识别

`TerraShell` 已提供 220px 侧栏、52px 顶栏、主题令牌与全局 Assistant；这证明令牌和壳层基础可复用，但不构成新体验已实现。`TerraNavData` 与 `TerraSidebar` 仍是旧“CEO 工作台 / 经营 / 业务版图 / 工作空间 + 更多”结构；人才市场已拥有专家/技能/连接器和右侧抽屉方向，资料库已有本地资料基础，会议页仍是规划占位。故本轮只把目标体验写入 UI Blueprint 和原型，不能把现有路由、接口或候选 UI 宣称为产品完成。

## 5. 旧 UI → 新 UI 的主变化

| 从 | 到 |
| --- | --- |
| 模块菜单和公司资产中心 | 六个用户工作区域；资产概念收敛为资料库，能力以人才市场和上下文装配出现。 |
| 固定左栏 + 顶栏 + 大面积页面 | 基础画布只保留固定一级侧栏 + 自由主工作区；其他空间只按任务出现。 |
| 把运行时/门禁/工作流术语暴露为页面结构 | 把内部结构翻译为“谁在做什么、需要我决定什么、结果来自哪里”。 |
| 员工、专家、能力容易混为公司对象 | 专家属于市场；只有招募后才成为组织中心员工；Skill 和 Connector 是可安装的职业能力/连接。 |
| Workspace 入口与统一运行台 | 业务空间只讲关系和结果；进入 Workspace 后由专业工作面接管，可进入大画布。 |
| 会议是上下文或纪要 | 会议是一级工作区：准备、讨论、资料、决定和后续责任要回到来源工作。 |

## 6. 第二轮修正：撤销“四栏 Desktop Shell”

### 6.1 上一轮错误

上一轮将“固定一级侧栏 + 上下文侧栏 + 主工作区 + 检查器”写成所有一级区域的默认四栏布局，并让多数对象点击进入 Inspector。问题不在四种空间本身，而在把它们误写为固定页面结构：CEO 工作台、业务空间、组织中心、人才市场和会议首页都因此失去宽主工作区；专家详情被压缩到 360px 右栏；“可折叠”也被误解为“默认存在”。

### 6.2 当前正式定义

> 基础画布 = 一级导航 + 主工作区。

Context Sidebar、Inspector、Dialog / Focus View、Popover 与 Full Workspace 都是按任务组合的空间原语：

| 先问什么 | 选择的空间 | 本轮示例 |
| --- | --- | --- |
| 这是用户当前主要工作吗？ | Main Workspace / Full Workspace | 员工直接工作、资料深度阅读、会议工作面、研发 Workspace。 |
| 用户只是暂时集中查看一个对象吗？ | Dialog / Focus View | 人才市场专家、Skill、Connector、业务与结果。 |
| 必须保持当前工作，同时查看或微调辅助对象吗？ | Inspector | 研发线程中的员工权限/文件属性；资料阅读中的来源/权限/引用。 |
| 需要持续浏览目录、层级或集合吗？ | Context Sidebar | 资料库的来源/文件夹；研发 Workspace 的项目/线程/文件/Review。 |
| 只是两三行状态或快捷操作吗？ | Popover | 通知、待处理提示、快捷筛选和上下文菜单。 |

“可折叠”现在的含义是：需要时出现，出现后允许用户折叠；不是默认存在后再让用户收起。

### 6.3 六区重新判定

| 一级区域 | 默认空间 | 需要时才出现的空间 |
| --- | --- | --- |
| 首页 / CEO 工作台 | 一级导航 + 宽主工作区 | Popover、Focus View、少量 Inspector。 |
| 业务空间 | 一级导航 + 宽主工作区 | 业务/结果 Focus View；进入 Workspace 后由 Workspace 决定。 |
| 组织中心 | 一级导航 + 大组织画布 | 员工 Focus View；真正工作进入员工 Full Workspace。 |
| 人才市场 | 一级导航 + 宽市场主区 | 专家/Skill/Connector 大 Focus View；招募时再开装配空间。 |
| 资料库 | 一级导航 + 资料 Context Sidebar + 主区 | 资料属性 Inspector；资料正文主区阅读。 |
| 会议 | 一级导航 + 宽主工作区 | 进入会议后成为 Full Workspace；复杂资料/参与者结构才加辅助空间。 |

## 7. 本轮需要 CEO Review 的问题

1. 默认是否采用深色主题（原型采用）还是跟随系统；结构和语义不受影响。
2. 第二侧栏默认宽度采用 256px，检查器采用 360px；这满足 1280px Desktop 的工作区下限，但更窄窗口需要优先收起检查器，是否接受。
3. 人才市场“招募”右侧装配是否先只展示公司身份、岗位、归属、权限与返回原工作，还是第一阶段就展示完整成本/版本/授权矩阵。
4. 业务空间首屏用“业务 → Workspace → 最近结果”的关系阅读，研发 Workspace 则采用大画布；首个要进入正式 UI Design / Business Runtime Review 的垂直 Workspace 仍需 CEO 选择。
5. 会议“需要准备”与 CEO 工作台“待处理”必须来自同一事实源；本原型只表达共享入口，尚不证明数据契约。

## 8. 交付状态

- 唯一 UI Blueprint：`docs/01_Product/Curis_Product_UI_Blueprint.html`，已原位升级，`Status: REVIEW REQUIRED`；该状态已由 §12 的 `Status: Review · READY FOR DESIGN` 覆盖。
- 可点击视觉原型：`docs/01_Product/Curis_UI_Blueprint_Prototype.html`，仅证明空间、信息架构、密度和交互方向。
- 下一步：CEO Review 通过公共 UI 契约和六区首屏后，专项设计只能合并回同一份 UI Blueprint；随后才可由独立正式 Issue 进入业务代码与 Runtime 验证。

## 9. Phase：完整产品高保真原型

### 9.1 本轮不再接受的替代品

“一张卡片 + 一段说明 + 未来这里显示”不能再作为产品空间设计的替代。本轮每个影响 Curis 形态的空间均有明确 UI 结构、示例状态、点击入口和返回关系；但仍只属于 Blueprint Prototype，不构成真实业务能力或 Runtime 证据。

### 9.2 新增具体决策

| 主题 | 决策 | 原因 |
| --- | --- | --- |
| 组织关系 | 采用“组织结构 / 协作关系 / 员工”三视图，而非单一树或纯文字链路 | 树回答归属和汇报，关系网络回答共享员工正在哪些业务 / Workspace 协作，员工视图支持查找。 |
| 人才市场 | 采用成熟市场主区 + 大 Focus View；专家卡不承担完整档案 | 专家介绍、能力、案例、来源、状态和招募需要足够的阅读与判断空间。 |
| 招募 | 用五步 Focus View 装配：专家 → 公司身份 → 业务 / Workspace → 能力 / 资料 / 授权 → Employee | 保持专家 ≠ 员工，也让 Department 保持可选，而不是招聘前置。 |
| 模型缺口 | 招募前发现缺模型时转 Settings / 模型，测试后返回原招募第 4 步 | 真实地表达“能力缺口可修复”，但不伪造凭据、Provider、健康或执行。 |
| 员工 | 进入员工工作面采用中央直接对话；配置仅按需打开 Inspector | 员工是持续协作对象，不是组织列表旁的详情卡。 |
| 研发 Workspace | 采用 IDE / Coding Agent 密度：线程、团队、文件、Diff、Terminal、Test、Review 与交接 | 体现 Curis 外壳内嵌成熟研发工作方式，而非再画一张 Dashboard。 |
| 小红书 Workspace | 采用内容周期、目标、内容日历、选题池、制作、审核、发布和复盘 | 让图文内容运营看起来像一间办公室，而不是 Workflow DAG 或任务列表。 |
| 短视频 Workspace | 采用脚本、素材、剪辑、审核、发布、播放 / 完播 / 互动 / 转化反馈生产面 | 短视频天然不同于图文；两者只共享 Curis 的公司与经营对象。 |
| 会议 | Company Meeting 用自然讨论流 + 引用 + 异议 / 方案 + Decision Proposal | 会议不能退化为纪要编辑器，Decision 必须带责任和返回来源。 |
| 设置 | 头像只保留账户 Popover；设置为独立 Settings Workspace | 清除长期可见“设置”二级入口；设置可持续扩展而不污染六区导航。 |

### 9.3 事实边界

- `GitHub / Git`、小红书发布渠道和任何模型 Provider 都只展示发现、待授权或示例测试状态；没有真实认证、账号、健康或平台数据。
- 内容发布、阅读、互动、涨粉、播放、完播、转化和会议批准均不作为真实完成事实；原型明确显示“待连接 / 人工回填 / 未记录 / 示例”。
- 原型创建的 Company、Employee、Decision 只在浏览器内存状态中演示路径，不写数据库、不调用 API、不修改 Runtime。

### 9.4 下一步

CEO Review 通过具体形态后，仍须以单独 Issue 选择一个垂直 Workspace 进入真实 UI / Business Runtime 设计与验证；其他专项只合并回同一份 UI Blueprint，不能形成平行 Blueprint。

## 10. Phase：Reference-Driven UI Redesign

### 10.1 本轮 Review 不通过的根因

上一版虽然列出 Workbuddy、Coze、Codex、Claude Code、ChatGPT、Linear、Notion、Relevance AI、EvoFlow 与 OpenOPC，却主要把需求清单翻译为卡片、说明文字、文字按钮和固定面板：对话被做成右下 Assistant 气泡，研发将 Thread / Diff / Terminal / Review 同时铺开，会议近似静态发言与 Proposal 版面，Context Sidebar 也被放进业务内容 `.content` Grid。问题不是缺少更多功能，而是没有把成熟产品的连续工作方式落实到空间。

### 10.2 本轮新增研究工作稿

1. `docs/01_Product/Curis_UI_Reference_Map.md`：将现有研究映射到 Shell、四种对话、市场、员工、三类 Workspace、资料库、设置与长任务；明确直接吸收、不复制和 Curis 的公司化补充。
2. `docs/01_Product/Curis_UI_Reference_Gap_Audit.md`：逐场景记录当前实现、参考产品、为什么不自然和修正方式。

点名的 `Curis_Product_Experience_And_Competitor_Audit_2026-08-10.md` 未在当前主目录、受控附件或可检索非依赖文件中发现。本轮没有捏造其结论，而以 2026-08-13 产品重新推导中的正式参考机制矩阵，以及现有 Coze、EvoFlow 与 UI 审计材料为输入；若原文件后续迁回主目录，只补证据，不自动越权覆盖产品边界。

### 10.3 已原位修正的 Prototype 结构

| 旧形态 | 新形态 |
| --- | --- |
| `.content` 内的 `contextlay` | Shell sibling Context Sidebar：只在资料库、研发 Workspace 与设置按需出现；收起后主区扩展。 |
| “继续对话”文字按钮或右下静态 Assistant 气泡 | CEO、Workspace、Employee、Meeting 各自拥有 Conversation Stream 与底部 Composer；CEO Assistant 只作全局按需能力。 |
| 研发把 Thread、文件、Diff、Terminal、Review 永远并列 | 项目 Context Sidebar → 当前 Thread → Conversation；文件、变更、终端、审查为当前工作切换。 |
| 图文与短视频同时展示整套生产流程 | 当前内容 / 当前视频 + 团队 Conversation；内容集合、素材和资料按阶段切换。 |
| 会议是静态发言与 Proposal 区块 | 顶部议题 / 参与者，中央多人 Conversation，底部 Meeting Composer；Proposal 在讨论中产生，按需查看。 |
| 市场卡片和详情夹杂大量设计说明 | Workbuddy 式紧凑市场卡、完整专家 Focus View、单一“招募” CTA；市场专家到 Employee 的装配路径保留。 |

### 10.4 验证边界

静态 HTML 已用浏览器实际点击核对：首页 → 研发 Workspace 的 Context Sidebar / 折叠 / Composer；组织 → Lin 员工对话 / Composer；员工 → 产品方向会议对话 / Composer；市场 → 专家 Focus View；资料库 → Shell Context Sidebar + 主区阅读；小红书 Workspace → 当前内容 Conversation。此证据仅说明原型交互和空间方向，不能证明模型、Connector、员工、会议、发布、数据、决定或恢复已真实接通。

### 10.5 下一步

继续保持唯一 UI Blueprint 的 `REVIEW REQUIRED`。CEO Review 应评估“是否自然地使用”，而非“每项需求是否都有卡片”；任何正式业务实现仍需独立 Issue、真实 Browser/Desktop、持久化、失败恢复与 Business Runtime 证据。

## 11. Workspace + Capability Recovery 同步审计（2026-08-14）

### 11.1 本轮上位依据

唯一 `Curis_Product_Blueprint.html` 已在原文件内补齐 Workspace 模型与能力回收，状态为 `Review / Workspace + Capability Recovery Review Required`。本轮只将已确认语义翻译回唯一 UI Blueprint 与现有 Prototype；不修改 Product Blueprint、Master / Page Map、Runtime、API、Schema、数据库或正式业务代码。

### 11.2 已发现的 UI 偏差与原位修正

| 偏差 | 风险 | 本轮修正 |
| --- | --- | --- |
| Workspace 仍被描述为单一 Conversation 主轴 | 容易退回中央团队群聊，员工看起来像联系人而非工作者 | 固定为“专业业务应用 + 多 Employee Workstation + 自动工作现场”；Employee Workstation 位于 Main Workspace，可同时缩小、展开、拉高、拉宽、聚焦、最大化、恢复。 |
| Context Sidebar 的允许内容不够严格 | 容易把员工列表塞回第二栏 | 明确仅放项目、Thread、资料目录、文件、业务对象、历史；员工 Workstation 不属于 Context Sidebar。 |
| `Inspector` 被误解为固定右栏 | 专业 Workspace 会被压缩，成果 / 配置 / 预览被混成一栏 | 正式更名为 Flexible Utility Pane：按当前对象变化、可隐藏/展开/调宽；研发显示 Code / Diff / Terminal / Test / HTML / Artifact，小红书显示图文 / 发布预览 / 数据 / 任务，抖音显示视频 / 脚本 / 素材 / 字幕 / 封面 / 数据。 |
| 自动化缺少普通用户语言 | 可能重新出现 Workflow / Scheduler / Runtime Console | 只表现下一次运行、当前运行、负责员工、阶段、下一步、等待原因、需要我、失败、恢复；自动与人工继续同一 Employee Session。 |
| 会议仍可能沦为纪要或常驻右栏 | Proposal 与资料挤压 Conversation，决定无法回到工作 | 会议改为自然多人 Conversation，AI 轻量识别结构标签，Proposal 按需出现；Decision 形成 Assignment / Owner / Checkpoint，回到来源 Workspace 与 Employee Workstation。 |
| Studio 只像创建向导 | 无法表达已运行办公室的安全演进 | Studio 增加当前运行版本 / 待修改版本、影响预览、测试这次调整、确认启用、恢复上一版本；不暴露 Draft / Simulation / Rollback 或自由 DAG。 |
| 小红书、抖音继承研发布局 | 专业工作面只是同一模板换名字 | 小红书明确总览 / 发布日历 / 内容 / 数据 / 自动化；抖音明确总览 / 内容计划 / 视频 / 素材 / 数据 / 自动化；二者各自围绕内容 / 视频对象与不同 Pane 工作。 |

### 11.3 本轮 Prototype 验收路径

1. 研发 Workspace → 多个 Workstation → 展开 Codex 开发员工 → 输入要求 → Diff / HTML / Test Pane → 恢复团队视图。
2. 小红书 → 总览 → 发布日历 → 自动任务 → 文案 Workstation → 当前图文发布预览。
3. 会议 → 多员工讨论 → Fact / Opinion / Evidence 标签 → Proposal → CEO Decision → Assignment → Employee Workstation。
4. Workspace Studio → 当前运行版本 / 待修改版本 → 影响预览 → 测试这次调整 → 确认启用 / 恢复上一版本。
5. 头像 → 账户 Popover → 独立 Settings Workspace → 返回原工作。

### 11.4 仍需 CEO Review

1. 多个 Workstation 的默认恢复策略、初始展开数量与最大化后恢复位置。
2. Decision 回驱 Workspace 是自动继续，还是始终等待 CEO 明确继续。
3. 真实平台数据、模型 / Connector 授权、健康、成本、发布与恢复的正式 Runtime / 数据合同。
4. 首个进入正式 UI / Business Runtime Review 的垂直 Workspace 与真实结果链。

## 12. Design Preflight Consolidation（2026-08-14）

### 12.1 目的与范围

本轮在进入 Design AI 前，把此前暂缓写回的全局 UI 原则与 `Curis_RD_Workspace_Design_Brief.md`（`READY FOR DESIGN REVIEW`）的已完成研发研究结论，原位收回唯一 UI Blueprint。

只更新：

- `docs/01_Product/Curis_Product_UI_Blueprint.html`
- 本审计稿。

不更新 Product Blueprint、Prototype、Runtime、代码、数据、Master Map 或 Page Map。

### 12.2 为什么 Prototype 不再是设计真源

当前 `Curis_UI_Blueprint_Prototype.html` 是早期空间与点击路径的示例快照；它不具备直接研究证据、完整视觉系统裁决或专项设计取舍的权威。它现在正式标记为：

> `REFERENCE ONLY / NOT DESIGN AUTHORITY`

后续 Design AI / Figma 以唯一 UI Blueprint + 对应专项 Reference Research / Design Brief 工作，而不是延续 Prototype 的卡片、按钮、尺寸或临时交互。Codex 也不再由 Product Blueprint 自行推导页面视觉；Approved Design 后才进入实现。

### 12.3 新增全局原则

| 原则 | 已收口的 UI 约束 |
| --- | --- |
| Low Surface Complexity, High Functional Density | 默认视口只显示当前任务立即需要的信息和动作；能力通过对象点击、`+`、`···`、Popover、Context Menu、Hover、按需 Sidebar / Utility / Focus 出现。禁止大量 Button、Card、永久 Tab、固定工具栏和能力全开。 |
| Progressive Disclosure | L1 Always Visible = 当前工作核心；L2 Contextual = 当前对象需要；L3 On Demand = 用户主动调用；L4 Advanced / Internal = 普通用户默认不见。任何可见控件都必须能回答“为什么现在需要看到”。 |
| 完整产品先定形，真实能力分阶段接通 | Provider / Agent / Connector / Permission 只能如实显示 `AVAILABLE`、未连接、未安装、需要授权、需要配置、健康未知、不可用、未来接入、阻塞或未知；不得用示例数据伪造真实接通。 |
| Provider-Native Workstation | Curis 统一 Employee Identity、Role、Responsibility、Status、Current Work、Workspace Context、Handoff、Company Permission、Result Return；Provider 负责已验证的 Conversation、Composer、Mode、Model、Context、Skill / Tool 与专业执行行为。 |

### 12.4 Employee Workstation 最终首版行为

| 项目 | 最终规则 |
| --- | --- |
| 视觉状态 | 仅 `Collapsed` 与 `Expanded`。删除显式 Focus、Maximize、拉宽、拉高按钮；Expanded Conversation 可自然调整高度。 |
| 默认展开 | `working`、`needs_ceo`、需要处理的 `failed` 展开；`idle`、`waiting`、`completed` 收起；多个并行 working 可同时展开。 |
| Handoff | 接受后发送方自然收起、接收方展开；拒绝或上下文不足时回到发送方或显著进入 Needs CEO。 |
| 用户布局 | 当前访问期间尊重用户手动收起；自动、人工介入、失败恢复和 Handoff 继续同一责任 Session。 |
| Session Management | 首版移出。默认继续责任 Session；责任真正变化才创建 / 切换新 Session；Session History 为 Reserved。 |

### 12.5 研发首版范围收窄

| 面 | DESIGN NOW | 移出首版 |
| --- | --- | --- |
| Composer | 自然语言输入、`+`、一个 Mode Selector、Model、Send / Stop；`+` 聚合文件、文件夹、图片、资料 / Context 与低频能力；Permission 仅在需要授权时出现。 | Skill、Tool、Knowledge、Plugin、Permission、File、Goal、Model 等永久横排；多个永久 Mode 按钮。 |
| Context Sidebar | 当前 Project / Workspace、Responsibility、相关文件 / 目录、Recent Work / Recent Object。 | Employee、Session Manager、Handoff Queue、Permission Center、Result / Review Detail、Tool Catalog、Model、Skill、完整 Git / Worktree。 |
| Utility Surface | 默认关闭；Code / Source、Diff / Changes、Preview / Result；Test Result 仅在理解结果确实需要时出现。 | 首版：Terminal、Git、Branch、Worktree、Review、External Editor、Session History、Permission Detail、Background Work。Later：Commit / Push / PR、Debug、Scheduled Work、Autopilot、Voice、Multiple Utilities、Advanced IDE。 |
| Conversation | Agent 自然输出、工作说明、当前状态、轻量活动、轻量 Result 引用。完整 Artifact 从“查看”打开 Utility Surface。 | 在消息正文中铺完整 Code、Diff、Preview、Terminal、Test。 |

### 12.6 参考方法升级

重要参考不再写成“参考 Codex：Diff / Terminal / Test”。每个参考至少记录 Product Object、Spatial Model、Interaction、Functional Layout、Visual Language：它管理什么、为什么放这里、入口/展开/关闭/返回、默认/隐藏内容、菜单和降低复杂度的视觉方式。

研发边界已固定为：Coding Agent Conversation 主要参考 Codex；Context / Editor interaction 参考 Cursor / VS Code；Plan / Permission 参考 Claude Code；专业工具空间参考 VS Code；Handoff / Needs Human 参考 Relevance AI 等。Curis 不机械拼贴任何竞品，只补回 Employee、Role、Responsibility、Automatic Handoff 与 Company Result。

### 12.7 后续权威链与状态

```text
唯一 Product Blueprint
→ 唯一 UI Blueprint
→ 专项 Reference Research / Design Brief
→ Design AI / Figma
→ Approved Design
→ Codex Implementation
```

本轮后 UI Blueprint 的状态为 `Status: Review · READY FOR DESIGN`。研发专项 Design Brief 已是 `READY FOR DESIGN REVIEW`。小红书、抖音 / TikTok、会议、Workspace Studio、人才市场、组织中心与资料库仍等待各自专项研究和设计；本轮不重做它们。
