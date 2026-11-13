# Curis · Workspace Engineering Gates & Acceptance（空间工程门禁与验收）

**Status**: `Review`
**Methodology State**: `WORKSPACE ENGINEERING METHODOLOGY APPROVED CANDIDATE`
**类型**: 方法论 · Gate 与验收定义
**日期**: 2026-08-16
**上位**: `Curis_Workspace_Engineering_Methodology.md` · `Curis_Workspace_Engineering_Lifecycle.md`
**配套**: Handoff 协议（Doc 4）· Case Study（Doc 5）· RD Gap（Doc 6）

---

## 0. 阅读指引

本文件定义 Workspace Engineering 的 **6 道 Gate** 与 **7+1 项核心 Acceptance 检查**（第 8 项 Operating Team Presence），并附 **§2.1 长期办公室 6 项检查**（仅在长期 Business → Operating Team 场景适用）。

- **Gate = 阶段闸门**：每个 Relevant Gate 都必须有当前证据或可复用的有效证据；不要求每次机械重跑完整 Lifecycle。
- **Acceptance = 完成判据**：Workspace 交付时必须逐项出示真实证据，否则不得宣称完成（对齐 ADR-0041 业务运行完成标准）。

**铁律**：Relevant Gate 不可跳；Acceptance 不可 Mock 替代；Template 的旧证据只有在版本、假设和适用范围仍匹配时才能复用。

---

## 1. 六道 Gate

### Gate 1 · BUSINESS UNDERSTANDING GATE（业务理解闸门）

| 项 | 内容 |
|---|---|
| **位置** | Lifecycle 步骤 1–3 之后，步骤 4 之前 |
| **问题** | 有没有真实行业经营模型？ |
| **进入条件** | Business Intent Brief + 领域专家研究 + Operating Model 草案 |
| **通过标准** | ① 已识别并调用真实 Domain Expert（非产品设计师代劳）；② 研究基于真实世界经营实践（非竞品 UI 模式研究冒充）；③ Operating Model 能回答「这门业务如何长期运行并变得更好」；④ 证据按 VERIFIED/CONDITIONAL/UNKNOWN/UNAVAILABLE 分类 |
| **签署** | Domain Expert + Methodology Expert |
| **不过后果** | **没有真实行业经营模型，不得直接画 Workspace** |
| **典型失败** | 跳过领域研究、用竞品 UI 研究替代经营研究、把功能列表当 Operating Model（见 Doc 6 RD 案例） |

---

### Gate 2 · PRODUCT TRANSLATION GATE（产品翻译闸门）

| 项 | 内容 |
|---|---|
| **位置** | 步骤 4–5 之后，步骤 6 之前 |
| **问题** | 专业语言是否已完成 → 用户语言？ |
| **进入条件** | Product Handoff（收敛单份）+ 产品翻译总纲 + 术语映射 |
| **通过标准** | ① 内部概念已映射为用户面自然语言问题；② 内部原语（Office/Routing/Queue/Token 等）已隐藏；③ 复杂度默认隐藏；④ 用户只需理解经营层概念，后台自管机制；⑤ 不把八步飞轮/五层配置树等内部架构机械画给用户 |
| **签署** | Product Expert + Methodology Expert |
| **不过后果** | **没有完成专业语言→用户语言，不得进入正式 UI** |
| **典型失败** | 把经营架构流程图直接呈现给用户；把员工工作方式做成工程配置后台；暴露内部术语 |

---

### Gate 3 · AUTHORITY / CAPABILITY GATE（权威/能力闸门）

| 项 | 内容 |
|---|---|
| **位置** | 步骤 7–8 之后，步骤 9 之前 |
| **问题** | 是否检查过 Company OS 已有 Shared 能力？ |
| **进入条件** | Capability Review（REUSE/EXTEND/DOMAIN SPECIFIC/MISSING 四象限） |
| **通过标准** | ① 对 Employee / Responsibility Routing / Context Isolation / Handoff / Decision / Result Reference / Computer Access 逐项判定；② 已明确业务对象、关系、状态、责任与关键业务真相；③ REUSE/EXTEND 项已确认复用点；④ MISSING 项先进入 Core Expressibility Check，仅在 Core / Capability Gap 成立时建立 bounded Issue；⑤ 不新建与 Frozen Shell/P1–P7 冲突的 Primitive |
| **签署** | Capability/Connector Engineer + Methodology Expert |
| **不过后果** | **没有检查 Shared 能力，不得新造 Domain Runtime** |
| **典型失败** | 每 Workspace 重造一套责任/交接/验收/失败恢复；新建与 Shared Authority 冲突的对象 |

**Authority 边界**：Package Domain Schema 可以承载单一 Workspace / Template 的局部语义。只有该语义跨多个 Instance 复用、成为官方 Domain 标准、影响 Company OS 或需要长期兼容保证时，才进入 Domain Authority / Frozen 流程。

---

### Gate 4 · DESIGN GATE（设计闸门）

| 项 | 内容 |
|---|---|
| **位置** | 步骤 9–11 的设计 / Package / Expressibility 收口 |
| **问题** | Semantic Model、Workspace Design、Package Candidate 与交付分支是否稳定？ |
| **进入条件** | Semantic Model + Workspace Design + Package Candidate；当前过渡路径另需 Gap Audit |
| **通过标准** | ① 直接引用 Frozen Shell Contract / Shared Patterns，不重定义；② 状态模型与 Frozen §3 对齐；③ 视觉只引用 Frozen 令牌；④ 四概念责任语义严格区分；⑤ Package 只引用允许的 Surface / Action / Capability；⑥ Core Expressibility 结论明确；⑦ 只有 Gap 路径的 Issue 才需要 bounded（范围/允许文件/验证证据） |
| **签署** | Product Expert/Designer + Methodology Expert |
| **不过后果** | **Semantic Model / Workspace Design / Package / Gap 判定未稳定，不得安装或实现** |
| **典型失败** | 设计稿直接进代码；Package 无局部语义；Core 能表达仍修改源码；Issue 范围不清；自建视觉令牌 |

---

### Gate 5 · IMPLEMENTATION ACCEPTANCE GATE（实现验收闸门）

| 项 | 内容 |
|---|---|
| **位置** | 步骤 11–12 之后，步骤 13 之前 |
| **问题** | 有没有真实证据？ |
| **进入条件** | 实现产物 + Acceptance Report（核心 8 项 + §2.1 长期办公室 6 项，见 §2） |
| **通过标准** | 核心 8 项 + §2.1 长期办公室检查全部以**真实证据**通过（非 Mock / 非设计稿 / 非接口数量） |
| **签署** | Quality（独立验收）+ Methodology Expert |
| **不过后果** | **没有真实证据，不得宣称 Workspace 完成** |
| **典型失败** | 用静态原型/空库/fixture 充当发布或 UI 完成；旧链/真实平台/Desktop 未进入却宣称完成 |

---

### Gate 6 · OPERATING LEARNING GATE（运营学习闸门）

| 项 | 内容 |
|---|---|
| **位置** | 步骤 14 之后，步骤 15 之前（持续触发） |
| **问题** | 上线后，经营方法本身是否需要进化？ |
| **进入条件** | 运营期真实信号：业务数据 / 用户反馈 / Employee 经验 / 异常 |
| **通过标准** | ① 不只看 Analytics 表面指标；② 已判断「经营方法（Operating Model / Rules / Employee Method）是否需要调整」；③ 给出进化建议或「当前无需进化」的明确结论；④ 重大结构性变化已回流 Domain Expert / Product Review |
| **签署** | Domain Expert + Product Expert + CEO（结构性变更） |
| **不过后果** | **上线后不能只看 Analytics，必须判断经营方法是否需要进化** |
| **典型失败** | 把「有数据在看板」当作「在运营学习」；从不触发 Workspace Evolution |

---

## 2. 七项 Acceptance 检查（对齐 ADR-0041）

Workspace 交付时，Acceptance Report 必须逐项出示真实证据：

| # | 检查项 | 定义 | 如何验证（真实证据） |
|---|---|---|---|
| 1 | **Business Truth** | 业务对象、关系、状态、责任与关键业务真相真实成立 | 领域对象在真实运行中被正确创建/关联/演化；Package Domain Schema 或已适用的 Domain Authority 通过场景验证 |
| 2 | **Runtime Truth** | Workspace 真实运行（非 Mock/静态） | Target 路径还必须证明已安装 Curis 在不改源码、不重新 Build 的情况下注册并运行未知 Package；Current 路径必须明确标注为内置源码交付 |
| 3 | **Persistence** | 状态/对象持久化、重启一致、跨租户隔离 | 临时/活动库重启恢复同一记录；Tenant/CEO fail-closed；迁移一致 |
| 4 | **Failure Truth** | 失败被真实识别、可恢复、不伪造 PASS | 失败原子暂停、降级员工、保留未验证证据；重试可恢复；无伪造成功 |
| 5 | **UX Fidelity** | 体验与 Frozen Instance Spec / Shell Contract 一致 | 真实 Browser 视觉验收对齐 Instance Spec；内部术语隐藏、复杂度隐藏达标 |
| 6 | **Desktop** | 本地 Desktop 运行链可用（Local Desktop 优先） | 隔离 HOME 真实窗口完成「空公司→…→Workspace→运行对象」；端口/sidecar 清理 |
| 7 | **No Regression** | 不破坏既有 Company OS / 其他 Workspace | 既有 Runtime 联合回归未扩大失败数；其他 Workspace 实例未因本次修改改变结论 |
| 8 | **Operating Team Presence（业务团队承载）** | 任何长期业务办公室必须有真实 Operating Team（Leader + 成员 + 明确职责）承载（对齐 Company OS Shared Authority §9 · Frozen） | 团队在真实 Company OS 中成立：Leader 已指定、成员已组队、职责已声明；Business Home / 组织中心可见真实团队；无真实团队承载的长期办公室不得 Go Live |

> 任一未以真实证据通过（含第 8 项 Operating Team Presence）→ IMPLEMENTATION ACCEPTANCE GATE 不过 → 不得 Go Live。

---

### 2.1 长期办公室检查（Long-term Office Acceptance）

> **适用范围**：仅当业务为**长期 Business Workspace**（Company OS Shared Authority §9 · Frozen：Operating Team + Business Workspace）时叠加于上述 8 项核心 Acceptance。临时 Conversation / Task、单 Employee 工作、临时 Task Team 不适用。
> **纪律（来自 IA Review §5–§7 / Frozen）**：Shared 只要求这些**长期信息能力必须存在**；具体页面、名称、资产类型、History 呈现方式由 Domain 决定。不新增 Runtime Primitive；不修改 Frozen Shell；不修改高保真；不 Frozen 存储周期（具体 Retention 期限由 Retention Policy 与 Local vs Commercial deployment 决定）。
> **来源**：`docs/03_Design/WORKBUDDY_PROJECT_TO_CURIS_WORKSPACE_LONG_TERM_IA_REVIEW.md`（仅引用其 IA 结论，不重做研究）。

| # | 检查项 | 定义 | 如何验证（真实证据） |
|---|---|---|---|
| LO-1 | Business-significant 历史工作可追溯 | 对未来经营仍有价值的 **Business-significant** historical work（Work / Conversation / Task）可检索、可继续、可回溯到来源；普通 Activity / 操作动态不要求永久保留 | Search / History 表面能列出该办公室的 Business-significant 历史工作并打开原始会话 / 任务 |
| LO-2 | 当前 Operating Setup 可查看 | 当前 Operating Team / Strategy / Rules / Capability / Connector / Automation 配置可查看，且不与临时会话混淆 | Office Profile / 配置表面（Nav 入口或 Main 独立 Domain 表面）展示当前运行配置 |
| LO-3 | 重要业务资产可沉淀 | Result / Artifact 与长期 Business Asset 区分，资产可按 Domain 晋升 / 保留规则沉淀 | Asset Library 存在且 Domain 定义了资产晋升 / 保留规则；关键成果可从 Conversation 轻量引用进入资产库（P6） |
| LO-4 | 重要团队 / 经营方法 / 配置变化可追溯 | **重要** Operating Team 变更、Employee Method 演进、Operating Strategy / Rules / 配置变更有历史轨迹；普通 routine 操作变化不要求永久保留 | Change Log 记录成员、方法、配置的重要变更事件，可回溯 |
| LO-5 | Shared 与 Domain 信息归属正确 | 长期信息按 Nav / Context / Main / Utility / Search·History 正确归属；Shared 复用 Frozen 四栏与 Employee 三概念 | 四栏信息归属符合 Frozen Shell；Employee Workstation 复用 Conversation-first Shared Pattern；Employee Detail 复用 Utility Shared Pattern |
| LO-6 | 四栏职责符合 Frozen Shell | Nav / Context / Main / Utility / Search·History 职责不越界；Context Isolation 保持 | Context 仅承载当前工作上下文，长期历史 / Knowledge 不自动全量注入员工 Session；Utility 不承载 Conversation；无固定右栏 |
> **Activity / History / Audit 三者不同**：Activity = 近期动态，可过期；History = 对未来经营仍有价值的历史，按 Business Significance 保留；Audit = 因责任 / 安全 / 外部影响 / 验收要求必须保留的证据（不受普通 Retention 清理影响）。本 §2.1 仅要求「Business-significant Historical work 可追溯」与「重要变化可追溯」，普通 Activity / 操作变化不要求永久保存；具体 Retention 期限不在此定义、不 Frozen。

> 任一 LO-1–LO-6 在长期办公室场景下未以真实证据通过 → IMPLEMENTATION ACCEPTANCE GATE 不过 → 不得 Go Live（与核心 8 项同序）。

---

## 3. Gate 决策记录模板

每次 Gate 评审产出一条记录，便于审计：

```markdown
## Gate: <Gate 名> · <日期>
- 关联 Lifecycle 步骤: <步骤 N>
- 进入证据: <清单>
- 通过标准逐项: ✅/❌（附证据链接）
- 结论: PASS / PASS_WITH_BLOCKERS / BLOCKED
- 阻塞项: <清单，含 owner 与时限>
- 签署: <角色: 姓名/AI 标识>
```

### 3.1 不同 Lifecycle 路径的 Gate 证据

| 场景 | Gate 处理 |
|---|---|
| 新业务首次创建 | 默认完整执行 Gate 1–5；上线后进入 Gate 6 |
| 已验证 Template 实例化 | Gate 1–2 复用匹配 Template 版本的有效证据；必须新增 Template Match / Goal 适配证据；Gate 3 逐 Company 重跑；Gate 4 在未改变语义 / Surface 时复用设计证据；Gate 5 对新 Instance 必须重跑 |
| 已有 Workspace 进化 | 从受影响的最早 Gate 重新进入，并重跑所有受影响的下游 Gate；未受影响证据可保留 |

复用证据不等于跳过 Gate；它必须记录来源版本、适用假设与未受影响理由。

---

## 4. 与现有 Curis 验收的关系

| 现有机制 | 本文件如何对齐 |
|---|---|
| ADR-0041 业务运行完成标准（Frozen） | 本 §2 七项 = ADR-0041 在「空间工程交付」上的具体化 |
| CURRENT_STATE 的 Review Decision 模式（PASS / PASS_WITH_BASELINE_BLOCKERS） | Gate 结论沿用该语义；BLOCKED 不得进入下一阶段 |
| Blueprint 变更顺序 | Gate 与 Lifecycle 步骤同序，不倒置 |

---

## 5. 状态

```text
WORKSPACE ENGINEERING GATES & ACCEPTANCE APPROVED CANDIDATE
```

- 引用的 **Company OS Shared Authority §9（Business = Team + Office）已于 2026-08-16 经 Review 批准 Frozen**；本文件第 8 项 Operating Team Presence 验收直接对齐该 Frozen 规则。本文件集不重定义 Authority。
- 2026-08-16 Delta：新增 **§2.1 长期办公室 6 项检查**（LO-1–LO-6），对应 Lifecycle 新增步骤 6 Curis Workspace IA Composition / Curis Host Adaptation（基于 IA Review 的 IA 结论，不重做研究）。仍 APPROVED CANDIDATE / Review。
- 2026-08-16 Retention Delta：§2.1 LO-1 / LO-4 改为按 Business Significance 追溯（普通操作变化不要求永久保留）；新增 Activity / History / Audit 三者区分说明；对应 Lifecycle 步骤 6 Retention 边界。仍 APPROVED CANDIDATE / Review。

*Curis Workspace Engineering Gates & Acceptance · APPROVED CANDIDATE / Review（非 Frozen）*
