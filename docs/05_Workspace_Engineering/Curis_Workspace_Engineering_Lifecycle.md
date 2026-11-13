# Curis · Workspace Engineering Lifecycle（空间工程生命周期）

**Status**: `Review`
**Methodology State**: `WORKSPACE ENGINEERING METHODOLOGY APPROVED CANDIDATE`
**类型**: 方法论 · 生命周期定义
**日期**: 2026-08-22
**上位**: `Curis_Workspace_Engineering_Methodology.md`
**配套**: Gates（Doc 3）· Handoff 协议（Doc 4）· Case Study（Doc 5）· RD Gap（Doc 6）

---

## 0. 阅读指引

本文件定义 Workspace Engineering 的 **15 步完整参考生命周期**（含步骤 6 Curis Workspace IA Composition）。它是新业务首次创建的默认路径，不是每次实例化或进化都机械重跑的清单。

**硬约束**：
- 进入某条路径后，适用 Gate 的前置关系不可倒置；这不是用户点击顺序或行业固定 Workflow。每个 **Relevant Gate** 必须有当前证据或可复用的有效证据（Gate 见 Doc 3）。
- 不同业务**不要求**都使用 Content Growth 模型；完整新业务路径的每一步都必须回答：「这门业务如何长期运行并变得更好？」
- 本文件不定义具体业务的 Operating Model，只定义「任何业务空间都应走的链路」。
- 受控声明式 Package P0 / P0.5 与 Multi-Surface Workspace Package v2 foundation 已完成既有验收；Canonical Child Work foundation 与 sequential cross-professional multi-Work proof 已由既有 commits 接受。Parallel multi-Work、Surface/UI projection、Package ↔ Runtime Work mapping 与完整 Studio productization 仍未完成。本文件不得把目标模型写成已交付事实。

---

## 1. 闭环总览

### 1.0A Activation / Publication / Migration（CEO Accepted 2026-09-15）

Authority Class: CURRENT / FROZEN PRODUCT SEMANTICS（仅本小节）；其余方法论仍Candidate。消费[Company OS Shared §19](../03_Design/Curis_Company_OS_Shared_Authority.md)，不修改Package Technical Architecture。

- Publication须稳定Package identity、不可变version、scope、maintainer/source、真实验证、诚实支持范围、migration/support policy及正式发布决定。Official≠Verified；Company缺Model/Account不影响包资格。维护者提供定义/验证，发布责任人批准范围，不由用户公司的工程员工发布全局Catalog。
- Application复用Package First：应用专业定义到Company Context / Workspace，不新增实例系统；不携employee_id、凭证或Company数据，组织/Assignment由同一Company Truth解析并确认。
- Version记录各Workspace实际版本/配置与Work依据，不执行latest、不单字段覆盖Business；旧定义继续解释旧Work/Result/Evidence。支持窗口内允许混版；共享Core升级验证全部受影响读写合同。
- Migration Plan说明源/目标版本、Scope/对象/字段/方法/责任/能力/Surface、自定义差异、显式mapping、在途Work/Approval/未知效果、停写范围/生效点、权限费用增量、恢复点/回退限制、负责人、确认快照与Resume判据。它是现有工程Proposal，不新增Migration Job/Registry。
- Preflight重验版本/数据/确认/引用/空间/支持与恢复点；变化则重计划。无法证明在线兼容就停相关写入，不以关闭UI代替控制写入。
- Apply仅必要时迁数据，保ID、Scope、自定义与历史；Unknown不补假值，deprecated保旧字段解释。验证后协调有效版本和读写切换，重试查同计划结果，不重复转换，不执行外部经营动作补数据。
- 在途Work固定输入/方法/能力/Permission/Approval；安全则旧版完成，否则等待/受控交接/重计划；EFFECT_UNKNOWN先核验。新Provider/权限/费用/重大责任另确认。
- 失败：切换前保原有效数据，切换后保新增事实；条件满足才回退，否则受控修复。恢复A不得覆盖B新数据。纯可逆UI更新无需全公司备份；数据恢复沿Shared§17排除Secrets/Cookie/Keychain/Browser Profile。
- 优先identity-preserving upgrade；不能安全原地则同Business sibling Workspace＋controlled Handoff，保旧环境/历史，不再Activation。Generic转Professional同理。
- 自动更新须既有政策、兼容/无新增权限费用/无重大方法责任变化/无损/历史可读/Recovery成立，不凭版本号。可在支持窗口延后；安全撤销停相关动作、给迁移/人工路线，下架不删Business。
- 实施Gate：旧数据/引用、自定义、混版、在途效果、中断重试、升级后新增数据回退、跨Business恢复隔离、权限负向和Resume真实验证。新primitive先Architecture Gate；现有Package foundation≠Catalog/通用Migration交付。

### 1.0 Three-Layer / Unknown Business contract（CEO Accepted 2026-08-20）

本生命周期属于 Employee Operating Layer 的方法与 Gate，不是用户必须逐步点击的死 Workflow，也不是新的 Runtime。对陌生业务，Lifecycle 先执行能力发现和研究，再选择 `USE EXISTING / COMPOSE EXISTING / RESEARCH / ADAPT / BUILD / ACQUIRE / ESCALATE / REFUSE`；已有可信 Package 可复用适用证据，缺少关键能力则停止在缺口并返回原 Stage。Package 的产品语义为 Domain Operating Capability Package，当前不新增 Playbook 对象。

专业环境的解析顺序固定为：`Business Intent → Current Company Truth → Domain / Scope / Risk Recognition → Verified Match → Instance Configuration → Maintained Derived → Safe Composition → Domain Truth Sufficiency Check → bounded Domain / Risk Research（必要时）→ Generic / Derived / Composed / Professional Candidate → Package Candidate → Relevant Validation → CEO Gate（必要时）→ Instance`。这是 resolution / design / acceptance 顺序，不是新的 Runtime Workflow；Research 按 Gap 插入，Generation 仅在没有更好路径时发生。

```text
┌──────────────────────────────────────────────────────────────────────────┐
│  BUSINESS INTENT → DOMAIN EXPERT RESEARCH → OPERATING MODEL →             │
│  PRODUCT HANDOFF → PRODUCT TRANSLATION → CURIS WORKSPACE IA COMPOSITION →  │
│  SHARED/DOMAIN CAPABILITY REVIEW →                                         │
│  WORKSPACE COMPOSITION → SEMANTIC MODEL + WORKSPACE DESIGN →               │
│  PACKAGE COMPOSITION → CORE EXPRESSIBILITY CHECK → VALIDATE/INSTALL/RUN →  │
│  ACCEPTANCE → ACTIVATION → OPERATING LEARNING →                            │
│  WORKSPACE EVOLUTION ↺（回到 OPERATING MODEL / PRODUCT TRANSLATION）       │
└──────────────────────────────────────────────────────────────────────────┘
```

### 1.1 三种进入方式

| 场景 | 必须执行的最短正确路径 | 证据复用规则 |
|---|---|---|
| **A. 新业务空间首次创建** | 先匹配 Verified / 配置 / 派生 / 组合；仅在 Truth / Domain / Risk Gap 存在时进入相关研究与后续步骤 | 不预设必须从零研究或生成 Professional Workspace |
| **B. 已验证 Template 实例化** | Business Intent → Template Match → Goal 适配 → Capability Check → Instance 生成 → Acceptance / Activation | Template 对应的 Domain Research / Handoff / Translation / Design Gate 证据可按版本复用；不重新做完整研究 |
| **C. 已有 Workspace 进化** | 从受影响的最早阶段重新进入 → 重过相关 Gate → Candidate Version → Acceptance / Activation | 未受影响且仍兼容的上游证据可复用；受影响后的 Gate 不得跳过 |

“Gate 不可跳”表示每个适用 Gate 都必须有有效证据，不表示每次都重新执行全部 15 步。

### 1.2 当前路径与目标路径

```text
CURRENT DELIVERY PATH
Instance Design → Gap Audit → bounded Issue → 修改 Curis 源码 → Rebuild → Acceptance

TARGET WORKSPACE STUDIO PRODUCT PATH（未完成）
Workspace Design → Package Composition → Core Expressibility Check
  ├─ EXPRESSIBLE → Validate → Install → Run
  └─ NOT EXPRESSIBLE → Core / Capability Gap → bounded Issue
                        → 扩展 Core → 回到 Package Composition
```

---

## 2. 15 步详解

### 步骤 1 · BUSINESS INTENT（经营意图）

| 项 | 内容 |
|---|---|
| **目的** | 明确 CEO 想经营什么、目标是什么、成功意味着什么 |
| **输入** | CEO 的自然语言经营目标；公司现状；可选的行业初步信号 |
| **活动** | 捕获经营意图；区分「业务目标」与「功能诉求」；定义成功判据（success = 经营结果，不是功能清单） |
| **负责** | CEO（定意图）+ Workspace Engineering Methodology Expert（结构化意图） |
| **输出** | 《Business Intent Brief》：经营目标 / 主次成功指标 / 范围边界 / Non-goals |
| **Gate** | → 进入 **BUSINESS UNDERSTANDING GATE**（Doc 3）前的基础 |

> ⚠️ 禁止把「CEO 说想加个 X 功能」直接当成业务意图。意图是经营结果，不是界面诉求。

---

### 步骤 2 · DOMAIN EXPERT RESEARCH（领域专家研究）

| 项 | 内容 |
|---|---|
| **目的** | 先找真正的行业专家 / Expert / Skill，研究：现实世界里这项业务到底怎么经营 |
| **输入** | Business Intent Brief；领域专家（真实权威，如 Social Media Growth Expert、R&D Org Expert） |
| **活动** | 调研真实世界经营实践：目标设定、策略归属、执行节奏、职责划分、反馈回路、学习方法、进化机制；区分 `VERIFIED / CONDITIONAL / UNKNOWN / UNAVAILABLE` 四类证据 |
| **负责** | **Domain Expert**（独立研究，不被产品设计师代劳） |
| **输出** | 多份领域研究（Research）+ Review 纪要（保持 `RESEARCH / EXPERT RECOMMENDATION`，不 Frozen） |
| **Gate** | 必须过 **BUSINESS UNDERSTANDING GATE**：没有真实行业经营模型，不得直接画 Workspace |

> ⚠️ **这是最常被跳过的一步**（见 Doc 6 的 RD 缺口）。禁止产品设计师凭想象定义业务流程；也禁止把「竞品 UI 交互模式研究」当作「行业经营方法研究」。

---

### 步骤 3 · OPERATING MODEL（经营模型）

| 项 | 内容 |
|---|---|
| **目的** | 提炼：经营目标 / 经营策略 / Operating Rules / 职责 / Employee Method / 反馈 / 学习 / 策略进化 |
| **输入** | 领域研究；Business Intent |
| **活动** | 把真实世界研究收敛为可执行的经营模型；定义「这门业务如何长期运行并变得更好」；不同业务可用不同模型（不强制 Content Growth 八步飞轮） |
| **负责** | Domain Expert（主笔）+ Methodology Expert（结构校准） |
| **输出** | 《Operating Model》：目标 / 策略 / 规则 / 职责 / 方法 / 反馈 / 学习 / 进化 八维（或等效） |
| **Gate** | 仍属 BUSINESS UNDERSTANDING GATE 范围；模型未稳定不得进入 Handoff |

> 判据：Operating Model 必须能回答「这门业务如何长期运行并变得更好？」——否则只是功能列表。

---

### 步骤 4 · PRODUCT HANDOFF（产品交接）

| 项 | 内容 |
|---|---|
| **目的** | 领域专家把专业研究**收敛成一份**下游产品专家可消费的 Handoff；不把几十份 Research 直接扔给设计专家 |
| **输入** | Operating Model + 全部领域研究 |
| **活动** | 收敛为单份 Handoff：核心经营模型 / 五层（或等效）策略归属 / 用户交互要求 / Business Home 必须看见什么 / Employee 必须展示什么 / 边界与 Non-goals / 证据分类；附参考索引 |
| **负责** | Domain Expert（作者）→ Product Expert（消费者），经 Handoff 协议中转（Doc 4） |
| **输出** | 《Product Handoff》（唯一入口文档，RESEARCH / EXPERT RECOMMENDATION） |
| **Gate** | 进入 **PRODUCT TRANSLATION GATE** 前的必需产物 |

---

### 步骤 5 · PRODUCT TRANSLATION（产品翻译）

| 项 | 内容 |
|---|---|
| **目的** | 产品专家把专业经营方法 → 普通用户理解的产品语言 |
| **输入** | Product Handoff |
| **活动** | 映射内部概念 → 用户面自然语言问题；隐藏内部原语（Office / Routing / Queue / Token 等）；复杂度默认隐藏；确定用户只看得到什么、后台自管什么 |
| **负责** | **Product Expert / Designer** |
| **输出** | 产品模型收敛 / UX 翻译总纲 / 术语映射（内部词 ↔ 用户词） |
| **Gate** | → **PRODUCT TRANSLATION GATE**：没有完成专业语言→用户语言，不得进入正式 UI |

> 原则：用户不学习行业架构；用户不学习 Curis 内部 Primitive；复杂度默认隐藏。

---

### 步骤 6 · CURIS WORKSPACE IA COMPOSITION / CURIS HOST ADAPTATION（Curis 空间信息架构组合 / 宿主适配）

| 项 | 内容 |
|---|---|
| **目的** | 在业务已被理解并翻译后、能力审查与视觉/实例设计前，组合这项业务进入 Curis 后的**长期信息架构（Host Adaptation）**：明确它需要哪些长期信息、哪些直接复用 Company OS / Shell Shared Pattern、哪些是 Domain-specific，以及 Operating Team / Leader / Employee 如何进入办公室 |
| **输入** | Product Handoff + 产品翻译 + Operating Model；Company OS Shared Authority（§9 Frozen）+ Frozen Shell Contract / P1–P7 Shared Patterns；来源参考 `docs/03_Design/WORKBUDDY_PROJECT_TO_CURIS_WORKSPACE_LONG_TERM_IA_REVIEW.md`（仅引用其 IA 结论，不重做研究） |
| **活动** | 逐项分解「IA 组合十问」：① 这项业务进入 Curis 后需要哪些长期信息；② 哪些直接复用 Company OS / Shell Shared Pattern；③ 哪些属于 Domain-specific Workspace UI；④ Operating Team / Leader / Employee 如何进入办公室；⑤ 当前工作 / 历史 Work·Conversation·Task / Result·Artifact / 业务资产 / Operating Strategy·Rules / Employee Method / Knowledge / Capability·Connector / Automation·Schedule / Decision·Handoff·Failure·Recovery / 配置·方法变更史 分别如何访问；⑥ Nav / Context / Main / Utility / Search·History 的信息归属；⑦ Employee Workstation 必须复用 Frozen Conversation-first Shared Pattern；⑧ Employee Detail 必须复用 Frozen Utility Shared Pattern；⑨ Result·Artifact 与长期 Business Asset 必须区分，由 Domain 定义资产晋升 / 保留规则；⑩ Context Isolation 必须保持，长期历史 / Knowledge 不得自动全量注入员工 Session；**并逐项回答 Retention 六问（见本步骤 Retention 边界行）** |
| **Retention 边界（必须回答）** | 长期信息可追溯 ≠ 所有变化永久保存。逐项回答：① 哪些属于 **Current Truth**（当前真相，始终可查）；② 哪些属于 **Business-significant History**（对未来经营仍有价值，需长期保留）；③ 哪些普通 Work / Conversation / Activity 应摘要或归档（不要求永久全量保留）；④ 哪些 Raw Trace / 临时 Artifact / Tool log / routine config change 按 **Retention 到期清理**（不要求永久）；⑤ 哪些 Result / Artifact 值得晋升为长期 Business Asset（Domain 定晋升规则）；⑥ 压缩 / 清理后必须保留哪些 **Learning / Decision / Responsibility / Evidence** 事实。统一原则：**Current Truth First · History by Business Significance · Raw Trace by Retention**。Activity / History / Audit 三者不同：Activity = 近期动态，可过期；History = 对未来经营仍有价值的历史；Audit = 因责任 / 安全 / 外部影响 / 验收要求必须保留的证据（不受普通 Retention 清理影响）。具体期限数字（如天数阈值）不在此定义、不 Frozen；未来由 Retention Policy 与 Local vs Commercial deployment 决定 |
| **负责** | Product Expert + Methodology Expert（引用 Frozen Shell，不重定义四栏 / 不重定义 Shared Pattern） |
| **输出** | 《Workspace IA Composition》：长期信息类别清单 + Shared 复用 / Domain 专属判定 + 四栏信息归属草图 + 长期办公室访问与资产晋升规则 + **Retention 边界判定**（Current Truth / Business-significant History / 待摘要归档 / 待 Retention 清理 / 晋升为长期 Business Asset 的分类，及压缩后必须保留的 Learning·Decision·Responsibility·Evidence 事实）+ Context Isolation 保持声明 |
| **Gate** | 属 AUTHORITY / CAPABILITY GATE 上游输入；其「Shared 复用 / Context Isolation / 四栏归属」结论在 Gate 3 与 Gate 4 复核；本步骤不新设 Gate |

> 纪律（来自 IA Review §7 / Frozen）：Shared 只要求这些**长期信息能力必须存在**；具体页面、名称、资产类型、History 呈现方式由 Domain 决定。不新增 Runtime Primitive；不修改 Frozen Shell；不修改高保真；不 Frozen 存储周期（具体 Retention 期限由 Retention Policy 与 Local vs Commercial deployment 决定）。

---

### 步骤 7 · SHARED / DOMAIN CAPABILITY REVIEW（共享/领域能力审查）

| 项 | 内容 |
|---|---|
| **目的** | 搭新 Workspace 前检查 Company OS 已有能力能否复用 |
| **输入** | 产品翻译结果；IA Composition 结论；Company OS Shared Authority；现有 Capability/Connector 目录 |
| **活动** | 对每类所需能力判定 `REUSE / EXTEND / DOMAIN SPECIFIC / MISSING`：Employee / Responsibility Routing / Context Isolation / Handoff / Decision / Result Reference / Computer Access 等 |
| **负责** | Capability / Connector Engineer + Methodology Expert |
| **输出** | 《Capability Review》：复用清单 / 扩展点 / 领域专属 / 缺失项（缺失项进入 Issue） |
| **Gate** | → **AUTHORITY / CAPABILITY GATE**：没有检查 Shared 能力，不得新造 Domain Runtime |

> ⚠️ 禁止每个 Workspace 重新造一套责任/交接/验收/失败恢复。

---

### 步骤 8 · WORKSPACE COMPOSITION（空间组合）

| 项 | 内容 |
|---|---|
| **目的** | 决定真正需要哪些空间构件，由业务反推，不由页面清单反推 |
| **输入** | 产品翻译 + 能力审查 + IA Composition |
| **活动** | 判定需要：Business Home / Professional Workspace / Context / Main / Utility / Employee / Presence / Conversation / Evidence / Operating Surfaces；明确哪些复用 Shell Contract / Shared Pattern，哪些是 Instance 专属；**同时必须确定该业务的 Operating Team 组建方案（Leader 是谁、需要哪些成员角色与职责、如何组队，不复制员工身份），团队与办公室一并交付** |
| **负责** | Product Expert + Methodology Expert |
| **输出** | 《Workspace Composition》：构件清单 + 复用/专属判定 + IA 草图 + 《Operating Team 组建方案》（Leader / 成员角色 / 职责 / 组队方式） |
| **Gate** | 仍属 AUTHORITY / CAPABILITY GATE 范围 |

---

### 步骤 9 · SEMANTIC MODEL + WORKSPACE DESIGN（语义模型与空间设计）

| 项 | 内容 |
|---|---|
| **目的** | 在实例生成前明确业务语义，并形成 Workspace Design |
| **输入** | 空间组合；IA Composition；Frozen Shell Contract / Shared Patterns；设计系统 |
| **活动** | 明确业务对象、关系、状态、责任、关键业务真相；推导 Domain Navigation、多个 Professional Surface、每个 Surface 所需 Responsibility、对象 / Detail 映射与共享 Work / Result / Evidence 投影；设计 Main / Context / Utility、交接、Needs CEO、Result Reference 与失败恢复；引用 Frozen 不重定义；视觉基线只引用 Frozen 令牌 |
| **负责** | Product Expert / Designer（设计），Methodology Expert（Gate 校准） |
| **输出** | 《Semantic Model》+《Workspace Design》；局部语义进入 Package Domain Schema 草案 |
| **Gate** | → **DESIGN GATE**：语义与 Workspace Design 未稳定，不得进入 Package Composition |

**语义升级规则**：普通用户自定义 Workspace 默认只需 Package Domain Schema。仅当语义跨多个 Instance 复用、成为官方 Domain 标准、影响 Company OS 或需要长期兼容保证时，才进入 Domain Authority / Frozen 流程。

---

### 步骤 10 · PACKAGE COMPOSITION（Package 组合）

| 项 | 内容 |
|---|---|
| **目的** | 把 Workspace Design 组合为声明式 Workspace Package，而不是默认修改 Curis 源码 |
| **输入** | Semantic Model；Workspace Design；IA Composition；Capability Review；Package Contract |
| **活动** | 组合 Domain Navigation、Professional Surface 声明、Surface Responsibility requirements、Object View / Detail mapping、Work / Result / Evidence projection、optional / conditional availability、Capability requirements、最小 Manifest、Package Domain Schema、允许 Action、版本与来源；实例数据、凭据、Employee ID、Employee 授权不得写入 Package。本步只形成 Authority Candidate，不冻结最终 Schema |
| **负责** | Workspace Engineer + Product Expert + Capability Engineer |
| **输出** | Workspace Package Candidate + Validator 输入 |
| **Gate** | 仍属 DESIGN GATE 收口；Package Candidate 未形成不得做 Core Expressibility Check |

> 当前已有受控声明式 Package P0 / P0.5 与 Multi-Surface Workspace Package v2 foundation；本步骤描述的 Workspace Studio productization、任意 Professional Package 创建与完整迁移仍不能作为已交付产品。Package v2 foundation 的安装/验证/持久化/渲染证据不得被扩大解释为 Studio 完成。

---

### 步骤 11 · CORE EXPRESSIBILITY CHECK + DELIVERY（Core 可表达性检查与交付）

| 项 | 内容 |
|---|---|
| **目的** | 判定现有 Curis Core 是否能完整表达 Package，并走最短正确交付路径 |
| **输入** | Workspace Package Candidate；当前 Core / Capability / Renderer / Action Registry 事实 |
| **活动** | 逐项判定 `EXPRESSIBLE / CORE_GAP / CAPABILITY_GAP / UNSUPPORTED`。`EXPRESSIBLE` 时 Validate → Install → Materialize → Run；Gap 时建立 bounded Issue，扩展共享 Core 后**回到步骤 10**重新组合与验证 |
| **负责** | Workspace Engineer + Core Engineer + Methodology Expert |
| **输出** | 已安装 Candidate Instance，或明确的 Core / Capability Gap + bounded Issue |
| **Gate** | → **IMPLEMENTATION ACCEPTANCE GATE**：没有真实安装 / 运行证据，不得宣称 Workspace 完成 |

**当前过渡事实**：受控声明式 Package P0 / P0.5 不证明 Generic multi-Surface Workspace 已实现。未知业务若需要 Domain Navigation、多个 Surface、Surface Responsibility declaration 或通用 Projection，仍必须登记明确 Gap 并通过独立授权的 bounded Issue；本文件不授权源码修改。

---

### 步骤 12 · ACCEPTANCE（验收）

| 项 | 内容 |
|---|---|
| **目的** | 至少检查 7 项核心真相（+ 第 8 项 Operating Team Presence + §2.1 长期办公室检查，见 Gates Doc 3） |
| **输入** | Target 路径的已安装 Package / Instance，或 Current 路径的实现产物；验证计划 |
| **活动** | 验收：Business Truth / Runtime Truth / Persistence / Failure Truth / UX Fidelity / Desktop / No Regression（详见 Doc 3 §验收七项） |
| **负责** | Quality（独立验收）+ Methodology Expert |
| **输出** | 《Acceptance Report》：核心 8 项 + 长期办公室 6 项证据 + 结论 |
| **Gate** | 过 **IMPLEMENTATION ACCEPTANCE GATE** 方可 Go Live |

---

### 步骤 13 · ACTIVATION / GO LIVE（激活 / 正式启用）

| 项 | 内容 |
|---|---|
| **目的** | Workspace 正式注册 / 启用 |
| **输入** | 通过的 Acceptance Report |
| **活动** | Target 路径启用已注册 Package Instance；Current 路径启用已验收内置 Workspace；CEO 可见并投入运营；记录版本 / 来源 / 启用事实 |
| **负责** | Workspace Runtime + CEO（确认启用） |
| **输出** | 已启用 Workspace（运营态） |
| **Gate** | 无新增 Gate；进入运营期 |

> ⚠️ **团队承载前置（见 Methodology §4.1 / Shared Authority §9）**：Go Live 前必须确认该长期业务已有真实 Operating Team（Leader + 成员 + 明确职责）承载。没有真实团队承载的长期办公室不得 Go Live，也不得算空间工程完整成功（对应 Gates Doc 3 验收第 8 项）。

---

### 步骤 14 · OPERATING LEARNING（运营学习）

| 项 | 内容 |
|---|---|
| **目的** | 投入使用后，从真实经营中回流，判断经营方法是否需要进化 |
| **输入** | 业务数据 / 用户反馈 / Employee 经验 / 异常 |
| **活动** | 收集真实经营信号；判断「经营方法本身是否需要调整」；不只看 Analytics 表面指标 |
| **负责** | Domain Expert（重新介入）+ Product Expert + CEO |
| **输出** | 进化建议 / 待 Review 议题 |
| **Gate** | → **OPERATING LEARNING GATE**：上线后不能只看 Analytics，必须判断经营方法是否需要进化 |

---

### 步骤 15 · WORKSPACE EVOLUTION（空间进化）

| 项 | 内容 |
|---|---|
| **目的** | 判断并执行业务空间的进化，形成闭环 |
| **输入** | Operating Learning 结论 |
| **活动** | 调整 Operating Rules / Employee Method / Semantic Model / Workspace Design / Package / Capability / Employee；从受影响的最早阶段重新进入，而不是固定回到某一步 |
| **负责** | 全角色协同；CEO 在结构性变更处拍板 |
| **输出** | 进化的 Business Space / Operating Model / Instance |
| **Gate** | 受影响阶段及其下游 Relevant Gate 重新过审；闭环 ↺ |

```text
          ┌─────────────────────────────────────────────┐
          │  WORKSPACE EVOLUTION                         │
          │     ↓ （回到）                                │
          │  最早受影响阶段 / Relevant Gate              │
          └─────────────────────────────────────────────┘
```

---

## 3. 步骤 ↔ Gate 对照表

| 步骤 | 关联 Gate（见 Doc 3） | Gate 不过的后果 |
|---|---|---|
| 1–3 | BUSINESS UNDERSTANDING GATE | 没有真实行业经营模型，不得画 Workspace |
| 4–5 | PRODUCT TRANSLATION GATE | 没有专业→用户语言，不得进正式 UI |
| 6–9 | AUTHORITY / CAPABILITY GATE | 没有查 Shared 能力或明确局部语义边界，不得新造 Domain Runtime / 全局 Authority |
| 9–11 | DESIGN GATE | Semantic Model、Workspace Design、Package Candidate 或 Gap 判定未稳，不得交付 |
| 11–12 | IMPLEMENTATION ACCEPTANCE GATE | 没有真实证据，不得宣称完成 |
| 14 | OPERATING LEARNING GATE | 只看 Analytics，不得判定经营成功 |

---

## 4. 不同业务的弹性

本生命周期是**骨架**，不是模板。不同业务在步骤 3（Operating Model）与步骤 8（Composition）可大不相同：

- **Content Growth**：八步飞轮 + 五层策略归属 + Office/Intent/Account 三层（见 Doc 5）。
- **RD**：八阶段研发 Cycle + 责任工作站 + 交接/Needs CEO（见 Doc 6，但其步骤 2 有缺口）。
- **未来销售 / 客服 / 电商**：各自的真实经营模型，由各自 Domain Expert 定义。

完整新业务路径的统一要求是：每一步都必须回答「这门业务如何长期运行并变得更好？」；已验证 Template 实例化则证明本次目标仍落在 Template 的已验证假设内。

---

## 5. 状态

```text
WORKSPACE ENGINEERING LIFECYCLE APPROVED CANDIDATE
```

- 2026-08-16 Delta：新增步骤 6 Curis Workspace IA Composition / Curis Host Adaptation（Lifecycle 总数 14 → 15）；对应 Gates Doc 3 新增 §2.1 长期办公室 6 项检查。仍 APPROVED CANDIDATE / Review。
- 2026-08-16 Retention Delta：步骤 6 新增「Retention 边界（必须回答）」行——Retention 六问 + 统一原则（Current Truth First / History by Business Significance / Raw Trace by Retention）+ Activity·History·Audit 三者区分；§2.1 LO-1 / LO-4 改为按 Business Significance 追溯，普通操作变化不要求永久保留。仍 APPROVED CANDIDATE / Review。

*Curis Workspace Engineering Lifecycle · APPROVED CANDIDATE / Review（非 Frozen）*
