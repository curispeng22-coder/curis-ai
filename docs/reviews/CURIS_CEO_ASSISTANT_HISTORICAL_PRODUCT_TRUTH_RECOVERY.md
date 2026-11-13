# CURIS CEO ASSISTANT
## HISTORICAL PRODUCT TRUTH RECOVERY

> 2026-09-09 applicability correction — CEO Phase A ACCEPTED：本文关于“可拖动=Vision/非当前必做”的历史判断已被 [Core Product Authority Repair](CURIS_CORE_PRODUCT_AUTHORITY_REPAIR.md) §7 替代。当前Assistant必须global floating / draggable / collapsible / cross-seven-area，同canonical identity/durable conversation、不占Pane。原文保留历史证据；桌面宠物造型、精确尺寸、snap等并未因此被接受。

**Authority Class:** REVIEW  
**Status:** Review  
**Disposition:** READ-ONLY HISTORICAL AUTHORITY AUDIT / STOP FOR CEO REVIEW  
**Date:** 2026-08-21  
**Scope:** Product、Design、Context、Decision、Review 与历史实现审计文档；不修改 Current Product Truth、Runtime、Schema、DB、Frontend、Prototype 或高保真 UI。

> 本文恢复历史证据，不建立新的 CEO Assistant Contract，也不把历史 Draft、Deprecated Review 或实现证据升级为 Current Authority。Current Product Truth 仍由 Pointer → Product Blueprint → Master Map → UI Blueprint → applicable Frozen Authority 决定。

## A. Executive Summary

历史材料对 CEO Assistant 的核心判断高度一致：它不是一个页面按钮、普通聊天框或单纯浮层，而是 Company Runtime 中真实存在的、公司级、面向 CEO 的第一位 AI Employee / Chief of Staff。它负责把 CEO 的注意力、公司事实、专业员工和跨页面工作连续起来，但不替代 Team Leader、Domain Expert、专业员工或执行者。

可以安全恢复为历史核心的内容：

- **身份：** Company-level AI Employee；历史推导明确称为“第一位 AI 员工”和 Chief of Staff。
- **职责：** 理解意图、搜集与整理事实、协调和监督跨部门工作、准备简报/决定、跟进责任、发现异常并升级。
- **全局性：** Runtime 与入口跨页面保持同一身份；CEO Desk 是主要工作面之一，不是 Assistant 的存在本身。
- **边界：** 可在明确授权范围内做可逆、低风险动作；高影响、外部承诺、结构/预算/责任变化和不可逆动作回到 CEO Gate。
- **上下文：** 使用当前页面/对象的白名单化上下文，同时保持 Company/Workspace/Employee scope 与权限隔离；跨页面不等于混合所有业务上下文。
- **交互：** 对话、简报、通知、事项、Decision、Result、Exception、Handoff 和回到来源工作面的组合，不是独立聊天世界。

仍不能直接当作 Current Product Truth 的内容：

- 桌面宠物、可自由拖动的陪伴形态：历史 Draft / Vision，未找到当前 Frozen Visual Authority。
- FAB、右滑抽屉、CEO Desk 默认展开：有实现/设计证据，但具体像素与最终入口应服从当前 Frozen Shell/UI Blueprint。
- “创建业务/项目、配置负责人和能力”的旧 Assistant 主导路径：已被后续“Assistant 协调，专业责任交给 Leader/Domain Expert”的 Current 语义收窄。
- 快捷键作为 Assistant 专属入口：历史页面地图提到快捷键，但没有找到 Assistant 专属且已接受的稳定 Contract。

## B. Historical Timeline

| 时间 / 来源 | 状态与原始判断 | 本次分类 |
|---|---|---|
| 2026-07-29 前后，`Product Bible v1.0/17 AI秘书`、`03 信息架构`、`05 全局交互` | AI 秘书是全局智能交互入口；支持页面/对象/历史上下文、对话、提醒、确认和“桌面宠物式交互”。 | **HISTORICAL DRAFT / CANDIDATE**；保留设计意图，不覆盖 Current。 |
| 2026-07-30，`ADR-0033-global-assistant-runtime.md` | 从 CEO Office 固定秘书栏切换到根布局 Global Assistant Provider/Host；状态跨页面；复用既有 Task/权限；Desktop Floating Assistant 留作未来宿主。 | **FROZEN AT THE TIME / ARCHITECTURE HISTORY**；全局 Runtime 方向被后续 Current 继续消费，固定秘书栏被 Superseded。 |
| 2026-07-30，`issues/20260730_global_assistant_runtime_v1.md` | Identity 可由用户配置；CEO Office 默认完整 Panel，其他 Workspace 使用统一隐藏入口；不新建第二套 Task/Chat/Memory；禁止 Desktop 浮窗。 | **CLOSED — PASS IMPLEMENTATION EVIDENCE**；证明当时实现边界，不单独决定今日视觉。 |
| 2026-07-31，`Curis_Product_Derivation_Journal.md` §20–25、§35–37；`Curis_Product_Reasoning_Record.md` §16、§18 | Assistant 从“入口”升级为 Company Runtime 第一位 AI Employee / Chief of Staff；以 CEO Operating Day 验证；生命周期 Created → Configured → Learning Context → Operating → Evaluating → Upgraded/Reassigned。 | **REASONING / HISTORICAL PRODUCT DECISION**；其核心已进入后续 Current。 |
| 2026-08-03–04，历史 UI Review / Audit | 统一 Global Assistant FAB + Drawer；旧 `curis-companion`/本地抽屉退役；ESC、遮罩和页面切换等交互被验证。 | **REVIEW / IMPLEMENTATION EVIDENCE**；不等于新的 Product Authority。 |
| 2026-08-09，`ui-runtime-migration-review-2026-08-09/README.md` | Company OS Shell → CEO Desk/Business Map/Workspace Portal → Workspace Runtime → Global CEO Assistant；共享身份/升级入口。 | **REVIEW — PASS TO UI RUNTIME IMPLEMENTATION**；已被 Current Shell/Blueprint 消费。 |
| 2026-08-10，`20260810_product_rederivation_review.md` | Assistant 是第一位 AI Employee，是产品主入口和经营协调者，不是按钮或聊天浮层；CEO Desk 承载 CEO Operating Day。 | **REVIEW / PRODUCT RETHINKING INPUT**；核心方向进入 Current。 |
| 2026-08-14，`ADR-0045-ordinary-user-desktop-product-rebaseline.md` | Assistant、搜索、最近工作、通知、上下文返回是跨层能力，不新增一级导航；普通用户不先理解 Runtime。 | **FROZEN CURRENT AUTHORITY**（其“六区”旧导航文字已由后续七区同步修正）。 |
| 2026-08-18–20，`Curis_Company_OS_Shared_Authority.md` §9.3、Current Product Blueprint §10 | Assistant 是公司级跨组织协调员工；Leader/Employee 负责专业结果；Bootstrap 中 Assistant 只协调/搜集/组织提案/跟进/升级。 | **CURRENT / FROZEN SHARED AUTHORITY**。 |

## C. Identity Truth

### C.1 历史上已经形成的身份结论

| 问题 | 证据 | 恢复结论 | 状态 |
|---|---|---|---|
| 是否真实 Employee？ | `ADR-0040-company-os-workspace-product-reset.md` 的 Company Runtime actor model；Journal §20、§35；Reasoning Record §16、§18 | 是。它是 Company-level AI Employee，不是仅存在于 Desk 的 UI component。 | **HISTORICAL FROZEN / CURRENT SEMANTIC PRESERVED** |
| 是否公司创建后的第一位员工？ | ADR-0040 明确“CEO’s first AI Employee”；Journal/Reasoning Record 明确“第一位 AI 员工”。 | 是这一历史产品定位；但“Company 创建事务是否始终自动物化 Assistant”的具体实现规则需以当前 APP/Runtime Contract 为准，不由本报告补写。 | **CORE PRESERVED; EXACT CREATION RULE REVIEW REQUIRED** |
| Employee Name 与 Role 是否分离？ | `issues/20260730_global_assistant_runtime_v1.md` 的 Identity 字段 `name/avatar/role/tone/personality`；Journal §36 的稳定身份/责任契约。 | 分离。Name 是可配置的展示/身份字段；Role/责任契约是公司语义与授权边界，不因改名改变。 | **HISTORICAL EVIDENCE; CURRENT EDIT CONTRACT PARTLY UNSET** |
| 是否允许命名/重命名？ | Global Assistant Runtime Issue 明确 Identity 由用户配置且不固定名称；Product Context 的 Brand Configuration 也把 Assistant display name 与品牌展示分开。 | 历史上允许用户配置名称；重命名是否保留历史版本、是否影响问候/报告署名、是否有限制，未找到单独 Frozen Contract。 | **SUPPORTED HISTORY; CEO REVIEW REQUIRED FOR FULL LIFECYCLE** |
| 是否等同本地 CEO Profile？ | 后续 APP-005 语义（Local CEO Profile）与 Assistant Setup 分开；当前 Blueprint 也分别表达 CEO 与 Assistant。 | 不等同。CEO 是人类身份；Assistant 是公司员工身份。二者不得合并成一个默认用户实体。 | **CURRENT BOUNDARY** |

### C.2 身份生命周期

历史推导定义：`Created → Configured → Learning Context → Operating → Evaluating → Upgraded / Reassigned`。其中 Learning Context 是可查看、可接受/拒绝、可回滚的 Company Context 版本，不是不可控的模型训练。该生命周期是历史产品语义与设计约束，不代表当前 Runtime 已完整实现。

## D. Organizational Responsibility

历史与当前共享权威共同形成以下责任关系：

```text
CEO
↓ 最终治理、Goal / Boundary / 高影响 Decision
CEO Assistant
↓ 公司级协调、注意力排序、汇报、跟进、升级
Professional / Department / Business Leaders
↓ 专业判断、团队组织、业务结果
Employees / Workspace Employees
↓ 具体责任、Work、Result / Evidence
```

Assistant 可以：

- 理解 CEO 意图，收集和整理信息；
- 汇报公司变化、风险、结果和待决定事项；
- 协调部门/业务/Workspace，跟踪 Handoff、承诺、检查点和未完成责任；
- 发现权限、能力、失败、延迟、冲突和高影响异常，并把 Owner、原因、恢复入口带回 CEO；
- 在授权范围内执行可逆、低风险、无外部不可逆副作用的整理、查询、摘要、草拟和检查点动作。

Assistant 不可以：

- 代替 Team Leader 持有某一业务的长期专业责任；
- 代替 Domain Expert 研究行业、制定专业经营方法或拥有专业结果；
- 代替工程团队完成研发、设计、实施、质量验收；
- 把所有 CEO 请求变成自己的 Task/Workflow，或成为每个员工工作的强制中转；
- 绕过 Company/Business/Workspace scope、权限、Evidence 或现有 Runtime 直接改写业务事实。

以上边界与 `docs/03_Design/Curis_Company_OS_Shared_Authority.md` §9.3 的 Frozen 规则一致：Assistant 与 Leader 不是二选一入口，CEO 可直接进入具体 Employee 的真实工作上下文。

## E. Global Placement Truth

### E.1 已有证据支持的内容

1. `ADR-0033-global-assistant-runtime.md`（Frozen at 2026-07-30）明确废弃 CEO Office 固定秘书栏，采用根布局级 Global Assistant Provider / Host，跨页面保持状态。
2. `issues/20260730_global_assistant_runtime_v1.md` 将 CEO Office 定义为默认完整 Assistant Panel，其他 Workspace 页面为统一隐藏入口；实现不成为固定第三列。
3. `Curis_Product_Master_Map_v1.0.md` 历史地图与 `ui-runtime-migration-review-2026-08-09/README.md` 都把 Global Assistant 作为共享身份/升级入口，而非某个 Business/Workspace 的专属员工。
4. 当前 Product Blueprint、ADR-0045 与 Frozen Shell 继续把 Assistant 归为跨层 Global Capability；它不是七个一级导航之一，也不是 Global Topbar 的固定结构。

### E.2 结论

- **全局可达：** 有充分历史与当前证据支持。
- **跨页面连续：** Runtime/状态/入口连续；页面仍必须提供当前 scope 的结构化上下文。
- **不属于 CEO Desk 单页：** 支持；CEO Desk 是主工作面之一，不是 Assistant 的本体。
- **不属于某个 Business/Workspace：** 支持；Assistant 是 Company-level，业务/Workspace 员工是其协调对象。
- **最终视觉形式：** 未被当前 Product Authority 固定为桌面宠物、FAB、固定栏或右侧永久面板。具体视觉必须服从 Frozen Workspace Shell 与当前 UI Blueprint。

## F. Context / Scope Contract

### F.1 历史上下文模型

旧 Product Bible §6 把上下文分为页面上下文、当前对象上下文（项目/任务/员工/资料/成果）和历史上下文（对话/决策/执行记录）；用户进入研发项目说“继续”时，应理解为继续当前对象，而不是新开一套聊天世界。

`docs/architecture/curis-assistant-runtime-architecture-report.md` §2/§3 将该意图收紧为：页面只提交白名单化结构化上下文，Backend 重新校验实体和组织归属；根布局挂载单一 Provider/Host，维护 open/minimized、当前页面上下文、未读和未提交输入。

### F.2 页面切换时的处理

| 场景 | Assistant 应保持 | Assistant 应切换/限制 |
|---|---|---|
| CEO Desk | Company-level identity、Brief、Matters、Decision/Exception/Handoff 入口 | 当前 CEO Desk scope；不把全部 Workspace 细节塞入简报 |
| Department / Business | 同一 Assistant identity、未读/待处理连续性 | 读取当前 Department/Business 的白名单事实；可返回来源范围 |
| Workspace | 同一身份、原有会话草稿/入口状态（若当前实现支持） | 只消费当前 Business/Workspace/Employee context；不得跨 Workspace 猜写目标 |
| Organization / Talent / Library / Meeting | 同一 Global Capability | 按页面类型提供安全结构化 context；高风险动作仍回到现有页面/Decision Gate |

### F.3 隔离规则

Global 不等于 unrestricted。Tenant/Company/Business/Workspace/Employee 归属、权限、Context isolation、reference-first 读取和返回原上下文必须继续生效。Assistant 不能因“全局入口”读取或混合没有当前授权的业务数据，也不能把一个页面的对象 ID 当成可信事实。

## G. Interaction Contract

| 入口/动作 | 历史证据 | 分类 |
|---|---|---|
| CEO Desk 主面板 / Assistant Brief | Journal §21、Reasoning Record §16、Current CEO Desk Contract | **CURRENT / ACCEPTED SEMANTIC**；不是独立 Assistant 页面 |
| 全局隐藏入口 / 浮层 | ADR-0033；Global Assistant Runtime Issue；历史 UI Review | **CURRENT CAPABILITY + IMPLEMENTATION EVIDENCE**；最终形态服从 Frozen Shell |
| 对话 | Product Bible §1/§5–§8；当前 Blueprint Conversation contracts | **CURRENT**，但对话必须锚定真实 Work/Decision/Context |
| Brief / Notification / Matter | Journal §21、§23；CEO Desk Contract | **CURRENT SEMANTIC**；应以可行动事实、来源和下一步为主 |
| Result / Evidence / Decision / Handoff / Exception | Journal §21–24；Current Blueprint/Shared Authority | **CURRENT CROSS-SURFACE CONTRACT**；Assistant 负责解释、准备、回收和升级，不拥有第二套 Truth |
| 点击 FAB / 右滑 Drawer | 2026-07-29–08-04 UI implementation reviews | **HISTORICAL IMPLEMENTATION EVIDENCE / CANDIDATE PRESENTATION**，不是独立 Product Authority |
| 拖动桌面宠物、自由移动 | Product Bible v1.0-draft §4；`05 全局交互`；`24 Design System` | **VISION / IDEA**，没有当前 Frozen visual confirmation |
| 快捷键 | 历史 Page Map / Settings Research 提及 Shortcuts | **UNSET**；未找到 Assistant 专属、已接受的快捷键 Contract |
| 主动提醒 / 汇报 | Product Bible §9；Journal §20–23；Current Blueprint §10 | **CURRENT SEMANTIC**，具体通知阈值和频率属于 Settings / Company Policy / Attention Contract |
| 语音、图片、文件、拖拽输入 | Product Bible §5 | **HISTORICAL CANDIDATE**；本报告不升级为当前必需输入面 |

## H. Proactive Attention Contract

### H.1 历史已明确的主动触发

历史 Product Bible 示例包括：项目长期无进展提醒会议、投入增加而互动下降时建议分析、任务失败时询问切换能力；Journal §23 将触发归纳为节律（早报/会前/检查点/日末）、事件（风险/异常/承诺到期/外部结果变化/能力过载/机会信号）和 CEO 请求。

### H.2 打扰 CEO 的最小解释

每次主动出现必须能回答：**为什么现在、依据什么、影响多大、CEO 最小需要做什么**。如果证据不足、已有责任人、重复提醒、超出关注窗口或没有可行动价值，Assistant 应聚合、延后或保持安静。

### H.3 CEO Gate

必须回到 CEO 的典型内容：外部承诺、启动或扩大业务、改变 Goal/Positioning/Strategy Boundary、公司结构或责任变化、重大预算/资源重新分配、不可逆发布/删除/关闭、高风险或无法恢复的动作。普通查询、摘要、整理、草拟和授权范围内可逆动作不应制造额外 Gate。

“主动”不等于“自主决策”；Assistant 的主动性受 Attention、Evidence、Permission、Risk 和现有 Decision Gate 约束。

## I. Business Bootstrap Role

### I.1 当前接受的产品路径

```text
CEO 表达经营意图
→ Curis 理解 Situation
→ 必要时 Capability Discovery / Research
→ Operating Proposal
→ 必要 CEO Gate（只处理不能合理代理的 Boundary）
→ Bootstrap / Reuse / Compose
→ 合法 Leader 接受专业责任
→ 开始经营
```

### I.2 Assistant 在其中的职责

- 让 CEO 用自然语言表达意图，识别缺少的情况信息和能力信息；
- 组织 Situation、Capability Discovery、Research 的输入与状态；
- 汇总专业 Leader / Workspace Engineering / Domain Expert 提出的方案；
- 准备 Proposal、列出可复用结构、缺口、风险、替代方案和需要 CEO 决定的边界；
- 跟进 Bootstrap、责任交接、结果和恢复；
- 在能力不足或未知业务时诚实返回 `USE EXISTING / COMPOSE EXISTING / RESEARCH / ADAPT / BUILD / ACQUIRE / ESCALATE / REFUSE` 等路径。

### I.3 明确不承担的职责

Assistant 不是未知行业的默认研究员、策略专家、Workspace Builder、Team Leader 或 Quality Owner。它可以协调这些责任主体，不能伪造自己已经拥有该行业方法。旧 Product Bible §8 中“推荐业务模板、询问信息、创建项目、配置负责人和能力”的路径属于较早 Draft，已由当前 Bootstrap/Three-Layer 产品语义收窄：成熟结构可复用，但未知业务先经过专业责任与能力发现。

## J. Team Leader / Domain Expert Boundary

| 角色 | 负责什么 | Assistant 的关系 |
|---|---|---|
| CEO Assistant | Company-level coordination、attention、brief、handoff、follow-up、escalation | 向 CEO 汇报；不持有某一 Domain 的专业结果 |
| Department / Business / Workspace Leader | 本责任 Scope 的 Goal/Strategy、团队组织、优先级、结果与异常 | Assistant 协调其跨层输入，不替代其判断 |
| Domain Expert / Professional Employee | 行业研究、专业方法、具体 Responsibility、Result/Evidence | Assistant 提供 context、收回结果、解释与升级 |
| Engineering Team | 研发、设计、实施、测试、发布等工程责任 | Assistant 可协调和汇报，不能冒充工程责任人 |
| Workspace Executor / AI Employee | 具体工作与受限工具执行 | Assistant 不创建第二套 Executor/Task/Result Runtime |

Current Frozen Shared Authority 的关键句是：`ASSISTANT_COORDINATES_NOT_REPLACES`；Assistant 与 Leader 不是二选一，CEO 可以直接进入 Employee Workstation。

## K. Desktop Pet / Companion Vision

### K.1 证据

`Product Bible v1.0-draft/17 AI秘书` §4、`03 信息架构` §1、`05 全局交互`、`24 Design System` 和 `50 Curis 产品最终结构总结` 都使用“桌面宠物式交互”，包含拖动、展开、收起、悬浮、页面内移动和场景状态变化。它表达的是“长期陪伴”的呈现方式，而不是一个新的 Company/Employee/Runtime 对象。

随后 `ADR-0033` 明确 Supersede 固定秘书栏；`issues/20260730_global_assistant_runtime_v1.md` 明确禁止 Desktop 浮窗；2026-08-04 UI Audit 记录旧 `curis-companion` 已退役、统一 Global Assistant Drawer 生效。

### K.2 分类结论

- **不是当前 Frozen Product Object：** 没有找到单独的 Desktop Pet identity、lifecycle、权限或数据合同。
- **更像未来 Presentation Form：** 如果未来重新考虑，它应是同一 CEO Assistant Runtime 的宿主/展示适配器，不应建立第二个 Companion Assistant。
- **当前状态：** **VISION / HISTORICAL DESIGN IDEA**，不是 Current UI requirement，也不是本轮授权的 UI 设计结论。

## L. Current vs Historical vs Vision Matrix

| 主题 | Current / Frozen | Historical / Consumed | Vision / Candidate | 本次判断 |
|---|---|---|---|---|
| Assistant 是第一位 AI Employee / Company-level Chief of Staff | Current Blueprint §10、Shared Authority §9.3；源自 ADR-0040/Journal | Journal/Reasoning 的完整推导 | — | **PRESERVED** |
| 全局跨页面身份与入口 | ADR-0033、ADR-0045、Current Shell/Blueprint | Runtime Issue 与 UI Review 的实现证据 | 具体 Desktop host 形式 | **PRESERVED SEMANTIC; VISUAL OPEN** |
| CEO Desk 是主工作面 | Current CEO Desk Contract / Blueprint | Journal §21/Reasoning §16 | — | **PRESERVED** |
| 固定秘书栏 / 永久第三栏 | ADR-0033 明确 Supersedes | 早期 CEO Office 方案 | — | **SUPERSEDED** |
| FAB + 右滑 Drawer | 当前实现/历史 Audit 有证据 | 2026-07-29–08-04 UI Reviews | 未来可调整形态 | **IMPLEMENTATION EVIDENCE, not a new Product Truth** |
| 桌面宠物、自由拖动、场景形态变化 | 无当前 Frozen Contract | Product Bible v1.0-draft | Future presentation form | **VISION / IDEA** |
| CEO Assistant 可命名 | ADR-0033 Runtime Issue：Identity 可配置 | Product Bible 身份/陪伴语义 | 完整重命名/版本历史规则 | **HISTORICAL SUPPORTED; lifecycle detail open** |
| 主动汇报、异常提醒、决策准备 | Current Blueprint §10、Desk/Operating Day；Journal | Product Bible 示例 | 频率/阈值细化 | **PRESERVED SEMANTIC; policy detail open** |
| Assistant 创建业务/项目并配置专业团队 | 早期 Draft | Product Bible §8 | — | **EVOLVED / NARROWED** |
| Assistant 直接执行行业研究/策略/设计/质量 | Current 明确禁止 | 早期 Draft 的隐含宽职责 | — | **SUPERSEDED / BOUNDARY CLOSED** |
| 语音/图片/文件/拖拽输入 | — | Product Bible §5 | Future input expansion | **CANDIDATE, not Current requirement** |
| Assistant 专属快捷键 | — | Page Map/Settings 提及通用 Shortcuts | Future accessibility/productivity option | **UNSET** |

## M. Conflicts / Missing Authority

1. **身份自动创建与删除/退休规则未完全统一。** 历史推导称 Company 创建后有唯一 Assistant；运行 Issue 曾允许 Identity 为空并禁止固定角色。Current Product Truth 已接受 Assistant 是第一位员工，但是否永远不可删除、如何暂停/退休/重新任命、重命名如何影响历史报告，仍需单独明确。
2. **Name / Role / Display Name 三者的最终字段边界未形成单一历史 Contract。** 历史材料支持“可命名 + 固定公司级责任”，但没有足够证据确定用户可否修改 role、是否可配置称谓、Assistant 的显示名称是否继承 Brand Configuration。
3. **全局语义已明确，视觉承载未冻结到“宠物/FAB/Drawer/Pane”中的某一个。** 不应让旧 Prototype 或某次实现审计自动覆盖当前 Frozen Shell/UI Blueprint。
4. **Proactive policy 只有原则和示例，细节在 Settings / Company Policy。** 阈值、免打扰窗口、聚合规则、通知渠道和 CEO override 需要后续 Product/Settings Review。
5. **Context continuity 的产品呈现与 Runtime 实现不完全等价。** 历史/实现文档证明了白名单化 page context、tenant 校验和 global state；不能据此宣称所有跨页面对话、记忆和多设备同步都已完整交付。

## N. What Current Visual Design Must Respect

以下是从历史证据和当前 Frozen Authority 中能安全带给设计的约束，不是新的视觉 Contract：

1. 以 Assistant 的**责任与事实**为主体：为什么出现、依据、影响、Owner、下一步和恢复入口；不要把聊天气泡或宠物形象当作产品价值主体。
2. Assistant 可在 CEO Desk 主内容、上下文抽屉或统一全局入口出现；不能恢复固定秘书栏、永久第三栏或独立一级导航。
3. 当前页面 scope 必须可见且可返回；Assistant 在 Department/Business/Workspace 中提供局部相关信息，不能制造跨业务混合上下文。
4. 主动提醒要可解释、可聚合、可稍后处理；没有真实 Needs CEO / Risk / Decision / Exception 时保持安静。
5. 高影响/不可逆操作必须显式 CEO Gate；普通查询、摘要、整理、草拟和授权内可逆动作不应被表单化或反复弹窗打断。
6. 专业问题回到 Leader/Domain Employee 的 Workstation；Assistant 负责连接，不把专业员工的工作压缩成 Assistant 聊天记录。
7. 若未来采用 Desktop Pet，它只能是同一 Assistant 的 Presentation Adapter；不得出现第二个身份、第二套记忆、第二套权限或第二个 Runtime。
8. UI Blueprint 中的 Assistant 形态仍需消费 Frozen Shell 的“Global Capability ≠ Global Topbar”与“Runtime State ≠ UI Expand/Collapse”边界。

## O. Questions genuinely requiring CEO decision

1. 是否正式冻结“每个 Company 恰有一个 CEO Assistant，Company 创建时物化；可暂停/退休但不可删除”的完整身份生命周期？
2. Assistant 的用户可编辑字段是否为 `name / displayName / avatar / tone / reporting cadence`，而 `role=CEO Assistant / Chief of Staff` 与责任范围保持不可任意修改？
3. 是否允许用户重命名/更换头像而保留同一 Employee identity、历史报告和 Result/Evidence 归属？
4. Assistant 是否可以被重新任命/升级版本，还是永远保持同一 Company-level 员工？
5. 最终全局呈现是否只保留统一入口 + 按需 Pane/Drawer，还是未来允许同一 Runtime 的桌面 Companion/Pet 适配器？如允许，是否需要先做独立 Visual Delta？
6. 是否需要正式定义 Assistant 专属快捷键；若需要，放在 Settings / Personal Preferences，而不是 Product 一级导航？
7. 主动提醒的默认静默窗口、优先级、聚合与 CEO override 由哪份 Settings / Company Policy Contract 冻结？
8. CEO Operating Day 的 Brief、Matters、Handoff、Decision、Exception、Evidence、Learning、Closeout 是否继续由 Assistant 统一组织，而不创建 Assistant 专属第二套 Truth？
9. Business Bootstrap 中，Assistant 是否允许在已授权的低风险范围内直接执行少量可逆动作；其余一律形成 Proposal 并交给 Leader/CEO Gate？
10. 当 Assistant 自身能力不足时，是否统一显示“缺少什么、由谁负责、返回哪里、下一步是什么”，而不是让 Assistant 代替专业 Owner 临场补全？

## Audit conclusion

- **历史核心已恢复：** Company-level 第一位 AI Employee / Chief of Staff、全局可达、跨页面 context、协调/汇报/跟进/升级、CEO Gate 与专业边界。
- **历史与 Current 已分离：** ADR-0033 的全局 Runtime 方向与 Current 保持一致；早期固定秘书栏、Assistant 直接拥有专业工作、旧 Companion UI 已标为 Superseded 或历史实现。
- **桌面宠物已正确降级：** 证据支持它是早期 Presentation Form / Vision，不是独立对象，也不是当前必做 UI。
- **没有发现需要本轮回写 Current Authority 的新事实。** 真正未决项集中在身份生命周期、重命名字段、主动策略细节和最终视觉承载，应由 CEO 单独 Decision，不由历史审计自行补答案。

**CURIS CEO ASSISTANT — HISTORICAL PRODUCT TRUTH RECOVERED / CURRENT–HISTORICAL–VISION SEPARATED / STOP FOR CEO REVIEW**
