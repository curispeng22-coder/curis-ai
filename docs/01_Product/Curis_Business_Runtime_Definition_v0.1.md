# Curis Business Runtime 定义 v1.6

> **文件名说明**：本文件沿用早期文件名 `..._v0.1.md` 以保留历史引用；当前有效内容与版本以本文标题、状态和修订记录为准（v1.6）。不得根据文件名推断 Runtime 版本。

> **状态**：Draft，待产品席 Review
> **日期**：2026-08-09
> **依据**：ADR-0040（Company OS 固定 + Workspace 开放）、ADR-0041（Business Runtime 完成标准）
> **来源**：`curis-ui-prototype/`（18 页 + `curis-prototype.js` 7036 行）的语义还原 + 缺口补齐决策
> **作用**：定义三类业务工作台共享的 Runtime 契约。本文件仍为 Draft，不能单独解锁开发；必须与唯一 Product Blueprint、Simulation 和独立 Issue 一起通过 Review。

---

## 0. 本文件怎么来的，以及它管什么

ADR-0041 规定：页面能渲染、按钮能点、接口返 200、单测通过，**都不算功能完成**；只有真实业务场景跑完整个生命周期（含至少一条失败路径）才算。因此每个模块必须先有 Business Runtime 定义。

此前判断是"10 个模块一份定义都没写"。这个判断需要修正：**定义其实已经写了七八成，只是写在原型的 JS 和中文文案里，不在文档里。** 本文件做的是翻译与补齐，不是重新设计。

三类内容用不同标记区分，实现时务必注意：

| 标记 | 含义 | 处理方式 |
|---|---|---|
| 【原型】 | 原型已明确写出 | 直接实现，不要二次发挥 |
| 【补齐】 | 原型缺失，本文件做出的新决策 | 需产品席确认 |
| 【存疑】 | 原型自相矛盾或语义不清 | 实现前必须澄清，不得猜 |

**本 v1.6 覆盖 5 个核心对象**：BusinessDirection、Commitment、Workspace（含 Blueprint/Stage）、Cadence + ScheduledRun、Outcome + Attribution，并增加 FoundingRun / Company Formation、CEOAssistant、AIEmployee / RoleSlot / CapabilityBinding、Cycle、Handoff、DecisionPacket、Acceptance、研发工作台 Stage Runtime、内容发布工作台的 ContentItem、版本审核审计、互动与线索回流、平台专属 Simulation、三业务 SimulationRun 的最小持久化契约、脉搏 / 置信度 / 容量 / 升级默认值、AI 组织版本与状态维度边界，以及旧执行链迁移边界。
业务范围为三类共享同一引擎的工作台：研发工作台、小红书运营工作台、抖音 / TikTok 运营工作台。Meeting、Knowledge、经营账和经营雷达在 Blueprint 中仍是 Company OS 的目标消费面，但不属于 `RUNTIME-FOUNDATION-001` 的新增业务对象；Foundation 只提供它们所需的 Cycle、Evidence、Decision 和 Handoff 反查能力，后续模块必须复用这些对象，不能另起状态机。
研发工作台中的“Curis 的自研发”（工作项名：完善 Curis）只是第一个真实研发任务，不是额外的业务类型。
它们构成"CEO 的一天"闭环的最小完备集。Meeting / Decision / Knowledge / 经营账 / 经营雷达留待后续版本。

---

## 1. 通用运行时契约（所有对象共同遵守）

这一节是 A1 状态机引擎的需求来源。**先读这节，否则下面每个对象的状态机都会被实现成第 13 套裸字符串。**

### 1.1 状态机契约

1. **状态值必须来自集中定义的枚举**，不允许在业务代码里写裸字符串。
   现状缺陷：后端仅 2 个 Enum、12 套裸字符串，已经出事——代码写 `succeeded`、数据库约束写 `completed`，对不上。
2. **流转必须走统一入口**，禁止直接 `UPDATE ... SET status = ?`。
3. **非法流转必须被拒绝并报错**，不允许静默写入。
   例：`running → resolved` 非法（原型 `resolveScheduledRuns` 明确只允许 `waiting_ceo / acknowledged / failed` 转 `resolved`）。【原型】
4. **每次流转必须留痕**：`from / to / trigger / actor / at / reason`，写入统一的流转日志表。
5. **触发者(actor)必须分类**：`CEO` / `AI_EMPLOYEE` / `SYSTEM` / `EXTERNAL`。这是后续归因与审计的基础。【补齐】

### 1.2 升级到 CEO 的契约（本产品最重要的一条）

原型的实现方式是：运行结束时用正则匹配任务描述文案，命中 `/CEO|授权|回传|失败|异常|确认/` 就转 `waiting_ceo`。【原型】

**这个实现不能照抄。** 它把"是否需要人拍板"这件事寄托在自然语言文案上——改个措辞就会静默改变系统行为，是很危险的隐式契约。

**【补齐】升级条件必须显式声明**，在 Cadence / Stage 定义上配置结构化字段：

```
escalation: {
  triggers: [ ON_FAILURE | ON_MISSING_AUTH | ON_EXTERNAL_DATA_RETURN
            | ON_ABNORMAL_RESULT | ALWAYS_BEFORE_PUBLISH | NEVER ],
  reason: string,        // 给 CEO 看的一句话，说明为什么找他
  timeoutHours: number   // 见 1.3
}
```

原型的正则可作为**迁移期的默认推断**：读旧数据时按正则推出 triggers，写入结构化字段，之后不再依赖文案。

**六件 AI 不得静默执行的事**（对应产品红线，必须落到 `ALWAYS_*` 类 trigger）：对外发布、花钱、对外承诺、动权限/授权、删除或不可逆操作、扩大业务范围。【补齐，源自产品口径】

### 1.3 超时兜底契约

原型**完全没有超时处理**：`queued` 可无限等待，`waiting_ceo` 不打开就永久常驻，决策室有"决策到期"字段但无任何对应逻辑。【原型·缺失】

**【补齐】** 三条兜底，全部只升级不替代——**系统永远不替 CEO 做决定**：

| 情形 | 超时后动作 |
|---|---|
| `queued` 超过 N 小时未获得容量 | 生成"容量不足"异常事项，升级 CEO；不自动抢占 |
| `waiting_ceo` 超过 `timeoutHours` | 提升提醒等级并在 CEO 桌面置顶；记 `overdueSince`；不自动批准 |
| 外部数据回流超时 | 标记结果为 `STALE`，保留手动补录窗口；不生成估算值 |

**反造假硬约束**【原型，逐字保留】：
> "外部平台未授权时，收入与结果必须由 CEO 补录；手动数据会标记为'待验证'，不会伪装成 API 事实。"
> "没有平台授权时，结果窗口必须由 CEO 补录，不会用假数据填满结果。"

### 1.4 证据契约

任何一条对外结果都必须可回溯到证据。证据采用两个正交维度，禁止把“是否验证”和“数据是否新鲜”压成一个状态：

**维度一 · `verificationStatus`（是否被采用为经营事实）**。统一 `EvidenceGrade` 枚举，被 Outcome / 经营账 / 公司脉搏共用：【补齐，收敛原型三处散落的口径】

| 值 | 界面文案 | 含义 |
|---|---|---|
| `UNVERIFIED` | 数据待验证 | 手动补录或无授权 |
| `VERIFIED` | 已验证价值 | 外部 API 回传或 CEO 真实验收 |
| `ABNORMAL` | 结果异常 | 数据冲突或验收未通过 |

**维度二 · `evidenceCondition`（证据当前状态）**：`FRESH`（新鲜） / `STALE`（待回流或已过窗口） / `CONFLICT`（来源冲突） / `MISSING`（关键证据缺失）。`UNKNOWN` 是当关键来源或组成项无法判断时的显示态，不是可被 CEO 采用的验证等级。

**硬规则**：只有 `verificationStatus=VERIFIED` 且 `evidenceCondition=FRESH` 的结果才能支持“扩大业务”；`ABNORMAL` 或 `CONFLICT` 冻结扩大权限，`STALE` / `MISSING` 只能进入补证据或暂停路径。【原型 + 补齐】

### 1.5 容量契约

每条业务有独立容量合同，节奏运行受其约束。【原型】

```
capacityContract: { maxConcurrent: int, capacityPct: float, queuePolicy: enum }
```

原型默认值（迁移时作为种子数据）：

| 业务 | maxConcurrent | capacityPct | queuePolicy |
|---|---|---|---|
| 研发工作台 | 3 | 82% | 失败即暂停 |
| 小红书运营 | 4 | 72% | CEO 发布前确认 |
| 抖音 / TikTok 运营 | 3 | 68% | 授权或结果异常时升级 |

**【补齐】** 跨业务容量不做运行中抢占。各 Workspace 先在自己的容量合同内排队；当共享 AI 员工或能力不足时，按“CEO 明确优先级 → 外部承诺截止时间 → 风险止损 → 正常节奏”的顺序决定下一项进入运行，平级按先到先得。等待超过 `queueTimeoutHours` 后升级 CEO，不自动挪用其他业务资源。

### 1.6 旧执行链迁移边界

当前代码中的 `workflow_runs / workflow_steps` 与 `content_workflow_runs` 是历史执行载体，允许继续保存内部执行过程，但不再承担新产品的业务状态真相：

1. `ContentItem.lifecycleStatus`、`ContentItem.exceptionStatus`、研发 Cycle / Stage 状态、`CEOAssistant.lifecycleStatus`、`AIEmployee.lifecycleStatus`、`RoleSlot.status`、`CapabilityBinding.status`、`FoundingRun.state` 和 `SimulationRun.passStatus` 必须由 v1.6 Runtime 入口写入；旧表的 `running / completed / failed` 只能作为 `executionRef` 或迁移来源。
2. 旧执行链可以作为 Stage 的子运行，但必须反向关联 `companyId / workspaceId / blueprintVersion / stageId / runId`；复制一段文本或只保存旧 `run_id` 不算跨模块交接。
3. 旧状态不能直接映射为 `VERIFIED`、`PUBLISHED`、`ACCEPTED` 或 CEO 已批准。只有外部回执或 CEO 真实验收才能产生这些业务事实。
4. 迁移既有记录时必须保留原始状态、来源表、来源时间和迁移原因；无法证明的字段标为 `UNKNOWN / UNVERIFIED`，不得补造成功链路。
5. 新 Runtime 建立后，任何直接写旧表 status 的路径都必须经过适配器或被限制为内部执行遥测；不得出现第二套可改变 CEO 所见业务状态的入口。

### 1.7 跨模块交接与 CEO 决策契约

`Handoff`、`DecisionPacket` 和 `Acceptance` 不是聊天消息，也不是复制到下一个页面的文本；它们是阶段之间可反查的业务输出。

| 对象 | 必须记录 | 关键约束 |
|---|---|---|
| `Handoff` | `handoffId / sourceType / sourceId / targetType / targetId / fromRole / toRole / inputRefs / outputRefs / acknowledgement / returnReason / missingRefs / attemptedScope / suggestedOwner / actor / at / nextCheckAt` | 目标 Owner 必须明确；未确认的交接不能被显示为已接手；跨 Workspace 交接必须带 Company / Workspace 范围；退回必须保留缺口与建议 Owner |
| `DecisionPacket` | `decisionId / subjectType / subjectId / currentState / whyNow / evidenceRefs / unknowns / options / impactMap / recommendation / effectiveAt / rollbackCondition` | AI 只能准备或推荐；高影响变化必须由 CEO 产生最终 choice；Decision 生效后必须回写目标对象 |
| `Acceptance` | `acceptanceId / subjectType / subjectId / criteria / evidenceRefs / actor / decision / reason / decidedAt / nextAction` | `ACCEPTED` 只能来自 CEO 真实验收或已定义的外部验收回执；拒绝、证据不足和待验证不得进入完成态 |

这些对象都必须能通过 `companyId / workspaceId / cycleId / runId` 反查；不能依赖自然语言摘要作为唯一关联。

三类交接输出各自有状态机：

```text
Handoff:        CREATED → SENT → ACKNOWLEDGED → COMPLETED
                                      ├──────────→ RETURNED / REJECTED / ESCALATED
DecisionPacket: DRAFT → READY → WAITING_CEO → DECIDED → APPLIED
                                      └────────→ SUPERSEDED / ROLLED_BACK
Acceptance:     PENDING → ACCEPTED → CLOSED
                         ├────────→ REJECTED
                         └────────→ INSUFFICIENT_EVIDENCE → WAITING_CEO
```

交接被拒、Decision 被回滚或验收证据不足都必须保留原记录，并生成新的下一步对象；不能通过编辑原文伪造“已完成”。

### 1.8 v1.2 已决策的运行默认值

以下规则把原型中仍需猜测的数字和分支收敛为可实现默认值。它们是运行默认值，不是 AI 可以绕过 CEO 的自动决策；未来调整必须形成版本化 Decision，并重新 Simulation。

#### 公司脉搏六维

六个维度先判断状态，再显示原因，不生成一个掩盖证据差异的总分：

| 状态 | 默认判定 | CEO 看到的意义 |
|---|---|---|
| `ON_TRACK` | 没有 `BLOCKED` / `AT_RISK`；关键证据新鲜且已验证；容量低于 80%；没有逾期 CEO 决策 | 正常运行，Assistant 默认不打断 |
| `ATTENTION` | 存在一个可控观察项：容量 80%–90%、非关键证据待验证、或检查点轻微逾期 | Assistant 汇总提醒，建议处理但不强制打断 |
| `AT_RISK` | 关键结果失败 / 未验证、容量超过 90%、重复失败，或 CEO 决策超过对应超时 | Assistant 置顶并准备 Decision Packet |
| `BLOCKED` | 缺少 Owner、能力、授权或外部条件，导致下一阶段无法开始 | 必须明确阻塞原因和恢复责任 |

`UNKNOWN`、`STALE`、`CONFLICT` 是证据维度，可与上述经营等级同时存在；它们不能被折算成“正常”。

#### 暂停与归档

- `pauseReviewAfter = 7d`：暂停满 7 天，Assistant 生成一次复盘事项。
- `archiveCandidateAfter = 30d`：暂停满 30 天，仅生成“可归档候选”，不自动归档。
- 存在未关闭外部承诺、客户验收或待回收结果时，不得生成可归档候选。
- 只有 CEO 的 Decision 才能恢复、转交或归档；归档必须释放容量并保留全部证据。

#### 置信度

置信度表示“当前依据有多完整”，不是成功概率，也不是模型自报的确定性。默认由可解释的五项证据组成：

```text
confidenceScore = sourceDirectness 30%
                + freshness 20%
                + corroboration 20%
                + coverage 20%
                + sampleAdequacy 10%
```

分数必须同时保存组成项与 `evidenceRefs`：`0–39` 低、`40–69` 中、`70–89` 高、`90–100` 很高。缺少关键组成项时显示 `UNKNOWN`，不得用模型生成的百分比填空。

#### AI 员工退回责任

AI 员工可以在发现能力、权限、容量或输入不满足责任契约时主动退回，不得静默失败。退回必须记录 `returnReason / missingRefs / attemptedScope / suggestedOwner / at`，Handoff 进入 `RETURNED`，原责任不标记完成；CEO Assistant 负责重新分配、补能力或请求 CEO 决策。退回不是惩罚，而是保持责任边界真实。

#### 升级超时默认值

| 触发类型 | `timeoutHours` | 超时后的唯一自动动作 |
|---|---:|---|
| 外部发布、对外承诺、不可逆动作 | 4 | 提升提醒、置顶 CEO Desk，不自动批准 |
| 资金、资源、战略方向、公司结构 | 24 | 提升提醒并生成影响摘要，不自动执行 |
| 普通失败、授权缺失、结果异常 | 24 | 追加检查点与恢复建议，不自动清除异常 |
| 声誉 / 安全 / 重大客户风险 | 2 | 立即置顶并暂停相关动作，不等待自动处理 |

超时只改变提醒等级和 `overdueSince`，不改变 CEO 的决定，也不把 `WAITING_CEO` 伪装成通过。

### 1.9 CEO Assistant Runtime 契约

CEO Assistant 是 Company Runtime 中真实存在的第一位 AI 员工，不是 Global Assistant UI、聊天入口或第二套任务系统。Global Assistant Runtime 只提供身份、通知、查询和命令承载；`CEOAssistant` 对象本身必须拥有可持久化的责任、上下文、权限、状态和质量证据。

#### 1.9.1 对象与组织位置

```text
Company
├── CEO                         人类 Owner / 最终决策者
├── CEOAssistant                Company-level AI Employee / Chief of Staff
├── Professional AI Employees   稳定职责与专业结果的 AI 员工
└── Workspace AI                业务运行时按 Workspace 实例化的执行 AI
```

`CEOAssistant` 最小字段：

```text
assistantId / companyId / ceoId / orgVersion / roleVersion / lifecycleStatus
contractVersion / contextVersion / capabilityRefs[] / escalationPolicy
reportCadence / quietHours / qualitySnapshot / createdAt / updatedAt
```

`CEOAssistant` 是一种特殊的 Company-level `AIEmployee`：它拥有独立的
`assistantId` 和自己的生命周期，但不再额外生成一条重复的 Professional
`AIEmployee` 记录，也不占用某个 Workspace `RoleSlot`。组织查询应把它作为
AI 组织根节点投影出来；需要执行具体业务时，由它向 Professional AI
Employee 创建 `Handoff`。

每个 Company 当前只能有一个 Operating 状态的 CEO Assistant。升级或换责必须保留旧版本、迁移原因、交接对象和生效时间；不能通过刷新页面或重建 Snapshot 产生第二个事实身份。

#### 1.9.2 生命周期与状态入口

```text
CREATED → CONFIGURED → LEARNING_CONTEXT → OPERATING → EVALUATING
                                             ├────────→ SUSPENDED
                                             ├────────→ UPGRADED → OPERATING
                                             └────────→ REASSIGNED → OPERATING
```

| 状态 | 进入条件 | Assistant 允许做什么 | 离开条件 |
|---|---|---|---|
| `CREATED` | Company 创建成功并生成唯一 Assistant | 生成初始角色契约，等待 CEO 配置 | CEO 确认服务范围、权限和汇报节奏 |
| `CONFIGURED` | 角色、能力、升级规则和默认节律已定义 | 读取 Company 基础事实，准备 Founding / Operating Day | Context 完整性检查通过 |
| `LEARNING_CONTEXT` | 首次接管公司或 Context 版本变更 | 归纳决议、偏好、业务状态和历史，提出可拒绝假设 | CEO 接受、修正或拒绝关键 Context |
| `OPERATING` | Context 已确认且至少一条责任链可运行 | 主动汇报、请求分流、协调专业 AI、跟进、升级和授权内可逆动作 | 到达评估周期、连续质量异常或 CEO 发起升级 |
| `EVALUATING` | 日 / 周 / Cycle 复盘或重大失败后 | 提交准确度、遗漏、误报、交接完成率、CEO 采纳率和成本 | CEO 批准升级、调整责任、降级、暂停或恢复 |
| `SUSPENDED` | CEO 暂停或质量 / 权限门禁触发 | 只保留安全通知、证据和迁移信息 | CEO 恢复、重配或重新指派 |
| `UPGRADED` | 新版本、公司扩展或能力变化生效 | 加载新契约，执行 Context / 权限迁移检查 | 迁移证据完整后进入 `OPERATING`，否则 `SUSPENDED` |
| `REASSIGNED` | CEO 改变 Assistant 的责任范围或交接对象 | 生成交接包，保留旧责任与历史证据 | 新责任接手并通过检查后进入 `OPERATING`，否则 `SUSPENDED` |

所有状态变化必须记录 `from / to / actor / at / reason / contractVersion / contextVersion / evidenceRefs`。`GlobalAssistant` 的在线状态、页面是否打开或模型是否可调用，不得替代 `lifecycleStatus`。

#### 1.9.3 责任、触发与输出

| 责任 | 触发 | 持久化输出 | 不得做什么 |
|---|---|---|---|
| 汇报与排序 | Morning Brief、周期开始、结果回流 | `Brief`、事项优先级、来源 / 新鲜度 / 置信度 | 不制造新的事实 |
| 请求分流 | CEO 自然语言请求 | `RequestClass`、最小澄清、直接答复或 `Handoff` | 不把每个请求包装成 Business / Project / Task |
| 专业协调 | Opportunity、Exception、缺口或跨业务影响 | `Handoff`、下一检查点、责任回收记录 | 不替专业 AI 做领域判断 |
| 决策准备 | 高影响变化、外部承诺、异常升级 | `DecisionPacket`、影响图、未知、回滚条件 | 不静默批准或对外承诺 |
| 连续跟进 | `Handoff` 到期、退回、失败、等待 CEO | 提醒、`overdueSince`、升级事项、重新分配建议 | 不把超时当成功，不静默换 Owner |
| 日末收束 | CEO Operating Day Closing | `Closeout`、明日承接、Context 候选版本 | 不覆盖历史决议或未关闭责任 |

触发优先级为：高影响风险 / 外部承诺 → CEO 明确请求 → 阻塞与退回 → 结果回流 → 周期性汇报。低影响、已有人负责、重复提醒或无行动价值的信息应聚合或静默，但仍保留可查询的审计记录。

#### 1.9.4 动作边界与 Assistant Simulation

CEO Assistant 可以读取 Company / Business / Workspace / Evidence，创建草案、Handoff、DecisionPacket、提醒和检查点，并在已有授权策略内执行可逆动作；以下动作必须回到 CEO 的 Decision / Acceptance：对外发布、资金与资源扩大、外部承诺、权限变更、公司结构变化、不可逆操作和证据采用。

Assistant Runtime 至少需要以下可执行验证：

1. **首次进入**：Company 创建后仅生成一个 `CEOAssistant`，由 `CREATED → CONFIGURED → LEARNING_CONTEXT`，CEO 接受 Context 后才进入 `OPERATING`。
2. **正常经营日**：Assistant 主动形成 Brief 和 Handoff；低影响事项保持安静，高影响事项进入 CEO Desk；不创建第二套任务真相。
3. **异常升级**：专业 AI 退回、外部授权缺失或证据冲突时，Assistant 生成带来源 / 责任 / 下一检查点的 Exception 或 DecisionPacket，不伪造完成。
4. **责任迁移**：Assistant 升级 / 换责时旧版本保持可追溯，新版本必须通过 Context、权限和交接检查后才可 Operating。
5. **质量评估**：周期结束形成质量快照；CEO 可接受、调整、暂停或重新指派，所有选择都回写 Assistant Runtime。

`CEOAssistant` 的 `assistantId` 必须能与 `Brief / Handoff / DecisionPacket / Closeout / qualitySnapshot` 反查；仅有 Global Assistant 的通知或聊天记录不构成 Assistant Runtime 证据。

### 1.10 First Arrival / Company Formation Runtime

Curis 的运行闭环必须从“公司尚未建立”开始，而不是从已有业务列表开始。首次打开时看到的 Assistant 是 **Pre-company Founding Guide**：它可以介绍 Curis、收集意图和准备草案，但在 CEO 确认 Company 之前，它不是拥有 Company 责任的 `CEOAssistant`，不能创建业务、委派专业 AI 或改变公司状态。Company 持久化成功后，系统才创建唯一的 `CEOAssistant` 对象并进入 §1.9 生命周期。

#### 1.10.1 Company 与 FoundingRun

Company 的经营投影状态：

```text
UNFORMED → DRAFT → CONFIGURING → OPERATING
                         └──────→ ABANDONED（仅草案可放弃）
OPERATING → RESTRUCTURING → OPERATING
```

首次创建使用一个可恢复的 `FoundingRun`，而不是多个表单页面各自推进：

```text
ARRIVED → INTENT_CAPTURED → CLARIFYING → PROPOSED → CEO_CONFIRMED
                                                   └→ COMPANY_CREATED
COMPANY_CREATED → FIRST_BUSINESS_CONFIGURING → FIRST_BUSINESS_READY → COMPLETED
       ├────────→ WAITING_CEO / RETURNED / REJECTED
       └────────→ ABANDONED（仅 Company 尚未创建时）
```

`FoundingRun` 最小字段：

```text
foundingRunId / ceoId / companyId? / guideSessionId / assistantId?
intentText / clarificationRefs[] / companyDraftVersion / businessDraftRefs[]
state / nextAction / actor / at / evidenceRefs[] / createdAt / updatedAt
```

规则：

1. `DRAFT` 只表示可审阅草案；没有 CEO 明确确认，不得写入 Operating Company、BusinessDirection 或 AI 员工责任。
2. CEO 确认 Company 后，必须在同一条可反查链上生成 `companyId`、`assistantId` 和 Company Context 初始版本；三者不能由不同页面分别伪造。
3. Company 可以先创建而暂时没有 Business，但只有 `FIRST_BUSINESS_READY` 通过最小 Outcome、Owner、Capability、Evidence Route 和失败出口检查后，才允许进入 Launch Check。
4. CEO 中途离开、拒绝或修改时，FoundingRun 保留原草案和原因，可恢复或重新提案；不能用“下一步”按钮覆盖历史。
5. `Pre-company Founding Guide` 的消息不计入 CEOAssistant 的质量和责任统计；Company 创建后产生的 Brief、Handoff、DecisionPacket 和 Closeout 才归属于 `assistantId`。

#### 1.10.2 First Arrival Runtime Contract

| 阶段 | Surface | Owner | 必须输入 | Durable Output | 失败 / 退出 |
|---|---|---|---|---|---|
| ARRIVED | Welcome / CEO 办公室空态 | Pre-company Founding Guide | CEO 身份、入口选择 | `foundingRunId`、欢迎上下文 | CEO 离开 → 可恢复，不创建假 Company |
| INTENT_CAPTURED | Founding Brief | CEO + Guide | “想经营什么”、为谁创造价值、第一结果 | `intentText`、初始未知项 | 内容不足 → `CLARIFYING` |
| CLARIFYING | Founding Brief 对话 | Guide | 目标、边界、时间盒、反馈路径 | `clarificationRefs[]`、假设列表 | CEO 拒绝假设 → 重新澄清 / `RETURNED` |
| PROPOSED | Company Design | Guide / CEO Assistant（Company 创建后） | Company 草案、Business 草案、影响预览 | `companyDraftVersion`、`businessDraftRefs[]` | 缺少关键输入 → `WAITING_CEO` |
| CEO_CONFIRMED | Company Design 确认门 | CEO | 草案、边界、决策权限、第一业务结果 | 审计化 CEO 确认 | 拒绝 → 保留草案并返回 `PROPOSED` |
| COMPANY_CREATED | Company 空间 | SYSTEM + CEO | CEO 确认记录 | `companyId`、唯一 `CEOAssistant`、Context v1 | 持久化失败 → 不显示创建成功 |
| FIRST_BUSINESS_CONFIGURING | First Business / AI Team / Launch Check | CEO + CEOAssistant | Outcome、Owner、Capability、Evidence、失败出口 | BusinessDirection、Commitment、最小 Workspace Draft | 缺口 → `WAITING_CEO`，不得启动 |
| FIRST_BUSINESS_READY | Launch Check | CEO | 模拟与启动条件 | 首个可运行 Cycle 候选 | 模拟失败 → 返回 Studio，草案保留 |
| COMPLETED | CEO Desk | CEOAssistant | Company、首个业务和下一检查点 | Operating Day 初始记录 | 任何未关闭责任必须承接到下一天 |

First Arrival 的通过证据必须形成：`foundingRunId → companyId → assistantId → businessId → workspaceId → cycleId`。页面截图、LocalStorage 草案或手动编辑数据库不能替代这条链。

### 1.11 AI Employee / Role Slot / Capability Binding Runtime

“招聘员工—配置能力—开始工作”是 Company Formation 到 Workspace Operating 之间的真实经营过程。AI 员工不是 Agent 卡片或模型下拉框，而是拥有稳定身份、汇报关系、责任契约、能力授权、容量合同和质量证据的 Company Runtime 对象。`RoleSlot` 是业务空间中的责任位置；`AIEmployee` 是可被多个 RoleSlot 复用的运行身份；二者不能混成一张配置卡。

#### 1.11.1 对象边界

```text
AIEmployee
├── identity: employeeId / companyId / reportsTo / orgVersion / roleVersion
├── responsibilityRefs[]: Outcome / Commitment / RoleSlot
├── capabilityBindings[]: CapabilityBinding
├── capacityContract: maxConcurrent / queuePolicy / capacityPct
├── presenceState: AVAILABLE / RUNNING / WAITING_CEO / BLOCKED / PAUSED
└── qualitySnapshot: evidence / cost / completion / return / escalation

RoleSlot（Workspace Blueprint 内）
└── roleSlotId / workspaceId / blueprintVersion / orgVersion / stageId
    / responsibility / ownerRef / requiredCapabilities / inputs / outputs
    / gates / failureExit / status

CapabilityBinding
└── employeeId / roleSlotId / capabilityId / authority / version / orgVersion
    / status / evidenceRefs
```

#### 1.11.1.1 身份、版本与状态维度边界

三个对象必须携带同一份 `orgVersion`；`RoleSlot` 还必须绑定具体
`blueprintVersion`。CEO 修改员工数量、责任拆分、能力授权或容量时，系统
生成新的 `orgVersion`，旧版本保持只读，并使受影响 Workspace 的
`simulationPassed` 失效。未完成迁移检查的新版本不能接收生产 Handoff。

`lifecycleStatus` 与 `presenceState` 是两个不同维度，不能混用：

- `AIEmployee.lifecycleStatus` 描述身份和责任生命周期，只允许使用下方生命周期值；
- `AIEmployee.presenceState` 描述当前是否可接活，`BLOCKED` 只属于此维度；
- `RoleSlot.status` 描述岗位在 Blueprint 中是否可被接手；
- `CapabilityBinding.status` 描述一条能力授权是否可调用。

因此，文档和界面必须写成 `lifecycleStatus=DEGRADED + presenceState=BLOCKED`，
或 `lifecycleStatus=SUSPENDED + presenceState=BLOCKED`，不得把 `BLOCKED`
当成新的 AIEmployee 生命周期状态。

#### 1.11.1.2 RoleSlot 生命周期

```text
DRAFT → READY → ASSIGNED → OPERATING
           ├──────────────→ BLOCKED
           └──────────────→ RETIRED
ASSIGNED / OPERATING → REASSIGNING → READY
```

`RoleSlot` 的 `BLOCKED` 是岗位投影状态，表示缺少 Owner、能力、授权、输入或
失败出口；它不会改变员工身份。岗位退回或换责时，旧 `RoleSlot` 与
`Handoff` 保留历史，新 Owner 必须在同一 `orgVersion` 下完成接手确认。

#### 1.11.2 AIEmployee 生命周期

```text
PROPOSED → CREATED → CONFIGURED → AVAILABLE → OPERATING
                         ├────────→ DEGRADED → AVAILABLE
                         ├────────→ SUSPENDED
                         └────────→ REASSIGNED → CONFIGURED
OPERATING → RETIRED（仅 CEO 决定，保留历史责任与证据）
```

| 状态 | 进入条件 | 允许动作 | 离开条件 |
|---|---|---|---|
| `PROPOSED` | CEO Assistant 根据 Outcome / Role Slot 形成最小团队建议 | 查看责任、能力、容量和影响 | CEO 接受、修改或拒绝 |
| `CREATED` | CEO 接受岗位身份与汇报关系 | 生成员工身份和责任契约草案 | 责任、权限和能力配置完成 |
| `CONFIGURED` | Role Slot、CapabilityBinding、容量和升级规则齐全 | 参与模拟，不得接生产责任 | 模拟通过且 CEO 批准 |
| `AVAILABLE` | 具备能力、权限和可用容量 | 接受 Handoff，准备运行 | 接到责任进入 `OPERATING`；缺口进入 `lifecycleStatus=DEGRADED + presenceState=BLOCKED` |
| `OPERATING` | 正在兑现已接受的责任 | 执行、提交证据、退回或升级 | 责任完成、退回、暂停、换责或失败 |
| `DEGRADED` | 能力质量下降、容量不足或连续失败 | 只处理已承诺范围，报告缺口 | 补能力 / 降载后回 `AVAILABLE`，或 CEO 暂停 |
| `SUSPENDED` | CEO 暂停、权限撤销或重大风险 | 保留证据、交接未完成责任 | CEO 恢复、换责或退休 |
| `REASSIGNED` | 原责任不再适合当前员工 / 业务 | 生成交接包，旧证据保持只读 | 新 Owner 完成配置和接手确认 |
| `RETIRED` | CEO 明确结束员工身份 | 只读历史责任、成本和质量 | 不可恢复为同一运行身份；需新员工版本 |

所有生命周期和 `presenceState` 变化都必须记录 `employeeId / roleSlotId / from / to / actor / at / reason / evidenceRefs / nextCheckAt`。`presenceState=RUNNING` 不能推断责任已完成；`AVAILABLE` 也不能推断能力已经通过真实验收。

#### 1.11.3 CapabilityBinding 与容量规则

`CapabilityBinding.status`：`PROPOSED → AUTHORIZED → ACTIVE → DEGRADED → REVOKED`。只有 `ACTIVE` 且 authority、版本、`orgVersion` 和 Workspace 范围匹配，AI 员工才能调用能力；撤销或版本失配立即阻止高影响动作，并生成 `RoleSlot.status=BLOCKED` 与 `presenceState=WAITING_CEO / BLOCKED` 的交接。

能力配置必须同时回答：能做什么、在哪个 RoleSlot 做、允许哪些 effect、使用哪一版、谁授权、消耗多少容量、失败如何恢复。一个 AI 员工承担多个 RoleSlot 时，必须按 `workspaceId / roleSlotId` 分别记录容量占用和交接，聚合占用不得超过员工的 `maxConcurrent`；公司级共享能力不得被某一业务静默独占；跨业务容量继续遵守 §1.5 的“不抢占”与优先级队列。

#### 1.11.4 组织配置运行链

```text
CEO / First Business Outcome
→ CEO Assistant 提出最小 AI 团队与 Role Slot
→ CEO 接受 / 修改 / 拒绝责任建议
→ 创建 AIEmployee 与 CapabilityBinding
→ 绑定 Workspace Role Slot，检查权限 / 容量 / 失败出口
→ 运行正常、能力缺席、过载、撤权和责任退回模拟
→ CEO 批准 Operating Team
→ AIEmployee 接受 Handoff 并开始 Cycle
→ 结果、质量、成本和退回记录回到 CEO Assistant
```

CEO 可以改变员工数量、角色拆分、能力和容量；任何变更必须创建新组织版本并使受影响 Workspace 的 Simulation 失效。一个 AI 员工可以承担多个 RoleSlot，但每个 RoleSlot 的责任、输入、输出、容量消耗和 Handoff 必须分开记录，不能用“内容 AI 已完成”掩盖无人负责。

组织运行至少需要验证：

1. 首个业务配置能够从 `PROPOSED` 生成最小可运行 AI 团队，CEO 拒绝后不创建生产责任。
2. 缺少能力或权限时，员工进入 `lifecycleStatus=DEGRADED`、`presenceState=BLOCKED`，Assistant 提供补能力、换责或暂停选项；权限撤销或重大风险则进入 `lifecycleStatus=SUSPENDED`。
3. 容量过载时进入业务隔离队列，不抢占其他 Workspace；超时升级 CEO。
4. AI 员工主动退回责任时，原 Handoff 进入 `RETURNED`，新 Owner 接手前不能显示完成。
5. CapabilityBinding 撤销或版本不一致时，发布、外部承诺和不可逆动作被阻断，并可反查授权版本。

---

## 2. 对象关系总图

```
Company
    │
    ├─ CEO（唯一人类 Owner）
    │     └─ CEOAssistant（Company-level 第一位 AI 员工）
    │            └─ Professional AI Employees
    │                   └─ Workspace AI（按业务空间实例化）
    │
BusinessDirection（业务方向：CEO 押的一条待验证路径，带时间盒）
    │
    ├─< Commitment（承诺：某部门对这条业务的责任约定）
    │        │
    │        └─→ Workspace（承诺落地的运行空间）
    │                 ├── Blueprint（装修蓝图：草稿版 / 运行版）
    │                 │       └─< Stage（环节五元组 + 失败出口 + CEO介入规则）
    │                 └─< Cycle（运行周期，如 2026-W31）
    │
    ├─< Cadence（节奏定义：什么时候自动跑）
    │        └─< ScheduledRun（单次运行实例 ← 7 态状态机，系统的心跳）
    │
    └─< Outcome（对外真实结果）
             └── Attribution（贡献分配：谁做的，权重合计 100%）
                      └─→ 经营账（继续投 / 暂停 / 扩大的依据）
```

**唯一归集键**：`businessId` 贯穿 Commitment / Workspace / Run / Outcome / 经营账 / 经营事项。【原型】
**执行回溯键**：`runId`，把任何一笔价值反查到具体运行、具体员工、具体模型与工具。【原型】

---

## 3. BusinessDirection（业务方向）

> CEO 押注的一条待验证的赚钱路径，带时间盒和外部反馈路径。是所有承诺与经营账的归集单元。

**界面用语纪律**：界面禁用"下注/赌注/ROI/KPI/投资组合"，一律说"业务方向""回报""投入产出"。【ADR，中文用语统一】

### 3.1 字段

| 字段 | 类型 | 含义 | 必填 |
|---|---|---|---|
| id | uuid | | 是 |
| name | string | 业务名称 | 是 |
| templateType | enum(software / xhs / douyin / custom) | 业务模板 | 是 |
| opportunity | text | 机会描述 | 是 |
| targetOutcome | text | 第一阶段要证明的结果 | 是 |
| timeboxDays | enum(30 / 60 / 90) | 时间盒 | 是 |
| evidenceRoute | enum(5 项，见下) | 外部反馈路径 | 是 |
| lifecycleStatus | enum | 生命周期，见 3.2 | 是 |
| verificationStatus | enum(EvidenceGrade) | 验证结论 | 是 |
| currentCycle | int | 责任周期序号 | 否 |
| createdAt / updatedAt | ts | | 是 |

`evidenceRoute` 五个枚举【原型，逐字】：CEO验收+产品使用反馈 / 客户合同签署+收款记录 / 产品使用数据API / 手动周报+客户访谈 / 第三方平台数据导入。

### 3.2 状态机

原型把"生命周期"和"验证结论"混在一个 pill 里显示（同时出现 `continue/scale/pause/close` 和 `operating/verified/pending`），造成语义重叠。

**【补齐】拆成两个正交维度**：

**维度一 · lifecycleStatus**

| 值 | 界面文案 |
|---|---|
| DRAFT | 草稿 |
| PENDING_APPROVAL | 待批准团队配置 |
| ACTIVE | 验证中 |
| SCALING | 扩大中 |
| PAUSED | 已暂停 |
| ARCHIVED | 已归档（唯一终态） |

**维度二 · verificationStatus**：复用 1.4 的 `EvidenceGrade`。

### 3.3 流转表

| 从 | 到 | 触发条件 | 触发者 |
|---|---|---|---|
| — | DRAFT | 填写创业简报 | CEO |
| DRAFT | PENDING_APPROVAL | 4 个必填字段完成 + AI 团队配置完成 | CEO |
| PENDING_APPROVAL | ACTIVE | 勾选"批准团队配置，授权 AI 员工在各自责任范围内自主执行并汇报" **且**启动检查通过 | CEO |
| ACTIVE | ACTIVE (cycle+1) | 结果回传后选择"继续验证" | CEO |
| ACTIVE | SCALING | **仅当 verificationStatus = VERIFIED** 才允许 | CEO |
| ACTIVE / SCALING | PAUSED | 选择"暂停复盘" | CEO |
| PAUSED | ACTIVE | 复盘后重启 | CEO |
| 任意 | ARCHIVED | 选择"关闭" | CEO |

**失败路径**
- `verificationStatus = ABNORMAL` → 冻结 `→ SCALING` 通道，进异常队列并升级 CEO。【原型】
- 无平台授权 → 阻断 API 读取，提供"手动补录"通道，结果标 `UNVERIFIED`。【原型】
- 验收未通过 → "保留证据并生成返工与下一周期决策"。【原型，逐字】
- 时间盒到期未达成 → **【补齐】** 不自动关闭，生成"时间盒到期"决策事项升级 CEO，由 CEO 选择继续/暂停/关闭。

**未勾选授权则启动按钮禁用**——这是硬门禁，不是提示。【原型】

### 3.4 验收场景

- **正常**：创建业务 → 配置团队 → 勾选授权 → 启动 → 首个周期跑完 → 结果 VERIFIED → 扩大。
- **失败路径（必测）**：结果 ABNORMAL → "扩大业务"按钮不可用且给出原因 → 进异常队列 → CEO 处理后可选继续验证。
- **失败路径（必测）**：未勾选授权 → 启动被拒绝。

---

## 4. Commitment（承诺）

> 某部门/AI 团队对某条业务方向作出的、有回报口径的责任约定。
> 产品意义：CEO 缺资源时想知道的不是"哪些任务延期"，而是"我答应了谁什么、哪些必须保住"。

### 4.1 字段

| 字段 | 类型 | 含义 | 必填 |
|---|---|---|---|
| id | uuid | | 是 |
| businessId | fk | 所属业务方向 | 是 |
| departmentId / departmentName | fk / string | 承诺方 | 是 |
| name | string | 承诺名 | 是 |
| targetOutcome | text | 要证明什么 | 是 |
| status | enum | 见 4.2 | 是 |
| cycle | int | 当前责任周期 | 是 |
| workspaceId | fk | 落地的工作空间 | 否 |
| capacityContract | json | 见 1.5 | 是 |
| lastReportedAt | ts | 最近一次回报 | 否 |

### 4.2 状态机【原型】

| 值 | 界面文案 |
|---|---|
| PENDING | 待接受 |
| ACTIVE | 运行中 |
| PENDING_REVISION | 待调整 |
| PAUSED | 已暂停 |
| FULFILLED | 已完成 |【补齐】
| RELEASED | 已解除 |【补齐】

原型只有前四态，没有正常收尾的终态——承诺只能被暂停，不能被"完成"。补 `FULFILLED` / `RELEASED` 两个终态。

### 4.3 流转表

| 从 | 到 | 触发条件 | 触发者 |
|---|---|---|---|
| — | PENDING | 创建业务时生成部门承诺 | CEO |
| PENDING | ACTIVE | 部门回报第一条真实结果 | AI_EMPLOYEE |
| ACTIVE | ACTIVE (cycle+1) | CEO 选择"继续运行" | CEO |
| ACTIVE | PENDING_REVISION | CEO 选择"调整责任" → 回 Studio 改蓝图 | CEO |
| PENDING_REVISION | ACTIVE | 蓝图改完并通过模拟与审批 | CEO |
| ACTIVE | PAUSED | CEO 选择"暂停这项责任"，**保留证据、释放资源** | CEO |
| PAUSED | ACTIVE | 重启 | CEO |
| ACTIVE | FULFILLED | 目标结果达成且 verificationStatus = VERIFIED | CEO |【补齐】
| 任意 | RELEASED | 所属业务方向 ARCHIVED | SYSTEM |【补齐】

**失败路径**：承诺下的运行连续失败 → 按 `queuePolicy` 处理（如"失败即暂停" → 承诺转 PAUSED 并升级）。【原型】

### 4.4 验收场景

- **正常**：创建承诺 → AI 回报首条结果转 ACTIVE → 周期推进 → 达成后 FULFILLED。
- **失败路径（必测）**：研发工作台下运行失败 → queuePolicy=失败即暂停 → 承诺自动 PAUSED + 异常队列出现条目 + CEO 桌面可见。
- **失败路径（必测）**：CEO 调整责任 → 承诺进 PENDING_REVISION → **未通过模拟前不得回到 ACTIVE**。

---

## 5. Workspace / Blueprint / Stage

> Curis 最大的产品差异点。不是"有一个运行空间"，而是"能把陌生业务装修成可运行、可模拟、可交付的空间"。

### 5.1 最重要的架构结论：这是一个引擎，不是三套产品

原型的四个 runtime 页面（短视频 / 小红书 / 软件研发 / 部门型）经比对，**是同一引擎的四份配置**：

- 原型演示通常呈现 **9 个渲染节点**，其中 `Produce` 被拆成多个业务阶段；它们共享同一组语义槽位；
- 同一段渲染代码 + 同一个阶段弹窗驱动三个页面；
- 页面 DOM 阶段数不足时会**按定义自动补建节点**——典型引擎行为；
- 部门型页面全是占位 id，即"未装修的通用 Workspace"。

**通用语义槽位骨架**【原型 + 补齐】：

引擎固定的是 **8 个语义槽位**，不是固定 9 张卡片。`Produce` 允许按业务拆成 1～N 个连续 Stage，因此某个业务可以渲染 8、9 或更多节点；节点数量变化不能改变状态门禁、责任链或证据语法。

```
Intake 意图/选题 → Produce 生产（1~N 个 Stage） → Deliver 交付/发布
→ Collect 结果回收 → Accept CEO验收 → Review 复盘
→ Improve 提升 → Archive 归档
```

| 槽位 | 抖音 / TikTok 运营工作台 | 小红书运营工作台 | 研发工作台 | 通用工作台配置 |
|---|---|---|---|---|
| Intake | 选题 | 信息搜集 | 意图 | 承接 |
| Produce | 脚本 / 拍摄 / 剪辑 | 拆解 / 分析 / 产出 | 产品 / 研发 / QA | 执行 |
| Deliver | 发布 | 待发布 | CEO 验收 | 验收 |
| Collect | 数据 | 数据 | 反馈 | 回收 |
| Review | 复盘 | 复盘 | 下一周期 | 下一步 |
| Improve | 提升 | 提升 | — | — |
| Archive | 归档 | 归档 | 归档 | — |

**实现要求**：必须实现为"通用引擎 + 配置数据"，**严禁为每个业务写一套页面或一套后端逻辑**。业务差异只允许存在于配置里。

### 5.2 Stage 五元组 + 失败出口【原型】

每个 Stage 是一个结构化定义，不是一段文案：

```
Stage {
  slot:        enum(INTAKE|PRODUCE|DELIVER|COLLECT|ACCEPT|REVIEW|IMPROVE|ARCHIVE)
  name:        string          // 业务自定义显示名，如"选题"
  owner:       { type: AI_EMPLOYEE | CEO, ref: id }
  inputs:      string[]        // 如「平台热点、竞品选题、CEO 意图」
  outputs:     string[]        // 如「候选选题池（含置信度）」
  evidence:    string[]        // 如「抖音/小红书 API 数据」
  humanGate:   enum(AUTO | CEO_CHECKPOINT | CEO_REQUIRED)
  failureExit: { condition: string, action: enum, target?: stageSlot }
  escalation:  见 1.2
}
```

原型给出的失败出口样例，全部要能被上面结构表达【原型，逐字】：

| 环节 | 失败出口 |
|---|---|
| 信号 | 外部授权缺失 → 转人工录入 |
| 发布 | 平台授权过期 → 暂停并通知 CEO |
| 数据 | 数据延迟 → 标记 `evidenceCondition=STALE` |
| 决策 | CEO 拒绝 → 返回选题池 |
| CEO 验收 | 退回修改 → 回到"研发"阶段 |

### 5.3 Blueprint 校验规则（硬门禁）【原型】

蓝图必须通过三条校验才允许提交：

1. **Owner 已分配至每个节点**
2. **Input-Output 已明确**
3. **失败出口已配置**

配置检查另有四类告警：`gap`（外部授权未配置）、`overload`（员工容量告警，如 85% > 建议 70%）、`risk`（缺少 CEO 手动反馈入口）、`passed`。

### 5.4 Workspace 生命周期与三级门禁

**装修流水线八步**【原型】：
`Discover → Blueprint → Compose → Bind → Staff → Simulate → Approve → Operate`

**状态机**：

| 值 | 界面文案 |
|---|---|
| DRAFT | 草稿 · 未命名 |
| BLUEPRINTING | 装修中 |
| SIMULATED | 模拟已通过，可提交审批 |
| PENDING_APPROVAL | 待审批 |
| OPERATING | 运行中 |
| PAUSED | 已暂停 |
| ARCHIVED | 已归档 |

**三级门禁（提交审批前依次校验，任一不过即拒绝）**【原型，逐字顺序】：
1. `!issuesResolved` → "请先修复配置问题"
2. `!simulationPassed` → "请先运行模拟"
3. 外部 Agent 未审阅 → "请先审阅已导入的外部 Agent"

**模拟场景必须覆盖四条**【原型】：`正常路径 / 能力缺席（CEO 离线 7 天）/ 外部延迟 / CEO 拒绝`。

**门禁失效规则（关键）**【原型】：任何一次蓝图修改（加模块、复用工作流、删节点、导入 Agent）都会把 `issuesResolved` 与 `simulationPassed` 重置为 false，**必须重新模拟**。

**审批四选项**【原型】：`批准并启动` / `延后 3 天` / `要求修改（退回 Studio）` / `拒绝并保留草案`。
注意：拒绝**不删除草案**，回退到装修态并保留。

**蓝图版本子状态机**【原型】：运行中修改蓝图 → 产生 `draftVersion`（v0.3）与 `activeVersion`（v1.0）并存 → 提示"受影响周期：N 个" → 审批通过后升版。决策批准带 **14 天回滚窗**。

### 5.5 Workspace 与 AI 员工

- 岗位（Role Slot）与员工（Agent）是**两个独立节点类型，解耦**。【原型】
- 能力绑定粒度是 **"空间 × 环节"**，不是"员工"。原型原话："切换只影响当前步骤，输入、上下文和已有成果会保留"。【原型】
- 同一员工可跨空间，在不同空间可有不同能力组合。【原型】
- 可配字段：`model / agent / skills[] / tools[] / connector / knowledgeScope`。

### 5.6 验收场景

- **正常**：新建空间 → 配置 8 个语义槽位（`Produce` 可拆成 1～N 个 Stage）→ 绑定员工与工具 → 正常 / 缺能力 / 工具失败 / 外部延迟 / CEO 拒绝等必需场景模拟通过 → 提交审批 → 批准 → 进入运行。
- **失败路径（必测）**：蓝图缺一个 Owner → 提交被拒并明确指出缺哪个节点。
- **失败路径（必测）**：模拟通过后再改一个节点 → 提交按钮重新变为不可用，提示需重新模拟。
- **失败路径（必测）**：审批选"要求修改" → 空间回 BLUEPRINTING 且草案完整保留。
- **必测**：同一引擎加载两份不同业务配置，均能正确渲染与推进，无业务专属分支代码。

### 5.7 三业务并行验证边界

三类工作台共享以下运行约束：

- `businessId`、`workspaceId`、`runId`、`outcomeId` 必须可回溯；
- CEO Assistant、AI 组织、能力授权、升级、Evidence、Acceptance 和 Decision 使用同一套运行时；
- 业务差异只通过 Workspace Blueprint、Stage 配置、外部连接器和 Evidence Route 表达；
- 不允许为研发、小红书、抖音分别复制页面、状态机或后端服务；
- 不允许用固定模板数据代替 CEO 创建、授权和真实运行结果。

三条业务的首个验证场景分别为：

| 工作台 | 首个验证场景 | 必须形成的外部结果 |
| --- | --- | --- |
| 研发工作台 | 第一个真实研发任务：Curis 的自研发（完善 Curis） | 可使用的软件增量、代码/构建/测试/CEO 验收证据 |
| 小红书运营工作台 | 从选题到发布再到数据回流 | 平台授权数据，或 CEO 手动录入并标记待验证 |
| 抖音 / TikTok 运营工作台 | 从选题到发布再到数据回流 | 播放/互动/粉丝/成交等平台数据，或 CEO 手动录入并标记待验证 |

### 5.7.1 内容运营 Workspace Studio：把办公室装修出来

内容工作台不能由一张“新增 Agent”表单生成。CEO 或 Business Engineering 必须先定义业务结果，
再把平台、岗位、能力、授权、节奏和证据装配成一间可模拟的运营办公室：

```text
定义内容 Outcome / 目标受众
→ 选择平台与账号（小红书 / 抖音 / TikTok）
→ 设计 ContentIntent 与平台变体规则
→ 配置岗位：研究 / 创作 / 发布 / 互动 / 复盘
→ 绑定 Agent、Capability、Tool、Knowledge、Connector
→ 配置 CEO 审核门禁、ReplyPolicy、Evidence Route 和结果窗口
→ 设置 Cadence 与升级条件
→ 模拟正常、未授权、适配失败、互动风险和外部数据延迟
→ CEO 审批并交付 Runtime
```

内容 Workspace Blueprint 至少保存：

| 配置组 | 必须配置 | 没有它会发生什么 |
|---|---|---|
| Outcome | 本周期目标、外部结果、验收口径 | 只能生产内容，无法判断是否值得继续 |
| Platform | 平台、账号、格式约束、授权范围 | 内容可能无法发布或错误跨平台复制 |
| Role Slot | 研究、创作、发布、互动、复盘的 Owner | Agent 平级运行，责任和交接丢失 |
| Safety | CEO 审核点、`ReplyPolicy`、敏感 / 承诺规则 | AI 可能越权回复或发布 |
| Evidence | 来源、回执、结果窗口、手动补录口径 | 互动和指标无法成为经营事实 |
| Cadence | 触发事件、检查点、超时和升级 | CEO 不知道何时需要介入 |

Studio 的页面不是 Agent 目录，而是“业务空间装修台”：左侧是 Outcome / 平台 / 约束，中间是
阶段与输入输出画布，右侧是岗位与能力配置，底部是模拟结果、缺口和审批门。任何配置变化都
必须使 `simulationPassed=false`，不能静默改变正在运行的办公室。

### 5.7.1 Cycle Runtime Contract

`Cycle` 是业务在 Workspace 中兑现一次 Outcome / Commitment 的最小经营周期。它不是 Project，也不是一组 Task；Project、Task、Workflow 只能作为 Cycle 内部执行载体。

**最小字段：**

```text
cycleId / companyId / businessId / workspaceId / outcomeId / commitmentId
blueprintVersion / sequence / intentRef / status / exceptionStatus / currentStage / ownerRefs[]
startedAt / dueAt / completedAt / evidenceRefs[] / acceptanceId / nextCheckAt
```

**生命周期：**

```text
PLANNED → READY → RUNNING → WAITING_CEO → ACCEPTED → REVIEWING → CLOSED
                              └──────────→ REJECTED → PLANNED（新修订）
                              └──────────→ PAUSED / FAILED
```

`PAUSED`、`FAILED` 是 Cycle 的生命周期状态；`STALE`、`ABNORMAL`、`WAITING_CEO`、`BLOCKED` 是独立的 `exceptionStatus`，不得被当作“已完成”。只有 `status=ACCEPTED` 且形成复盘输出后才能进入 `CLOSED`；关闭后仍保留证据、Decision、学习和下一周期引用。

`Cycle.exceptionStatus` 允许值：`NONE | WAITING_CEO | BLOCKED | FAILED | STALE | ABNORMAL | ESCALATED`。异常解决只能通过显式恢复命令清除，并必须写入恢复人、时间、原因和证据；不得通过把 `status` 直接改成 `ACCEPTED` 来消除异常。

| 转换 | 必要条件 | 触发者 | 输出 |
|---|---|---|---|
| `PLANNED → READY` | Outcome、Owner、Blueprint Version、验收标准和能力检查齐全 | CEO / SYSTEM | 启动包与责任交接 |
| `READY → RUNNING` | CEO 已批准启动且授权有效 | CEO | Cycle 开始事件 |
| `RUNNING → WAITING_CEO` | 进入审核、外部承诺、权限或异常门禁 | AI / SYSTEM | DecisionPacket / Handoff |
| `RUNNING → PAUSED / FAILED` | 能力、工具、构建、平台或数据失败 | AI / SYSTEM | FailureEvent 与恢复命令 |
| `WAITING_CEO → ACCEPTED` | Acceptance 条件满足且 CEO 确认 | CEO | Acceptance、下一周期候选 |
| `WAITING_CEO → REJECTED` | CEO 退回并给出原因 | CEO | 修订范围、新 Cycle 或关闭决定 |
| `ACCEPTED → REVIEWING → CLOSED` | 复盘完成、证据归档、下一步已明确 | AI + CEO | Insight、Archive、Decision |

每次转换都必须写入统一审计，并与 Stage、Handoff、Outcome 和 Acceptance 关联。研发工作台的“完善 Curis”、小红书的一轮内容发布、抖音的一轮视频发布都必须各自产生自己的 `cycleId`。

### 5.7.2 研发工作台 Stage Runtime Contract

研发工作台不能只复用旧的 `workflow_runs / workflow_steps`。那些表是执行载体，不足以表达 CEO 意图、研发责任、真实工程证据和 CEO 验收。因此研发工作台也必须有完整的业务 Stage：

| Stage | Page / Surface | Entry State 与 Input | Owner | Runtime Action | Durable Output / Exit | Exception / Next Stage | Audit |
|---|---|---|---|---|---|---|---|
| INTAKE | CEO Desk · Assistant 意图收件 | CEO 提出“完善 Curis”等意图；目标、范围、验收问题 | CEO Assistant | 澄清目标、识别影响范围、形成有限研发意图 | `intentId`、验收标准、影响范围；进入 DESIGN | 信息不清 → `WAITING_CEO`；越权范围 → 退回澄清 | `intentId / actor / at / source / clarificationRefs` |
| DESIGN | 研发办公室 · 方案与周期 | `intentId`；现状、约束、知识、历史 Decision | 产品 AI / 技术负责人 AI | 拆解方案、接口边界、风险、测试策略和 Cycle | `cycleId`、实现计划、验收清单；进入 IMPLEMENT | 风险未解决 / 能力缺失 → `BLOCKED` 并升级 Assistant | `cycleId / owner / inputs / planVersion / nextCheckAt` |
| IMPLEMENT | 研发办公室 · 执行现场 | 已批准 Cycle；代码范围、工具授权、实现计划 | 工程 AI | 在允许路径内修改代码，产生可复现构建输入 | commit / diff / artifact；进入 VERIFY | 工具失败、路径越界、凭据缺失 → `PAUSED`；不报告完成 | `commitRef / actor / toolRefs / changedPaths / at` |
| VERIFY | 研发办公室 · 验证区 | commit / build 输入；测试清单、真实用户流程 | QA AI | 运行构建、单测、集成和真实用户流程，记录失败 | build / test / browser evidence；进入 ACCEPT | 任一关键验证失败 → `PAUSED`；保留错误和重试 | `testRunId / commands / results / evidenceRefs / at` |
| ACCEPT | CEO Desk · 研发验收抽屉 | 验证证据、变更摘要、已知缺口、影响范围 | CEO | 使用真实增量，确认是否符合验收标准 | CEO acceptance / reject Decision；进入 REVIEW 或回到 DESIGN | CEO 拒绝 → 新 Cycle；证据不足 → `WAITING_CEO` | `decisionId / approver / decidedAt / reason / evidenceIds` |
| REVIEW | CEO Desk · 结果与复盘 | acceptance、使用反馈、失败记录、版本差异 | 复盘 AI | 区分事实与假设，形成产品 / 技术 Insight | `insightId`、下一周期建议；进入 IMPROVE 或 ARCHIVE | 使用反馈冲突 → 升级 CEO；不得自报 VERIFIED | `insightId / citations / confidence / actor / at` |
| IMPROVE | Workspace Studio / Decision | `insightId`；CEO 决策及影响分析 | CEO + 产品 AI | 调整研发蓝图、能力、节奏或下一 Cycle | 新 Blueprint Draft / Cycle；重新模拟受影响范围 | 模拟未通过 → 保持草稿；不改运行版本 | `blueprintVersion / impactMap / simulationRunId / approver` |
| ARCHIVE | 研发办公室 · 周期归档 | Cycle 已验收或 CEO 关闭；证据完整 | Workspace AI | 固化代码、构建、测试、验收和复盘引用 | 只读 Cycle Archive；释放责任 | 证据缺失 → 带缺口归档，不删除 | `archiveId / archivedAt / retention / references` |

研发工作台第一个 Cycle 的 `intentId` 必须指向“Curis 的自研发”，工作项名为“完善 Curis”；这只是第一个真实研发任务，不改变业务名称“研发工作台”。

### 5.8 内容发布工作台：把外部参考转译成 Curis 运行契约

对 Buffer、Hootsuite、Predis、Later 等内容产品的公开机制做了对照。它们共同证明了四件事：

1. 内容 AI 必须理解平台语境，而不是只生成一段通用文案；
2. 内容从草稿到发布必须有明确的责任、审核和状态；
3. 内容日历 / 队列是运行节奏的投影，不是业务本身；
4. 发布之后的真实平台结果必须回到下一轮选题与决策。

这些是参考证据，不是 Curis 的第二套产品定义。Curis 只吸收运行机制，不复制外部产品的后台布局。研究来源：
[Buffer AI Assistant](https://support.buffer.com/article/583-using-buffers-ai-assistant)、[Hootsuite AI](https://www.hootsuite.com/platform/ai)、[Predis 内容日历](https://help.predis.ai/en/article/how-to-use-the-content-calendar-on-predisai-qmb83y/)、[Later 团队审批](https://later.com/blog/social-media-management-for-teams/)。

#### 5.8.1 内容业务的统一 Stage 配置

小红书与抖音共享以下 Stage 顺序，差异只能通过配置表达：

| Stage | 小红书运营工作台 | 抖音 / TikTok 运营工作台 | 默认 Owner | CEO 门禁 |
|---|---|---|---|---|
| INTAKE | 用户问题、搜索词、热点与历史表现 | 热点、用户场景、账号目标与历史表现 | 选题研究 AI | 选题方向不明确时 |
| PRODUCE | 笔记结构、标题、图文 / 轮播素材 | 脚本、分镜、拍摄 / 剪辑素材与封面 | 内容创作 AI | 需要改变业务口径时 |
| DELIVER | 笔记预览、账号与发布时间 | 视频预览、账号、发布时间与发布权限 | 发布执行 AI | ALWAYS_BEFORE_PUBLISH |
| COLLECT | 浏览、点赞、收藏、评论、关注 | 播放、完播、互动、涨粉、成交 | 数据回收 AI | API 失败或数据冲突时 |
| ACCEPT | CEO 确认内容是否符合承诺 | CEO 确认内容与外部承诺是否兑现 | CEO | 未达到验收标准时 |
| REVIEW | 哪类主题、结构、表达带来有效反馈 | 哪个钩子、节奏、素材带来有效反馈 | 数据复盘 AI | 结论影响下一周期资源时 |
| IMPROVE | 更新选题规则、表达模板与发布时间 | 更新脚本规则、素材策略与发布节奏 | 内容策略 AI | 修改工作台蓝图时 |
| ARCHIVE | 保留内容、证据、复盘和引用 | 保留视频、证据、复盘和引用 | Workspace AI | 无 |

#### 5.8.1.1 内容发布 Stage Runtime Contract

按 ADR-0041，每个内容阶段必须有可验证的工作面、输入、输出、Owner、异常出口和审计记录。平台差异只改变输入约束和产出格式，不改变阶段责任与回到 CEO 的路径。

| Stage | Page / Surface | Entry State 与 Input | Owner | Runtime Action | Durable Output / Exit | Exception / Next Stage | Audit |
|---|---|---|---|---|---|---|---|
| INTAKE | 运营办公室 · 外部信号摘要 / 选题池 | `IDEA`；平台信号、用户问题、历史结果、来源 | 选题研究 AI | 采集、去重、判断来源新鲜度，形成候选选题 | 带来源和置信度的 `ContentIntent`；进入 `PRODUCE` 或等待 CEO | 来源冲突 / 过期 → `WAITING_CEO`；否则进入 `PRODUCE` | `contentId / source / actor / at / confidence / nextCheckAt` |
| PRODUCE | 运营办公室 · 内容队列 / 版本抽屉 | `DRAFT`；已接受的 `ContentIntent`、平台约束、知识范围 | 内容创作 AI | 生成平台变体、素材清单、事实与未知标记 | 新 `versionId` 与 `platformVariant`；提交 `IN_REVIEW` | 能力缺失 / 格式不合规 → `INVALID` 并回到 `DRAFT` | `versionId / platformVariant / author / createdAt / constraintsCheck` |
| DELIVER | 内容详情抽屉 · 发布权限区 | `APPROVED` 或 `SCHEDULED`；不可变批准版本、账号授权、发布时间 | 发布执行 AI（已授权）或 CEO | 校验权限、排期、执行发布并接收平台回执 | `ScheduledRun`、外部发布 ID、`publishedVersionId`；进入 `PUBLISHED` | 未授权 → `WAITING_CEO`；失败 / 超时 → `FAILED`；成功 → `PUBLISHED` | `runId / actor / connector / externalReceipt / at / retryCount` |
| COLLECT | 运营办公室 · 外部结果 / Assistant 事项 | `PUBLISHED`；发布回执、结果窗口、平台 API 或 CEO 手动数据 | 数据回收 AI | 在窗口内回收原始指标，标记验证等级和证据新鲜度 | `Outcome` / `Evidence`；进入 `AWAITING_FEEDBACK`、`ACCEPT` 或异常状态 | API 缺失 → `evidenceCondition=STALE`；来源冲突 → `verificationStatus=ABNORMAL + evidenceCondition=CONFLICT`；不得伪装 `VERIFIED` | `outcomeId / source / window / freshness / verificationStatus / evidenceCondition / actor` |
| ACCEPT | CEO Desk / 内容审核抽屉 | `AWAITING_FEEDBACK`；结果、证据、承诺影响和版本差异 | CEO | 确认外部结果是否兑现本周期承诺 | `Acceptance` 与继续 / 调整 / 暂停 Decision；进入 `REVIEW` | 未达标准、承诺风险或证据不足 → `PAUSED` / `WAITING_CEO` | `decisionId / approver / decidedAt / reason / evidenceIds` |
| REVIEW | 运营办公室 · 复盘面板 | `REVIEWED` 前；已验收结果、互动反馈、版本历史 | 数据复盘 AI | 解释变化、区分事实与假设，提出下一轮建议 | `Insight` 与下一轮候选动作；进入 `IMPROVE` 或 `ARCHIVE` | 结论冲突 → 升级 CEO；无可靠证据 → 保持 `UNVERIFIED` | `insightId / inputs / citations / confidence / actor / at` |
| IMPROVE | Workspace Studio / Decision Room | `Insight` 已形成；CEO 决策范围和影响分析 | 内容策略 AI + CEO | 修改选题规则、平台约束、Cadence 或岗位能力 | 新 Blueprint Draft；重新进入 `BLUEPRINTING` 和全量 Simulation | 影响未评估 / 模拟未通过 → 保持草稿，不改 Runtime | `blueprintVersion / impactMap / simulationRunId / approver` |
| ARCHIVE | 内容详情 · 归档与知识引用 | 已完成复盘或 CEO 关闭；全部证据和版本齐全 | Workspace AI | 固化内容、版本、回执、复盘和引用，释放运行责任 | 只读归档；生命周期终态 `ARCHIVED` | 证据未完整 → 标记缺口后归档，不删除历史 | `archiveId / archivedAt / actor / retention / references` |

#### 5.8.2 内容对象状态机

每一条内容必须是可追踪的 `ContentItem`，不能只存在于聊天记录或日历格子中：

```text
IDEA → DRAFT → IN_REVIEW → APPROVED → SCHEDULED → PUBLISHED
     → AWAITING_FEEDBACK → REVIEWED → CARRIED_FORWARD / ARCHIVED
```

每次流转必须记录 `contentId / workspaceId / stage / owner / evidence / actor / at / nextCheckAt`。
`APPROVED` 不等于 `PUBLISHED`；平台授权失败、发布失败和数据延迟都必须进入显式失败出口。
这里的 `APPROVED` 是“内容发布前审核通过”，而 5.8.1 的 `ACCEPT` 是“外部结果经 CEO 验收”；两者不能合并成一个“已完成”状态。

内容生命周期、验证等级和证据新鲜度是三个正交维度：CEO 手动发布可以让生命周期进入 `PUBLISHED`，但证据仍必须标为 `verificationStatus=UNVERIFIED`；连接器回执或 CEO 真实验收后，且证据仍新鲜，才可将验证等级升级为 `VERIFIED`。界面显示为“已发布 · 待验证”，不得显示为已验证价值。

**异常状态不得偷偷扩展生命周期。** `ContentItem.lifecycleStatus` 只使用上面的正常生命周期；另设 `exceptionStatus`（可为空）记录运行异常：

```text
NONE | INVALID | WAITING_CEO | FAILED | STALE | ABNORMAL | ESCALATED
```

例如：授权缺失时保持 `lifecycleStatus=APPROVED`、`exceptionStatus=WAITING_CEO`；发布失败时保持
`lifecycleStatus=SCHEDULED`、`exceptionStatus=FAILED`；数据延迟时保持 `lifecycleStatus=AWAITING_FEEDBACK`、
`exceptionStatus=STALE`。异常解决后只能通过显式命令清除，并留下恢复审计；不能把异常直接改写成成功态。

#### 5.8.2.0 版本、审核意见与批准审计

`ContentItem` 必须同时保存 `versionId / platformVariant / author / createdAt`，并保存绑定到具体版本的
`reviewComments[]`、`reviewer`、`approver`、`decision`、`decidedAt` 和 `publishedVersionId`。审核意见不能漂浮在
聊天、邮件或独立任务中；每条意见至少包含 `actor / at / category（事实、观点、品牌、风险）/ text / resolved`。

一个内容意图可以产生多个平台变体，但平台变体不是同一篇内容的复制品：

```text
ContentIntent
├── XHS Variant：图文 / 轮播 / 标题 / 搜索表达 / 封面
└── TikTok Variant：脚本 / 分镜 / 视频比例 / 时长 / 钩子 / 封面
```

每个 `platformVariant` 必须保存 `format / constraintsCheck / preview / versionId /
variantStatus`。`variantStatus` 至少包含 `MISSING / INVALID / READY / APPROVED / PUBLISHED`。
一个平台变体的 CEO 批准不会自动批准另一个平台变体；任一平台的格式、长度、敏感表达、
封面或外部承诺发生变化，都必须重新生成该平台版本并重新审核。

- 选题研究 AI、内容创作 AI 可以对版本提出意见和修改建议，但不能成为发布批准者。
- CEO 是当前唯一的发布批准者；`APPROVED` 必须指向一个不可变的版本。
- 已批准版本发生任何内容、素材、平台适配或外部承诺变化时，必须创建新版本并回到 `DRAFT` 或 `IN_REVIEW`，不能原地覆盖。
- 发布回执必须记录实际发布的 `publishedVersionId`，让 CEO 能确认“批准的版本”和“平台实际发布的版本”一致。

#### 5.8.2.0.1 Content Runtime 最小持久化契约

以下是进入 Runtime Foundation Issue 前必须冻结的最小对象边界。它不是数据库实现方案，但每个字段都必须有可查询的持久化事实；JSON 快照只能作为内容载荷或外部原始回执，不能代替状态、版本和责任关系。

| 对象 | 必须字段 | 不变量 |
|---|---|---|
| `ContentItem` | `contentId / companyId / workspaceId / outcomeId / intentId / platform / lifecycleStatus / ownerRole / currentVersionId / approvedVersionId / publishedVersionId / verificationStatus / evidenceCondition / nextCheckAt / createdAt / updatedAt` | 一个内容只属于一个 Company / Workspace；`approvedVersionId` 和 `publishedVersionId` 必须指向不可变版本；状态转换只能通过 Runtime；删除只能归档 |
| `ContentVersion` | `versionId / contentId / platformVariant / payloadRef / author / createdAt / constraintsCheck / versionStatus` | 正文、素材、平台适配或外部承诺变化必须创建新版本；已批准版本不可原地修改；不同平台必须拥有独立版本 |
| `ContentReview` | `reviewId / contentId / versionId / reviewer / decision / reviewComments[] / decidedAt` | 意见必须绑定具体版本；CEO 是当前唯一发布批准人；拒绝不能覆盖旧记录 |
| `PublicationReceipt` | `receiptId / contentId / runId / platform / approvedVersionId / publishedVersionId / externalId / status / source / receivedAt / rawRef` | 回执是追加记录；批准版本与实际发布版本不一致时运行失败并升级 CEO；无回执不得显示为平台已发布 |
| `InteractionItem` | `interactionId / companyId / workspaceId / contentId / platform / source / externalId / receivedAt / lifecycleStatus / intent / sensitivity / replyPolicy / responseVersion / evidenceRef / nextCheckAt` | 互动必须绑定内容或明确标记为未归属；回复策略由 Workspace 配置决定，不能由 Agent 临时改变；高风险互动不可自动响应 |
| `InteractionResponse` | `responseVersion / interactionId / renderedTextHash / author / ceoDecision / decidedAt / externalReceipt / sentAt` | 每次修改回复都生成新版本；涉及承诺、报价、投诉、隐私或合作时必须有 CEO 决策；外部回执缺失时不得进入 `RESPONDED` |

所有对象都必须带 `tenant / company / workspace` 范围并关联统一审计：
`stateTransitionId / actor / at / reason / evidenceRefs / nextCheckAt`。现有 `content_publish_packages` 可以作为发布包载荷来源，但不能直接充当 `ContentItem`、`ContentVersion` 或 `PublicationReceipt`。

#### 5.8.2.0.2 Studio 版本与模拟失效不变量

1. Workspace 运行必须引用不可变的 `blueprintVersion`；草稿编辑不得静默修改正在运行的版本。
2. 修改 Stage、Agent、Capability、Connector、平台变体约束、ReplyPolicy 或 Evidence Rule 时，必须创建新的 Blueprint Draft，并将 `simulationPassed` 置为 `false`。
3. 只有完整 SimulationRun 通过后，Draft 才能进入 `SIMULATED`；只有 CEO 批准后才能生成新的 Operating Version。
4. 任何运行对象必须能反查其 `blueprintVersion`；运行中修改草稿不能改变既有 ContentItem、InteractionItem 或 ScheduledRun 的责任和规则。
5. 归档保留版本、回执、互动、证据和 CEO 决策；归档不是物理删除。

#### 5.8.2.1 状态动作与权限矩阵

| ContentItem 状态 | 合法动作 | 允许执行者 | 禁止行为 |
|---|---|---|---|
| `IDEA` | 查看来源、接受选题、退回补证据 | 选题研究 AI、CEO | 直接发布、直接排期 |
| `DRAFT` | 继续创作、提交审核、退回选题 | 内容创作 AI、CEO | 未提交审核即发布 |
| `IN_REVIEW` | 批准、退回并填写原因、请求补证据 | CEO；Assistant 只能准备材料 | AI 自动批准、拖拽进入发布 |
| `APPROVED` | 连接器排期、授权后发布、CEO 手动发布 | 发布执行 AI（已授权）或 CEO | 无回执却显示已发布；再次修改内容不改版本 |
| `SCHEDULED` | 查看排期、取消排期、处理连接器失败 | 发布执行 AI、CEO | 拖回草稿或直接改成已发布 |
| `PUBLISHED` | 查看发布回执、等待结果窗口 | 系统、CEO | 手动改写平台结果；跳过结果窗口进入复盘 |
| `AWAITING_FEEDBACK` | 回收 API 数据、CEO 手动补录、标记 `evidenceCondition=STALE / CONFLICT` | 数据复盘 AI、CEO | 用估算值填充已验证结果 |
| `REVIEWED` | 形成下一轮 Decision、归档、复制为草案 | CEO、内容策略 AI | 直接覆盖历史证据或复盘结论 |

因此，卡片上不能再使用所有阶段共用的“移动至下一阶段”按钮。按钮必须由状态和角色共同生成，例如：`提交审核`、`批准发布`、`退回修改`、`排期`、`手动发布并录入证据`、`查看回执`、`补录结果`、`形成下一轮决策`。

#### 5.8.3 内容团队的责任分工

内容团队的汇报与授权关系不是平级 Agent 列表：

```text
CEO
└── CEO Assistant
    └── 内容策略 AI
        ├── 选题研究 AI
        ├── 内容创作 AI
        ├── 发布执行 AI
        ├── 互动回收 / 分流 AI
        └── 数据复盘 AI
            └── Workspace AI（在具体办公室执行岗位，可一人多岗）
```

CEO Assistant 负责排序、准备、升级和收束；内容策略 AI 负责把业务目标翻译成内容节奏与
平台策略；专业 Agent 承担具体岗位责任。第一版本可以由同一个 Workspace AI 承载多个岗位，
但岗位责任、容量和交接记录必须分开。

| 角色 | 对什么负责 | 何时升级 CEO Assistant |
|---|---|---|
| CEO Assistant | 汇报本周期承诺、排序队列、准备审核材料、收回结果 | 需要 CEO 审核、外部承诺将失守、结果异常或跨业务影响 |
| 选题研究 AI | 发现信号、形成候选选题并附来源与置信度 | 信号冲突、来源过期、需要改变业务方向 |
| 内容创作 AI | 产出平台适配内容与素材清单 | 缺少能力、无法满足内容标准、需要新工具 |
| 发布执行 AI | 校验账号 / 权限 / 时间并执行发布 | 缺授权、发布失败、涉及不可逆外部动作 |
| 数据复盘 AI | 回收原始数据、解释变化、形成下一轮建议 | 数据缺失、冲突、异常或建议扩大投入 |

第一版本可以由一个 Workspace AI 承载多个岗位，但运行记录必须按岗位责任分开，不能用“内容 AI 已完成”掩盖具体环节无人负责。

#### 5.8.3.1 Content Agent Role Contract

每个内容 Agent 都必须以“触发 → 输入 → 责任动作 → 输出 → 下一 Owner”的方式运行。Agent 的存在不是头像或聊天记录，而是一段可审计的责任契约。

| Agent / 岗位 | 触发 | 必须读取 | 责任动作 | 交付输出 | 可执行的外部动作 | 必须升级 |
|---|---|---|---|---|---|---|
| CEO Assistant | 新周期开始、审核窗口、异常、待决策或收束时间到达 | Company Context、当前承诺、队列、Evidence、历史 Decision | 排序、准备审核包、召集专业 Agent、提醒 CEO、收回结果 | Brief、Handoff、Decision 草案、下一检查点 | 不直接发布内容；仅在既有授权策略下调用低风险提醒 | 任何 CEO 审核、外部承诺、敏感互动、跨业务影响 |
| 内容策略 AI | CEO 批准业务目标、周期关闭或复盘产生新假设 | Outcome、受众、平台规则、历史结果、容量 | 把经营目标拆成内容节奏、平台策略和岗位责任 | ContentIntent、Cadence Draft、策略变更建议 | 不发布、不回复、不修改已运行 Blueprint | 目标改变、资源扩大、策略冲突或证据不足 |
| 选题研究 AI | 新外部信号、互动聚类、结果异常或 `INTAKE` 到达 | 平台信号、来源、时间、新鲜度、历史 ContentItem | 去重、核验来源、区分事实与假设，提出候选选题 | 带来源 / 置信度的 `IDEA` | 可抓取授权信号；不得自动承诺或发布 | 来源冲突 / 过期、信号需要改变业务方向 |
| 内容创作 AI | `IDEA` 被 CEO 接受或 `DRAFT` 被退回 | ContentIntent、平台约束、知识范围、模板版本、CEO 意见 | 生成平台变体、素材清单和版本差异，标注未知 | `versionId`、`platformVariant`、预览、`constraintsCheck` | 不可调用发布或外部回复动作 | 缺能力、无法满足标准、敏感表达或需要新工具 |
| 发布执行 AI | `APPROVED` / `SCHEDULED` 到达，或 CEO 手动发布请求 | 不可变批准版本、账号授权、排期、平台回执规则 | 检查权限、执行排期 / 发布、保存回执和失败原因 | `ScheduledRun`、外部发布 ID、`publishedVersionId` | 仅在授权且版本一致时发布；不改变内容正文 | 未授权、失败、超时、平台拒绝、版本不一致 |
| 互动回收 / 分流 AI | 新评论、私信、提及、咨询、订单意向或 API 异常 | 原文、来源、contentId、平台、历史回复、ReplyPolicy | 去重、分类意图与风险、绑定内容、决定是否生成回复草案 | `InteractionItem`、风险标签、`CLASSIFIED` / `WAITING_CEO` | 仅可按批准模板生成或发送低风险回复 | 潜在线索、投诉、敏感内容、承诺或模板越界 |
| 数据复盘 AI | `PUBLISHED` 结果窗口到达、互动结束或数据异常 | 原始指标、来源、时间窗、证据等级、CEO 验收 | 解释变化、区分相关与因果、形成下一轮建议 | `Outcome`、`Insight`、复盘草案 | 不得直接扩大投入或修改 Blueprint | 数据缺失 / 冲突、异常、建议扩大投入 |

每个内容岗位还必须有一个可被 CEO 读懂的运行状态投影，不新增平行员工系统：

| `presenceState` | 界面文案 | 运行含义 | CEO 可做的事 |
|---|---|---|---|
| `AVAILABLE` | 可承接 | 当前无阻塞，可接受下一条责任 | 查看容量或委派 |
| `RUNNING` | 工作中 | 正在处理指定 ContentItem / InteractionItem | 查看当前产出与检查点 |
| `WAITING_CEO` | 等待 CEO | 权限、审核、外部承诺或风险需要人决策 | 处理事项、退回或暂停 |
| `BLOCKED` | 被阻塞 | 能力、工具、容量或外部平台失败 | 查看原因、调配能力或升级 |
| `PAUSED` | 已暂停 | CEO 暂停岗位或所属业务方向 | 恢复、交接或关闭 |

运行投影至少显示 `role / currentResponsibility / activeItemIds / capacityPct /
lastHandoffAt / nextCheckAt / presenceState`。它是 Workspace Runtime 的事实投影，不是聊天状态；
Agent 之间的交接仍必须写入 `Handoff`，由 CEO Assistant 汇总到 CEO Desk。

#### 5.8.4 运行态界面契约

内容工作台不是“内容后台”，而是“运营办公室”：

```text
顶部：业务目标 / 当前周期 / 本周期承诺 / Assistant 状态
中部：内容生产队列（按状态与下一动作排列，不按项目文件夹排列）
右侧：按需打开 Assistant，上下文包含当前内容、来源、权限与审核原因
底部：发布结果、证据等级、复盘结论、下一周期动作
```

首屏必须先回答“本周期要创造什么结果”，再展示内容条目；内容条目必须同时显示当前状态、责任人、外部证据和下一检查点。日历只能作为节奏视图，不得取代运行队列与结果反馈。

#### 5.8.5 内容工作台 Simulation 门禁

除通用四场景外，内容工作台必须验证：

1. 正常：选题 → 创作 → CEO 审核 → 授权发布 → 结果回流 → 复盘；
2. 未授权：发布按钮不可用，转入 CEO 手动发布 / 手动结果录入；
3. 发布失败：内容保留在 `IN_REVIEW` 或 `SCHEDULED`，不得伪装为已发布；
4. 数据延迟 / 冲突：结果标记 `STALE` / `ABNORMAL`，不得支持扩大业务；
5. CEO 拒绝：内容返回 `DRAFT`，保留拒绝原因与下一检查点。

#### 5.8.6 互动与线索回流：不是第二个 CRM

评论、私信、提及、咨询和订单意向是内容发布后的外部反馈。它们不能只作为指标数字，
也不能膨胀成独立 CRM；它们是 `ContentItem` / `Outcome` 的子级 `InteractionItem`，
只在需要响应、验收或升级时进入 CEO Operating Day。

```text
CAPTURED → CLASSIFIED → DRAFTED → WAITING_CEO → RESPONDED
         → OUTCOME_TRACKING → CLOSED / ESCALATED
```

`InteractionItem` 至少记录：`interactionId / contentId / platform / source / receivedAt /
intent / sensitivity / evidence / responseVersion / actor / nextCheckAt`。

| Agent / 角色 | 责任 | 默认动作 | 必须升级 CEO 的情况 |
|---|---|---|---|
| 互动回收 AI | 抓取评论、私信、提及与平台回执，去重并绑定内容 | 形成 `CAPTURED`，标来源和新鲜度 | API 断开、重复或来源冲突 |
| 互动分流 AI | 判断问题、反馈、线索、投诉、风险和无效信息 | 进入 `CLASSIFIED`，给出意图与置信度 | 低置信度、敏感词、投诉、隐私或潜在线索 |
| 回复准备 AI | 按平台语境生成回复草案并引用内容事实 | 进入 `DRAFTED`，绑定 `responseVersion` | 涉及报价、承诺、退款、合作或品牌立场 |
| CEO Assistant / CEO | 汇报重要互动、批准高影响回复、跟进线索 | `WAITING_CEO → RESPONDED` 或 `ESCALATED` | 外部承诺、客户关系或经营方向变化 |

低风险、已批准的回复模板可以由 AI 在授权范围内自动执行；任何外部承诺、报价、隐私、
投诉和合作信息必须等待 CEO。互动价值只能由 API 回传或 CEO 真实确认产生，不得从点赞、
评论数量自动估算收入。

每个 Workspace 必须显式配置 `replyPolicy`，不能由 Agent 自行判断：

| `replyPolicy` | 可执行范围 | 必须记录 |
|---|---|---|
| `AUTO_APPROVED_TEMPLATE` | 只能使用已批准模板和允许变量；不改变价格、承诺、立场或隐私内容 | `templateVersion / renderedTextHash / actor / externalReceipt` |
| `CEO_APPROVAL` | AI 可以生成草案，但不能调用外部回复动作 | `responseVersion / CEO decision / decidedAt` |
| `NO_AUTO_REPLY` | 投诉、隐私、敏感事件或高风险互动只允许准备材料 | `escalationReason / evidence / nextCheckAt` |

即使是 `AUTO_APPROVED_TEMPLATE`，平台未授权、回执缺失或渲染结果超出允许变量时也必须转为
`WAITING_CEO`，不得把“回复已准备”显示为“已回复”。

运行界面只增加一个“互动回流”面板和 Assistant 事项投影，不新增一级导航。面板必须显示：
来源、关联内容、意图、风险、回复版本、处理状态、证据和下一检查点。

---

## 6. Cadence（节奏） + ScheduledRun（运行实例）

> 这是整个系统的心跳。"CEO 不用天天盯着，到点了 AI 自己干活，出了需要拍板的事才找我"——就靠这一组对象。

### 6.1 Cadence 字段【原型】

| 字段 | 含义 |
|---|---|
| id / name | 节奏标识与名称（业务 · 动作） |
| businessId | 所属业务（**节奏绑业务，不绑工作空间**） |
| schedule | 触发表达式 |
| ownerId | 负责的 AI 员工 |
| task | 任务描述与产出 |
| escalation | **结构化升级声明**，见 1.2【补齐，替换原型正则】 |
| estimatedCost | 预计单次成本 |
| route | 运行入口 |
| enabled | 是否启用 |

**`schedule` 是自由文本，同时容纳时间型与事件型**（"每天 08:00" / "每次提交后"）。【原型】
**【补齐】** 实现时必须解析成结构化触发器：`{ kind: CRON | EVENT, expr: string }`，否则无法真正调度。原文本保留作显示用。

原型四条种子节奏（迁移种子数据）：

| 节奏 | 触发 | 业务 | 负责 | 任务 |
|---|---|---|---|---|
| 小红书 · 每日研究 | 每天 08:00 | 小红书运营 | 策略分析 AI | 输出 3 条候选选题 |
| 抖音/TikTok · 数据回流 | 每天 18:00 | 抖音 TikTok 运营 | 数据回收 AI | API 失败则提醒 CEO 手动补录 |
| 公司 · 每周经营简报 | 每周一 09:00 | 公司共享 | CEO 助理 | 汇总财务、成果与风险 |
| 研发 · 回归检查 | 每次提交后 | 研发工作台 | QA AI | 失败时暂停发布并升级 |

内容工作台的节奏不是独立的第二套任务系统，而是绑定 `ContentItem` 状态事件的运行入口：

| 节奏 | 触发 | 业务 | 负责 | 输出 / 升级 |
|---|---|---|---|---|
| 小红书 · 内容审核准备 | `ContentItem → IN_REVIEW` | 小红书运营工作台 | CEO Assistant | 生成审核包；始终在发布前升级 CEO |
| 小红书 · 结果窗口回流 | `PUBLISHED + 24h / 72h` | 小红书运营工作台 | 数据复盘 AI | 回收 API 结果；失败转 CEO 手动补录 |
| 抖音/TikTok · 发布前权限检查 | `ContentItem → APPROVED` | 抖音 / TikTok 运营工作台 | 发布执行 AI | 检查授权与排期；缺授权转 `WAITING_CEO` |
| 抖音/TikTok · 结果窗口回流 | `PUBLISHED + 24h / 72h` | 抖音 / TikTok 运营工作台 | 数据复盘 AI | 关联原始指标；冲突转 `ABNORMAL` |
| 小红书 / 抖音 · 互动回流 | `InteractionItem → CAPTURED` | 对应运营工作台 | 互动回收 / 分流 AI | 事件到达即分类；敏感、线索或冲突转 `WAITING_CEO` |

这些节奏必须由事件和状态共同触发，不能只靠固定 cron。Assistant 默认静默准备，只有
发布门禁、权限缺失、结果异常、证据冲突或需要 CEO 价值判断时才升级；未授权时保留
手动发布 / 手动补录窗口，不生成估算事实。

互动回流不能等待下一次日报才处理：`CAPTURED` 事件进入队列后，分流 AI 立即分类；
低风险且符合 `AUTO_APPROVED_TEMPLATE` 的回复可以自动执行，其余事件按风险升级 CEO。

**Cadence 状态**：原型只有 `enabled` 布尔。【补齐】扩为 `DRAFT / ENABLED / PAUSED / RETIRED`，并保留版本历史（原型缺失）。

### 6.2 ScheduledRun 字段【原型】

`runId / cadenceId / businessId / title / ownerId / status / requestedAt / queuedAt / startedAt / finishedAt / executionMs / statusUpdatedAt / task / output / nextStage / requiresCEO / escalationReason / cost / capability / capacityContract / route`
CEO 介入后追加：`ceoResponseMs`（多久被看到）、`ceoResolutionMs`（多久被处理完）。
【补齐】追加：`overdueSince`、`attemptCount`、`lastError`。

### 6.3 状态机（7 态，原型中最完整的一个）【原型】

| 值 | 界面文案 |
|---|---|
| QUEUED | 排队中 |
| RUNNING | 执行中 |
| WAITING_CEO | 待 CEO |
| ACKNOWLEDGED | 已打开 |
| RESOLVED | 已处理 |
| FAILED | 异常 |
| COMPLETED | 已完成 |

### 6.4 流转表

| 从 | 到 | 触发条件 | 触发者 |
|---|---|---|---|
| — | QUEUED | 到点触发但并发已达 maxConcurrent | SYSTEM |
| — | RUNNING | 到点触发且容量可用 | SYSTEM |
| QUEUED | RUNNING | 容量释放后自动提升 | SYSTEM |
| RUNNING | COMPLETED | 执行成功且升级声明未命中 | SYSTEM |
| RUNNING | WAITING_CEO | 命中结构化升级声明 | SYSTEM |
| RUNNING | FAILED | 执行异常 | SYSTEM |
| WAITING_CEO | ACKNOWLEDGED | CEO 打开该条（记 ceoResponseMs） | CEO |
| ACKNOWLEDGED | RESOLVED | CEO 完成处置（记 ceoResolutionMs） | CEO |
| FAILED | ACKNOWLEDGED / RESOLVED | CEO 介入 | CEO |
| QUEUED | FAILED | 排队超时（见 1.3） | SYSTEM |【补齐】

**非法流转（必须被引擎拒绝）**：`RUNNING → RESOLVED`。运行中不得被直接判结。【原型】
**终态**：`COMPLETED` / `RESOLVED`。

### 6.5 原型缺口与当前处理边界

1. **没有真实定时器**：原型无 cron / 无 setInterval 驱动，全靠手工点击模拟"到点"。→ 这正是 A2 要解决的。
2. **无超时兜底** → 见 1.3。
3. **无员工拒单/退回机制** → 已补齐 `Handoff.RETURNED` 与责任退回字段；实现必须记录原因、缺口和建议 Owner。
4. **queued 无限等待** → 见 1.3。
5. **无跨业务容量抢占仲裁** → 已明确不做运行中抢占，采用业务隔离队列与显式优先级。

### 6.6 验收场景

- **正常（必测）**：配置一条"每天 08:00"节奏 → **不做任何手工操作**，到点后系统自行产生 RUNNING 实例 → 完成 → CEO 桌面出现记录。
  *这一条是整个 A2 的验收核心：没有真实定时触发就不算完成。*
- **必测**：并发打满 → 新实例进 QUEUED → 前序完成后自动提升为 RUNNING。
- **失败路径（必测）**：节奏声明 `ON_MISSING_AUTH`，在无授权情况下运行 → 转 WAITING_CEO → CEO 桌面出现且带明确原因 → CEO 处理后转 RESOLVED，全程记录响应耗时。
- **失败路径（必测）**：**重启后端进程** → 已排期的节奏仍能按时触发，QUEUED 实例不丢失。
  *这一条直接否决"内存调度线程"方案。*
- **必测**：尝试把 RUNNING 直接改成 RESOLVED → 被引擎拒绝并报错。

---

## 7. Outcome + Attribution（结果与归因）

> 闭环的收口。没有这一环，前面所有运行都只是"干了活"，不是"经营"。

### 7.1 字段【原型 + 补齐】

**Outcome**：`id / companyId / workspaceId / businessId / route / value（金额）/ verificationStatus / evidenceCondition / source / evidenceRef / evidenceType / capturedAt / resultWindow / runId / runIds[]`
**Attribution**：`contributors[] / allocation{权重} / allocationStatus / agent / model / skills[] / tools[]`

`verificationStatus` 使用 §1.4 的 `UNVERIFIED / VERIFIED / ABNORMAL`；`evidenceCondition` 使用 `FRESH / STALE / CONFLICT / MISSING`。因此“数据过期”不能被实现成新的成功 / 失败生命周期，也不能覆盖原始验证结论：例如 CEO 手动录入应为 `UNVERIFIED + FRESH`，等待平台回传应为 `UNVERIFIED + STALE`，来源冲突应为 `ABNORMAL + CONFLICT`。

### 7.2 状态机

**证据采用态**【原型】：`PENDING_ADOPTION 待 CEO 采用` → `ADOPTED 已采用` / `UNREGISTERED 未登记`
**分配态**【原型】：`PENDING_REVIEW 待复核` → `REVIEWED 已确认`
**硬规则**：贡献权重合计必须 = 100%，否则不得确认。【原型】

### 7.3 流转

| 从 | 到 | 条件 |
|---|---|---|
| — | UNVERIFIED | CEO 手动补录 / 无 API 授权 |
| UNVERIFIED | VERIFIED | 平台 API 回传 或 CEO 真实验收，且 `evidenceCondition=FRESH` |
| UNVERIFIED / VERIFIED | ABNORMAL | 数据冲突或验收未通过；同时记录 `evidenceCondition=CONFLICT` |
| PENDING_REVIEW | REVIEWED | CEO 确认贡献权重（合计 100%） |

**终态**：`VERIFIED + REVIEWED`。
**归档不删除证据**："历史证据仍可在成果库中追溯"。【原型，逐字】

### 7.4 验收场景

- **正常**：运行产出成果 → 外部数据回流 → 标 VERIFIED → CEO 确认贡献权重 → 计入经营账 → 业务方向获得"可扩大"资格。
- **失败路径（必测）**：权重合计 ≠ 100% → 确认被拒绝。
- **失败路径（必测）**：无授权 → 结果只能手动补录且强制标 `UNVERIFIED`，界面明示“待验证”；若结果窗口过期则同时标 `evidenceCondition=STALE`，**不得**参与“已验证价值”统计。

---

## 8. 端到端验收：CEO 的一天

ADR-0041 要求验证单位是"CEO 的一天"而不是模块。这是 v0.1 的最终验收剧本，**七步必须连续跑通，中间不允许人工改库**：

| # | 步骤 | 涉及对象 | 通过标准 |
|---|---|---|---|
| 1 | CEO 定下一条节奏 | Cadence | 节奏落库，可查询下次触发时间 |
| 2 | 到点系统自动开跑 | ScheduledRun | **无人操作**下产生 RUNNING 实例；重启进程不影响 |
| 3 | 运行中命中升级声明 | ScheduledRun + 升级契约 | 转 WAITING_CEO，CEO 桌面出现条目并说明原因 |
| 4 | CEO 处理 | ScheduledRun | ACKNOWLEDGED → RESOLVED，记录响应与处理耗时 |
| 5 | 外部数据回流 | Outcome | 生成 Outcome，正确标记 VERIFIED / UNVERIFIED |
| 6 | 收束成果 | Outcome + Attribution | 权重合计校验生效，成果入库可追溯到 runId |
| 7 | 记账归因 | 经营账 + BusinessDirection | 业务方向的验证结论被更新，"扩大业务"权限随之开闭 |

**至少一条失败路径必须同时跑通**（ADR-0041 硬要求）：
第 5 步外部授权缺失 → 结果强制 UNVERIFIED → 第 7 步"扩大业务"被冻结且给出明确原因。

---

## 9. 三业务 Runtime Simulation 契约

### 9.0 SimulationRun 最小持久化契约

三条业务必须通过同一种 `SimulationRun` 记录执行，不允许研发、小红书、抖音各自写一套不可互查的测试日志。SimulationRun 是一次业务运行的证据聚合，不是演示用的“模拟结果”字段。

必需字段：

```text
simulationRunId / companyId / ceoId / workspaceId / blueprintVersion
scenarioId / startedAt / finishedAt / participants[] / inputRefs[]
stateTransitions[] / handoffs[] / externalReceipts[] / evidenceRefs[]
failureEvents[] / ceoDecisions[] / finalState / passStatus
reviewer / reviewedAt / reviewNotes
```

数组元素必须使用统一结构，避免把一段汇总文本当成证据：

```text
stateTransitions[] = {
  entityType, entityId, from, to, command, actor, at,
  reason, evidenceRefs[], nextCheckAt
}
handoffs[] = {
  handoffId, fromRole, toRole, at, inputRefs[], outputRefs[],
  acknowledgement, nextCheckAt
}
failureEvents[] = {
  failureId, entityType, entityId, kind, detectedAt, detectedBy,
  impact, recoveryCommand, resolvedAt, evidenceRefs[]
}
ceoDecisions[] = {
  decisionId, entityType, entityId, choice, actor, at,
  reason, evidenceRefs[], resultingState
}
```

执行不变量：

1. `scenarioId` 必须来自已批准的 Simulation Plan；未登记场景不得标记通过。
2. 每个 `stateTransitions[]` 必须同时存在于对象自身的运行审计中；SimulationRun 只是聚合引用，不能成为第二套状态机。
3. `passStatus=PASS` 必须同时满足所有必需状态、失败路径、CEO 决策和外部证据条件；AI 自报、截图或空数据库不能使其通过。
4. 运行失败、未授权、数据延迟、版本错配和 CEO 拒绝必须保留在 `failureEvents[]`，不得被后续成功运行覆盖。
5. 运行重启后可按 `companyId / workspaceId / scenarioId` 恢复，并能反查到具体 ContentItem、InteractionItem、研发 cycle 或 Outcome。
6. 研发链必须形成 `intentId → cycleId → commit/build/test evidence → CEO acceptance`；内容链必须形成 `contentId → runId → outcomeId → decisionId`；互动链必须形成 `interactionId → responseVersion → externalReceipt`。

`SimulationRun` 的通过状态只表示“该 Blueprint 版本在该场景下通过验证”，不等于 Workspace 已上线；通过后仍需 CEO 审批生成 Operating Version。

`SimulationRun` 自身也有生命周期，不能只保存一个布尔值：

```text
DRAFT → RUNNING → REVIEWED → ARCHIVED
                    ├──────→ PASSED
                    ├──────→ FAILED
                    └──────→ CANCELLED
RUNNING → WAITING_CEO → RUNNING
```

其中 `passStatus` 是独立结果维度：`NOT_RUN / IN_PROGRESS / PASS / FAIL / REVIEW_REQUIRED`。
`WAITING_CEO` 表示模拟中的高影响节点需要 CEO 输入；CEO 返回后继续同一次运行，不能直接把它写成通过。`PASSED` 只允许在 `state=REVIEWED`、`passStatus=PASS` 且所有必需场景、失败路径和证据完整时产生；`FAILED` / `CANCELLED` 只能由明确的失败或取消命令产生。配置变化、证据撤回或运行版本失效都会使下一次运行重新从 `DRAFT` 开始，不会修改历史 SimulationRun。

## 9.1 内容发布 Workspace Simulation 细则

本节把 5.8 的运行契约变成可执行的业务验证。Simulation 不是静态截图，也不是直接写库；每条场景必须由 CEO 入口开始，经过 Workspace、AI 交接、外部发布 / 反馈和 CEO 决策，最后形成可追溯的终态。

#### 9.1.1 共同前置条件

| 前置 | 通过标准 |
|---|---|
| Company / CEO | 当前 Company 已存在，唯一真实用户是 CEO；所有对象带 `companyId` |
| Workspace | 由 CEO 创建或确认，Blueprint 已通过 Owner、Input/Output、失败出口检查 |
| AI 组织 | CEO Assistant、选题研究 AI、内容创作 AI、发布执行 AI、数据复盘 AI 均有责任契约；容量可用 |
| 外部连接 | 明确 `AUTHORIZED`、`UNAUTHORIZED` 或 `STALE`，不得用默认成功状态代替 |
| 结果窗口 | 明确指标来源、时间窗、证据等级和 CEO 手动补录路径 |

#### 9.1.2 小红书运营工作台

| 场景 ID | CEO / 系统动作 | 必须观察到的状态与证据 | 终态与 CEO 选择 |
|---|---|---|---|
| XHS-CONTENT-001 正常闭环 | CEO 确认本周期目标 → 研究 AI 提交带来源的候选选题 → 创作 AI 生成笔记与图文素材 → CEO 审核 → 授权连接器发布 | `IDEA → DRAFT → IN_REVIEW → APPROVED → PUBLISHED`；内容详情可见来源、负责人、发布时间和发布回执；CEO Desk 收到回报 | 平台在结果窗口回传浏览 / 点赞 / 收藏 / 评论 / 关注；Outcome=`VERIFIED`；复盘 AI 提交下一轮建议；CEO 选择继续或调整 |
| XHS-CONTENT-002 未授权 | 发布前发现账号未授权 | 发布动作禁用；`ScheduledRun=WAITING_CEO`；Assistant 说明“需要小红书授权或 CEO 手动发布”；不生成发布成功状态 | CEO 外部手动发布后录入 URL、时间窗、指标来源；Outcome=`UNVERIFIED`；“扩大业务”保持禁用 |
| XHS-CONTENT-003 发布失败 | 授权存在但平台返回失败 / 超时 | `ScheduledRun=FAILED`；ContentItem 保留在 `APPROVED` 或 `SCHEDULED`，显示错误、重试次数和责任人；CEO Desk 出现异常 | CEO 选择重试、改发布时间或退回草稿；不得进入 `PUBLISHED` |
| XHS-CONTENT-004 数据延迟 / 冲突 | 结果窗口到期但 API 无数据，或 API 与 CEO 录入冲突 | `Outcome.verificationStatus=UNVERIFIED / ABNORMAL`，同时标 `evidenceCondition=STALE / CONFLICT`；显示来源、新鲜度、冲突字段；不得进入已验证价值 | CEO 请求补证据、采用手动数据并保留 `UNVERIFIED`，或暂停本周期 |
| XHS-CONTENT-005 CEO 拒绝 | CEO 在审核阶段拒绝标题 / 表达 / 素材 | `APPROVED` 不产生；ContentItem 回到 `DRAFT`；保留拒绝原因、修改责任和下一检查点 | 创作 AI 修改后重新进入 `IN_REVIEW`；原审核记录不可覆盖 |

#### 9.1.3 抖音 / TikTok 运营工作台

| 场景 ID | CEO / 系统动作 | 必须观察到的状态与证据 | 终态与 CEO 选择 |
|---|---|---|---|
| TTK-CONTENT-001 正常闭环 | CEO 确认本周期目标 → 研究 AI 提交选题与证据 → 创作 AI 生成脚本 / 分镜 / 素材清单 → CEO 审核 → 发布执行 AI 发布视频 | `IDEA → DRAFT → IN_REVIEW → APPROVED → PUBLISHED`；详情显示视频版本、账号、授权状态、发布回执和责任链 | 平台回传播放、完播、互动、涨粉、成交（若有）；Outcome=`VERIFIED`；复盘 AI 解释钩子 / 节奏 / 素材影响；CEO 选择继续或调整 |
| TTK-CONTENT-002 未授权 | 发布前发现抖音 / TikTok 账号或发布权限缺失 | 发布动作禁用；`WAITING_CEO` 升级；Assistant 不把“视频已准备好”说成“视频已发布” | CEO 授权或手动发布并录入外部链接与结果；Outcome=`UNVERIFIED`；扩大通道冻结 |
| TTK-CONTENT-003 发布失败 | 视频处理失败、权限失效或平台拒绝 | `FAILED`；视频版本仍可查看；保留失败原因、原始素材和重试策略 | CEO 选择修复素材、重试、改发布时间或退回脚本；不得伪装为发布成功 |
| TTK-CONTENT-004 数据延迟 / 归因异常 | 播放或成交数据未回传，或不同来源口径冲突 | `Outcome.verificationStatus=UNVERIFIED / ABNORMAL`，同时标 `evidenceCondition=STALE / CONFLICT`；显示指标口径和来源；不能触发放量或预算扩大 | CEO 选择补证据、手动录入待验证数据，或暂停该内容的扩展动作 |
| TTK-CONTENT-005 CEO 拒绝 | CEO 认为脚本、钩子、素材或外部承诺不合适 | ContentItem 回到 `DRAFT`；拒绝原因必须绑定具体版本和责任人 | 创作 AI 重新生成并保留版本差异；重新审核后才能发布 |

#### 9.1.4 Simulation 通过条件

每条场景必须同时满足：

1. UI 可从 CEO Desk / 工作空间入口进入，并在处理完成后回到原来的 Operating Day 上下文；
2. 每次状态变化都有 `actor / at / reason / evidence`，且可由 `contentId → runId → outcomeId` 反查；
3. 未授权、发布失败、数据延迟和 CEO 拒绝均不能被成功态覆盖；
4. `VERIFIED` 只能由平台回传或 CEO 真实验收产生；手动补录必须保持 `UNVERIFIED`；
5. 只有 `VERIFIED` 且完成 CEO 复盘后，才允许生成“继续扩大 / 调整投入”的 Decision；
6. 任意一次 Blueprint、Stage、Agent、Connector 或 Evidence Rule 修改，均使两个工作台重新回到 `BLUEPRINTING`，必须重新跑全部场景；
7. 已批准内容发生编辑时，必须生成新 `versionId` 并重新审核；发布回执的 `publishedVersionId` 与 CEO 批准版本不一致时，运行必须阻断并升级 CEO。

---

#### 9.1.5 互动回流 Simulation

| 场景 | 必须观察到的运行事实 | CEO 结果选择 |
|---|---|---|
| 低风险评论 | 评论被抓取并绑定 `contentId`；互动分流 AI 分类；已批准模板自动回复并保存平台回执 | 继续自动处理或暂停该模板 |
| 潜在线索 / 合作咨询 | `CLASSIFIED → DRAFTED → WAITING_CEO`；回复草案显示事实、未知和承诺影响；不会静默发出报价 | CEO 批准回复、修改后发送，或升级人工跟进 |
| 投诉 / 敏感互动 | 风险标签、来源和原文保留；自动回复禁用；Assistant 置顶升级 | CEO 回复、转为异常，或暂停相关内容方向 |
| API 不可用 / 重复冲突 | 保留手动补录窗口；标记 `STALE / ABNORMAL`；禁止生成已验证价值 | CEO 补录、请求补证据，或放弃本次互动 |
| 模板越界 / 回执缺失 | `AUTO_APPROVED_TEMPLATE` 渲染出未允许变量，或平台没有外部回执 | 强制转 `WAITING_CEO`；CEO 查看渲染文本、策略版本和失败原因后决定 |
| 平台变体不合规 | XHS 图文 / 轮播或 TikTok 视频的格式、长度、比例、敏感表达检查失败 | `variantStatus=INVALID`；禁止发布；创作 AI 生成该平台新版本并重新审核 |

互动 Simulation 通过条件：回复必须能追溯到 `interactionId → responseVersion → externalReceipt`；
任何涉及外部承诺的回复没有 CEO 记录不得进入 `RESPONDED`；互动结果只能进入下一轮
Decision，不能直接扩大业务。

---

## 10. v1.6 决策闭合与实现验证项

原先 Q1–Q6 的定义歧义已在 §1.8 收敛。它们不再是产品空白，但必须在 Runtime Foundation 与 Simulation 中留下可查询证据：

| 原问题 | v1.0 默认 | 实现 / Simulation 必须证明 |
|---|---|---|
| 公司脉搏阈值 | 六维分级 + 证据维度正交，不生成总分 | 同一事实能产生正确等级； `UNKNOWN / STALE / CONFLICT` 不被覆盖 |
| PAUSED 最长时限 | 7 天复盘提醒、30 天归档候选，CEO 才能归档 | 超时只提醒；存在外部承诺时不得生成归档候选 |
| 置信度 | 五项证据组成，保存组成项和来源 | 缺关键证据显示 `UNKNOWN`，禁止模型自报百分比 |
| 跨业务容量 | 不抢占；显式优先级 + 业务隔离队列 | 运行中不能挪用其他业务资源；超时升级 CEO |
| AI 员工退回 | Handoff `RETURNED`，保留原因、缺口、建议 Owner | 退回不能生成完成态，并能重新分配或升级 |
| 升级超时 | 发布 4h、重大经营 24h、风险 2h、普通异常 24h | 超时只提升提醒，不自动批准或清除异常 |

---

## 11. 修订记录

| 版本 | 日期 | 变更 |
|---|---|---|
| v0.1 | 2026-08-03 | 首版。从 UI 原型还原 5 个核心对象的 Business Runtime 定义，补齐升级契约、超时兜底、证据分级、终态缺失等 6 类缺口。 |
| v0.2 | 2026-08-09 | 收敛为研发、小红书、抖音 / TikTok 三业务共享引擎，并补充三业务并行验证边界。 |
| v0.3 | 2026-08-09 | 将内容发布类参考转译为 ContentItem 状态机、专业 AI 责任、运营办公室布局和小红书 / 抖音五类可验收 Simulation 场景。 |
| v0.4 | 2026-08-09 | 增加 Buffer / Hootsuite / Predis / Later 机制转译、ContentItem 版本化审核意见、批准版本审计与 publishedVersionId 版本错配 Simulation 门禁。 |
| v0.5 | 2026-08-09 | 增加内容运营 Workspace Studio 装修链、互动与线索回流的 InteractionItem、互动 / 分流 / 回复 Agent 责任、ReplyPolicy 自动化边界、平台变体与适配门禁、外部承诺升级规则和互动 Simulation；明确不新增 CRM 一级导航。 |
| v0.6 | 2026-08-09 | 增加 Runtime Foundation 的最小持久化契约：ContentItem / ContentVersion / ContentReview / PublicationReceipt / InteractionItem / InteractionResponse、Studio 版本失效不变量和统一 SimulationRun 聚合记录；明确现有发布包不能替代业务对象。 |
| v0.7 | 2026-08-09 | 完成 Runtime 自审：补充研发工作台 Stage Runtime Contract；将 ContentItem 正常生命周期与 `INVALID / WAITING_CEO / FAILED / STALE / ABNORMAL` 异常状态分离；细化 SimulationRun 的状态转换、交接、失败事件和 CEO 决策记录结构。 |
| v0.8 | 2026-08-09 | 增加旧 `workflow_runs / workflow_steps / content_workflow_runs` 的迁移边界：只能作为内部执行遥测或 `executionRef`，不得替代当时定义的业务状态、外部结果、CEO 验收或 SimulationRun。 |
| v0.9 | 2026-08-09 | 补齐 ADR-0041 要求但此前缺少的 Cycle 生命周期、Handoff / DecisionPacket / Acceptance 契约，以及 SimulationRun 自身生命周期与 `passStatus` 正交维度。 |
| v1.0 | 2026-08-09 | 补充 Handoff、DecisionPacket、Acceptance 各自的状态机，明确交接拒绝、决策回滚和验收证据不足不能通过编辑原文伪造完成。Runtime Foundation 的产品契约形成可进入 Review 的完整版本。 |
| v1.1 | 2026-08-09 | 收敛原先 Q1–Q6 的实现歧义：明确公司脉搏分级、暂停复盘与归档候选、证据置信度组成、跨业务容量不抢占、AI 员工责任退回和按风险等级的升级超时；这些规则进入 Runtime Foundation 与三业务 Simulation 验证。 |
| v1.2 | 2026-08-09 | 完成产品 Review 反向校验：将验证等级与证据新鲜度拆为正交维度，明确 Cycle 异常字段，修正 8 个语义槽位与可变 Stage 数量的歧义，补齐 Outcome 反查字段，并收敛 SimulationRun 的等待 CEO / 复核 / 通过状态机。 |
| v1.3 | 2026-08-09 | 补齐 CEO Assistant Runtime：将 CEO Assistant 定义为 Company-level 独立 AI 员工，增加身份 / 契约 / Context / 权限 / 生命周期、触发与输出、动作边界、质量评估和 Assistant Simulation；Global Assistant 仅作为承载基础设施。 |
| v1.4 | 2026-08-09 | 补齐 First Arrival / Company Formation：定义 Pre-company Founding Guide 与 FoundingRun、Company 生命周期、CEO 确认门、恢复 / 拒绝 / 失败路径和从 foundingRunId 到首个 Cycle 候选的证据链；增加 FIRST-ARRIVAL Simulation。 |
| v1.5 | 2026-08-09 | 补齐 AI Employee / Role Slot / Capability Binding Runtime：定义 AI 员工生命周期、汇报关系、能力授权、容量、在岗状态、组织配置链、撤权 / 过载 / 退回路径和组织 Simulation 门禁；明确现有 Employee / Capability 不能直接替代目标 Runtime。 |
| v1.6 | 2026-08-09 | 完成 AI 组织契约反向 Review：明确 CEOAssistant 是 Company-level 特殊 AIEmployee 而非重复记录；补齐 `orgVersion`、RoleSlot 生命周期、员工 `lifecycleStatus` 与 `presenceState` 的维度边界、岗位级容量占用和版本失效规则；修正 `BLOCKED` 不能作为员工生命周期状态的歧义。 |
