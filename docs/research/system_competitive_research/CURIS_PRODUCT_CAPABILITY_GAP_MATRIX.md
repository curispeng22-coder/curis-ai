# CURIS PRODUCT CAPABILITY GAP MATRIX

> Authority Class: RESEARCH / EVIDENCE
> Status: v1 COMPLETE（Curis 状态列依据 CURRENT_STATE / Structure Baseline / 各 Accepted Review；竞品对照列随各 FUNCTION_INVENTORY 交叉引用）
> Date: 2026-09-12
> 规则：Curis 状态只用八档：`COMPLETE / IMPLEMENTED BUT WEAK UX / PARTIAL / RUNTIME ONLY / UI ONLY / NOT IMPLEMENTED / NOT DESIGNED / UNKNOWN`。
> **Runtime 存在 ≠ Product 完成。** 依据均为 docs/00_Context/CURRENT_STATE.md 与 PRODUCT_DOCUMENT_POINTER.md 登记，不使用历史 checkpoint 覆盖 Current。

## 1. 七个一级产品区

| # | Capability | Curis 状态 | 证据 / 缺口 | 竞品均已有 | Gap 定性 |
|---|---|---|---|---|---|
| 1 | CEO 工作台（注意力/事项/简报/结果/决定） | IMPLEMENTED BUT WEAK UX | Batch1 + Whole-App Live AI accepted；但空态=零值仪表、注意力优先级缺失（见 UI AUDIT §2） | ChatGPT Projects 首页 / Devin dashboard / Manus 首页均有"今天要做什么"主行动 | 注意力模型有 Runtime，无成熟 Surface |
| 2 | 业务空间（Business + Workspace 目录/入口） | IMPLEMENTED BUT WEAK UX | Scope/Phase B closure accepted；页面仍后台目录式（UI AUDIT §3） | Coze workspace/team space、Manus sessions、Cursor projects | 结构领先，空间"进入感"缺失 |
| 3 | 组织中心（公司版图/员工目录） | IMPLEMENTED BUT WEAK UX | 两 Tab UI accepted；Search/Filter wiring、Dark/1024 为 P2 | Workbuddy 专家中心、Coze 团队空间成员管理 | 领先：真实组织树 vs 竞品均为扁平 agent 列表 |
| 4 | 人才与能力（专家发现/招聘/Employee/Skill/Capability/Provider binding） | PARTIAL | Talent & Capability IMPLEMENTED/ACCEPTED，但外部 Connector 授权/执行、外部 provider、unsupported Skill、Capability 用户语言均为 bounded gap；**无 Expert/Marketplace 级浏览体验**（UI 证据缺位，UI AUDIT §8） | Workbuddy 专家中心 140+ 专家/SkillHub 7 万+技能/连接器市场；Coze 插件市场；GPT Store | Curis 有组织化 Employee 模型（领先），但发现/安装/理解能力的产品面远落后 |
| 5 | 经营洞察（Analyst/趋势/比较/归因/报告/Decision support） | IMPLEMENTED BUT WEAK UX | Operating Intelligence IMPLEMENTED/ACCEPTED；外部 Outcome/Feedback connector、自动报告 authoring 为 gap | ChatGPT Deep Research、Manus 报告交付 | 分析→P7 决策链独有；数据接入面缺失 |
| 6 | 资料库（Company Reference Space） | IMPLEMENTED BUT WEAK UX | Knowledge Library IMPLEMENTED/ACCEPTED（Figma 187 基线）；格式/连接器、语义检索、引用/版本、ACL、graph、去重、retention 为 bounded gaps | Claude Projects knowledge、Coze Knowledge（表格/图片/分段/检索配置）、ChatGPT 文件 | Curis 引用→Work→Evidence 溯源链独有；检索与接入面落后 |
| 7 | 会议（多人经营讨论） | PARTIAL | Meeting CORE IMPLEMENTED / autonomy ACCEPTED CANDIDATE；final multi-cycle real-world evidence pending | 无竞品有"AI 员工会议"对等物（Coze multi-agent 对话最接近） | 组织语义独有；产品打磨与证据未闭合 |

## 2. 全局能力

| Capability | Curis 状态 | 证据 / 缺口 | 竞品参照 | Gap 定性 |
|---|---|---|---|---|
| 全局 CEO Assistant（浮层、跨区、可拖动） | PARTIAL | Phase B E 已集成验证；但 UI 资产无 Composer 证据、回复无结构（UI AUDIT §9） | Claude/ChatGPT 全局助手、Zcode 会话 | Runtime 已通；Surface 未成熟 |
| Conversation（CEO↔Employee，attention lifecycle） | IMPLEMENTED BUT WEAK UX | Conversation Attention Lifecycle IMPLEMENTED/ACCEPTED；Model Selector/Composer 曾登记 Partial/P1 | 全部竞品以 Composer 为第一公民 | 事件模型独有；输入面与呈现成熟度低 |
| Composer（附件/模型选择/工具开关/命令） | PARTIAL | Shared Composer Shell 合同 Frozen（X10）；实现与截图证据薄 | Claude/ChatGPT/Cursor/Manus 全量字段 | 合同有、成熟面无 |
| Work 执行（Employee delegated work, real model） | IMPLEMENTED BUT WEAK UX | Whole-App live AI accepted（DeepSeek 链）；no-key 委托 PLANNED | Manus/Devin/Zcode 执行链 | 独有责任链；进度可视化缺失（对照 Z1-Z3） |
| Result / Evidence / Artifact 链 | IMPLEMENTED BUT WEAK UX | Result→Evidence→P7→回流 accepted；Result Utility 独立副本验证 | Claude Artifacts、Manus deliverables、Devin replay | 溯源独有；Result 最终工作面是 Current P1 |
| Usage Ledger（统一用量/成本） | RUNTIME ONLY | 唯一 Usage Ledger 贯通四层 scope；无用户侧成本/用量 Surface | 竞品：Cursor usage 面板、Coze credits、Devin ACU、Manus credits | 需要 Settings/页面级消费面 |
| Model Management（provider/key/模型） | PARTIAL | Model Management UI accepted；Keychain/DeepSeek 云连续性 accepted；Provider 架构当前单一 proven | Cursor（多 provider+自定义 key）、Coze（多模型参数）、ChatGPT（模型选择） | 多 provider 产品面与每员工模型配置缺 |
| Skill 安装/绑定 | PARTIAL | Skill Installation + Employee Capability Binding accepted；触发语义/用户语言缺（对照 Z5） | Workbuddy SkillHub、Coze 插件、Claude Skills、Zcode skills | 有绑定无"能力市场语言" |
| MCP / Connector | PARTIAL | MCP/Connector Registry（Review）；Connector truth 未连接/需授权；外接执行未验收 | Claude MCP 全配置面、Zcode MCP、Coze 插件/MCP | 设计在先、产品面缺失 |
| Automation / 定时任务 / 触发器 | NOT DESIGNED（D 代 XHS Workspace 原型有"自动化"Surface，UI ONLY） | 无产品定义/实现登记；Meeting advancement cycle 为内部 Runtime 机制 | ChatGPT Tasks、Manus scheduled jobs、Workbuddy automations（本地一手证据：trigger+memory+飞书推送） | 全档缺失，竞品已普及 |
| Notification / 待办提醒 | PARTIAL | CEO Desk attention projection 承载；无系统级通知面 | 全部竞品有通知中心 | 需要通知模型 |
| Memory（公司记忆/偏好/长期记忆） | PARTIAL | 共识归档、Knowledge 沉淀、Meeting 决议归档为 Runtime 机制；无用户可理解 memory 面与编辑能力 | ChatGPT Memory、Manus knowledge/memory、Coze 长期记忆 | 需要产品化 |
| Global Object Search | UI ONLY（D 代原型有 `10-global-search.html`）→ NOT IMPLEMENTED | CURRENT_STATE Remaining Core P1 明示；实现无 | 竞品全部具备（ChatGPT search、Claude search、Linear 式 ⌘K） | 明确 P1 |
| Settings（模型/员工/权限/隐私/数据/外观…） | UI ONLY + PARTIAL 实现 | D 代原型有五类 IA 骨架（个人偏好/公司设置/AI 与能力/权限与数据/运行与成本，UI ONLY）；实现仅"公司设置"本地草稿（公司档案/品牌主题/通知偏好）；模型管理入口 + 左下 CEO 头像路径已登记 | 竞品 Settings 均为多节完整面（见 SETTINGS_MATRIX） | 需要完整 Settings IA 与实现 |
| Permission（员工执行授权/工具白名单） | RUNTIME ONLY | Scope/授权/溯源 Runtime 贯通；无用户可读"这个员工能做什么"面（对照 Z4） | Claude tool permission、Cursor allowlist、Devin org policy | 政策面缺失 |
| Multi-Workspace 并行（parallel multi-Work） | NOT IMPLEMENTED | Professional Workspace 策略登记为 Gap；sequential cross-professional multi-Work 已 proof | Devin parallel sessions、Manus 并行任务、Zcode background tasks | 结构性缺口 |
| Professional Workspace（Surface 投影/Package↔Work 映射） | PARTIAL | Package v2 foundation + XHS G2 accepted（mixed source）；Surface/UI projection、Package↔Runtime Work mapping 未完成 | （无直接对等；最接近 Coze workflow+plugin 组合） | Curis 独有方向，实现中 |
| Workspace Engineering（Package 生命周期/Evolvable） | PARTIAL | P0/P0.5/P1/P1.5 bounded accepted；Evolvable NOT ACCEPTED；marketplace/update 排除 | Coze workflow 版本、Dify 应用编排 | 独有；演化能力未闭合 |
| Computer Access（本机操作） | NOT IMPLEMENTED | ADR-0046 冻结 authority；Runtime Delta Plan 仅规划 | Claude Computer Use、Manus VM、Devin browser、Zcode computer use | 已决策未实现 |
| 通知式 Handoff（员工间交接） | RUNTIME ONLY | Responsibility routing/handoff Runtime + Quick Panel 交接字段（B 代截图）；无交接收件箱/流面 | Coze handoff、Devin slack assign | 缺 Surface |
| Meeting→Decision→Work 闭环 | IMPLEMENTED BUT WEAK UX | Proposal→P7→CEO Decision→Work→Result→Evidence→Leader 再评估 accepted | 无竞品对等 | 独有强项；UI 呈现待 Final UI |
| Dark / 1024 / Accessibility | NOT IMPLEMENTED | 多个 acceptance 记为 P2 | 竞品桌面普遍支持 | 打包债务 |
| 多租户/计费/Marketplace 生态 | NOT DESIGNED | 既有裁决明确暂不建设（v1 self-use 红线；L2 Gate 管控） | Coze/Workbuddy 已商业化 | 按裁决缺席，非缺陷 |
| Voice | NOT DESIGNED | 无登记 | ChatGPT voice、Coze voice | 缺席 |
| 桌面分发（GitHub Beta DMG/notarization） | PARTIAL | Stage A 策略 Frozen；closure gate 未完成 | 竞品均有安装面 | 分发流程未闭合 |
| Desktop-specific（菜单栏/全局快捷键/overlay） | NOT DESIGNED | 无登记 | ChatGPT desktop overlay、Claude desktop、Zcode sidecar | 桌面差异化能力缺 |

## 3. 汇总计分（按档计数）

| 状态 | 数量 | 说明 |
|---|---|---|
| COMPLETE | 0 | 无任何能力达到完整产品闭环 |
| IMPLEMENTED BUT WEAK UX | 8 | 七区中 5 个 + Conversation + Work + Result 链 |
| PARTIAL | 11 | 人才与能力、会议、Assistant、Composer、Model、Skill、MCP、Notification、Memory、Settings、Professional Workspace、Workspace Engineering、分发 |
| RUNTIME ONLY | 4 | Usage Ledger、Permission 面、Handoff 面 |
| NOT IMPLEMENTED | 4 | Global Search、parallel multi-Work、Computer Access、Dark/1024/A11y |
| NOT DESIGNED | 5 | Automation、Desktop-specific、Voice、多租户/Marketplace（裁决性缺席）、— |
| UI ONLY | 0 | 无只有设计没有运行的能力（方向健康） |
| UNKNOWN | 0 | — |

**核心结论**：Curis 的独有资产全部在**组织与经营语义层**（Employee/Responsibility/Meeting/Result→Evidence→Decision），这一层没有任何竞品有对等物；而**通用 AI 桌面产品层**（Composer/进度可视化/结果呈现/Settings/Automation/Notification/Search/Marketplace 语言）几乎全面落后于 2026 年竞品标配。Gap 的本质不是"缺 Runtime"，是"Runtime 之上没有产品面"。

## 4. 更新记录

- 2026-09-12 v1：基于 CURRENT_STATE + Pointer + UI AUDIT 建立；竞品对照列待各 INVENTORY 返回后细化（不改变 Curis 状态列）。
