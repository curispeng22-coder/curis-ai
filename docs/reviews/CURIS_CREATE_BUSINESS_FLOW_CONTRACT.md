# CURIS V1 — CREATE BUSINESS FLOW CONTRACT

**Status:** Review
**Authority Class:** REVIEW / PRODUCT + INTERACTION CONTRACT
**Disposition:** READY FOR CEO / TRAE REVIEW
**Scope:** Create Business Flow only；原 First Run 页面合同的身份/范围修正；不是视觉、Runtime、Schema 或实现授权

> 本文件原名为 First Run 页面合同，现正式收敛为“创建业务流程”合同。它不定义 Curis App 的首次打开/Company 初始化生命周期，不创建第二份 Product Blueprint，不修改 Product Blueprint、Master Map、UI Blueprint、Runtime、Schema、DB、Frontend、Prototype、Figma 或高保真设计。视觉实现另行消费 Frozen Direction D 与现有 Shell Authority。

## 1. USER GOAL

Create Business Flow 面向 Company 已存在、准备开始或新增业务的普通用户 / CEO。用户只需要回答：

> **告诉 Curis，你想开始做什么。**

用户不应先理解 Workspace、Employee、Capability、Provider、Workflow 或模型配置。Curis 负责理解经营意图、识别必要能力、提出可确认的经营方案，并在确认后开始建立真实公司经营上下文。

创建业务的结果不是“填完一张配置表”，而是：

`CEO 意图 → Curis 理解 →（必要时）研究与能力发现 → Operating Proposal → 必要 CEO Gate → Bootstrap / Reuse / Compose → 合法 Leader 承责 → 开始经营`

这是一条责任合同，不是所有业务都必须经过同样箭头的固定 Workflow。成熟能力、已有公司结构或已确认资料可以跳过重复步骤。

### Conversation 作为默认入口

对于已存在且 AI Ready 的 Company，Create Business Flow 默认可以由 CEO Assistant Conversation 发起。CEO 可以直接表达“我想开始做什么业务”，Conversation 负责连续协作；Understanding、Clarification、Proposal、Decision、Capability Gap、Creation Progress 等重要对象以 Structured Surface 插入，不退化为纯聊天，也不打开第二套 Wizard。First Business 与 Additional Business 共享这一入口和合同。

如果 AI 尚未 Ready，Conversation 仍可显示 CEO Assistant identity 与模型缺口，但不能假装完成意图理解、Proposal、Research 或业务创建推理。

## 2. ENTRY STATE

### 2.1 Company Ready / No Business

- 页面说明 Company 已建立但尚无 Business；不显示伪造的业务、员工或 Workspace。
- 主任务是输入第一个 Business 的经营意图；不把“配置 Workspace”作为首屏任务。
- 若平台能力尚未准备，仍可表达意图并进入提案/能力缺口语义；能力不足必须清楚说明，不假装已可执行。

### 2.2 已有 Company，创建新业务

- `创建新业务`复用同一套 Intent → Proposal → creation contract。
- 不创建第二套业务创建逻辑，不要求重建 CEO、Company 或已有员工身份。
- 可读取当前 Company Truth，优先复用已有 Department、能力、资料、团队与工作空间；新的 Business / Workspace 身份仍需独立确认。

### 2.3 已有 FoundingRun

- 通过持久化 `founding_run_id` 恢复同一运行，不丢失已确认的阶段、意图引用或已物化结果。
- Reload / restart 后应回到最近合法页面状态；不得重复创建 Company、Assistant、Business 或 Workspace。
- 若同一 FoundingRun 收到不一致的创建参数，显示失败原因并保留原提案，不覆盖既有事实。

## 3. INFORMATION MODEL

页面只围绕以下信息组织，不把内部对象全部暴露给用户：

| 信息 | 用户可见表达 | 责任归属 |
|---|---|---|
| Intent | “我想开始做什么”及可选补充 | 用户输入；可被 Curis 总结 |
| Reference | 账号、链接、视频、网站、产品、文件等参考 | 可选证据入口；不等于已接入能力 |
| Situation | Curis 对目标、对象、约束、未知项的理解 | Curis 生成的可编辑摘要 |
| Capability discovery | 已具备、可复用、缺失或需授权的能力 | Curis 解释；Capability Center / 设置承载配置 |
| Operating Proposal | 目标、方向、第一步、责任与待确认边界 | CEO 可确认、修改、补充 |
| Creation result | Company、首个 Department/Business/Workspace、Assistant 与下一步 | 真实持久化结果 |

区分三种层次：

1. UI 草稿：输入、临时编辑、未确认的建议，不是 Company Truth。
2. FoundingRun / Proposal 状态：沿用现有 FoundingRun 生命周期和持久化引用。
3. Company / Department / canonical Business / First Workspace / Assistant：只有真实创建成功后才显示为已存在。

本合同不引入 `ProposalV2`、`BusinessContextV2`、`IntentStoreV2` 或第二套 Create Business Runtime。

## 4. PRIMARY ACTION

首屏唯一主任务：输入自然语言经营意图。

- 输入支持一句话或多句描述；允许模糊、不完整、口语化。
- 主按钮语义为“开始”和“继续了解我的想法”一类用户语言，不要求用户理解“建立 FoundingRun”。
- 技术状态、引用 ID、内部状态码不得成为主 CTA。
- 用户可以暂存、返回和继续；未确认的建议不得自动变成业务事实。

## 5. NATURAL-LANGUAGE INPUT

输入提示应引导结果而非字段，例如：

> 我想开始做什么？可以告诉我你想服务谁、想达成什么，或者先说一个模糊想法。

可接受示例：

- “我想做一个帮助小企业整理客户反馈的业务。”
- “继续开发 Curis，让它更容易交给团队使用。”
- “我想开始做宠物寄养，但还不知道应该怎么经营。”

不要在首屏要求 Positioning、Strategy、Team、Workflow、Workspace Structure、Operating Plan、Provider 或 Model 等技术/设计字段。

## 6. REFERENCE INPUT

参考资料是可选的意图理解入口，可包括：

- 外部账号、频道或业务对象；
- 视频、网页、产品链接；
- 本地文件、文件夹或已有资料；
- 用户补充的文字、截图或上下文。

引用的产品语义：

- 有引用只代表 Curis 可以尝试理解情况，不代表已读取、已验证或已连接该平台。
- 未接入浏览器、连接器、资料源或权限时，分开表达 `Product Intent` 与 `Current Capability Truth`。
- 不因用户提供一个平台名就自动创建 Channel、Channel Account、Connector 或专业 Workspace。
- 需要额外能力时，显示缺什么、由谁处理、没有产生什么、可从哪里配置以及如何回到原阶段。

## 7. CLARIFICATION RULE

Curis 只询问会改变经营方向、风险或确认边界的最少问题。优先问题例如：

- 你希望先服务谁，或先验证什么结果？
- 这是新业务，还是已有业务的继续？
- 有无必须遵守的预算、权限、时间或外部发布边界？
- 是否有可供参考的账号、资料或现有工具？

无需询问的信息由 Curis 推断、标记未知或留到后续工作中。不得把澄清变成十字段表单，不得在无法理解时让 CEO 自己配置完整员工、技能、工作流和 Provider。

## 8. PROPOSAL

Proposal 对普通用户只呈现四个核心问题，避免变成 AI Business Plan、Strategy Form 或 Company Configuration：

1. **你的目标**：Curis 理解你想做什么、主要想达到什么。
2. **Curis 建议怎么开始**：用普通语言说明建议的经营方向，不要求理解 Positioning、Strategy 或 Methodology。
3. **Curis 准备先做什么**：确认后将立即开展的研究、分析、准备、验证或初始工作环境建设。
4. **需要你确认 / 补充什么**：只显示真正需要 CEO 决定或补充的 Goal、重要方向、风险、约束和必要缺失事实。

以下只作为 Supporting Information，不能与四个核心问题同等视觉权重：谁/什么角色负责、使用哪种工作环境、当前能力缺口、Reference 状态。内部仍可保留 Situation、Capability、Responsibility、Workspace 等语义，但不平铺为普通用户表单。

用户可确认、修改、补充或退回 Proposal。Proposal 不是静态摘要，也不是要求 CEO 选择内部对象。

## 9. PROFESSIONAL WORKSPACE MATCH

专业工作环境是能力加速器，不是创建 Business 的门槛，也不是模板商城。

- Content Growth 与 RD 是 Curis 当前明确提供的两个 Professional Workspace / 样板专业业务能力。
- 用户意图匹配内容账号、内容增长或内容运营时，Proposal 可以直接说：“Curis 已经为这类业务准备了专业工作环境。”
- 用户意图匹配软件研发、App/网站开发或工程研发时，同样明确说：“Curis 已经为研发业务准备了专业工作环境。”
- 普通用户不显示 Candidate、Unverified、Package Candidate 等内部术语。
- Professional Workspace 存在不等于其中每项 Capability 都已 Verified。XHS、Douyin、TikTok、YouTube、Bilibili、Analytics 或某些 Source Connector 的真实状态，在真正相关时独立显示为可用、人工、未验证或未连接。
- 用户未匹配或未选择专业工作环境也不影响开始任意业务；无专业匹配时进入 General Business Workspace。

## 10. GENERAL FALLBACK

没有成熟专业匹配时：

`CEO Intent → Situation → Capability Discovery / Research（需要时）→ General Operating Proposal → CEO Gate（需要时）→ General Business Workspace`

General Workspace 是真实可经营、可恢复、缺口透明的起点，不是 Demo、空壳或失败页面。它不承诺自动生成任何行业的专业软件；Curis 不知道如何经营某业务时，必须诚实进入研究、能力获取、升级、等待或暂不能经营。

## 11. EMPLOYEE / RESPONSIBILITY EXPRESSION

- Create Business Flow 先表达责任，不先展示人员目录。
- 可以说“Curis 会为这项工作安排合适的负责人”，但不能在未物化前虚构员工姓名、头像或完成状态。
- CEO Assistant 负责协调 Situation、Capability Discovery、Research、Proposal、跟进和升级；它不替代 Team Leader、Domain Expert、专业员工或 Executor。
- Leader 接受合法 Operating Responsibility 后，专业判断和团队工作进入对应 Workspace；员工能力来自身份/岗位、Agent/模型、Skill、Knowledge、Tool、Connector、权限和上下文的组合。
- 不要求 CEO 逐任务创建员工或 Work；Work 可由 Goal、Strategy、Operating Plan、Team Operating、Result、Trigger、Schedule 或员工判断产生。

## 12. CONFIRMATION

最终确认只让 CEO 处理不能安全代理的事项：

- Goal / 成功定义；
- Strategy Boundary / Positioning / Audience；
- 风险、预算、权限和约束；
- 高影响、不可逆或外部副作用决定。

不要求 CEO 确认：

- Employee、RoleSlot、Skill、Tool、Provider 的技术组合；
- Workflow/DAG/Router/Runtime 细节；
- 已被能力合同允许的普通 tactic、cadence、experiment、work priority 或 bounded plan 调整。

确认必须对应真实 FoundingRun / Proposal 状态，并保留修改与退回路径。

## 13. CREATION

成功创建的产品语义是：

`FoundingRun / Proposal →（必要时）Company → Department → canonical Business → First Workspace`

并在同一 Company Truth 中 materialize 第一位 CEO Assistant（如果该 Company 尚不存在）。

创建必须：

- 原子或可证明幂等；
- 返回真实对象、状态、父级关系和下一步；
- 支持同一 FoundingRun 重试而不重复创建；
- 不自动复制 Employee identity、Secret、Conversation、Task、Execution、Result、Evidence 或历史；
- 不把失败的请求渲染成“公司已建立”。

## 14. UI STATE 与创建状态

以下是页面最小 UI 状态集合，不是新的 Runtime enum：

| UI State | 用户看到的语义 | 可执行动作 |
|---|---|---|
| `FIRST_OPEN` | 说说想开始做什么 | 输入意图、添加可选参考 |
| `INTENT_ENTERED` | Curis 已收到想法 | 继续理解、补充或修改 |
| `CLARIFICATION` | 只缺少会改变方向的少量信息 | 回答、跳过、返回 |
| `PROPOSAL_PROFESSIONAL` | 已匹配 Curis 提供的专业工作环境 | 查看、修改、确认、退回 |
| `PROPOSAL_GENERAL` | 先从通用工作环境开始 | 查看、修改、确认、退回 |
| `CREATING` | 正在建立真实公司经营上下文 | 等待、恢复、查看进度 |
| `FAILURE_OR_CAPABILITY_LIMIT` | 未完成；原因、Owner、缺口、无副作用和恢复入口清楚 | 配置、补充、重试、返回 |
| `SUCCESS_FIRST_LANDING` | Company/Business/Workspace 已真实存在 | 进入首个工作空间、开始对话 |

这些 UI 状态必须消费已有 FoundingRun / Company / Business / Workspace / capability truth。不要让 Runtime 状态（如 `ARRIVED`、`INTENT_CAPTURED`、`CLARIFYING`、`PROPOSED`、`CEO_CONFIRMED`、`COMPANY_CREATED`）直接决定 UI 展开方式或替代用户语言；页面可将正式状态映射为友好的产品文案。

## 15. FAILURE / WAITING / RETRY

每次未完成都必须说明：

- 当前阶段和真实状态；
- 原因与缺口；
- Owner（CEO、Capability、Leader 或系统）；
- 没有产生的副作用；
- 配置 / 补资料 / 等待回调 / 重试入口；
- 返回原 Proposal 或 FoundingRun 的位置。

规则：

- 等待不等于成功；
- capability limit 不创建假的 Professional Workspace 或 Employee；
- Provider、权限、连接或资料缺失时先展示可恢复的缺口；
- 同一 FoundingRun 允许安全恢复；参数冲突要阻断并保留原事实；
- 失败重试不得创建第二 Company、Business、Workspace 或 Assistant；
- 若只能建立部分事实，明确显示 Partial，并列出已创建和未创建对象。

## 16. FIRST LANDING

Create Business Flow 创建 Business 成功后，默认直接进入刚创建 Business 的 First Workspace；不默认落到 CEO Desk。路径是：

`Intent → Proposal → Confirm → canonical Business → First Workspace → First Landing`

匹配 Professional Workspace 时进入该 Professional Workspace；无匹配时进入 General Business Workspace。CEO Desk 保留为已有 Company 的公司级经营入口、回访入口和跨 Business 经营视图。

首次落地必须让 CEO 一眼知道：

- Company / Business 已存在；
- 当前 Goal / 方向是什么；
- 哪位 Leader / 哪项责任已承接（没有合法负责人时明确缺口）；
- Curis 下一步会做什么；
- 仍缺哪些资料、能力或授权；
- 如何开始对话、提出新 Work 或查看结果。

First landing 进入新建 Business 的真实 First Workspace，不停留在 FoundingRun 技术详情页。

## 17. RETURNING USER / CREATE BUSINESS REUSE

创建新业务仍走同一产品心智：

`表达经营意图 → 读取 Current Company Truth → 提案 → 必要 Gate → Reuse / Compose / Create → 新 Business / Workspace`

已有 Company、Department、Employee、Skill、Knowledge、Connector 或 Package 可以复用；Business identity、Goal、Positioning、外部账号/权限和业务特定资料按需要重新确认。不得把“复制业务”误实现为复制历史、员工身份、凭证、运行或结果。

## 18. BACKEND CONTRACT MAPPING（CURRENT IMPLEMENTATION FACTS）

本节只记录当前代码可核对的接缝，不改变产品合同：

| 页面语义 | 当前实现接缝 | 事实与边界 |
|---|---|---|
| 建立 FoundingRun | `POST /api/workspace/runtime/foundation/founding-runs` | `FoundingRunIn` 接收 `owner_ref`、可选 `intent_ref`、`org_version`、`blueprint_version`；持久化的是意图引用，不是原始自然语言正文 |
| 读取 FoundingRun | `GET /api/workspace/runtime/foundation/founding-runs/{id}` | 返回生命周期、Owner、版本与 `intent_ref`；物化后可返回 `first_business` 引用 |
| FoundingRun 状态 | `POST /api/workspace/runtime/foundation/entities/{id}/transition` | 复用既有 FoundingRun 状态机；当前代码包含 `ARRIVED`、`INTENT_CAPTURED`、`CLARIFYING`、`PROPOSED`、`CEO_CONFIRMED`、`WAITING_CEO`、`REJECTED` 等状态映射 |
| Company + CEO Assistant | `POST /api/workspace/runtime/foundation/founding-runs/{id}/materialize-company` | 通过现有 Foundation 事务物化 Company 与 Assistant，需匹配当前 CEO identity |
| General Business + First Workspace | `POST /api/workspace/runtime/foundation/founding-runs/{id}/materialize-first-general-workspace` | 接受 `company_id`、`ceo_id`、`company_name`、`department_name`、`business_name`、`goal`、`positioning`、`workspace_name`、`intent_summary`、`recommendation_reason`、固定 `NO_VERIFIED_MATCH` 与 blueprint；以同一 FoundingRun 幂等物化 canonical Department/Business/Workspace |
| Parent truth | 物化响应中的 `business`、`parent` 与 `parentPath` | 当前实现要求 Workspace → Business → Department → Company 关系可解析；不能用自由 `business_ref` 冒充创建成功 |
| Home readiness | `GET /api/workspace/home/summary` | 当前实现只提供 `ai_readiness` 与已有 Company 摘要；它不是完整 First Run Proposal 服务 |

当前可见的实现差距（不在本轮实现）：

- 当前 `FoundingRunIn` 只持久化 `intent_ref`；自然语言正文、参考资料及 Proposal 编辑/研究编排需由后续受授权的产品实现映射到现有合法对象或登记最小 Gap。
- 当前前端 `onboarding/page.js` 主要是旧的状态按钮与 Company-only materialization；尚未实现本合同要求的 Proposal、Professional/General 分支、参考输入和 First Workspace 一体化页面。
- 当前前端 `runtimeApi.js` 暴露 Company materialization，但尚未暴露 General Workspace materialization 接缝；不得因此新增第二套后端合同。
- 专业模板匹配与 Verified assurance 仍依赖现有 Package/Registry 事实；本合同不把 Content Growth 或 RD 宣称为已验证默认模板。

## 19. TRAE MUST SHOW

Trae 后续只消费本合同、现有 Frozen Shell Contract 与 Frozen Visual Standard，不在本轮设计页面。

Trae 只需展示四个核心视觉状态；其余状态作为 variation / inline state，不要求独立页面：

1. **FIRST OPEN**：普通用户马上看到“告诉 Curis 你想开始做什么”，支持自然语言与 Reference 入口，不出现技术配置。
2. **UNDERSTANDING / CLARIFICATION**：用户已表达意图；展示原始 Intent、Curis 当前理解，并仅在必要时追问 1–2 个关键问题，不做表单 Wizard。
3. **PROPOSAL**：展示四个核心问题（你的目标、Curis 建议怎么开始、Curis 准备先做什么、需要你确认 / 补充什么），并证明两种 variation：已准备好的 Professional Workspace 与 General Business Workspace fallback。两者不是两套产品。
4. **CREATING → FIRST LANDING**：确认后真实创建，随后直接进入新建 Business 的 First Workspace，并显示业务、Goal、责任、下一步、缺口与对话入口。

Failure、Capability Limit、Partial、Retry、Resume、Proposal Editing 可出现在上述四个状态中。例如 Capability Limit 以内联方式出现在 Proposal，Creation Failure 以内联方式出现在 Creating。页面应保持低表面复杂度，把 Proposal、缺口和责任集中表达。

## 20. TRAE MUST NOT INVENT

- 不新增模板商城、行业选择器或强制先选 Professional Template。
- 不新增 Employee Picker、员工假名、员工完成/等待状态或第二套身份系统。
- 不把 Provider、Model、Capability、Skill、Workflow、DAG、Router、Runtime 细节变成首屏表单。
- 不新增 ProposalV2、BusinessContextV2、IntentStoreV2 或第二套 FoundingRun。
- 不新增 Operating Console、Strategy Center、Review Center、Learning Center 或 Dashboard Wall。
- 不把 CEO Assistant 写成行业研究员、策略专家、Workspace Builder、Team Leader 或 Executor。
- 不伪造外部账号读取、平台连接、成功发布、Result、Evidence、Analytics 或能力 Verified 状态。
- 不把视觉颜色、字体、卡片、间距、Pane 比例写入本合同；视觉遵循 Frozen Direction D。

## 21. ACCEPTANCE CRITERIA

后续实现只有同时满足以下条件，才能声称 Create Business Flow 页面完成：

1. 首屏首先询问经营意图，而不是 Workspace 配置。
2. 可用自然语言开始，模糊意图不会被错误拒绝。
3. 参考输入可选，引用与能力事实分离。
4. 只询问影响 Goal、方向、风险或边界的必要问题。
5. Proposal 用普通语言解释理解、目标、方向、第一步、责任、缺口与待确认项。
6. 专业能力只是可复用加速器；无匹配仍可进入 General Workspace。
7. 用户不需要选择 Employee、Skill、Workflow、Provider 或 DAG。
8. CEO Assistant 的协调边界清楚，不冒充专业 Owner。
9. 确认只覆盖 Goal、Strategy Boundary、Risk、Constraint 与高影响决定。
10. 创建对应真实 FoundingRun、Company、Department、canonical Business、First Workspace 和 Assistant 事实。
11. 创建可恢复、幂等、可重载；不存在假成功或重复实体。
12. 失败、等待、部分成功和能力缺口都显示责任、原因、无副作用与恢复路径。
13. First landing 显示业务、目标、责任、下一步、缺口和对话入口。
14. 已有 Company 的新业务创建复用同一合同，不出现第二条路径。
15. UI 状态与 Runtime 状态分离，不新建 Runtime enum。
16. Trae/Frontend 不凭空添加导航、模板商城、技术配置页或视觉设计规则。

## 22. OPEN GAPS / REVIEW BOUNDARY

这些是实现或验证事项，不是本产品合同的隐含承诺：

- 参考资料读取、网页/平台分析与外部连接需要各自合法 Connector、权限和证据；未连接时仍必须支持 Intent 表达。
- Professional Workspace 的页面与物化接缝仍需后续实现；其存在与 XHS/Douyin/TikTok/YouTube/Bilibili 发布、Analytics、Source Connector 等单项 Capability 的可用性独立验证。
- 当前 Frontend Create Business Flow 仍是 UI-HOLD，需要后续正式 Issue、Allowed Files、设计消费与回归验收。
- 当前后端已有 General materialization 代码和测试，但必须通过最终页面验证真实 Company/Business/Workspace 链。
- 如实现过程中发现字段或持久化缺口，先登记 `PRODUCT → IMPLEMENTATION GAP`；不得以 UI 草稿、静态 JSON 或测试 fixture 充当产品完成。

## 23. AUTHORITY / NEXT GATE

本文件是 Create Business Flow 产品与交互候选合同，受当前 Product Blueprint、Master Map、UI Blueprint、Frozen Shell 与 Frozen Visual Standard 约束；它不能覆盖这些 Current Authority。

下一 Gate：CEO / ChatGPT Review →（接受后）UI Blueprint 消费确认 → Design/Trae 输入确认 → 独立 Frontend Issue。未经该 Gate，不开始代码、Runtime、Schema 或 DB 变更。

**— CREATE BUSINESS FLOW CONTRACT READY FOR TRAE —**
**STOP FOR CEO / CHATGPT REVIEW**
