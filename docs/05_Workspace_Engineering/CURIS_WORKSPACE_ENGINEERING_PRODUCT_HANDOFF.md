# Curis · Workspace Engineering Product Handoff（空间工程专业交接 · 给 Product / UX Designer）

**Status**: `Review`
**Handoff State**: `WORKSPACE ENGINEERING PRODUCT HANDOFF READY FOR PRODUCT TRANSLATION`
**类型**: 专业交接（方法论层 → 产品/设计层）
**日期**: 2026-08-16
**From**: Workspace Engineering Methodology Expert（空间工程方法论专家）
**To**: Curis Product Expert / UX Designer（产品专家 / 设计专家）
**上位约束**（不修改）:
- `docs/05_Workspace_Engineering/Curis_Workspace_Engineering_Methodology.md`（APPROVED CANDIDATE）
- `docs/05_Workspace_Engineering/Curis_Workspace_Engineering_Lifecycle.md`（APPROVED CANDIDATE）
- `docs/05_Workspace_Engineering/Curis_Workspace_Engineering_Gates_and_Acceptance.md`（APPROVED CANDIDATE）
- `docs/05_Workspace_Engineering/Curis_Workspace_engineering_Expert_Handoff_Protocol.md`（APPROVED CANDIDATE）
- `docs/05_Workspace_Engineering/Curis_Workspace_Engineering_Content_Growth_Case_Study.md`（APPROVED CANDIDATE）
- `docs/05_Workspace_Engineering/Curis_RD_Methodology_Gap_Review.md`（APPROVED CANDIDATE）
- `docs/02_Architecture/WORKSPACE_PACKAGE_TECHNICAL_PROPOSAL.md`（TECHNICAL DIRECTION APPROVED CANDIDATE · `NOT IMPLEMENTED`）
- Content Growth 已完成并收口的 **M1 / M2 / M3**（见 §1 定义）

**铁律（本文件范围）**:
- ❌ 不重新研究业务（Domain Expert Research 已由上游完成）
- ❌ 不设计 UI（本文件只定义交接边界，设计在下游 Product Translation 阶段进行）
- ❌ 不修改 Workspace Engineering 方法论（6 份文档保持 APPROVED CANDIDATE / REVIEW）
- ❌ 不提出新架构（只引用已收口的 Technical Direction）
- ✅ 仅把「空间工程方法」正式交给 Product / UX Designer，明确边界、必答问题与禁止自行重定义的语义

---

## 0. 阅读指引

本文是 **Doc 4（Expert Handoff Protocol，领域专家→产品专家）的下游延续**：领域专家已把研究收敛为《Product Handoff》，现在方法论层把**整个 Workspace Engineering 方法**交接给 Product / UX Designer，让设计专家知道：

1. 自己从哪一步接手、上游已经替 CEO 和 Curis 系统做完了什么；
2. CEO 真正需要拍板的是什么，什么**绝不**该让 CEO 去配置；
3. 内部 Gate（方法论质量闸门）和用户可见交互有何本质区别；
4. 新业务创建 / 已验证 Template 实例化 / Workspace Evolution 三条用户旅程分别长什么样；
5. Operating Model 如何转成用户能看懂的 Workspace Proposal；
6. Employee / Capability / Operating Rules 如何以「用户语言」进入空间；
7. Package First 在产品层意味着什么（以及它**当前并未实现**）；
8. 哪些内部概念**不得**直接暴露给普通用户；
9. Frozen / Approved Candidate / Technical Candidate 三态边界；
10. P0 验证前，哪些东西**不能**交给设计师自行假设；
11. 设计专家需要回答的问题，以及**明确禁止自行重新定义**的语义。

> 本文结束时状态为 `READY FOR PRODUCT TRANSLATION`。**本文不进入 UX 设计**——设计工作由下游 Product Translation（Lifecycle 步骤 5）及其后的 Instance Design（步骤 8）承接。

---

## 1. 已收口的上游（来源基线）

设计专家接手前，以下材料已收口，作为本交接的不可动摇输入：

| 来源 | 身份 / 状态 | 设计专家如何使用 |
|---|---|---|
| **6 份 Workspace Engineering 方法论文档** | APPROVED CANDIDATE / REVIEW（非 Frozen） | 本方法的权威定义；引用不修改 |
| **M1 · Frozen Authority（语义真相层）** | `Curis_Company_OS_Shared_Authority.md` + `Curis_Content_Growth_Domain_Authority.md`（**Frozen**） | 业务语义真相的唯一来源；引用不重定义 |
| **M2 · UX / IA Exploration** | 5 份 DESIGN RECOMMENDATION（**APPROVED**，未 Frozen） | 体验探索结论；可消费但非终态 |
| **M3 · Product Model Closure** | `Curis_Content_Growth_Product_Model_Closure.md`（**APPROVED**，未 Frozen） | 产品模型收敛结论；Office→「经营方向」等已裁定 |
| **当前 Technical Direction** | `WORKSPACE_PACKAGE_TECHNICAL_PROPOSAL.md`（TECHNICAL DIRECTION APPROVED CANDIDATE，**`NOT IMPLEMENTED`**） | Package First 目标模型；设计只能**面向**它，不能假设它已运行 |

> **M1/M2/M3 说明**：这是产品团队对 Content Growth 已完成并收口的三阶段里程碑的简称——
> **M1 = Frozen Authority（语义真相）**，**M2 = UX/IA Exploration（体验探索）**，**M3 = Product Model Closure（产品模型收敛）**。
> 它们代表「Content Growth 的经营方法已被研究、被翻译、被收敛、被 Frozen/APPROVED」，是本交接中 Operating Model → 用户语言这一段的现实样板。

---

## 2. CEO Business Intent（给设计师的入口理解）

**Business Intent = CEO 的经营意图，不是功能诉求。**

- 意图是**经营结果**（例：「我要做内容增长」「我要监督 AI 员工真实研发」），不是「我想加个 X 页面 / 配个 Y Agent」。
- Business Intent 由 **CEO 定意图 + 方法论专家结构化** 产出《Business Intent Brief：经营目标 / 主次成功指标 / 范围边界 / Non-goals》。
- **设计专家不定义 Business Intent，也不把它当界面需求。** 你接手时，意图已经明确，你的起点是「如何把这门已理解的经营业务翻译成用户能运营的产品」。

> ⚠️ 禁止：把「CEO 说想加个 X 功能」直接当成业务意图；把功能列表当作成功判据。

---

## 3. 系统自动完成的阶段 vs CEO 真正需要参与的 Decision Gate

Workspace Engineering 的大多数步骤由 **Curis 系统能力 + 方法论专家 + 领域专家 + 产品专家** 在后台完成，**不需要 CEO 参与**。CEO 只在少数经营决策点拍板。

### 3.1 系统 / 专家自动完成的阶段（CEO 不出现）

| 阶段 | 由谁完成 | CEO 是否参与 |
|---|---|---|
| Domain Expert Research（真实行业经营研究） | Domain Expert | 否 |
| Operating Model（经营方法提炼） | Domain Expert + 方法论专家 | 否 |
| Product Handoff（收敛单份） | Domain Expert | 否 |
| Product Translation（专业→用户语言） | Product Expert / Designer | 否 |
| Shared / Domain Capability Review（REUSE/EXTEND/…） | Capability Engineer + 方法论专家 | 否 |
| Workspace Composition / Semantic Model / Design | Product Expert + 方法论专家 | 否 |
| Package Composition / Core Expressibility Check | Workspace Engineer + Core Engineer | 否 |
| Acceptance（7 项真实证据） | Quality（独立） | 否 |
| Operating Learning（经营信号回流） | Domain + Product Expert | 否（仅结构性变更需 CEO） |

### 3.2 CEO 真正需要参与的 Decision Gate（经营决策点）

| CEO 决策点 | 拍板什么 | 注意 |
|---|---|---|
| **业务意图确认** | 经营目标 / 成功指标 / 范围边界 / Non-goals | 这是意图，不是配置 |
| **策略边界与 Operating Rules 适配** | 这门业务默认怎么运行、哪些可调、红线在哪 | CEO 定「经营策略边界」，不调内部路由/队列 |
| **Go Live / 激活确认** | 是否正式启用已验收的 Workspace | 看到的是「可运营的空间」，不是工程开关 |
| **Evolution 结构性变更** | 是否调整 Operating Model / 增员 / 重构 Business Space | 仅在影响经营方法结构时 |

> ⚠️ **铁律**：CEO 绝不被迫配置 Routing / Queue / Organization / Employee 绑定 / Token 等内部机制。这些由系统自动完成，CEO 只感知经营层结果（「默认这样运行 / 这个账号单独设置 / 这次例外」）。

---

## 4. 内部 Gate 与用户可见交互的区别（关键澄清）

这是最容易被混淆的一点，必须分清：

| 维度 | 内部 Gate（6 道） | 用户可见交互 |
|---|---|---|
| 本质 | 方法论 / 质量闸门，保证「方法正确」 | CEO / 用户实际操作的 Workspace 表面 |
| 可见性 | **对普通用户不可见** | 用户每天看到并使用 |
| 例子 | BUSINESS UNDERSTANDING GATE / PRODUCT TRANSLATION GATE / AUTHORITY·CAPABILITY GATE / DESIGN GATE / IMPLEMENTATION ACCEPTANCE GATE / OPERATING LEARNING GATE | Business Home、Professional Workspace、Conversation、Employee Presence、Evidence |
| 谁过 | 方法论专家 + 对应角色签署 | CEO / 用户 |
| 失败后果 | 不得进入下一阶段（返工 / 伪完成） | 用户无法完成某经营动作 |

**核心纪律**：
- ❌ 不要把内部 Gate 画成 UI（用户不需要「通过业务理解闸门」）。
- ❌ 不要让用户「自行通过」某个方法论 Gate。
- ✅ 内部 Gate 是 Curis 工程质量的内部保证；用户交互是经营体验。两者在设计与实现上严格隔离。
- ✅ 设计专家在设计时**必须满足** Gate 的通过标准（例如 PRODUCT TRANSLATION GATE 要求内部原语隐藏），但 Gate 本身不进入界面。

---

## 5. 三条用户旅程（New / Template / Evolution）

设计专家需理解 CEO 会经历的三类旅程。**本文只描述旅程结构，不设计界面。**

### 5.1 A · 新业务空间首次创建
```
CEO 表达经营意图
→ [系统/专家] 领域研究 → Operating Model → 收敛 Handoff → 翻译
→ [系统/专家] 能力审查 → 空间组合 → Semantic Model + Design → Package
→ [系统/专家] 验收（7 项真实证据）
→ CEO 确认激活（Decision Gate）
→ 投入运营
```
- CEO 感知：回答「我想经营什么 / 成功是什么」→ 看到「已为你建好可运营的空间」→ 确认启用。
- 全程不要求 CEO 配置内部机制。

### 5.2 B · 已验证 Template 实例化
```
CEO 选择启用一个已验证 Template（如 Content Growth）
→ [系统] Template Match（匹配已验证版本）
→ CEO 做目标适配（本公司的经营方向 / 目标 / 账号）
→ [系统] 能力检查（复用已验证研究/Handoff/Translation 证据）
→ [系统] 生成 Instance + 验收
→ CEO 确认激活
```
- CEO 感知：「启用内容增长」→ 填少量本公司目标/账号 → 立即得到可运营空间。
- 不重新做完整领域研究；只新增「意图 / 匹配 / 目标适配 / 能力检查 / 实例生成 / 验收」证据。

### 5.3 C · 已有 Workspace 进化
```
[系统] 运营学习发现：经营方法需要调整
→ 从受影响的最早阶段重新进入（可能是 Operating Model，也可能是 Design）
→ 重过相关 Gate
→ 生成 Candidate 版本 → 验收
→ CEO 在结构性变更处确认
```
- CEO 感知：空间「自己变好了」；仅在结构性变化时收到确认请求。
- 不受影响的上游证据可复用，不重跑。

---

## 6. Operating Model 如何转成用户可理解的 Workspace Proposal

这是 Product Translation（步骤 5）的核心，也是设计专家的主战场。链路：

```
Domain Expert 的 Operating Model（8 维：目标/策略/规则/职责/方法/反馈/学习/进化）
        ↓ 收敛
Product Handoff（单份，唯一入口：能力 + 边界，不含页面）
        ↓ 翻译（设计专家）
用户语言产品：Workspace Proposal（CEO 看懂并决策的「这门业务在你这里长什么样」）
```

**Workspace Proposal（用户面）必须回答**：
1. **经营方向**——这门业务为 CEO 贡献什么经营结果（不是功能清单）。
2. **成功长什么样**——CEO 在主屏能看到什么经营层指标 / 状态。
3. **要启用哪些空间**——Business Home（聚合）+ 按需进入的 Professional Workspace（深度工作），不做超级 Workspace。
4. **默认怎么运行**——系统默认行为（用户无需配置）；哪些可「这个账号单独设置 / 这次例外」。
5. **用户能直接做什么 / 系统替 CEO 做了什么**——复杂度默认隐藏。
6. **需要连接什么（Capability）**——以「需要接入 X 平台 / 工具」呈现，不是「缺一个 Connector Primitive」。

> 原则：用户不学行业架构、不学 Curis 内部 Primitive、复杂度默认隐藏。八步飞轮 / 五层策略归属等**内部经营模型不进用户视野**（见 §9、§12）。

---

## 7. Employee / Capability / Operating Rules 如何进入空间

这三类要素都来自上游（Domain Expert 的 Operating Model + Capability Review），设计专家负责把它们**翻成用户语言**，不是重新定义它们。

### 7.1 Employee（员工）
- **来源**：Operating Model 的「职责 / Employee Method」→ 收敛 Handoff 的「Employee 需要展示什么」→ Package 的 Employee 模板。
- **用户感知**：能看到「某员工怎么工作」（Employee Method ≠ 复杂后台配置）；一个员工可承担多职责，增长再拆。
- **禁止**：把员工工作方式做成工程配置后台；虚构未绑定/未生效的员工。

### 7.2 Capability（能力）
- **来源**：Capability Review 的 `REUSE / EXTEND / DOMAIN SPECIFIC / MISSING` 判定 → Package 的 Capability 需求声明。
- **用户感知**：「这个空间能做什么 / 需要连接什么外部平台或工具」；缺失能力以「需连接 X」呈现，而非「缺一个 Primitive」。
- **禁止**：每 Workspace 重造一套责任/交接/验收/失败恢复；把 Package 需求声明显成「已具备该能力」（权限是 request，不是 grant）。

### 7.3 Operating Rules（经营规则）
- **来源**：Operating Model 的「规则 / 策略」→ Handoff 的边界与 Non-goals → Package 的 Strategy / Operating Rule 默认值。
- **用户感知**：「默认这样运行 / 这个账号单独设置 / 这一次例外」三态自然语言表达。
- **禁止**：把内部规则引擎暴露为配置面板；把研究中的第三方数字（权重/频率/最佳时间）写死成产品规则（平台事实四态：VERIFIED/CONDITIONAL/UNKNOWN/UNAVAILABLE）。

---

## 8. Package First 在产品层意味着什么

**Design target = 声明式 Workspace Package；源码修改不是默认交付方式。**

| 角度 | 含义（产品层） |
|---|---|
| 设计思维 | 用「Surface 组合 / 领域对象 / 允许 Action / 能力需求」思考，而非「写页面 / 改代码」 |
| 复用 | 优先复用 Frozen Shell Contract 与已有 Shared Pattern；不私造 Primitive |
| 当前事实 | **Dynamic Workspace Package Runtime `NOT IMPLEMENTED`**。当前已安装 Curis 不能动态安装未知 Workspace；Codex 能改源码 ≠ Curis 已具备动态搭 Workspace 能力 |
| 设计约束 | 设计只能**面向** Package First 模型（声明式 Surface / 通用领域对象 / Core 允许 Action 注册表），**不能假设**该 Runtime 已可运行 |
| 当前交付 | 明确标注为 `CURRENT DELIVERY PATH`（Instance Design → Gap Audit → bounded Issue → 改源码 → Rebuild）；该路径不能冒充 Target Package Runtime |

> 设计专家应假设：**你设计的东西最终要能用一份声明式 Package 表达**，但 P0 之前没有可运行的 Package Runtime 替你证明这一点。因此设计必须落在 Frozen Shell Contract + 有限的 Core Surface 注册表 + Package Domain Schema 概念之内。

---

## 9. 不得直接暴露给普通用户的内部概念

以下内部概念**必须隐藏**，仅在翻译层以用户语言呈现等价语义（如有）：

| 内部概念 | 用户面等价（如有） | 禁止 |
|---|---|---|
| Office / Organization / Intent / Account 内部原语 | 「经营方向」「账号」 | 暴露 Office/Organization 正交性等内部词 |
| Responsibility Routing / Queue | 「系统自动分配 / 排队处理」 | 暴露路由/队列配置 |
| Token / Credential / Keychain | 不可见；连接状态以「已连接/需连接」呈现 | 任何明文或内部令牌词 |
| Employee Primitive / P7 Decision | 「某员工怎么工作」「需要你确认」 | 暴露内部责任/决策原语 |
| Handoff / Result Reference 内部机制 | 「交接记录」「结果引用」 | 暴露 Handoff 工程语义 |
| Workspace Package 内部结构 | 不可见 | 暴露 manifest/schema/签名 |
| Core Expressibility / Capability Gap | 「暂不支持 / 需要连接 X」 | 暴露 Core Gap 判定过程 |
| 八步飞轮 / 五层策略归属（内部经营模型） | 不进用户视野 | 画流程图/配置树给用户 |
| Tenant / Company / Workspace 隔离 | 不可见 | 暴露隔离机制 |

> 判据：如果用户需要理解一个 Curis 内部 Primitive 才能用产品，说明翻译失败（违反 PRODUCT TRANSLATION GATE）。

---

## 10. Frozen / Approved Candidate / Technical Candidate 边界

设计专家必须清楚每个上游材料的**状态**，并据此决定能否引用、能否修改、能否假设其已运行。

| 状态 | 含义 | 设计专家行为 |
|---|---|---|
| **Frozen** | 终态真相，不可动摇 | M1（Company OS Shared Authority + Content Growth Domain Authority）。**只引用，不重定义**，即使发现更好的表述也先走变更流程 |
| **Approved Candidate** | 已批准候选，未 Frozen | 6 份方法论文档、M2（UX/IA 5 份）、M3（Product Model Closure）、9 份 CG 契约。**可消费、可参考，但非终态**；不要当成 Frozen 去「依赖其永不改变」 |
| **Technical Candidate / Technical Direction** | 技术方向候选，**`NOT IMPLEMENTED`** | `WORKSPACE_PACKAGE_TECHNICAL_PROPOSAL.md`。Package First 是可追求的目标模型，但**当前未实现**；设计不能假设其已运行 |

> 铁律：**Approved Candidate 不是 Frozen，Technical Candidate 不是已交付。** 把候选当 Frozen、把技术方向当已实现，是两类最常见的越界错误。

---

## 11. P0 验证前，不能交给设计师自行假设的内容

在 Dynamic Workspace Package Runtime 经 P0 PoC（客户反馈办公室）验证之前，以下**禁止**交给设计师自行假设为「已可行」：

1. **动态安装未知 Workspace**——当前已安装 Curis 不能不改源码、不重新 Build 就装新 Workspace。
2. **任意新 Surface 类型**——只能用 Frozen Shell Contract + 有限的 Core Surface 注册表（object list / object detail / field editor / status-owner summary / Employee Presence / Result Reference list / Evidence list / activity timeline / empty-failure-gap card）。
3. **自定义领域对象自动运行**——P0 之前只能用通用领域对象投影 + Package Schema 校验；不能假设每业务一套表/类已支持。
4. **Capability 检查自动通过**——权限是 request，解析为 `AVAILABLE/MISSING/NEEDS_AUTH/UNSUPPORTED/UNKNOWN`，缺失即阻塞，不静默降级。
5. **签名 / 市场 / 第三方信任**——P0 只做受控本地包 + digest 校验，不做通用 PKI / Marketplace。
6. **升级 / 迁移 / 回滚**——P0 只做版本钉扎与不兼容升级的明确拒绝；迁移/回滚是 post-P0。

> 设计专家的工作方式：**面向** Package First 模型设计，但所有「它能不能真的跑起来」的断言，必须等 P0 PoC 用真实证据回答。在此之前，设计落点限定在 Frozen Shell + 允许 Surface + Package Domain Schema 概念。

---

## 12. 设计专家需要回答的问题 & 明确禁止自行重新定义的语义

### 12.1 设计专家（在 Product Translation 阶段）必须回答的问题

不重新定义业务方法，只回答「如何把已收敛的专业方法翻译成用户可运营体验」：

1. CEO 在主屏（Business Home）**只**需要看到哪些经营层信息？如何避免堆 Dashboard？
2. 哪些交互是对话驱动、哪些是直接编辑？两者是否修改**同一份**底层经营方法（禁止两套存储）？
3. 复杂度隐藏到什么程度？哪些内部原语绝对不出现？
4. 「默认这样运行 / 这个账号单独设置 / 这次例外」三态如何在 UI 上自然表达？
5. Employee「怎么工作」以什么形式对用户可见、且不等于后台配置？
6. 缺失 Capability 以什么用户语言呈现（「需连接 X」而非「缺 Primitive」）？
7. 失败 / 空 / 能力缺口状态卡（empty / failure / capability-gap card）如何对齐 Frozen Shell？
8. 目标适配（Template 实例化）时，CEO 需要填的最少信息是什么？

### 12.2 明确禁止设计专家自行重新定义的语义（裁定语义，引用即准）

以下语义已由产品/方法论裁定（见 working memory §10 与 M1/M3），**设计专家只能引用消费，不得自行重新解释或改名**：

- **Office 与 Organization 正交**——「经营方向」与「组织/公司结构」是两套独立维度，不混。
- **Target ≠ Eligibility**——发布目标与「是否有资格/已授权」是不同概念，不合并。
- **OAuth 失效仅 BLOCKED 不删 Target**——授权失效时发布目标保留为受阻状态，不被删除。
- **Publication per-Account 真相**——发布是「逐账号」事实，不是全局一次性动作。
- **Shared Employee ≠ Shared Context**——共享员工不代表共享其上下文/记忆。
- **Bottleneck ≠ 缺员工**——瓶颈是流程/能力受限，不等于「需要更多员工」（⑨ 未 Frozen，未来以 Frozen P7 白话表述）。
- **三层职责语义**：`Process-asks-WHAT`（流程问做什么）· `Org-decides-WHO`（组织定谁做）· `Capability-determines-HOW`（能力定怎么做）。
- **Frozen Authority 语义**：Content Growth Domain Authority（①②③④⑤）+ Company OS Shared Authority（⑥⑧⑦ + Context Isolation）。这些是 M1 真相，引用不重定义。
- **八步飞轮 / 五层策略归属是内部经营模型**——只用于领域专家建立方法，**不进用户视野**，不得画给用户。

> 若设计中发现某裁定语义与新业务冲突，回到 Methodology Expert / Domain Expert 走变更流程，**不得在设计层自行推翻**。

---

## 13. 设计专家的起点清单（READY FOR PRODUCT TRANSLATION）

你接手时，应已持有：

- [ ] 6 份 Workspace Engineering 方法论文档（APPROVED CANDIDATE）
- [ ] M1（Frozen Authority）/ M2（UX/IA APPROVED）/ M3（Product Model Closure APPROVED）
- [ ] 当前 Technical Direction（Package First，`NOT IMPLEMENTED`）
- [ ] 上游《Product Handoff》（单份收敛，领域专家产出）
- [ ] 对应的 Capability Review（REUSE/EXTEND/DOMAIN SPECIFIC/MISSING）
- [ ] 本文（边界、必答问题、禁止重定义语义）

你下一步（下游，不在本文内）是：**Product Translation（Lifecycle 步骤 5）→ Workspace Composition / Semantic Model / Instance Design（步骤 7–8）→ 经 DESIGN GATE → Package Composition**。

> **本文到此停止。不进入 UX 设计。**

---

## 14. 状态

```text
WORKSPACE ENGINEERING PRODUCT HANDOFF READY FOR PRODUCT TRANSLATION
```

- 本文是 6 份方法论文档、M1/M2/M3 与当前 Technical Direction 的**正式产品交接**，将方法交给 Product / UX Designer。
- 状态 `Review`；不修改方法论、不设计 UI、不提出新架构。
- 后续由产品专家进入 Product Translation 阶段，受 PRODUCT TRANSLATION GATE 与 DESIGN GATE 约束。
- Dynamic Workspace Package Runtime 仍为 `NOT IMPLEMENTED`；本文交接不授权 P0 实现，仅明确 P0 前设计落点边界。

---

*Curis Workspace Engineering Product Handoff · READY FOR PRODUCT TRANSLATION（非 Frozen · 非 UI · 非 Runtime · 非新架构）*
