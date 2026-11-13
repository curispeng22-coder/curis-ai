# CURIS SHARED VISUAL DESIGN SYSTEM RESEARCH

Status: Review
Authority Class: RESEARCH
Disposition: CEO REVIEW REQUIRED
Owner: Product / Design
Updated: 2026-08-23
Baseline: main @ c797db840bad285d7e9f1962d06eac61aa28508b
Supersedes: none

> 研究交付，不是 Product Blueprint、Master Map、UI Blueprint、Frozen Shell、Frozen Design System 或实现授权。当前 XHS Structural Candidate 保持不变。

## 0. Scope and truth boundary

对象是普通用户能够理解、但承载 Company、Business、Workspace、Team、Employee、Work、Result、Evidence、Decision、Conversation 等经营对象的 AI Company Operating Product。研究只处理视觉语言、注意力、阅读、密度、表面与交互表达，不重新定义产品模型。

本文件区分：

- `OBSERVED`：外部产品或官方设计系统公开表达的规则。
- `INFERENCE`：将观察翻译到 Curis 的推论。
- `CANDIDATE`：可进入 Visual System Candidate 的未冻结规则。
- `UNVERIFIED`：当前仓库没有真实视觉证据，须由 Figma Make / CEO 评审确认。

现有 Frozen baseline 已明确 Calm Executive Workspace、内容优先、中性表面、单一主强调色、低对比边界、禁止多彩 Dashboard / 控制台卡片堆叠。本研究扩展其验证范围，不覆盖它。

## 1. Executive answer

1. Curis 的视觉性格应是 **Calm Surface / Strong Focus / Rich Work**：表面安静，焦点明确，工作内容真实丰富。
2. 当前 Figma Structural Candidate 的主要问题不是颜色不足，而是结构正确后仍缺少“谁最重要”的视觉契约：标题、当前对象、状态、行动、辅助信息的权重没有稳定拉开。
3. “简洁”来自主动后退、内容宽度、行距、空白、单一焦点和渐进披露，不来自删掉真实业务内容。
4. Deep Green 值得保留为候选品牌语义，但不应直接成为全局大面积皮肤；它应主要承担品牌识别、主要行动和少量焦点状态。
5. Professional Domain Accent 可以存在，但只表达对象、图表、内容类型或领域状态；不能改变 Curis 的壳层、主文字、导航、Composer 或基础表面。
6. Card 必须是稀缺的语义边界；默认顺序是 Typography → Spacing → Alignment → Divider/Subtle Surface → Card。
7. Employee、Conversation、Current Work 应共享同一焦点体系：Employee 是责任主体，Conversation 是沟通入口，Current Work 是协作对象，不变成 Agent Monitoring Wall。
8. 下一轮只用 Research 与 Employee Conversation 做三方向 benchmark；结构冻结、视觉开放，三方向必须使用相同信息架构和内容。

## 2. External research matrix

| Source | OBSERVED principle | Curis translation | Do not copy |
|---|---|---|---|
| Linear Brand | 低饱和品牌色、克制品牌曝光、清晰产品识别 | 单一低饱和品牌锚点，品牌不铺满表面 | 工程 issue 工具的暗色/密度/对象模型 |
| Stripe Dashboard | 用决策相关内容组织界面，信息层级和 microcopy 建立信任 | CEO 视图先呈现当前经营重点，再呈现支持证据 | 把 Curis 变成财务后台/KPI 墙 |
| Atlassian Design | tokens、spacing、typography、color、elevation、border、radius 共同构成基础 | 候选系统必须有语义角色和可复用关系，而非散落 Hex | 复制 Jira/Trello 的业务组件形态 |
| Apple HIG | 层级、调和、一致；材料按语义而不是外观颜色选择；可访问性不依赖颜色 | 表面、对比、焦点、动效都必须服务内容和状态 | 把 Liquid Glass 当成 Curis 的品牌风格 |
| Figma Design Systems | 变量支持主题、尺寸、字体和跨上下文变化；语义命名连接设计与代码 | 先定义 semantic role，再由候选 primitive 赋值 | 本轮直接建立实现 token 或修改库 |
| Notion / Craft | 内容优先、空白组织、渐进披露、低 chrome | 长文本、Research、Employee 对话用阅读节奏而非卡片墙 | 复制 block editor 或文档产品模型 |
| ChatGPT Canvas | 对话与可编辑工作面在需要时自然切换；Composer 是入口 | Conversation 可引用 Work/Result/Evidence，并按需要打开 Focus Surface | 让 Curis 退化成聊天产品 |
| Claude | 对话承载研究与起草；上下文和风格可被用户控制 | 长回答要可读、上下文要可见但可收起，员工语言保持稳定 | AI 专属紫色、AI 监控状态、无限对话墙 |

### 2.1 Evidence limits

官方来源能证明设计系统原则和公开产品模式，不能证明 Curis 用户偏好或当前 Figma 的具体问题。Curis 的“好看”“疲劳”“第一眼抓住重点”仍是 `UNVERIFIED`，必须由固定内容、固定视口、CEO 比较评审验证。

## 3. Visual philosophy test

### 3.1 Candidate: Calm Surface / Strong Focus / Rich Work

**Calm Surface**：中性背景、低噪音边界、受控圆角、少量 elevation、稳定的中文阅读节奏。

**Strong Focus**：每个视口只有一个 L1 主焦点；焦点用位置、字号、留白、对比和必要的 surface 联合表达，不只靠颜色。

**Rich Work**：Result、Evidence、Decision、Handoff、Goal、Current Activity 等真实对象保留，但通过支持层级、折叠、分组和内容宽度管理，而不是压缩成一堆小卡片。

结论：`CANDIDATE / 成立，但需要 Figma benchmark`。它与 Frozen Calm Executive Workspace 一致，但本轮首次把视觉焦点和 attention budget 作为明确可测规则。

## 4. Visual focus hierarchy L1–L4

| Level | Meaning | Typical content | Primary variables |
|---|---|---|---|
| L1 Primary Focus | 当前页面必须先理解/处理的一个经营重点 | Decision、Current Work、Insight、Conversation、Critical Change、当前 Business Object | position, scale, weight, contrast, whitespace; accent only when semantic |
| L2 Active Context | 解释 L1 所属的当前范围和状态 | Employee、Surface、Cycle、Work state、Current Workspace | proximity, medium contrast, concise label, restrained surface |
| L3 Supporting Work | 让用户判断和行动所需的支持内容 | Result、Handoff、Evidence、Plan、related objects、supporting metrics | rows, dividers, disclosure, smaller type |
| L4 Reference | 需要可追溯但不应抢焦点的来源 | time、source、history、file、technical metadata | tertiary text, compact spacing, hover/detail |

候选硬约束：一个视口默认一个 L1；L2 不超过三个主要上下文块；L3 可丰富但必须可扫描；L4 不参与第一眼竞争。多个 L1 只有在明确比较/决策场景中允许，并要说明比较关系。

## 5. Visual attention budget

### 5.1 Candidate budget

- 1 Primary Focus。
- ≤2 明显 accent areas。
- ≤1 Primary CTA。
- Raised surface 高度稀缺：默认 0，焦点/overlay 才可使用。
- 首屏首扫中，不超过 7 个可独立识别的信息组。
- 可见状态颜色只给会改变用户判断或行动的状态。

### 5.2 Review questions

每张设计稿必须回答：如果遮掉所有颜色，L1 仍然明确吗？如果隐藏 L4，任务是否更清楚？Primary CTA 是否唯一？哪个元素可以删除而不损失经营判断？若没有答案，说明“所有东西都重要”。

## 6. Typography research

`CANDIDATE` 中文优先、英文辅助、数字可扫描。候选语义层级：Display/Focus、Page Title、Section Title、Object Title、Body、Supporting、Metadata、Label、Interactive Text。

| Role | Candidate size | Weight | Line-height | Use |
|---|---:|---:|---:|---|
| Display/Focus | 28–36 | 600 | 1.15–1.25 | 极少数 L1 / CEO attention |
| Page Title | 22–24 | 600 | 1.25–1.35 | 页面主标题 |
| Section Title | 17–18 | 500–600 | 1.30–1.45 | 区域和对象分组 |
| Object Title | 15–17 | 500 | 1.35–1.50 | Work / Employee / Result 名称 |
| Body | 14–15 | 400 | 1.55–1.70 | 默认中文阅读 |
| Supporting | 13–14 | 400 | 1.45–1.60 | 解释、辅助内容 |
| Metadata/Label | 11–12 | 400–500 | 1.40–1.55 | L4、状态、时间、控件 |
| Numeric | 13–18 | 500–600 | 1.30–1.45 | tabular-nums、比较、指标 |

规则：正文不使用 Light；中英文混排需在实际字体上校验视觉大小；数字使用 tabular-nums；中文长文优先保证行高和行宽；不要通过加粗解决所有层级。候选字体栈延续系统字体优先：SF/系统 sans + PingFang SC / Microsoft YaHei fallback；具体字体仍 `UNVERIFIED`。

## 7. Spacing rhythm and density

候选 4px 基础节奏，语义级别为 4/8（micro）、12/16（component）、24（section）、32/48（page）、64+（极少数 hero/empty）。

- spacing 表达相邻关系；divider 表达同层分隔；surface 表达范围/状态；card 表达独立对象。
- Comfortable 是普通用户默认；Compact 只减少行间与 chrome，不把正文压到不可读。
- 任何页面必须同时通过 1440×900 和 1280×800；移动/窄宽度是重排和优先级测试，不是把桌面压缩成窄列。
- `UNVERIFIED`：具体中文行长、comfortable/compact 的最终 px，需要 Research / Employee Conversation benchmark。

## 8. Content width modes

| Mode | Surfaces | Candidate behavior |
|---|---|---|
| Reading | Conversation、Research、Evidence | 约 640–760px 主阅读列；长回答不铺满 |
| Work | Current Work、Employee Profile、Workspace | 720–1040px；允许主内容 + 轻 Utility |
| Operating | Business、CEO Desk | 920–1200px；优先一个叙事和少量并列 supporting work |
| Dense Data | Table、Calendar、Metrics | 可横向扩展，但列/行有稳定锚点和 sticky context |

不采用“所有 Main 一个 max-width”。宽度由阅读、判断、操作密度决定；Shell 的 Context/Main/Utility 职责保持不变。

## 9. Color roles

颜色首先承担语义，不承担分类装饰。候选角色：`brand.primary`、`focus.primary`、`focus.soft`、`action.primary`、`action.secondary`、`surface.canvas/default/subtle/focus`、`text.primary/secondary/tertiary/on-brand`、`border.default/subtle/focus`、`attention.pending/warning/critical`、`success`、`error`、`employee.active/blocked`。

关系规则：品牌色 ≠ 所有 CTA；status 色必须同时有文字/图标/形状；focus.soft 不能替代真实状态；domain accent 不能改写 Curis semantic roles。Deep Green 结论是 `CANDIDATE / 保留但降频`：可用于品牌锚点、主行动和少量 focus；大面积背景、所有链接、所有 active 状态不宜使用。

不冻结 Hex。Light/Dark 需使用 semantic role 映射；不是简单反转。对比度、色盲、focus indicator 需在候选稿中逐项检查。

## 10. Brand identity without brand wash

Curis 的识别度来自组合：安静中性表面 + 深绿少量焦点 + 中文排版节奏 + 责任主体的 Employee presence + Work/Result/Evidence 的清晰引用 + 稳定的 spacing 和克制 motion。Logo 只是入口，不是页面背景。禁止 gradient SaaS、彩色 domain skin、AI sparkle 作为默认品牌符号。

## 11. Domain accent boundary

允许出现在：图表系列、Calendar/Content 类型、Domain Object 标识、专业可视化、明确的领域状态。禁止出现在：Company OS shell、主导航、通用 Composer、页面基础文字、通用 Employee 身份、默认 Button、Focus L1 的基础语义。Curis identity 永远高于 XHS/RD/Commerce identity；领域色最多是“辅助注释”。

## 12. Surface, elevation, border, radius, shadow

候选层级：Canvas → Default Surface → Focus/Raised → Overlay。Raised 只给可被移动/操作的对象、单个重要焦点或需要脱离背景的暂时内容；Overlay 只给 popover、dialog、menu、floating action。普通分组优先用空白、对齐、divider、subtle surface。

Card policy：

- **Must Card**：独立可操作对象、明确 selected/focus object、跨内容边界的 action group、需要脱离背景的 overlay。
- **Can Card**：一组需要整体扫描或整体操作的经营摘要、单一 Focus Surface。
- **禁止 Card**：每条消息、每个 KPI、每个 metadata、每个 section、每个 employee、仅为“看起来完整”的空容器。

候选 border：默认用低对比 hairline；同层分组可无边框；focus 用明确但不刺眼的 outline；shadow 只表达 elevation/overlay，不做装饰。候选 radius：4/6/8 为默认层级，10/12 仅为大型 focus/overlay；禁止所有组件统一 12px。具体值 `UNVERIFIED`。

## 13. Employee visual language

Employee 用统一身份组表达 Avatar/Name/Role/Scope/Status/Current Work/Conversation affordance。存在感来自名字、责任和当前工作，不来自在线绿点墙。状态应区分 Active、Blocked、Needs Attention、Unavailable，并以文字/图标/位置补充颜色。

### 13.1 Three-entry model

同一 Employee 的三入口保持同一身份头部与视觉锚点，但动作语义不同：

- Direct Conversation = Communication：Composer/阅读流优先。
- Current Work = Work Collaboration：Work object、进展、判断、结果优先。
- Employee Profile = Employee Identity：角色、责任、能力、历史与配置优先。

三者不是三个皮肤，也不是三个重复 Card；它们共享身份，改变主焦点。

## 14. Conversation and Composer

Conversation 采用阅读流，不采用聊天气泡墙。候选规则：CEO 与 Employee 通过稳定身份、对齐、轻量 label 区分；正文列优先 640–760px；长回答有标题、段落、列表和可折叠支持内容；Work/Result/Handoff/Evidence 以 inline reference 或轻量 Focus Surface 引用。

Composer 是共享入口：Input + 目标/路由 + Auto + Voice + Send；低频能力默认收起，Primary action 清楚，技术能力不抢主视觉。Focus/hover/disabled/expanded/attachment/voice/model-routing 要用状态和可访问 focus 表达，不能只靠颜色。Composer 的最终布局、目标选择和 Voice 形态 `UNVERIFIED`。

## 15. Current Work, Result, Evidence, Decision

Current Work 的主焦点是 Goal / Current Activity / Important Judgment / Result / Handoff；用标题、timeline、rows、渐进披露和单一 Focus Surface 建立“工作感”，不做 Dashboard Card Grid。

Result 是“产出了什么”；Evidence 是“凭什么相信/追溯”；Decision 是“需要谁在什么范围做什么选择”。统一使用对象标题、来源、状态和时间关系，不用三种大彩色 Card 粗暴区分：Result 偏产出阅读，Evidence 偏引用/展开，Decision 偏行动/批准。

## 16. Business / CEO Desk / dense data

CEO Desk 的 L1 是 CEO Attention / Decision；Business 的 L1 是 Operating State / Current Problem / Value；XHS/RD 的 L1 是当前专业 Work。三者共享同一 hierarchy，不共享同一 layout。

Table/List/Calendar/Metrics 先保证列、行、时间和比较关系，再使用颜色。指标不逐个卡片化；趋势用线、位置、数值和解释共同表达；表格可 Compact，但必须保留可读正文、行 hover、键盘 focus 和 status text。

## 17. Responsive desktop, dark mode, accessibility, motion

- 1440×900：Context/Main/Utility 都可见，L1 保持稳定。
- 1280×800：Utility 退为 overlay 或收窄，Main 不被挤成阅读困难的列。
- 1024：Context/Utility 优先折叠，L1 不迁移到装饰性 header。
- Dark mode：semantic roles 重映射，surface 层级靠明度/材质关系，不能反相；所有 focus/disabled/status 重新校验。
- Accessibility：对比度、键盘 focus、target size、文字缩放、色彩独立性、屏幕阅读器命名、disabled 可理解性都属于系统规则。Focus 不能只靠颜色。
- Motion：只服务 pane transition、utility open、focus change、employee response、work status update、decision arrival；默认短、可打断、可减少；禁止持续闪烁和装饰 spring。

## 18. Anti-patterns

| Anti-pattern | Why it fails Curis |
|---|---|
| Card Wall / Dashboard Wall | 把真实工作拆成同权重块，用户看不到主判断 |
| Pill Everywhere | 状态、导航、对象、动作失去语义差异 |
| Gray-on-Gray Everywhere | 层级靠猜，尤其伤害中文小字可读性 |
| Color Everywhere | 注意力预算失控，颜色不再表示风险/行动 |
| Everything Bold/Equal | 无法扫描，页面没有叙事 |
| Huge Empty Space | 把安静误做空洞，丢失真实工作 |
| Over-compressed Density | 把专业误做监控台，增加误读和疲劳 |
| Agent Monitoring Wall | Employee 被简化为在线状态和运行指示器 |
| File Manager Feel | Work/Decision/Evidence 失去经营语义 |
| Chat Bubble Wall | 长回答和引用难读，Curis 退化为聊天产品 |
| Engineering Console | 技术状态压过普通用户的经营意图 |
| Gradient AI SaaS | 用装饰替代品牌和层级，长时段疲劳 |
| Excessive Radius/Shadow | 所有对象都浮起，真正焦点消失 |

## 19. XHS Structural Candidate case study

结构正确之处：Multi-Surface Workspace、Employee Quick Panel、Direct Conversation、Current Work、Employee Profile，以及 Context/Main/Utility 职责已经形成可复用结构；三入口的产品模型不应在本研究中重做。

视觉未成熟的诊断假设：标题与对象名的 L1/L2 关系不足；Quick Panel、Conversation、Work 可能同时争夺焦点；Card/边界承担了过多结构；正文与 metadata 的中文字号/行高差异不够；Utility 可能以“第二个主页面”出现；domain accent 可能比 Curis focus 更抢眼。以上是 `INFERENCE / UNVERIFIED`，需要固定截图逐项验证，不能把它们当作当前 Figma 的已证事实。

## 20. Cross-domain stress test

| Rule | XHS | RD | CEO Desk | Business | Commerce | Shared? |
|---|---|---|---|---|---|---|
| One L1 per view | Work/Content | Work/Artifact | Decision/Attention | Operating Problem | Current Value | Yes |
| Neutral shell | Yes | Yes | Yes | Yes | Yes | Yes |
| Domain accent bounded | content type | artifact/status | none or semantic | portfolio grouping | object/chart | Yes |
| Reading width mode | research/content | evidence/code reference | decision brief | operating summary | dense object | Yes, mode varies |
| Card scarcity | result/focus only | artifact/focus only | attention packet only | group summary only | object summary only | Yes |
| Employee language | operator | engineer/researcher | leader/support | responsible leader | operator | Yes, role varies |

若某条规则只能让 XHS 好看，就不是 Shared Rule；只能保留为 Domain pattern。

## 21. Visual experiment plan and stop gate

下一步只做两个 benchmark screens：`Research`、`Employee Conversation`。三方向相同 IA、相同内容、相同交互模型：

- Direction A — Quiet / Neutral baseline：中性、低边界、阅读优先。
- Direction B — Curis Strong Focus：更明确 L1、深绿 focus、强弱更大。
- Direction C — Curis Focus + restrained Professional Accent：B 的焦点规则，加受限领域注释。

比较维度：2 秒首扫是否找到 L1；长内容是否舒服；Employee 三入口是否一眼可区分；Work/Result/Evidence/Decision 是否不混；Card 是否稀缺；1440/1280/1024 是否保持 Main Priority；普通用户是否需要解释。

完成三份文档后停止，等待 CEO Review。不得进入 Figma 修改、Frozen 更新、Frontend、Runtime、Package、Schema 或 DB。

## 22. Source map

- [Apple Human Interface Guidelines — Foundations](https://developer.apple.com/design/human-interface-guidelines/foundations) — hierarchy, color, layout, motion, typography, accessibility topics.
- [Apple — Accessibility](https://developer.apple.com/cn/design/human-interface-guidelines/accessibility) — contrast, larger text, color independence, screen-reader considerations.
- [Apple — Materials](https://developer.apple.com/design/human-interface-guidelines/materials) — semantic material use, legibility, light/dark behavior.
- [Atlassian Design — Foundations](https://atlassian.design/foundations) — spacing, color, typography, elevation, border, radius and token foundations.
- [Atlassian Design — Elevation](https://atlassian.design/foundations/elevation/) — raised/overlay scarcity and shadow pairing.
- [Linear Brand](https://linear.app/brand) — restrained, desaturated brand expression.
- [Figma — Design Systems 101](https://www.figma.com/blog/design-systems-102-how-to-build-your-design-system/) — semantic tokens, accessibility, typography, elevation.
- [Figma — The future of design systems is semantic](https://www.figma.com/blog/the-future-of-design-systems-is-semantic/) — variables, modes and semantic language.
- [OpenAI — Apps in ChatGPT](https://openai.com/index/introducing-apps-in-chatgpt/) — conversation plus contextual interactive surfaces.
- [OpenAI Help — ChatGPT Canvas](https://help.openai.com/en/articles/9930697-what-is-the-canvas-feature-in-chatgpt-and-how-do-i-use-it) — conversation-to-work surface transition.
- [Anthropic — Meet Claude](https://www.anthropic.com/claude) — conversation as research/drafting context.
- [Anthropic — Claude Design](https://www.anthropic.com/news/claude-design-anthropic-labs) — design-system-informed visual exploration and conversation-based refinement.

