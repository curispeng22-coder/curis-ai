# CURIS — VISUAL DESIGN CHATGPT HANDOFF PACK

> 给新的普通 ChatGPT 产品 / 视觉审查会话使用。Authority Class：RESEARCH / HANDOFF；不是 Product Authority、IA Authority、Figma Contract 或实现授权。基于当前本地 Current 文件。

## 0. Truth 分层

区分 Current Product Truth、Implementation Truth、Research / IA / Review（Candidate）和 History / Archive（provenance）。冲突报告 Authority Conflict；产品与 Runtime 不一致写 Product → Implementation Gap。本包不是新 Authority。

## 1. Curis 是什么

Curis 是一个 **AI Company Operating Product**。它不是把一个聊天窗口包装成 SaaS，也不是把 Agent、Workflow、Task、Dashboard 拼在一起，而是把成熟 AI 工作能力组织成一家公司，让普通用户可以：

- 说出自己想做什么；
- 看到谁负责、正在做什么、结果是什么；
- 在必要的重大判断、授权、风险或不可逆动作处介入；
- 让公司在结果、证据、反馈和学习的基础上继续运转。

Curis 的产品价值不在于让 CEO 学会专业工具，而在于把专业经营交给 AI Employee，并让 CEO 仍然保有目标、边界、风险和相关决定权。

因此 Curis 不是要求 CEO 配置页面 / 流程 / 字段的传统 SaaS，不是让用户管理 Agent / Prompt / Workflow / Tool 的工具，不是首屏铺满指标的 Dashboard，也不是文件库、任务列表或不保留责任与结果的单纯 Chat。

核心承诺：我说想做什么，知道谁负责，在专业 Workspace 看到工作和结果，并在真正重要时做决定。

## 2. 用户与责任边界

小白 CEO 不是内容运营专家、研究员、渠道管理员或自动化工程师。CEO 提供 Intent、Reference、Constraint、Relevant Decision，主要消费 Result、Value、Recommendation、Risk、Unknown、Decision；默认不管理专业参数、Workflow、Agent、Trace 或 Runtime State。

Employee 是责任承担者，不是匿名 badge、监控对象或 Domain 私有 Agent；同一 Employee 可服务多个 Workspace，identity 不复制。Responsibility 是“谁负责什么问题 / 结果”的范围，不能复制 Employee、Team 或 Runtime。

Leader 不是新的 Employee Type，也不是 Admin。Department / Business / Workspace Leader 都是普通 Employee 的 scoped Responsibility Assignment。正常工作停留在最低有效责任范围；跨 Scope、冲突、无法解决或高风险不可逆问题才向 `Employee → Workspace → Business → Department → Company / CEO` 上移。

如果 CEO 仍需维护 Topic Pool、Research Scope、Source rules、Channel matrix、Agent、Workflow、Retry 或专业参数，Curis 就退化成传统 SaaS。因此 AI Employee 承担 Research、Strategy、Configuration、Operation、Evaluation、Learning；CEO 保留目标、边界、重大策略、授权、暂停和 Relevant Decision。进入 Employee 是 Shared Workstation；查看“这个人是谁”是 Employee Detail，二者不混。

## 3. Company / Business / Workspace / Channel / Account

```text
Company → Department → Business → Workspace
```

Company 持有共享 Truth；Department 是组织范围；Business 聚合同类 Workspace 并持有业务方向；Workspace 是独立长期专业经营环境和唯一 canonical product identity，拥有 Goal、策略、Team、Responsibility、Work、Result、Risk、History 与 Professional Surface。Surface 只是 Workspace 内的专业观察 / 工作面，不是 Team、Employee、Cycle、Runtime、Session 或新 Workspace。

Channel 是外部平台；Account 是平台内具体账号及定位；二者都不是 Workspace。Office 只保留历史 / implementation provenance。Professional Workspace 遵循 Verified-first / resolution-first；Professional 不自动等于 Verified。

## 4. Four-Pane 产品框架

“四范式”在当前视觉设计语境中指 **Four-Pane Product Framework**，不是四种工作模式、四种 Conversation 或四种 Workspace 类型。

```text
Navigation | Context | Main | Utility
```

Navigation 是全局 / 产品导航，回答“我在哪里”；设置等进用户入口。不要新增 Domain 私有一级导航、Workflow、Agent 或 Workspace Builder。Context 是 Main 左侧按需展开的 Workspace / Domain / Object / Work / bounded context；Utility 是 Main 右侧按需展开的 Detail、Editor、Preview、Evidence、Tool、Artifact 或 Action。二者都不是固定员工列表、Conversation 区或第二主工作区。

Main = Domain Business Surface + Shared Work Area，Context / Utility 收起时仍应让 CEO 理解业务并完成主要工作；进入 Employee 时，Main 可承载 Conversation-first Workstation。默认只显 Navigation + Main；需要上下文或辅助能力时展开相应 Pane；深度工作可三 Pane 协同，但 Main 始终 Primary Focus。四区职责稳定，物理列不必永久同时展开。

## 5. Shared Shell / Shared Work Area / Professional Surface

Shared Shell 提供跨 Workspace 的导航、返回、Adaptive Surface、Conversation、Composer、Employee Pattern 和状态表达；Shared Work Area 位于 Main 内，承载 Employee Workstation 与工作现场。Professional Surface 只贡献 Domain 的专业内容、selected Surface、对象、Result projection、Action 和 bounded Context，不能创建第二套 Shell、Conversation、Employee、Work / Result / Evidence truth 或 Runtime / Team / Cycle / Session truth。

## 6. Conversation、Employee Workstation 与三入口

CEO Assistant 是公司级协调入口；Employee Workstation Conversation 是具体员工的持续工作现场；Meeting 是重大分歧 / 协作讨论；Workspace Thread 属于业务对象上下文。它们不是中央群聊，也不是第五 Pane。每个 Employee 有三个入口：直接对话、当前工作、员工资料；前两者进入同一 Workstation 的不同焦点，资料不含 Conversation。Conversation / Workstation 不进入 Context Sidebar。Composer 使用 Shared semantic slots，真实 Provider capability 决定可用槽位，不另造技术 Composer。

## 7. Context / Result / Evidence / Handoff

视觉层级从结果和决定开始，而不是资料和运行图：

```text
Primary Focus      Result / Decision / Action
Secondary Context  谁负责、为什么重要、下一步
Supporting Detail  Context / Work / Risk / Unknown
Deep Evidence      Evidence / Source / History / Technical detail
Quiet Background   不需要 CEO 处理的运行状态
```

Result 可查看依据、进入 Evidence / Source / History、询问负责 Employee（自动携带 Workspace / Responsibility / Object / Result refs）、按建议继续下一 Work，并返回原对象与位置。Context 只提供本次工作的 bounded context，不全量塞入 Workspace 或历史。Handoff 表达 From / To Responsibility、Holder、Result、Evidence、Status、Next Work，不是 DAG、流程图或任务队列。

## 8. Workspace Engineering / Professional Workspace

Workspace Engineering 是 resolution-first 的专业环境建设路径，不是隐藏 Runtime Service 或唯一创建入口。优先复用 Verified professional environment，只有真实 Truth / Domain / Risk gap 才做 bounded Research，Generation 是 last resort：

```text
Business Intent → Current Company Truth → Domain / Scope / Risk
→ Verified Match → Instance Configuration → Safe Composition
→ bounded Research（必要时）→ Candidate → Generation（last resort）
```

长期 Workspace 由真实 Team、Leader、成员和职责承载；轻量 Conversation、临时 Task 或单 Employee 工作不必升级。不要设计 Workspace Builder、Low-code Builder、Workflow DAG、自由画布或第二套 Organization Truth；Professional UX 仍装入 Shared Shell。

## 9. Content Growth：第一套 Professional Workspace Candidate

Content Growth 是第一个需要完整展示“AI Employee 团队替小白 CEO 做专业经营”的 Professional Workspace Candidate。它不是 Verified Workspace，因此视觉可以展示专业业务结构，但不得暗示平台能力、账号授权、归因或发布闭环已经成立。

它的价值不是“多几个内容页面”，而是把经营闭环压缩成 CEO 能理解的结果：

```text
目标 / Intent
→ 情报 / Signal
→ Opportunity
→ Topic
→ Research
→ Content
→ Asset / Variant
→ Channel / Account
→ Publication / Receipt
→ Feedback
→ Evaluation
→ Learning / Next Work / Topic
```

这条链是业务对象关系，不是要求为每一步创建一个一级页面，也不是新增 Runtime primitive。

## 10. Content Growth 已接受 IA

- **默认经营结果**：Domain-scoped selected Surface，回答“现在最值得 CEO 关注什么”；默认 0–3 个高价值事项、Quiet、轻量进行中，不是 Dashboard、固定 8 态 / 4 桶或卡片墙。
- **Topic / Topic Pool**：Topic 聚合选题、Why、Goal、时效、价值、风险 / Unknown、Responsibility、状态和下一步；状态不是多个 Tab。Pool ON-DEMAND，由 AI 维护，CEO 可查看、指定、干预和找历史。
- **Research / Source**：Research 首先给结论，再给原因、意义、风险 / Unknown、建议；Evidence、Source、Question、Scope、History 按需展开。同问题 / Scope 续接原 Research，改变关键边界才新建。Source 默认由 Employee 使用与配置，Deep View 才管理。
- **Content / Version / Asset**：Content 关联 Topic / Research / Goal；Draft 可编辑，Version 可恢复，Recommended Version 是指针，Asset 是可复用素材。修改生成新 Version，恢复不删历史。
- **Publishing**：`Content → Channel → Account → Variant → Publication → Receipt`。对象语义区分，但 CEO 不管理矩阵；Employee 推荐地点、账号、时间和理由，CEO 确认 / 调整 / 讨论。
- **Evaluation / Feedback**：先看结果、原因、Goal 关系、有效 / 未证明和下一步；平台浏览、点赞、粉丝不自动等于 Business Value，归因不足标 `UNKNOWN / Attribution not proven`。
- **Employee Current Work**：Shared Work Area 的 Domain Context 投影，显示 Work、关联对象、Result、Evidence、等待、下一步和 Handoff；进入 Conversation 自动携带 Workspace / Responsibility / Object / Result refs 并可回到原对象。

核心关系：

```text
Signal / Opportunity → Topic → Research → Content → Variant → Publication
→ Feedback → Evaluation → Next Work / Topic
```

## 11. AI Employee 自主经营的当前真相

当前 accepted evidence 证明的是一条有界 Autonomous Operating control path：持久化一个 active Cycle，释放 canonical Employee / Provider Work，要求 Result / Artifact / Evidence 后才能 close，经过 Acceptance / Evaluation，支持 Leader / CEO 的继续、调整、等待、升级、暂停、停止，Provider / capability failure fail closed，并能重启恢复、避免重复。accepted Learning 是 evidence-bound、scope-bound、需要明确 Leader / CEO acceptance 的 Artifact / reference，不能自动改写 Strategy、Goal、Envelope、Package、Capability routing、Prompt authority 或代码。

这不等于通用自治政策。当前没有证明 universal chain depth、Cycle token / cost budget、外部 Provider 完整成本、统一 retry / timeout、consecutive-failure threshold、semantic repeated-decision detector、自动 cost degradation、parallel DAG expansion 或自动策略 mutation。

`≥2 evidence → HIGH`、`≥3 observations → Learning`、`Retry ≤2`、`Research Timeout =30min`、`连续失败≥3`、`同决定重复≥3 STOP` 都只能是 Candidate / Calibration Required。IA / Figma 可以表达 waiting、failed、paused、stopped、insufficient evidence、WAITING_CEO，不得画精确自治数字或无限自我优化。

## 12. Current Capability Truth vs Target Product

五个平台 XHS、Douyin、TikTok、YouTube、Bilibili 没有任何 audited `VERIFIED` capability。

当前按 Audit 原值表达：Auth 五平台 `PARTIAL`（仅凭据管线）；Publish 五平台 `CONDITIONAL`（无 live publication evidence）；XHS 的 Schedule / Status / Receipt / Comments 为 `PARTIAL`、Analytics 为 `UNAVAILABLE`；其他平台大多为 `UNKNOWN`；Multi-account 为 `UNAVAILABLE`。这不是 OAuth、账号归属或真实发布的证明。

视觉和 IA 禁止伪造 Connected、Live Publish、Published URL、Live Analytics、Live Comments 或 Multi-account。

Target Product 仍可表达完整的：

```text
Content → Channel → Account → Variant → Publication → Receipt
```

但所有目标发布流、账号定位、跨渠道 Variant、真实回执、Analytics、Comments、多账号都必须显式标记：

`TARGET SCENARIO / NOT CURRENT CAPABILITY`

当前缺能力时，产品应显示未连接、未授权、UNKNOWN、等待能力、人工未验证回执、失败或部分能力存在，而不是假成功。

## 13. 当前视觉设计目标

当前视觉候选语言是：

> Calm Surface / Strong Focus / Rich Work

- Calm Surface：中性、低噪音、长时间阅读舒适；
- Strong Focus：每个视口一个清晰 Primary Focus，通常一个主要行动；
- Rich Work：保留真实 Work、Result、Evidence、Decision 和责任关系，通过层级与渐进披露管理复杂度。

视觉层级应为：

```text
PRIMARY FOCUS      当前 Result / Decision / Action
SECONDARY CONTEXT  谁负责、为什么重要、下一步
SUPPORTING DETAIL  Context / Work / Risk / Unknown
DEEP EVIDENCE      Evidence / Source / History / Technical detail
QUIET BACKGROUND   无需 CEO 处理的运行状态
```

视觉自由存在于 layout、grid、spacing、typography、density、content width、surface treatment、component geometry、progressive disclosure、transition、motion idea 和 accent strategy；产品结构、对象关系、Shared / Domain ownership、Current Capability Truth 和 Runtime Truth 不属于 Figma 自由范围。

## 14. 已失败、禁止回退的方向

禁止回退到 Dashboard / 大卡片墙 / 固定 8 态或 4 桶、传统 SaaS 永久 Tab 与全量专业配置、Agent 控制台 / DAG / Token 面板、大卡片 Conversation / 中央群聊、员工监控墙或 Domain 私有 Employee system。Conversation-first Workstation 不进 Context，Conversation 不进 Employee Detail / Utility；Four-Pane 不永久四栏，Content Growth 不重造 Shell / Work / Result / Runtime。XHS / Douyin / Account 不是 Workspace，低保真 HTML 不是视觉答案，Target 不能画成 Current，英文内部术语不能压过中文小白用户语言，也不能把 Evidence / Runtime detail 铺满首屏或暗示无限自治。

## 15. 当前 Figma 阶段

当前已完成 Shared / Domain / Workspace identity、Frozen Four-Pane、Employee Workstation / Composer / Conversation 边界、Content Growth IA Round 1/2、Channel Capability Truth、Autonomy Guardrail / Calibration Boundary、Shared Visual Framework Contract，以及 Figma Make 最小输入包。

当前 Contract 的最终决定是：

> **READY FOR FIGMA VISUAL DESIGN**

但“Ready”只表示产品结构和视觉输入边界足够开始设计，不表示已经有 Figma 文件、已完成视觉方案、已接受截图或已实现产品。

### 首轮 Figma 目标

先做完整 Curis Shared Four-Pane Visual Framework：

1. Four-Pane Default：Navigation + Main，Context / Utility 收起；
2. Context Expanded；
3. Utility Expanded；
4. Universal Conversation / Shared Composer；
5. Employee Conversation-first Workstation。

再把 Content Growth 装入同一母体：

1. 经营结果；
2. Topic / Research 结果优先下钻；
3. Content 推荐成品 + 按需修改；
4. Evaluation 经营结论；
5. Publishing Current Truth / Target Structure；
6. Source / Topic Pool Deep View（如需要）。

不要一次画几十个页面、先做孤立内容运营软件或直接进入前端实现。

## 16. 下一步工作流

工作流必须是：

```text
Figma visual design
→ screenshots / result frames
→ ChatGPT visual + product review
→ bounded correction only
→ CEO review / acceptance
```

### Figma 阶段

先证明共享视觉母体、四区自适应、Main Primary Focus、Conversation-first Workstation 和渐进披露，再证明 Content Growth 是 Domain Instance。Figma 可自由探索视觉，不得重定产品结构。

### Screenshot / result 阶段

输出能审查 Default、Context Expanded、Utility Expanded、Conversation、Employee Workstation 和 Content Growth 核心对象的真实 Frame / screenshot；截图是视觉证据，不自动成为 Product Authority。

### ChatGPT Review 阶段

新的 ChatGPT 必须先审查：

- 是否仍是 AI Company，而不是 SaaS / Agent console；
- Four-Pane 是否保持职责稳定且自适应；
- Main 是否保有 Primary Focus；
- Shared Shell 与 Domain 是否混淆；
- Employee / Conversation / Context / Utility 是否越界；
- Content Growth IA 是否被改写；
- Current / Target Capability 是否诚实；
- 中文小白 CEO 是否能理解；
- 是否回退到 Dashboard、Card Wall、Task Manager 或专业后台。

如果问题只涉及视觉层级、布局、密度、可读性或披露，应提出 bounded correction。不能趁 Review 重做 Authority、IA、对象模型或 Runtime。

## 17. LOCKED / ACCEPTED CANDIDATE / FIGMA FREE / FORBIDDEN

### LOCKED / Current Product or Frozen Shared Truth

Workspace 是唯一 canonical identity；Office 仅历史 provenance；Company / Business / Workspace / Channel / Account 不混用。Four-Pane 是 Navigation / Context / Main / Utility 职责模型，Context / Utility Adaptive；Main = selected Professional Surface + Shared Work Area。Shared Shell、Universal Conversation、Employee Workstation、Composer、Employee 三入口、Responsibility ≠ Employee、Headcount 不冻结均保持。Surface 不拥有独立 Runtime / Work / Team / Result Truth；CEO 不配置 Workflow / Agent / 专业参数；Capability Truth 不伪造。

### ACCEPTED CANDIDATE / current design input, not Product Authority

Content Growth = Professional Workspace Candidate；CEO Operating Result 是 default selected Surface；0–3 注意力项、Quiet、Topic Pool On-demand、Research conclusion-first、Source Employee tool、Content + Asset merge、Channel + Publishing merge、Evaluation + Feedback merge、Round2 Object Model、Cross-object Context、Calm Surface / Strong Focus / Rich Work，以及首轮 Figma Frame 范围。

### FIGMA FREE

layout、grid、spacing、typography、density、content width、surface treatment、component geometry、focus、disclosure、transition、restrained motion、accent / color strategy，以及中文信息层级。自由必须在 Locked / Accepted Candidate 边界内；旧低保真 HTML 只可作 `STRUCTURAL UX REFERENCE ONLY — VISUAL NOT ACCEPTED`。

### FORBIDDEN

新增一级导航、Domain Shell、第二套 Conversation / Employee / Work / Result / Runtime；重新发明 Four-Pane / 工作模式 / Workspace 类型；把 8 States / 4 Buckets、示例 Headcount、Candidate / Mock / Target / 单个 API 结果升格为 Truth；伪造账号、发布、URL、Analytics、Comments、Multi-account；让 CEO 配置专业参数；把视觉审查升级成代码、Prototype、Figma Authority 或 Runtime 改动。

## 18. 当前仍 OPEN 的问题

不阻塞 Figma，但必须显式保留：Four-Pane 的具体布局、Pane header、响应式和 motion；Content Growth 各对象的最终视觉组件；平台授权、真实发布、回执、Analytics、Comments、多账号等 Runtime / Evidence；Autonomy 的成本、Cycle budget、chain depth、retry、timeout、failure threshold 与 loop detection；带货 / 品牌 / IP 的 Business Value attribution（可能 UNKNOWN）；四区开启交互；以及 Calm / Neutral、Strong Focus、Professional Accent 的视觉方向选择。以上不能被夸大成“产品结构未定义”，也不能被视觉稿填成 Current Truth。

## 19. 给新 ChatGPT 的审查原则

先区分 Product Truth、IA / Visual Candidate、Current Capability、Runtime Calibration 和视觉质量。截图不证明模型、Connector、Runtime 或商业能力已完成。审查从 CEO 任务出发：是否知道公司在做什么、自己要做什么、能否问负责 Employee、返回原对象并理解 Unknown / 等待。视觉不能掩盖结构问题。

# NEW SESSION BOOTSTRAP INSTRUCTION

请把以下内容作为新 ChatGPT 会话的启动指令：

```text
你现在接手 Curis Visual Design / Figma Review。完整阅读本文件后，先用自己的话复述：Curis 的 AI Company 理念；CEO / Leader / Employee / Responsibility 边界；Company / Business / Workspace / Channel / Account 层级；Four-Pane 及其 Adaptive Context / Utility；Shared Shell / Work Area / Professional Surface；Conversation、Employee Workstation 与三入口；Content Growth IA、对象链和 Capability Truth；当前 Figma 阶段、首轮 Frames、Review workflow；以及 LOCKED / ACCEPTED CANDIDATE / FIGMA FREE / FORBIDDEN / OPEN。

随后明确 Current Phase / Gate，并区分 Current / Frozen Truth、Accepted Candidate、Target-only / UNKNOWN capability 和仍 OPEN 的问题。不要重新开启这些已关闭误区：XHS / Douyin ≠ Workspace；Workspace 是 canonical identity；Office 只属 provenance；Four-Pane 不是四种模式；8 States / 4 Buckets 不是固定 UI；Surface 不拥有独立 Runtime；Responsibility ≠ Employee；Headcount 不冻结；Content Growth 不重造 Shared Shell；Conversation 不做大卡片墙；CEO 不配专业参数；Target ≠ Current；低保真 HTML ≠ Visual Reference。

然后等待 CEO 提供 Figma Frame / 截图，再做 bounded Review；不要修改 Authority、IA、Runtime、Frontend、Prototype 或 Figma，除非 CEO 另行授权。
``` 

**STOP FOR CEO REVIEW.**
