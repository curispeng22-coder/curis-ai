# Curis · Workspace Engineering Product Translation（空间工程产品翻译 + 核心交互 / IA）

**Status**: WORKSPACE ENGINEERING PRODUCT TRANSLATION · **APPROVED CANDIDATE**（设计候选已批准 · 非 Frozen · 非最终高保真 · 非前端代码 · 非 Runtime/Connector）
**阶段**: PRODUCT / WORKSPACE DESIGN — Product Translation + Core Interaction / IA（承接《Workspace Engineering Product Handoff》）
**上位依据（只引用，不重定义）**:
- `CURIS_WORKSPACE_ENGINEERING_PRODUCT_HANDOFF.md`（Review · 已 READY FOR PRODUCT TRANSLATION）
- `Curis_Workspace_Shell_Contract_And_Shared_Patterns.md`（Frozen · P1–P7 · 四独立 Pane · T1/T2/T3 · 无 Global Topbar）
- `Curis_Company_OS_Shared_Authority.md` + `Curis_Content_Growth_Domain_Authority.md`（Frozen · M1 语义真相层）
- Content Growth 已完成并收口的 **Frozen Authority（语义真相）** / **UX/IA Exploration（体验探索）** / **Product Model Closure（产品模型收敛）** 三阶段（见 Handoff §1 定义，本文引用其结论、不复述其研究）
- `WORKSPACE_PACKAGE_TECHNICAL_PROPOSAL.md`（TECHNICAL DIRECTION APPROVED CANDIDATE · **`NOT IMPLEMENTED`**）

**本轮边界（硬约束）**：
- 不重新研究业务方法（Domain Expert Research 已由上游完成）。
- 不重新定义 Handoff 中已裁定的语义（Office⊥Org、Target≠Eligibility、OAuth 失效 BLOCKED 不删、Publication per-Account、Shared Employee≠Shared Context、Bottleneck≠缺员工、三层 WHAT/WHO/HOW、Frozen Authority 语义、八步飞轮/五层为内部不进用户视野）。
- 不把 Package / Gate / Router / Schema 等内部概念暴露给用户。
- 不进入最终视觉高保真、不进 Figma、不写前端。
- 不修改 Frozen Authority / Shell / P1–P7 / Product Blueprint / XHS·RD Instance / Runtime / Connector / 代码 / UI。

> **与 Content Growth 翻译的关系**：本批「空间工程」翻译与已收口的 Content Growth Operating Strategy UX Translation 是**同一套产品语言的两段**。Content Growth 已落地的用户面约定（Business Home 八问、经营方式聚合入口、默认/单独设置/例外三态、Employee Method = Shared Employee Detail 内「工作方式」扩展、Conversation + Direct Edit 同一份方法、capability 以「需连接 X」呈现、失败/缺口卡对齐 Frozen Shell）在本文**直接复用**，不重复发明。本文只新增「空间如何被创建 / 启用 / 进化」这一段 CEO 体验，并明确哪些现在可定、哪些等 P0。

> **Product Translation Review 批准 + 一处语义修正（APPROVED CANDIDATE）**：Review 通过，状态升 APPROVED CANDIDATE。仅做一处产品语义修正：**Capability Gap 不再默认全部阻塞 Workspace 激活**，按「Required for Activation（启用必需）/ Required for Specific Action（某项功能需要）/ Optional·Enhancement（可增强）」三分类；用户侧仍只用自然语言（如「启用前需连接 X」/「连接 X 后可用 Y」/「可稍后连接 X 获得增强」），不暴露 Capability Primitive。其余设计未重做。详见 §8 / §9 Q6 / §10。

---

## 0. 阅读指引与本批范围

本文回答 Handoff §12.1 的 8 个设计问题，并把 Handoff §5 的三条用户旅程翻译成 CEO 真实体验。本文**不设计界面像素**，只确定：

1. 信息架构（IA）——这些体验落在 Frozen Shell 的哪个位置、用哪些已注册 Surface；
2. 三条旅程的 CEO 触点时序（入口 → 背景自动 → Proposal → 决策 → 激活 → 进化/失败）；
3. 哪些设计**现在就可以定**（落在 Frozen Shell + 允许 Surface + Package Domain Schema 概念内），哪些**必须等 P0 Runtime 验证**（见 §11）。

本文结束状态为 `WORKSPACE ENGINEERING PRODUCT TRANSLATION APPROVED CANDIDATE`（见配套 Review 文档）。**不进入高保真；待 P0 返回后做 Technical Reality Delta Review。**

---

## 1. 信息架构（IA）总览

### 1.1 两个层级 + 一个轻量流

空间工程在 Frozen Shell 上只新增两层，不新增导航维度、不新增 Surface 类型：

| 层级 | Frozen Shell 落点 | 角色 | 复用 Surface（注册表内） |
|---|---|---|---|
| **经营总览（Company Home）** | Navigation 六区之一（公司层）+ Main 承载 | 所有「经营方向 / 业务空间」的聚合入口；新业务创建 / 已验证业务启用的入口所在地 | status-owner summary / object list / activity timeline / empty-failure-gap card |
| **业务空间首页（Business Home，per 经营方向）** | Navigation 进入某业务 → Main 承载 | 单个业务的可运营主屏（Content Growth 已落地的八问模型在此复用） | status-owner summary / activity timeline / Employee Presence / Result Reference list / Evidence list / empty-failure-gap card |
| **创建 / 启用流（Creation Flow）** | 从经营总览发起的专注流；Main 承载，Context 显示「Curis 正在准备」渐进状态，Utility 显示验收证据 | 表达经营意图 → 看 Proposal → 确认激活；不是常驻页面，是一次性引导流 | object detail / field editor（仅目标适配）/ activity timeline / Evidence list / empty-failure-gap card |

> **纪律**：不采用 Global Topbar；创建流不在 Navigation 占常驻项；不新增任何 Surface 类型（仅用 Handoff §11.2 注册表：object list / object detail / field editor / status-owner summary / Employee Presence / Result Reference list / Evidence list / activity timeline / empty-failure-gap card）。

### 1.2 与 Content Growth 的关系

- Content Growth 是**第一个被创建出来的业务空间**，它自身走 §2.A（新业务）或 §2.B（已验证 Template）之一；它运行后，其 Business Home 就是 §1.1 第二行的实例。
- 后续每新增一个业务空间，都复用同一套创建流与 IA，不重新设计。
- 「经营方式 / 当前经营节奏 / 最近学到了什么 / 进化通知」等 Content Growth 已定义的能力，在 Business Home 层被本 IA 复用，不是本批新设计。

---

## 2. 三条用户旅程的 CEO 产品体验

> 通用原则（来自 Handoff §3）：旅程中的「系统 / 专家自动阶段」**对 CEO 不可见**，CEO 只在少数经营决策点出现。下文每个旅程分「CEO 可见」与「背景（不可见）」两栏。

### 2.A · 新业务空间首次创建

| 阶段 | CEO 可见 | 背景（CEO 不可见 · 由 Curis 系统/专家完成） |
|---|---|---|
| 入口 | 经营总览 → 「创办新业务」 | — |
| 表达意图 | 轻量引导：回答「你想经营什么结果 / 怎样算成功」（经营意图，非功能清单）；可一句话开始 | — |
| 系统构建 | 看到「Curis 正在为你准备这个业务空间」的友好进度（**不是闸门**，只是背景状态） | 领域研究 → 经营方法提炼 → 收敛 Handoff → 产品翻译 → 能力审查 → 空间组合 / Semantic Model / Design → Package 组合 → 验收（7 项真实证据） |
| Proposal | 看到 **Workspace Proposal**（这门业务在你这里长什么样，见 §4） | — |
| 决策 | **业务意图确认**（目标/指标/边界）+ **策略边界与经营规则适配**（这门业务默认怎么运行、红线在哪）+ **激活确认** | — |
| 激活 | 「已启用 · 现在可以运营」→ 进入该业务的 Business Home | — |
| 失败/缺口 | 若出现能力缺口 → capability-gap 卡「需连接 X」并阻塞激活；若构建失败 → failure 卡（重试/引导） | 验收失败 → 返工，不伪完成 |

CEO 感知总结：**「我想经营什么 / 成功是什么」→ 看到「已为你建好可运营的空间」→ 确认启用。** 全程不配置内部机制。

### 2.B · 已验证 Template 实例化

| 阶段 | CEO 可见 | 背景（CEO 不可见） |
|---|---|---|
| 入口 | 经营总览 → 「启用一个已验证的业务」（如「启用内容增长」） | — |
| 匹配 | 选择 Template；系统提示「将复用已验证的研究与方法」 | Template Match（匹配已验证版本） |
| 目标适配 | 填**最少信息**（见 §9 Q8）：经营方向名 + 主要目标（从候选选）+ 要启用的账号（选已连接账号） | — |
| 能力检查 | 若缺连接 → capability-gap 卡「需连接 X」 | 复用已验证研究/Handoff/Translation 证据；仅新增意图/匹配/适配/能力检查/实例生成证据 |
| Proposal | 看到针对本公司的 Proposal（结构同 §4，但大部分已预填） | 生成 Instance + 验收 |
| 决策 | **激活确认**（意图已在适配时确认，此处只确认启用） | — |
| 激活 | 「已启用 · 立即得到可运营空间」 | — |

CEO 感知总结：**「启用内容增长」→ 填少量本公司目标/账号 → 立即得到可运营空间。** 不重做完整领域研究。

### 2.C · 已有 Workspace 进化

| 阶段 | CEO 可见 | 背景（CEO 不可见） |
|---|---|---|
| 触发 | 业务空间「自己变好了」；Business Home 浮现「最近变化 / 最近学到了什么」 | 运营学习发现经营方法需调整 → 从受影响最早阶段重入 → 重过相关 Gate → 生成 Candidate 版本 → 验收 |
| 轻量进化 | 自动微调留痕可查（如发布时段内优化），不需 CEO 批准 | 在授权范围内自主调整 |
| 结构性变更 | **仅在此处**收到确认请求（Needs CEO / P7 语义）：「建议把教程内容占比提高，是否采纳？」 | 结构性变化走决策包 |
| 拒绝/采纳 | CEO 决定；采纳即新经营方法生效 | 受影响上游重跑，未受影响证据复用 |

CEO 感知总结：**空间「自己变好了」；只在结构性变化时收到确认请求；不受影响的上游不重跑。** 与 Content Growth 已定义的「进化三类 / 最近学到了什么 / 提案 vs Needs CEO」完全一致（本文不重复，仅把同一机制确认为「所有业务空间通用」）。

---

## 3. Business Intent 入口设计（Handoff §2）

**Business Intent = CEO 的经营意图，不是功能诉求。**

- 入口位置：经营总览的「创办新业务」是**轻量引导**，不是配置表单、不是「加页面 / 配 Agent」的后台。
- 表达形式：先用一句话或几个自然语言选项开始（例：「我想做内容增长获得客户」），再由 Curis 把意图结构化为《经营目标 / 主次成功指标 / 范围边界 / Non-goals》——这一步是系统/专家后台完成，CEO 只确认结果。
- **禁止**：把「CEO 说想加个 X 功能」直接当成业务意图；把功能列表当作成功判据；让 CEO 填写内部原语（Office / Intent / Routing / Queue / Token）。

> 本批**不设计 Business Intent 的填写表单**——它属于上游「意图结构化」的产物，CEO 在这一步只做轻量表达 + 结果确认。界面语言见 §2.A 入口行。

---

## 4. Workspace Proposal（用户面，须回答 Handoff §6 的 6 问）

Proposal 是 CEO 在激活前看到的「这门业务在你这里长什么样」。它必须回答：

1. **经营方向**——这门业务为 CEO 贡献什么经营结果（不是功能清单）。
2. **成功长什么样**——CEO 在主屏能看到什么经营层状态/指标（用 status-owner summary，不堆 Dashboard）。
3. **要启用哪些空间**——经营总览（聚合）+ 按需进入的 Professional Workspace（深度工作）；不做超级 Workspace。
4. **默认怎么运行**——系统默认行为（CEO 无需配置）；哪些可「这个账号单独设置 / 这次例外」（三态自然语言表达，见 §9 Q4）。
5. **用户能直接做什么 / 系统替 CEO 做了什么**——复杂度默认隐藏。
6. **需要连接什么（Capability）**——以「需要接入 X 平台 / 工具」呈现，不是「缺一个 Connector Primitive」（见 §8 / §9 Q6）。

> Proposal 是**一份可读的经营说明**，不是设置面板。CEO 在这里「看懂并决策」，不在这里「配置」。

---

## 5. CEO 真实决策点（Handoff §3.2，内部 Gate 不进 UI）

CEO 只在以下经营决策点出现；Handoff 的 6 道内部 Gate（BUSINESS UNDERSTANDING / PRODUCT TRANSLATION / AUTHORITY·CAPABILITY / DESIGN / IMPLEMENTATION ACCEPTANCE / OPERATING LEARNING）**对普通用户不可见、不画成 UI、不让用户自行通过**。

| CEO 决策点 | 拍板什么 | 用户面呈现 |
|---|---|---|
| **业务意图确认** | 经营目标 / 成功指标 / 范围边界 / Non-goals | Proposal 顶部「确认这门业务的经营目标」 |
| **策略边界与经营规则适配** | 这门业务默认怎么运行、哪些可调、红线在哪 | Proposal 中「默认这样运行 / 这个账号单独设置 / 这次例外」 |
| **激活确认（Go Live）** | 是否正式启用已验收的空间 | 「确认启用」按钮；看到的是「可运营的空间」不是工程开关 |
| **进化结构性变更** | 是否调整经营方法 / 增员 / 重构业务空间 | Business Home 的 Needs CEO 决策包（P7 语义） |

> **铁律重申**：CEO 绝不被迫配置 Routing / Queue / Organization / Employee 绑定 / Token 等内部机制。这些由系统自动完成，CEO 只感知经营层结果。

---

## 6. 激活 / 投入运营（Go Live）

- 激活是**确认动作**，不是工程部署开关。CEO 点「确认启用」后看到的是「可运营的空间」（Business Home 已就绪），而不是「构建成功 / 包已安装」等内部状态。
- 激活前若能力检查返回 `MISSING` / `NEEDS_AUTH`（见 §8），激活被阻塞并提示「需连接 X」，不静默放行。
- 激活后，业务空间进入运营，Business Home 开始呈现经营状态、AI 在做什么、机会、决策、进化通知。

---

## 7. 进化通知（Evolution，Handoff §5.3）

- 进化通知是 Business Home 的轻量浮现（复用 Content Growth「最近学到了什么 / 最近变化」机制），不是独立页面。
- 轻量自动微调（授权范围内）→ 留痕可查，不弹确认。
- 结构性变更 → 以 Needs CEO 决策包（P7 语义）呈现，CEO 采纳/拒绝即生效。
- 不受影响的上游证据复用，不重跑；Candidate 版本验收后才替换。

---

## 8. 失败 / 能力缺口状态卡（对齐 Frozen Shell）

复用 Handoff §11.2 注册表中的 **empty-failure-gap card** Surface，三态：

| 状态 | 触发 | 用户面呈现 |
|---|---|---|
| **empty** | 业务刚创建、尚无运营数据 | 「这个业务还在起步，先确认经营目标」+ 引导 |
| **failure** | 构建/验收失败（如 Package 组合不通过） | failure 卡：发生了什么（白话）+ 重试 / 查看详情（Evidence list）；**不伪完成** |
| **capability-gap** | 能力检查 `MISSING` / `NEEDS_AUTH` / `UNSUPPORTED` | 按 §8.1 三分类呈现自然语言；**不再默认全部阻塞激活** |

### 8.1 Capability Gap 三分类（不默认全部阻塞激活）

Capability 缺口**不默认全部阻塞 Workspace 激活**。按对业务运行的影响分三类，用户侧只用自然语言，不暴露 Capability Primitive：

| 分类 | 用户面自然语言 | 对激活 / 功能的影响 |
|---|---|---|
| **Required for Activation（启用必需）** | 「启用前需先连接 X 平台/工具」 | 阻塞激活，直到连接；连接后可启用 |
| **Required for Specific Action（某项功能需要）** | 「连接 X 后，[某功能，如自动发布] 才能用」 | **不阻塞激活**；该特定功能在连接前不可用（置灰/提示），其余功能正常 |
| **Optional / Enhancement（可增强）** | 「可稍后连接 X，获得增强（如更全的数据看板）」 | 不阻塞；可启用后随时连接，纯增强 |

> 三类都来自同一份能力检查（权限 request，解析为 `AVAILABLE / MISSING / NEEDS_AUTH / UNSUPPORTED / UNKNOWN`），区别在「该能力对这门业务是否启用必需」——这是**产品语义层判定，不是 Capability Primitive 暴露给用户**。仍**不静默降级**：任何缺口都诚实呈现，绝不假装已具备。

Capability 缺口的用户语言规则（Handoff §7.2 / §9）：
- `REUSE`（已具备）→ 不提示。
- `EXTEND` / `DOMAIN SPECIFIC`（需少量接入）→「需连接 X」（按 §8.1 三分类定性为 Required for Activation 或 Required for Specific Action）。
- `MISSING` / `NEEDS_AUTH` → 按 §8.1 三分类呈现；仅 Required for Activation 阻塞激活。
- `UNSUPPORTED` / `UNKNOWN` → 「暂不支持 / 尚不确定」诚实呈现，不伪造。

> 权限是 **request**，解析为 `AVAILABLE / MISSING / NEEDS_AUTH / UNSUPPORTED / UNKNOWN`；缺失即诚实呈现、不静默降级（Handoff §11.4）。是否阻塞激活取决于 §8.1 三分类——仅 Required for Activation 阻塞，其余缺口不阻断启用。

---

## 9. 回答 Handoff §12.1 的 8 个设计问题（具体决策）

**Q1 · Business Home 只显示哪些经营层信息、如何避免堆 Dashboard？**
- 经营总览层：业务列表（名 / 状态 / 一句「最近变化」/ 有无待你确认），用 status-owner summary + activity timeline，**不**做指标网格。
- 业务空间层：复用 Content Growth Business Home 八问模型（公司今天按什么策略运行 / 重要机会 / AI 已自动做了什么 / 异常 / 用户反馈 / 最近学到什么 / 策略建议 / 需 CEO 决定的事）。
- 反 Dashboard 原则：每屏只回答「现在公司怎么经营 / AI 在做什么 / 为什么 / 学到什么 / 怎么改」，指标只在 Evidence list 按需展开。

**Q2 · 哪些对话驱动、哪些直接编辑？是否修改同一份底层方法？**
- 两者都修改**同一份**底层经营方法（禁止两套存储）。
- 对话：「把这个业务的目标改成涨粉」→ 更新 Business Proposal / Operating Method。
- 直接编辑：在业务设置 / Proposal 里改同一字段 → 同一结果。
- 与 Content Growth「Conversation + Direct Edit 同一份方法」完全一致。

**Q3 · 复杂度隐藏到什么程度？哪些内部原语绝对不出现？**
- 隐藏 Handoff §9 全部：Office/Organization/Intent/Account 内部原语、Responsibility Routing/Queue、Token/Credential/Keychain、Employee Primitive/P7 Decision、Handoff/Result Reference 内部机制、Workspace Package 内部结构、Core Expressibility/Capability Gap、八步飞轮/五层策略归属、Tenant/Company/Workspace 隔离。
- 判据：若用户需理解一个 Curis 内部 Primitive 才能用产品，说明翻译失败（违反 PRODUCT TRANSLATION GATE）。

**Q4 · 「默认这样运行 / 这个账号单独设置 / 这次例外」三态如何自然表达？**
- 自然语言三态 pill：「默认按经营方式运行」/「这个账号单独设置」/「这次例外」。
- 复用 Content Growth Operating Rules 三态；不出现「Policy inheritance / override 层级」等内部词。

**Q5 · Employee「怎么工作」以什么形式可见、且不等于后台配置？**
- 通过 **Shared Employee Detail**（右侧详情）内的「工作方式」扩展 Section 呈现（沿用 T5 裁定：Employee 始终是 Company OS Shared Employee，CG 只在 Detail 内加业务扩展，不改全局 Employee UI）。
- 不是工程配置后台；不暴露 Token 数 / 扫描秒数 / 内部评分。

**Q6 · 缺失 Capability 以什么用户语言呈现？**
- 按 §8.1 三分类自然语言：「启用前需连接 X」/「连接 X 后可用 Y」/「可稍后连接 X 获得增强」；capability-gap 卡只阻塞 Required for Activation，其余缺口不阻断启用。
- 不写「缺一个 Connector Primitive / Capability Gap 判定失败」。

**Q7 · 失败 / 空 / 能力缺口卡如何对齐 Frozen Shell？**
- 全部用注册表 **empty-failure-gap card** Surface；三态见 §8。
- 与 Frozen Shell 其他 Surface（Evidence list / activity timeline）配合呈现原因与进度。

**Q8 · Template 目标适配时 CEO 需填的最少信息是什么？**
- 经营方向名称（如「Curis AI 内容增长」）。
- 主要目标（从候选选：涨粉 / 获得客户 / 推广产品 / 建立个人影响力 / 做品牌 / 其他）。
- 要启用的账号（从已连接账号中选）。
- 其余全部复用已验证 Template 的研究/Handoff/Translation 证据，不重填。

---

## 10. Employee / Capability / Operating Rules 进入空间（复用 Handoff §7，落到用户语言）

- **Employee**：以「某员工怎么工作」呈现（Shared Employee Detail 内「工作方式」扩展）；一个员工可承担多职责，增长再拆；不虚构未绑定员工；不做工程配置后台。
- **Capability**：以「这个空间能做什么 / 需连接什么外部平台或工具」呈现；缺口按 §8.1 三分类（仅 Required for Activation 阻塞激活）；用户侧不暴露 Capability Primitive；权限是 request 不是 grant。
- **Operating Rules**：以「默认这样运行 / 这个账号单独设置 / 这一次例外」三态呈现；不暴露内部规则引擎；平台事实用四态（VERIFIED / CONDITIONAL / UNKNOWN / UNAVAILABLE），不把研究中的第三方数字写死成产品规则。

---

## 11. 现在可确定 vs 必须等待 P0 Runtime 验证（决策矩阵）

> 依据 Handoff §8 / §10 / §11。设计**面向** Package First 模型，但 P0 之前没有可运行 Runtime 替我们证明「它能真的跑起来」。

### 11.1 现在就可以确定（落在 Frozen Shell + 允许 Surface + Package Domain Schema 概念内）

| 设计项 | 确定内容 |
|---|---|
| IA 布局 | 经营总览 / 业务空间首页 / 创建·启用流 在 Frozen Shell 四 Pane 内的位置与角色 |
| Surface 类型 | 仅用注册表 9 种，不新增任何 Surface 类型 |
| 内部概念隐藏 | Handoff §9 全部内部原语不进用户视野 |
| CEO 决策点 | 4 个经营决策点语义（意图确认 / 规则适配 / 激活 / 结构性进化） |
| Workspace Proposal | 6 答结构（§4） |
| 三态表达 | 默认/单独设置/例外 自然语言 pill |
| Employee 可见 | Shared Employee Detail 内「工作方式」扩展（T5 裁定） |
| Capability 缺口 | 「需连接 X」+ capability-gap 卡；不静默降级 |
| 进化通知 | Business Home 轻量浮现 + 结构性变更走 P7 决策包 |
| 同一份方法 | Conversation + Direct Edit 修改同一底层（§9 Q2） |
| 失败/空/缺口 | empty-failure-gap card 三态（§8） |
| Package First 思维 | 用「Surface 组合 / 领域对象 / 允许 Action / 能力需求」思考，不写页面 |

### 11.2 必须等 P0 Runtime 验证（Handoff §11 明确禁止现在假设可行）

| 待验证项 | 为什么现在不能确定 |
|---|---|
| 动态安装未知 Workspace | 当前已安装 Curis 不能不改源码、不重建就装新 Workspace（§11.1） |
| 任意新 Surface 类型 | 只能用 Frozen Shell + 有限 Core Surface 注册表（§11.2） |
| 自定义领域对象自动运行 | P0 前只能通用领域对象投影 + Package Schema 校验（§11.3） |
| Capability 检查自动通过 | 权限是 request，缺失即阻塞，不静默降级（§11.4） |
| 签名 / 市场 / 第三方信任 | P0 只做受控本地包 + digest 校验（§11.5） |
| 升级 / 迁移 / 回滚 | P0 只做版本钉扎与不兼容升级明确拒绝（§11.6） |

> 当前交付路径（CURRENT DELIVERY PATH）= Instance Design → Gap Audit → bounded Issue → 改源码 → Rebuild；该路径**不能冒充** Target Package Runtime。CEO 体验层面两者一致（表达意图 → Proposal → 激活），但「是否能自助、不改源码就上新业务」要等 P0 用真实证据回答。

---

## 12. 禁止自行重新定义的语义（引用 Handoff §12.2 裁定，逐条引用不重解释）

以下语义已由产品/方法论裁定，本文**只引用消费**：
- **Office 与 Organization 正交**——「经营方向」与「组织/公司结构」独立维度，不混。
- **Target ≠ Eligibility**——发布目标与「是否有资格/已授权」不同概念，不合并。
- **OAuth 失效仅 BLOCKED 不删 Target**——授权失效时发布目标保留为受阻状态，不被删除。
- **Publication per-Account 真相**——发布是「逐账号」事实，不是全局一次性动作。
- **Shared Employee ≠ Shared Context**——共享员工不代表共享其上下文/记忆（T5 已落地）。
- **Bottleneck ≠ 缺员工**——瓶颈是流程/能力受限，不等于「需要更多员工」（⑨ 未 Frozen，未来以 Frozen P7 白话表述）。
- **三层职责语义**：Process-asks-WHAT · Org-decides-WHO · Capability-determines-HOW。
- **Frozen Authority 语义**：Content Growth Domain Authority（①②③④⑤）+ Company OS Shared Authority（⑥⑧⑦ + Context Isolation）。
- **八步飞轮 / 五层策略归属是内部经营模型**——只用于领域专家建立方法，不进用户视野。

> 若翻译中发现某裁定语义与新业务冲突，回到 Methodology / Domain Expert 走变更流程，**不在设计层自行推翻**。

---

## 13. 状态

```text
WORKSPACE ENGINEERING PRODUCT TRANSLATION APPROVED CANDIDATE
```

（承接《Workspace Engineering Product Handoff · READY FOR PRODUCT TRANSLATION》；本文为 **APPROVED CANDIDATE**；不重新研究、不重定义已裁定语义、不暴露内部原语、不进高保真、不改 Frozen/Blueprint/Shell/P1–P7/XHS·RD/Runtime/Connector/代码/UI。本轮仅做一处语义修正：Capability Gap 三分类（§8.1）。暂不进入最终高保真；待 Workspace Engineering P0 返回真实 Runtime / PoC 结果后，做一次 **Technical Reality Delta Review**，再决定 Visual Design；其中 §11.2 六项须等 P0 Runtime 验证。）

---

*Curis Workspace Engineering Product Translation · APPROVED CANDIDATE（非 Frozen · 非高保真 · 非 Runtime · 非新架构）*
