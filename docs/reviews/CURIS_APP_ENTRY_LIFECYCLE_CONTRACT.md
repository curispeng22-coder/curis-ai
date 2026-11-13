# CURIS V1 — FIRST OPEN / COMPANY INITIALIZATION LIFECYCLE CONTRACT

**Status:** Review
**Authority Class:** REVIEW / PRODUCT + INTERACTION CONTRACT
**Disposition:** READY FOR CEO / CHATGPT REVIEW
**Scope:** App Entry、Company 初始化与 Create Business Flow 的边界；不含视觉设计或实现授权

> 本文件修正 App Entry 生命周期的层级。它不推翻 `CURIS_CREATE_BUSINESS_FLOW_CONTRACT.md`，而是把该合同放在 Company 已存在之后复用。它不修改 Product Blueprint、Master Map、UI Blueprint、Runtime、Schema、DB、Frontend、Prototype 或 Figma。

## 1. PRODUCT HIERARCHY

Curis 的产品对象层级固定为：

`Curis → Company → Department → Business → Workspace`

- Curis 是当前产品品牌，不是 Business 或 Runtime identity。
- Company 是用户第一步建立的公司经营容器。
- Business 必须属于 Company 的 Department；Workspace 属于真实 Business。
- Company、Business、Workspace 不能在产品入口中被隐式跳过或用默认对象伪造。

因此，“打开 Curis”“创建 Company”“准备 AI 能力”“创建第一个 Business”是四个不同层级，不得合并成一张直接从 Intent 创建 Business 的首屏。

## 2. FOUR APP LIFECYCLE STATES

### STATE A — PRE-COMPANY

条件：Curis 已安装并打开，但当前身份下尚无 Company。

目标：让用户快速理解 Curis 是帮助其建立和经营 AI 公司的产品，并创建第一家 Company。

此状态的首要动作是创建 Company，不是回答“你想开始做什么业务”。不显示伪造的 Business、Department、Employee、Workspace、Result 或活动。

PRE-COMPANY 内允许一个不创建 Company 的合法呈现模式：`EMPTY CURIS`。它不是第五个 Company lifecycle，也不是 Demo；只是用户选择暂不初始化后的真实空壳状态。

### STATE B — COMPANY EXISTS / AI NOT READY

条件：Company 已创建，但没有可工作的 Model / Provider / Agent execution capability。

产品语言：

> 你的 AI 公司已经建立，但还需要连接 AI 能力，AI 员工才能真正开始工作。

Company 存在不等于 AI execution ready。此状态可以展示 Company、身份、设置和恢复入口；任何需要模型推理的理解、研究、提案、员工执行或 AI Result 必须等待 AI Ready。

### STATE C — COMPANY READY / NO BUSINESS

条件：Company 存在，AI 能力 Ready，但尚无 Business。

Curis 已经是一家可以工作的 AI 公司，只是还没有具体业务。此时进入正常 Curis Shell 的 Empty Company State，主任务是“开始第一个业务”。从这里才进入 `CURIS_CREATE_BUSINESS_FLOW_CONTRACT.md`。

不显示伪造的 Business、Workspace 或经营活动；可以进入必要的 Company 设置、能力入口和 CEO Assistant Conversation。AI Ready 时，Conversation 可承接第一个 Business；未 Ready 时，Composer 显示模型缺口并可返回模型配置。

### STATE D — OPERATING

条件：Company 存在且至少有一个 Business。

正常重新打开默认进入 CEO 工作台 / Company Operating Experience。创建新业务是已有产品中的普通 Action，复用同一 Create Business Flow，不重新进入 First Open，也不重复创建 Company。

## 3. CURIS FIRST OPEN

首次打开的最小理解应是：

> 欢迎来到 Curis。Curis 帮你建立并经营属于自己的 AI 公司。AI 员工可以替你研究、执行、协作和汇报；你主要负责目标与关键决定。

这不是官网 Landing Page、Marketing Website 或十屏 Feature Tour。用户已经在 App 内，路径可以是：

`快速理解 Curis → 创建 Company`，或 `快速理解 Curis → 先看看 Curis`

Welcome 必须提供两个合法 Action：

- **Primary：创建我的 AI 公司 / 开始设置**：进入 Company creation。
- **Secondary：先看看 Curis**：`SKIP = ENTER CURIS WITHOUT INITIALIZATION`，进入 Empty Curis Shell；不是取消产品，也不是隐蔽的法律式跳过。

具体 copy 由后续 Design 确定，但语义不可丢失。不要在 PRE-COMPANY 首屏要求用户填写行业、业务、Department、Employee、Workspace、Capability、Workflow、Provider 或 Strategy。

## 3.1 EMPTY CURIS STATE

条件：`Company = 0`，且用户在 Welcome 选择“先看看 Curis”。

Empty Curis 进入真实 Curis App Shell，可浏览七区产品结构，但所有区域只表达真实空态：

| 产品空间 | Empty Curis Truth |
|---|---|
| CEO 工作台 | 未建立 Company 的真实空态 |
| 业务空间 | 无 Business |
| 组织中心 | 无组织实例 |
| 人才与能力 | 无 Employee；可展示合法能力入口/说明，不虚构员工 |
| 经营洞察 | 无经营数据 |
| 资料库 | 只显示真实存在的资料；没有则为空 |
| 会议 | 无会议事实 |

禁止为了“让用户看看产品”生成假 Company、Business、Workspace、Employee、Result、Evidence、Meeting 或经营数据。Empty Curis 不是 Demo、Preview、Tour 或 Prototype。

App-level 能力仍可出现，例如 Settings、Theme、Help、产品说明和 AI Readiness 入口；Company-level / Business-level 事实必须保持 Empty。

如果 AI 也未 Ready，仍允许浏览 App，但 CEO Assistant 对话、Intent Understanding、Proposal、Research 和 Employee execution 等需要推理的 Action 必须进入 AI Readiness / Capability Limit，不得假装工作，也不得强制把用户踢回完整 Onboarding Wizard。

Empty Curis Shell 始终保留明显的“创建我的 AI 公司”入口。用户可以先浏览，之后任何时候创建 Company；创建后继续 `Company → AI Readiness → Empty Company → Create Business`。

跳过动作应记录已有的本地 onboarding presentation / dismissal preference（若系统已有机制则复用），但不得创建 Runtime lifecycle state。没有适合的本地机制时，登记为 `IMPLEMENTATION GAP`。

## 4. CEO DISPLAY IDENTITY + CREATE COMPANY

Company 是 First Open 的第一个真实产品对象。

最小必要输入原则：

- “你的名字 / 怎么称呼你”——仅在当前安装没有可用 CEO Display Identity 时询问；可使用昵称、英文名或自定义称呼，不要求真实姓名、职位、简介或行业。
- CEO Display Identity 包括 `Display Name` 与可选 `Avatar`；头像可上传、从 Curis 预置卡通头像集中选择或跳过使用 fallback，不是创建门槛。统一规则见 `docs/reviews/CURIS_AVATAR_IDENTITY_PATTERN.md`。
- “给你的 AI 公司起个名字。”
- CEO Display Name 与 Company Name 是两个不同语义；前者用于 AI 员工称呼 CEO、头像菜单、Conversation、Decision 与 Meeting，绝不是新的 Employee。
- Company Name 是默认必要字段。
- CEO identity 若已由当前安装 / 身份上下文确认，不重复询问。
- 只有当前 Runtime Truth 证明为创建必需的字段才能增加；不要为了丰富页面增加行业、业务或组织字段。

创建 Company 时不得要求：

- Business / Department / Workspace；
- Employee、Role、Team 或 Skill；
- Model、Provider、Endpoint、Credential；
- Workflow、DAG、Operating Plan 或 Strategy。

## 5. COMPANY CREATION SUCCESS

Company 创建成功后必须明确显示：

> 你的 AI 公司已经建立。

此时不得说“AI 员工已经开始工作”，除非 AI Readiness 也已真实成立。

后续分流：

- AI 未 Ready → STATE B：进入 AI Readiness。
- AI 已 Ready 且无 Business → STATE C：进入 Empty Company State。
- 已有 Business（例如恢复已有 Company）→ STATE D：进入正常 Operating。

Company 创建成功可以同时创建真实 CEO Assistant identity。Company Created 后的第一项产品存在应是 CEO Assistant identity + Conversation Surface；identity 存在与 AI 推理能力可用必须分开显示。

AI 未 Ready 时可显示确定性产品文案，例如：“你好，[CEO Display Name]。我是你的 CEO 助理。公司已经建立。启用一个 AI 模型后，我就可以开始帮你协调公司和推进业务。”这不是 AI 生成回复，不得伪装模型已经响应。

## 6. AI READINESS / ASSISTANT AVAILABILITY

AI Readiness 首先表示 CEO Assistant 当前是否具备可用 AI 模型，用户目标是：

> 让你的 AI 公司开始工作。

默认路径只让用户选择或连接一个可用 AI 能力。普通用户不先看到 Provider、API Endpoint、Model ID、Base URL 或 Credential 等术语；Advanced 入口才暴露这些技术设置。管理入口继续是左下角 CEO 头像菜单 → 模型配置 / AI 能力设置，不新增第二模型配置中心。

模型配置与模型使用分开：配置负责添加/验证/启用模型；使用发生在 CEO Assistant、Team Leader 或 Employee Conversation 的 Model Selector 中。

产品必须定义以下语义而不是假装成功：

- 已连接并通过真实 Health：AI Ready；
- 连接存在但未验证 / Credential 缺失：需要补充或验证；
- Capability unavailable：说明缺口、Owner、恢复入口和原上下文；
- 连接失败：说明没有发生的副作用，并允许安全重试。

具体支持哪些 Provider、Model、Local Model 或 Agent，必须消费当前 Capability Truth；本合同不虚构 OpenAI、Claude、Gemini、Ollama 或 Codex 已全部可用。

## 7. AI CONFIGURATION SIMPLE BY DEFAULT

默认体验：

1. 选择一种 Curis 当前可用的 AI 能力；
2. 输入必要凭证或完成原生授权；
3. 验证连接与 Health；
4. 回到原上下文并显示 AI Ready。

Advanced 才显示 Provider、Model、Endpoint、Credential、Local Model 等技术细节。AI Readiness 不是让用户搭建 Provider Registry，也不是 Workspace 配置表单。

## 8. NO AI READY = NO FAKE AI

AI 未 Ready 时，Curis 仍可以：

- 展示产品与 Company；
- 创建确定性的 Company 对象；
- 保存不依赖 AI 推理的合法输入；
- 展示设置、缺口和恢复入口。

AI 未 Ready 时，Curis 不能假装已经完成：

- 复杂经营意图理解或 AI Clarification；
- AI Proposal、Research、Strategy；
- Employee reasoning、AI Result 或 Autonomous Operation。

任何需要模型推理的行为必须等待 AI Ready，或明确显示 Capability Limit。

## 9. M3 KEYCHAIN IMPLEMENTATION BOUNDARY

当前工程记录的 M3 macOS Keychain credential persistence 为 `SECURITY BLOCKED`。这是实现阻塞，不是产品层取消 AI Readiness。

在该阻塞解除前，不得在页面或验收中声称“连接一次永久可用”。必须如实区分：

- Desired Product Experience：连接、验证、跨会话恢复；
- Current Implementation Truth：凭证跨重启持久化尚未形成安全可验收事实。

该项应作为后续实现 / 安全 Issue 的明确依赖，不在本合同中通过环境变量、文件明文或假凭证绕过。

## 10. EMPTY COMPANY STATE

Company Ready / No Business 时，用户已经进入自己的 AI 公司，而不是 Onboarding Wizard。

正常 Shell 至少表达：

- 当前 Company 已存在；
- AI 能力已 Ready；
- 当前尚无 Business；
- 可以开始第一个 Business；
- 可以进入必要的 Company 设置 / 能力入口；
- CEO Assistant 是否存在，以及此时能做什么。

主 Action 是“开始第一个业务”，点击后聚焦 CEO Assistant Conversation 并复用 Create Business Flow，不打开第二套 Wizard。该入口可以允许用户稍后返回，不强制完成完整业务配置才可浏览 Company。

## 11. CREATE BUSINESS ENTRY / HANDOFF

`CURIS_CREATE_BUSINESS_FLOW_CONTRACT.md` 负责：

`Intent → Understanding → Clarification → Proposal → Confirm → canonical Business → First Workspace`

它同时服务：

- STATE C：Company Ready / No Business 创建第一个 Business；
- STATE D：已有 Company 创建 Additional Business。

它不负责 PRE-COMPANY 的产品介绍与 Company 创建，也不负责 AI Readiness 的技术连接页面。

## 12. CEO ASSISTANT LIFECYCLE

如果当前 Company materialization 会同时创建 CEO Assistant：

- Company 创建成功后，CEO Assistant identity 可以真实存在；
- AI Not Ready 时，Assistant 可以说明身份和能力缺口，但不能假装有 AI 推理能力；
- AI Ready 后，Assistant 才可参与 Intent understanding、协调、Proposal、跟进和升级。

Assistant 仍是 Company-level coordinator，不替代 Team Leader、Domain Expert、专业 Employee 或 Executor。它不因存在于 First Open 就成为行业研究员、策略专家、Workspace Builder 或默认专业 Owner。

## 13. REOPEN / RETURNING USER

- Company = 0 且 Welcome 未跳过：回到 PRE-COMPANY Welcome，可创建 Company 或选择“先看看 Curis”。
- Company = 0 且 Welcome 已跳过：直接进入 Empty Curis Shell，不每次重新弹出 Welcome；Shell 仍保留“创建我的 AI 公司”入口。
- Company Exists / AI Not Ready：回到 AI Readiness，并保留 Company identity 与恢复入口。
- Company Ready / No Business：进入 Empty Company State，可开始第一个 Business。
- Operating：正常 App reopen 默认进入 CEO Desk / Company Operating Experience。
- 中断的 Company creation、AI Readiness 或 Create Business Flow 必须恢复同一合法上下文；不得重复创建对象。

每次进入 Operating 不重新进入 Create Business；创建新业务可从 Company / Business / Workspace 的合法 Action 发起并聚焦 CEO Assistant Conversation，复用同一 Create Business Flow。

## 14. CURRENT IMPLEMENTATION MAPPING

本节是实现事实与差距，不覆盖产品合同：

| 产品层 | 当前实现接缝 | 当前事实 |
|---|---|---|
| FoundingRun | `POST /api/workspace/runtime/foundation/founding-runs` | 当前可创建并持久化 `owner_ref`、`intent_ref`、`org_version`、`blueprint_version`；它不是 PRE-COMPANY 产品页面合同 |
| Company 创建 | `POST /api/workspace/runtime/foundation/founding-runs/{id}/materialize-company` | Foundation 通过现有事务物化 Company 与 CEO Assistant，并校验当前 CEO identity |
| General Business + First Workspace | `POST /api/workspace/runtime/foundation/founding-runs/{id}/materialize-first-general-workspace` | 现有后端接受 normalized goal、positioning、intent summary 等字段并幂等物化 canonical Department/Business/Workspace；由 Create Business Flow 消费 |
| Company readiness | `GET /api/workspace/home/summary` | 当前提供 `ai_readiness.has_private_model` 与 `has_bound_employee` 及 Company 摘要；不是完整 AI Readiness UI 合同 |
| 当前前端入口 | `frontend/app/onboarding/page.js`、`frontend/components/terra/FirstRunGate.js` | 当前仍混合 FoundingRun 状态按钮、Company-only materialization 与模型引导；不能作为最终 App Entry 设计 |

当前实现差距：

- PRE-COMPANY First Open / Create Company 页面尚未与本合同形成独立产品实现；
- AI Readiness 的普通用户默认路径、Advanced 配置、Health/credential 恢复仍需后续实现 Issue；
- Company Ready / No Business Empty State 与 Create Business Flow 的最终 UI 接缝仍是 UI-HOLD；
- 当前 M3 Keychain 安全持久化阻塞必须先按安全规则解决，不能用明文或假凭证替代。

## 15. TRAE DESIGN TASK SPLIT

Trae 不一次设计整个生命周期，后续拆为三个独立 Design Candidate：

### DESIGN TASK A — FIRST OPEN + CREATE COMPANY

只证明 PRE-COMPANY：Curis 是什么、Company Name、创建成功、失败/重试，以及 Welcome 的两个合法选择：创建我的 AI 公司、先看看 Curis → Empty Curis Shell。不要进入业务意图或 Provider 配置。

### DESIGN TASK B — AI READINESS + EMPTY COMPANY

只证明 Company 已存在、AI 尚未/已经 Ready、缺口与恢复入口，以及 Company Ready / No Business 的主 Action。不要画 Business 业务提案。

### DESIGN TASK C — CREATE BUSINESS FLOW

复用 `CURIS_CREATE_BUSINESS_FLOW_CONTRACT.md` 的四个核心视觉状态。其原“First Open”状态正式命名为 `CREATE BUSINESS — INTENT ENTRY`，不是 Curis App First Open。

## 16. ACCEPTANCE CRITERIA

1. 全新安装首次打开显示 PRE-COMPANY Welcome，而不是直接显示 Business Intent 表单。
2. Welcome 同时提供“创建我的 AI 公司”和“先看看 Curis”两个合法 Action。
3. Skip 后进入真实 Empty Curis Shell，不生成任何假产品数据，且可随时创建 Company。
4. PRE-COMPANY 的第一个真实创建对象是 Company。
5. Company 创建成功后明确显示 Company 已建立，不谎称 AI 员工已开始工作。
6. AI Not Ready 与 Company 不存在、Company Ready 清楚区分。
7. AI 未 Ready 时不发生需要模型推理的假成功。
8. AI Readiness 默认路径简单，技术字段仅在 Advanced / 按需入口出现。
9. Company Ready / No Business 显示 Empty Company State，主 Action 是第一个 Business。
10. 第一个 Business 与 Additional Business 复用同一 Create Business Flow。
11. Company = 0 且 Welcome 已 Skip 时，reopen 直接进入 Empty Curis Shell，不强制重弹 Welcome。
12. Operating reopen 默认回到 CEO Desk，不重新进入 First Open 或 Create Business。
13. CEO Assistant identity 与 AI execution readiness 分开表达。
14. Company、Business、Workspace 层级不被跳过，不能创建 orphan 或默认业务。
15. M3 Keychain blocker 不被页面、测试或假凭证掩盖。
16. Company creation、AI Readiness、Create Business 的失败/等待/恢复都保留原上下文且不重复创建对象。
17. Design Task A/B/C 可分别验证，不要求 Trae 一次设计全生命周期。

## 17. CEO REVIEW ANSWERS

**A. 全新安装第一次打开看到什么？** 看到 PRE-COMPANY Welcome：简短理解 Curis 的说明，以及两个合法选择——创建第一家 Company，或“先看看 Curis”进入 Empty Curis Shell；不是业务意图表单。

**B. 第一个创建的真实对象是什么？** 是 Company；Business 必须在 Company 存在后创建。

**C. Company 什么时候算创建成功？** Company 与其合法 CEO identity 通过真实 Foundation 事务持久化并返回可读取对象时；若同时物化 Assistant，也必须返回真实 Assistant identity。

**D. 没有 AI Model 时能做什么、不能做什么？** 可以浏览真实 Curis App、创建/读取 Company、保存确定性的合法输入、显示 AI Readiness 与恢复入口；不能假装完成 AI 理解、Clarification、Proposal、Research、Strategy、Employee reasoning 或 AI Result。

**E. 用户怎么让 AI 员工真正开始工作？** 在 AI Readiness 中连接当前可用 AI 能力，完成必要凭证/授权与 Health 验证；Ready 后从 Empty Company 开始第一个 Business，随后由合法 Leader/Employee 承担工作。

**F. Company Ready 但没有 Business 时看到什么？** 正常 Curis Shell 的 Empty Company State：Company 已存在、AI Ready、尚无 Business，主 Action 是“开始第一个业务”，并保留设置、能力和 Assistant 入口。

**G. 什么时候才出现“你想开始做什么业务”？** 只有在 STATE C Company Ready / No Business，或 Operating Company 发起“创建新业务”时；两者都进入同一 Create Business Flow。

## 18. OPTIONAL ONBOARDING DECISION SUMMARY

- **FIRST OPEN:** OPTIONAL
- **SKIP:** ENTER EMPTY CURIS SHELL
- **COMPANY REQUIRED TO BROWSE APP:** NO
- **COMPANY REQUIRED FOR COMPANY / BUSINESS OPERATIONS:** YES
- **AI READY REQUIRED TO BROWSE APP:** NO
- **AI READY REQUIRED FOR AI REASONING / EXECUTION:** YES
- **FAKE DEMO DATA:** FORBIDDEN

## 19. AUTHORITY / NEXT GATE

本文件是 App Entry 生命周期产品与交互候选合同，受当前 Product Blueprint、Master Map、UI Blueprint 与 Frozen Shell/Visual Authority 约束；它不能覆盖这些 Current Authority。

下一 Gate：CEO / ChatGPT Review → Design Task A/B/C 分别确认 → UI Blueprint 消费确认 → 独立实现 Issue。未经对应 Gate，不开始代码、Runtime、Schema 或 DB 变更。

**— APP ENTRY LIFECYCLE CONTRACT READY FOR CEO REVIEW —**
**STOP**
