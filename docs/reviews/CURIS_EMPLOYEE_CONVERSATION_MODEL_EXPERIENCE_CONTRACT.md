# CURIS V1 — CEO IDENTITY / ASSISTANT / MODEL EXPERIENCE CONTRACT

> 2026-09-15 Disposition: **CONSUMED SUBSET / PROVENANCE — NOT DEFAULT CURRENT INPUT**。
> Model配置/使用分离、用途选择/连接/有效权限等已接受产品语义已写入[Current Authority](../03_Design/Curis_Company_OS_Shared_Authority.md)及当前Master Map/UI Blueprint。下文保留原Review/历史实现/未接受候选，不整篇升级Frozen；发生冲突只消费已回写Current正文。原ADR-0046已Frozen部分继续按ADR，G1-V～G6-V未验。


**Status:** Review
**Authority Class:** REVIEW / PRODUCT + INTERACTION CONTRACT
**Disposition:** READY FOR CEO / CHATGPT REVIEW
**Scope:** CEO Display Identity、CEO Assistant first presence、Conversation Model usage；不含视觉设计、Settings IA 或实现授权

> 本合同把 CEO 身份、CEO Assistant 和模型“配置 / 使用”边界对齐。它不新增身份系统、Employee 系统、Conversation 系统、Model Configuration Center、Provider 系统、Runtime、Schema 或 DB。

## 1. CEO DISPLAY IDENTITY

Fresh Install 且当前身份没有可用 CEO Display Identity 时，Company Setup 最小询问：

> 你的名字 / 怎么称呼你

允许昵称、英文名或自定义称呼；不要求真实姓名、职位、个人简介、行业或组织规模。

CEO Display Name 用于 AI 员工称呼 CEO、头像菜单、Conversation、Decision、Meeting 与 Company operating surfaces。CEO Display Identity 同时支持可选 Avatar；可上传、选择 Curis 预置卡通头像或跳过使用 fallback，规则统一见 `docs/reviews/CURIS_AVATAR_IDENTITY_PATTERN.md`。它不是新的 Employee，也不替代现有 CEO identity。若当前身份已有合法 Display Name，不重复询问。

Company Setup 的另一最小输入是：

> 给你的 AI 公司起个名字

因此 Fresh Install 的最小 Setup 是 `CEO Display Name（若缺失） + Company Name`。复用当前 Runtime 已有 Identity 字段；没有可复用字段时登记最小 `PRODUCT → IMPLEMENTATION GAP`，禁止创建 `CEOProfileV2`、`UserIdentityV2` 或第二套 Account。

Employee Display Identity 同样只需名称与可选 Avatar；头像不阻塞 Employee 创建，也不影响 Role、Responsibility、Capability、Execution 或 Conversation history。CEO 与 Employee 共用 Avatar Pattern，不新增第二套身份系统。

## 2. COMPANY CREATION RESULT

Company 创建成功后，产品必须形成并区分：

`CEO Identity + Company + CEO Assistant Identity`

如果当前 Foundation 事务同时创建 Assistant，应返回真实 Assistant identity。不要把 Assistant identity 存在误写成 AI execution ready。

## 3. CEO ASSISTANT = FIRST AI EMPLOYEE PRESENCE

Company 创建后用户首先遇见的 AI 员工是 CEO Assistant。它是 Company-level coordinator，负责：

- 理解 CEO 目标（仅在 AI Ready 后进行模型推理）；
- 协调 Company、Team、Leader 与 Employee；
- 跟进跨 Business 事项；
- 汇总 Result；
- 把真正需要 CEO 判断的 Decision 带回来；
- 协调 Create Business Flow。

它不替代 Team Leader、Domain Expert、专业 Employee 或 Executor，不直接承担所有业务 Execution，也不成为未知行业的默认专业 Owner。

## 4. FIRST PRESENCE

Company Created 后，页面应出现 CEO Assistant identity 与 Conversation Surface，而不是只显示“去配置 AI”。

AI 未 Ready 时可使用确定性文案：

> 你好，[CEO Display Name]。我是你的 CEO 助理。公司已经建立。启用一个 AI 模型后，我就可以开始帮你协调公司和推进业务。

该文案不是 AI 生成回复，不得伪装模型已响应。Assistant identity 可以存在，AI reasoning capability 仍可用性不足。

## 5. MODEL CONFIGURATION ≠ MODEL USAGE

### 5.1 Model Configuration（管理入口）

管理入口固定复用：

`左下角 CEO 头像菜单 → 模型配置 / AI 能力设置`

配置面负责：

- 添加 Provider 或完成登录 / Credential；
- API Key / Endpoint 等必要设置；
- 添加、启用、禁用模型；
- Health 验证；
- Default Model；
- Advanced Model Settings。

不新增第二模型配置中心，不把这些技术字段放进 First Open 或普通 Conversation 首屏。

### 5.2 Model Usage（使用入口）

模型使用发生在 Employee Conversation Composer：CEO Assistant、Team Leader 和普通 AI Employee 共享同一 Model Selector Pattern。Selector 只显示当前已启用且该员工允许使用的模型，用户无需离开 Conversation 即可切换。

Model 是当前 AI 推理 / 执行能力，不是 Employee identity；Employee identity 仍由 Role、Responsibility、Skill、Knowledge、Tool、Connector、Permission 与 Context 等组成。

## 6. NO PER-EMPLOYEE MANUAL BINDING

冻结普通用户体验：创建 Employee 后，不要求 CEO 逐个打开 Employee Settings 绑定 Provider / Model 才能工作。

默认禁止以下流程成为前置门槛：

`创建 Employee → 手工绑定 Provider → 手工绑定 Model → 才能工作`

若当前 Runtime 存在显式 binding 要求，必须标为 `CURRENT IMPLEMENTATION` 与目标体验之间的最小 Gap，不能让旧实现反向改写产品语义。

## 7. DEFAULT MODEL RESOLUTION

当至少一个模型 Enabled 且通过真实 Health：

- Conversation 自动获得一个可用默认模型；
- 用户无需每次选择；
- 用户想换模型时，在 Conversation Model Selector 直接切换。

默认解析优先消费已有 Model / Agent / Capability Authority；本合同不发明复杂 Router。没有 Enabled Model 时，Selector 显示“尚未启用 AI 模型 / 添加 AI 模型”一类产品语义，并深链既有头像菜单模型配置。

## 8. AI READINESS

AI Readiness 首先表示 CEO Assistant 当前是否具备可用模型，不应默认成为强制的“Onboarding Step 3”。

- Company 可存在而 AI Not Ready；
- Assistant identity 可存在而 Conversation 不可发送 AI 请求；
- Model Enabled + Health verified 后，Assistant Conversation 才是 AI execution ready。

用户完成配置后：

`添加 / 登录 / API Key → Health 通过 → Model Enabled → 返回原 CEO Assistant Conversation → 显示默认模型 → 可开始对话`

## 9. CONVERSATION + STRUCTURED SURFACE

Conversation 负责连续协作；Structured Surface 负责重要业务对象。CEO Assistant Conversation 中可以插入：

`Understanding / Clarification / Proposal / Decision / Capability Gap / Creation Progress / Result`

例如：

`CEO Message → Assistant Understanding → Structured Clarification → Assistant response → Structured Proposal → CEO Confirm → Creation Progress → First Workspace`

这不是纯聊天记录，也不是 Wizard / Form flow。结构化表面必须引用真实对象与状态，不以静态 UI 代替 Company / Business / Workspace Truth。

## 10. CREATE BUSINESS CONVERSATIONAL ENTRY

当 `Company exists + Enabled Model available + Business = 0`：

- CEO Assistant Conversation 可以主动说：“公司已经准备好了。你想先做什么？”
- CEO 可直接在 Conversation 输入第一项业务意图；
- Empty Company State 仍可保留“开始第一个业务” Action，点击后聚焦同一 Conversation；
- 不打开第二套 Create Business Wizard。

Operating 状态下点击“创建新业务”也进入同一 CEO Assistant Conversation + Create Business structured flow。First Business 与 Additional Business 共享同一交互模型。

## 11. SKIP / EMPTY CURIS

若 Welcome 选择“先看看 Curis”且 `Company = 0`：

- 进入真实 Empty Curis Shell；
- 没有 Company identity 时，不伪造公司级 CEO Assistant Employee；
- 可保留 App-level 帮助、产品说明、创建 Company 与 AI Readiness 入口；
- 不显示假 Assistant Conversation，不产生假模型响应；
- 创建 Company 后再进入 Assistant identity → AI Readiness → Empty Company。

## 12. ALL EMPLOYEE CONVERSATIONS

CEO Assistant、Team Leader、Domain Employee 和有 Conversation Surface 的 Executor 共享：

`Employee identity + Current responsibility/context + Conversation + Enabled Model Selector`

共享的是使用模式，不是共享责任历史。Conversation 仍须遵守 Assignment / Workspace context isolation；不得把 Leader 的完整经营 Context 复制给每个 Employee。

## 13. CURRENT AUTHORITY REGISTRATION

- 左下 CEO 头像 → 设置 → Models & AI Providers 已是 Current UI Blueprint 的模型管理入口，本合同不新增 Settings IA。
- Frozen Shell Composer 已定义 `Input / + / 访问权限 / 工作模式 / 已选资源 / Model·Agent / Voice / Send`；本合同补充 Model Selector 的“会话内使用”语义，不替换该 Frozen 槽位。
- `CURIS_APP_ENTRY_LIFECYCLE_CONTRACT.md` 负责 App Entry、Company 初始化与 AI Readiness 生命周期；本合同负责 Assistant first presence 与模型配置/使用分离。
- `CURIS_CREATE_BUSINESS_FLOW_CONTRACT.md` 负责 Company 已存在后的 Intent → Proposal → Business → First Workspace；本合同补充其默认可由 CEO Assistant Conversation 发起。

## 14. IMPLEMENTATION GAPS

只记录真实接缝，不扩大产品模型：

- 当前 Company creation 是否已安全接收 CEO Display Name，需核对既有 Identity 字段；没有则登记最小 Gap。
- 当前前端尚未把 CEO Assistant identity / Conversation first presence 与 Company creation 统一呈现。
- 当前前端 Model Selector、Enabled Model 默认解析与无模型深链仍需独立实现与回归。
- M3 macOS Keychain credential persistence 的既有 `SECURITY BLOCKED` 仍是实现边界；不能声称连接一次永久可用。
- 当前 Runtime 若需显式 Employee Model binding，属于实现与产品目标的 Gap，不得升级为普通用户前置流程。

## 15. CEO REVIEW ANSWERS

**A. Fresh user 的 CEO Display Name 什么时候获得？** Company Setup 阶段；仅在当前身份没有可用 Display Name 时询问。

**B. Company 创建后第一个出现的 AI 员工是谁？** CEO Assistant。

**C. 没有 Model 时 CEO Assistant 是什么状态？** Identity Exists，AI Execution Not Ready；可显示确定性说明，不能发送假 AI 请求。

**D. 用户从哪里添加 / 管理模型？** 左下角 CEO 头像菜单 → 模型配置 / AI 能力设置。

**E. 用户在哪里切换当前对话模型？** Employee Conversation Composer 的 Model Selector。

**F. 是否需要逐 Employee 绑定 Model？** 不需要；默认由 Enabled Model Pool + 默认解析提供。

**G. Enabled Model 如何成为默认 Conversation Model？** 通过真实 Health 的 Enabled Model 进入既有默认解析；Conversation 自动选取，用户可直接切换。

**H. CEO Assistant 如何发起 Create Business？** 在 Company Ready / No Business 时从 Assistant Conversation 询问并承接 Intent；Empty Company 的 Action 聚焦同一 Conversation。

**I. Conversation 与 Proposal 等 Structured Surface 是什么关系？** Conversation 负责连续协作，Structured Surface 插入重要对象与 Decision，不退化为纯聊天或 Wizard。

**J. First Business 和 Additional Business 是否共享同一交互模型？** 是，同一 Create Business Flow。

**K. Skip 进入 Empty Curis 是否保持合法？** 是；Company=0 时只显示真实空态，不伪造公司级 Assistant。

**L. Runtime 与目标体验不一致时，最小 Gap 是什么？** 记录 Identity 字段、Assistant first presence、Conversation Model Selector、默认解析或 Keychain 持久化的具体实现 Gap；不创建第二系统、不让旧 binding 变成用户前置门槛。

## 16. NEXT GATE

CEO / ChatGPT Review → UI Blueprint 消费确认 → Design Task A/B（Assistant + Model usage）→ 独立 Frontend Issue。未经 Gate，不修改代码、Runtime、Schema、DB 或 Settings IA。

**— CEO ASSISTANT / MODEL EXPERIENCE READY —**
**STOP FOR CEO / CHATGPT REVIEW**
