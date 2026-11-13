# WorkBuddy Project → Curis Business Workspace 长期信息架构参考研究（IA Review）

> **Status**：RESEARCH + GAP REVIEW（仅研究 + 缺口评审）
> **纪律**：不修改 Frozen Authority（Blueprint / Shell / P1–P7 / Shared）· 不改 Workspace Engineering 高保真 · 不写产品代码 · 不直接设计页面 · 只做 IA 建议与缺口判定。
> **三来源区分**：下文用 **[官方事实]** = WorkBuddy 官方文档陈述；**[实际观察]** = 本机 WorkBuddy 运行时数据层实测；**[产品映射]** = 仅映射语义到 Curis，不照搬技术模型。
> **核心约束（来自 Frozen）**：长期 Business = Operating Team + Business Workspace；临时 Conversation/Task 不强制升级为 Business；Employee Presence=入口 / Workstation=Main·Conversation-first / Detail=Utility；Employee Conversation 禁止进 Context/Utility；Result/Artifact 在 Conversation 轻量引用→Utility 查看；**Context Isolation：不得因进入 Workspace 就把全部历史/Knowledge 注入员工上下文**；Workspace Domain UI 可不同，Shared Employee Workstation 不变。

---

## 0. 研究范围与本次结论先导

本次研究 WorkBuddy「项目（Project）」为何能作为**长期工作容器**，以及哪些机制值得 Curis Business Workspace 借鉴。结论是：

- **最值得借鉴**：Project 作为「共享配置 + 共享上下文 + 资产沉淀 + 动态（活动）」的长期容器；任务=对话会话、可重开可继续；产物可沉淀为资产；配置变更进入「项目动态」活动流。
- **绝对不应照搬**：① 项目配置/资料库**自动注入每个任务上下文**（与 Curis Context Isolation 冲突）；② 右侧固定「项目配置 / Artifacts / Files / Changes」常驻栏（与 Frozen Adaptive Surface + 不固定工具墙冲突）。
- **Curis 真实缺口**：Frozen 已锁定**机制与原则**（四栏、Context Isolation、Result Reference、Company-wide Object Search、Employee 三概念），但**未定义 Business Workspace 的长期信息表面**（历史/资产/配置与经营方法变更史/活动流）的具体 IA。这是 Domain Extension 层缺口，非机制缺口。

---

## 1. WorkBuddy Project 研究

### 1.1 官方事实（来源：codebuddy.cn/docs/workbuddy · Project 文档 + 公开产品指南）

**[官方事实] 层级模型**：`空间(Space) → 项目(Project) → 任务(Task)`。项目是「团队的核心协作阵地」，把**指令 / 连接器 / 专家 / 技能 / 资料**统一组织；任务 = 项目成员创建的**对话会话**（一个任务 = 一个对话 + 一个工作空间）。

**[官方事实] 配置自动注入**：成员在项目中创建任务时，「项目配置会自动从项目配置中拉取必要信息注入到任务上下文」——具体为：项目指令**拼入模型上下文**、项目资料库**以 reference 形式进入**、个人记忆**拼入上下文**；专家/技能/连接器的可选范围 = 项目 + 已安装 + 现场导入（项目项置顶）。

**[官方事实] 项目动态（活动流）**：分三类——「与我有关」（别人分享/转交给我）、「成员动态」（上传更新文件、邀请成员、公开任务、增删 Skill/专家/连接器、更改指令）、「自动化」（本人自动化通知）。即**配置变更与协作事件进入统一活动流**。

**[官方事实] 项目资产 / 资料库**：每个项目有统一文件管理中心（默认 5GB），支持成员手动上传或将任务产物保存到资料库；资料库内容**以 RAG 形式注入任务上下文**；文件列表显示「更新人 / 更新时间」。

**[官方事实] 产物（Artifact）**：任务执行中 Agent 生成的文件制品；操作权限 = 任务角色 + 项目角色叠加。产物可「上传到云端」进入项目资产。

**[官方事实] 任务流转（Handoff）**：将任务产物 + 进度摘要 + 自定义字段 + 附件打包移交他人；接收方基于完整上下文继续推进，无需重复背景。

**[官方事实] 自动化**：特殊任务形式，触发方式=定时（仅「定时执行」一种），在创建者本人会话中运行、仅本人可见；配置 = 名称/提示词/执行频率/连接器（可选）。

**[官方事实] 四大面板（来自第三方指南）**：计划（ToDoList 看板）/ 任务（项目内所有任务，按时间排列可搜索筛选）/ 资产（文件管理）/ 设置（项目配置：指令、专家、技能、连接器、成员）。

**[官方事实] 右侧面板四 Tab（来自第三方指南）**：Artifacts（生成文件）/ All Files（文件树）/ Changes（diff）/ Preview（网页预览）——**固定右侧栏**。

### 1.2 实际观察（来源：本机 WorkBuddy 运行时数据层，只读）

**[实际观察] 持久化表**：`~/.workbuddy/workbuddy.db` 含 `sessions`（对话会话）、`workspaces`（工作空间/目录）、`automations`、`automation_runs`、`automation_runtime_state`、`session_usage`、`automation_delivery_outbox`、`migration_meta`。即**会话与空间是分离的一等实体**，自动化是带调度字段的特殊任务。

**[实际观察] automations 字段**：`name / prompt / status / schedule_type / next_run_at / last_run_at / cwds / rrule / scheduled_at / valid_from / valid_until / model_id / skills_json / expert_id / connector_ids_json / permission_mode / push_to_wechat / wecom_bot_source / owner_user_id`。印证：自动化携带**技能/专家/连接器/工作目录/有效期**等长期配置，且为**个人级（owner_user_id）**。

**[实际观察] 技能双层**：`~/.workbuddy/skills`（用户级）+ `{workspace}/.workbuddy/skills`（项目级）；当前 Curis workspace 的项目级 skills 为空。印证：**能力包分用户级与项目级两层**。

**[实际观察] 连接器**：`~/.workbuddy/mcp.json`（用户级，111 bytes，未读密钥）+ `~/.workbuddy/connectors` + `connectors-marketplace` 目录。印证：连接器配置在用户级，按授权方式分公共/个人。

**[实际观察] 资产与审计**：`blobs`（文件体）+ `artifact-index` + `audit-log` + `edge-sync-mapping*.db`。印证：产物以 blob 持久化、有索引与审计轨迹。

### 1.3 产品映射（仅语义映射，不照搬技术模型）

| WorkBuddy 概念 | Curis 对应（语义） | 映射性质 |
|---|---|---|
| 项目 Project（共享配置+共享上下文容器） | **Business Workspace + Operating Team**（长期业务容器） | 类比，但 Curis 的 Business 是更高承诺（非随手创建） |
| 任务 Task（对话会话） | **临时 Conversation / Task** | Curis 明确：不强制升级为 Business |
| 项目配置（指令/专家/技能/连接器） | **Operating Strategy / Operating Rules / Capability / Connector** | 语义对应；**继承方式不同**（见 Q5/Q8） |
| 资料库 / RAG 注入 | **Knowledge** | Curis 有 Context Isolation，**不自动注入** |
| 项目动态 | **Activity / Event feed**（Decision/Handoff/Failure/Recovery + 变更） | 概念可借鉴 |
| 产物 / 资产 | **Result / Artifact / 业务资产** | 对应 |
| 自动化 | **Automation / Schedule** | 对应 |
| 右侧固定面板（Artifacts/Files/Changes/Preview） | **Utility（Adaptive，非固定栏）** | 机制不同，不可照搬 |

---

## 2. WorkBuddy 九问回答

**Q1 · Project 与单次 Task / Conversation 如何分层？**
[官方事实] Project = 长期共享容器（配置 + 共享上下文 + 资产 + 动态）；Task = 一次对话会话（一个对话 + 一个工作空间），持久化为 `sessions` 表。分层为 **Project（长期、共享）⊃ Task（每次会话实例）**；配置在 Project 层，注入每个 Task。

**Q2 · 一个 Project 中过去所有任务如何查看和继续？**
[官方事实] 项目详情页「任务」面板列出项目内所有任务，按时间排列、可搜索筛选；点击可重开对话、「继续处理已有任务、查看对话记录」。[实际观察] `sessions` 表独立于 `workspaces`，证明会话可持久重开。

**Q3 · Conversation 结束后，Result / Artifact 如何保留？**
[官方事实] 产物持久化为文件制品，存于任务内并可「上传到云端」进入项目资产；右侧 Artifacts Tab 展示。[实际观察] `blobs` + `artifact-index` 持久化文件体并建立索引。

**Q4 · Task 产物如何沉淀成 Project Asset？**
[官方事实] 手动将任务产物「保存到资料库」→ 成为项目共享资产，后续以 RAG 注入任务上下文；资产库记录更新人/时间。

**Q5 · Project 的长期配置如何被后续 Task 继承？**
[官方事实] **自动继承**：创建任务时项目指令拼入模型上下文、资料库以 reference 进入、个人记忆拼入；专家/技能/连接器范围自动包含项目项。→ **这是与 Curis 根本分歧点**（见 §3 / Q8）。

**Q6 · 专家 / Skill / Connector / Instruction 属于 Project 还是单次 Task？**
[官方事实] 主要属于 **Project（共享配置）**，并有个人/已安装层叠加；Instruction 是项目级全局行为规则，所有任务继承。运行时可选范围 = 项目 + 已安装 + 现场导入。

**Q7 · 项目配置变化如何进入历史 / Dynamic？**
[官方事实] 「项目动态」活动流记录成员动态：增删 Skill/专家/连接器、更改指令、上传文件、邀请成员等。配置变更即进入活动流，全员可见（自动化通知仅本人）。

**Q8 · 多个独立 Conversation 如何共享 Project 长期上下文，同时避免上下文混乱？**
[官方事实] 每个任务 = **独立 AI 会话沙箱（并行沙箱）**，互不干扰；共享的是 **Project 记忆 / 资料库（以 reference / RAG 形式，非全量倾倒）**。即「共享长期上下文 = 项目配置 + 资产库（引用级）」，每个对话保持独立。→ Curis 应借鉴「引用而非全量」，但需更严格（见 §3）。

**Q9 · Project 首页如何同时表达「现在发生什么」和「过去发生过什么」？**
[官方事实] 项目详情页 = 「项目动态」（现在：与我有关/成员动态/自动化通知）+ 「项目任务」（过去：任务列表）+ 「资产」+ 「计划」看板。即 **动态/进行中 = 现在；任务列表/资产/变更动态 = 过去**。

---

## 3. 映射到 Curis：核心长期问题

**问题**：一间 Curis 业务办公室经营半年后，CEO 在哪里查看它过去做过什么、产生过什么成果、积累了什么资产、团队和经营方法发生过什么变化，以及它现在怎么配置和运行？

**[产品映射] Curis 对应机制**：
- 长期容器 = **Business Workspace + Operating Team**（Frozen 已定）。
- 过去做过什么 / 产生过什么 = **历史 Work / Conversation / Task + Result / Artifact**（需 History/Activity 表面）。
- 积累了什么资产 = **业务资产库**（Domain 定义「资产」语义）。
- 团队/方法变化 = **Operating Team 变更 + Employee Method 演进 + 配置与经营方法变更历史**。
- 现在怎么配置和运行 = **Office Profile / 配置**（Operating Strategy/Rules/Capability/Connector/Automation）+ 当前工作（Business Home）。

**[关键分歧 · 不照搬 WorkBuddy Q5/Q8 的自动注入]**：WorkBuddy 把项目指令+资料库+个人记忆**自动拼入每个任务上下文**。Curis **Context Isolation** 明令禁止「因进入 Workspace 就把全部历史/Knowledge 注入员工上下文」。因此 Curis 的长期信息必须 **按需访问（Search / History / Activity / Office Profile / Utility），而非自动注入员工 Workstation**。WorkBuddy 的「引用级（reference/RAG）」思路可借鉴，但 Curis 连「自动 RAG 全量资料库」也不取，改为**显式、按需、可回溯**。

**[关键分歧 · 不照搬固定右栏]**：WorkBuddy 右侧固定 Artifacts/Files/Changes/Preview + 项目「设置」常驻栏。Curis Frozen：Utility 是 **Adaptive Surface**（默认收起、按需展开、非永久栏），且「不把工具墙常驻」。故「办公室配置」**不能是固定右栏**，应是 Nav 入口 / Main 独立 Domain 表面 / Utility 详情（见 §5）。

---

## 4. Curis 长期 Workspace IA 缺口分析

### 4.1 14 类长期信息 · 当前 Frozen 覆盖判定

| 长期信息类别 | Frozen 现有覆盖 | 缺口 |
|---|---|---|
| 当前工作 | ✅ Main(Workstation/Domain) + Context(Presence 简要) | 无 |
| 历史 Work / Conversation / Task | ⚠️ Company-wide Object Search(§1.5.4) 机制在，但无显式「历史/Activity」表面定义 | **缺口：缺 History/Activity 表面** |
| Result / Artifact | ✅ P6 Result Reference（Conversation 轻量引用→Utility） | 无（长期归档机制未定义，但模式已够） |
| 业务资产 | ❌ 无「资产库」表面定义 | **缺口：Domain 资产库未定义** |
| Operating Team | ✅ Organization 轴 + Shared Employee（T5） | 无（团队变更史未定义） |
| Leader / Employee / Responsibility | ✅ Presence(P2)/Workstation(§3.1)/Detail(§3.14) | 无 |
| Operating Strategy | ❌ 无 Office Profile/配置表面 | **缺口** |
| Operating Rules | ❌ 同上 | **缺口** |
| Employee Method | ⚠️ Employee Detail 含「能力/工作方式」，但无方法演进史 | **缺口：方法变更史** |
| Knowledge | ⚠️ 存在概念，但 Context Isolation 禁止自动注入；无按需访问表面定义 | **缺口：Knowledge 按需访问表面** |
| Capability / Connector | ⚠️ Connector 概念存在；无 Office 级配置/变更表面 | **缺口** |
| Automation / Schedule | ⚠️ 概念存在（Automation 工具）；无 Office 级视图 | **缺口** |
| Decision / Handoff / Failure / Recovery | ✅ P5/P7 + Failure Truth 原则 | ⚠️ 事件需进入 Activity/History 流（表面缺口） |
| 配置与经营方法变更历史 | ❌ 完全未定义 | **缺口（核心）** |

### 4.2 真实缺口结论
**机制层（四栏 / Context Isolation / Result Reference / Search / Employee 三概念）已 Frozen 足够**。
**信息架构层（Business Workspace 长期信息表面）未定义**——具体为：① History/Activity 表面；② 业务资产库；③ Office Profile / 配置（Operating Strategy/Rules/Capability/Connector/Automation）；④ 配置与经营方法变更历史（Change Log）。这四类属于 **Domain Extension**，应在各 Workspace 实例中定义，但需一条 **Shared 护栏**说明「长期信息按需访问、不污染 Context」。

---

## 5. 建议的 Curis Workspace 长期信息模型

### 5.1 模型分层（不设计页面，只定义信息归属）

```
Business Workspace 长期信息层（每间办公室一份）
├─ Office Profile / 配置（现在怎么配置和运行）
│   ├─ Operating Strategy / Operating Rules
│   ├─ Operating Team（Leader/Employee/Responsibility 当前）
│   ├─ Capability / Connector（Office 级）
│   ├─ Automation / Schedule
│   └─ 配置与经营方法变更历史（Change Log）★核心缺口
├─ Business Home（现在发生什么 · Main Domain 表面）
│   ├─ 当前工作 / 活跃员工(Presence) / 近期 Result / 待 CEO Decision
│   └─ 进入 历史/资产/配置 的入口（非 Dashboard 堆砌）
├─ History / Activity（过去发生过什么 · 按需）
│   ├─ 历史 Work / Conversation / Task
│   ├─ Decision / Handoff / Failure / Recovery 事件
│   └─ 成员/方法/配置变更事件
├─ Asset Library（积累的资产 · 按需/Utility）
│   └─ 业务资产（Domain 定义「资产」语义：RD=代码/Diff，CG=笔记/库，SpaceEng=已交付办公室组合）
└─ Knowledge（按需访问，绝不自动注入 Context）
```

### 5.2 14 类归属映射

| 类别 | 主归属 | 访问方式 |
|---|---|---|
| 当前工作 | Main（Workstation/Domain）+ Context(Presence 简要) | 常驻 |
| 历史 Work/Conversation/Task | History/Activity | 按需（Search/History 表面） |
| Result/Artifact | Conversation(P6 轻量) + Asset Library(归档) | P6→Utility；归档→Asset |
| 业务资产 | Asset Library | 按需 / Utility 预览 |
| Operating Team | Office Profile + Org 表面(Nav) | 按需 / Employee Detail(Utility) |
| Leader/Employee/Responsibility | Presence(入口) + Detail(Utility) + Office Profile | 按需 |
| Operating Strategy / Rules | **Office Profile（Main Domain 表面或 Nav 入口）** | 按需，**不注入 Context** |
| Employee Method | Employee Detail + Method Change Log | 按需 |
| Knowledge | Knowledge 表面 | **按需，严禁自动注入 Context** |
| Capability/Connector | Office Profile + Connector 管理 | 按需 |
| Automation/Schedule | Office Profile + Activity | 按需 |
| Decision/Handoff/Failure/Recovery | Activity/History + 单条 P6/P7 | 按需 |
| 配置与经营方法变更历史 | **Change Log（Office Profile 内或 History）** | 按需 |

---

## 6. 四栏信息归属建议（IA 建议，非页面设计）

| Pane / 入口 | 应承载的长期信息 | 禁止 |
|---|---|---|
| **Nav** | 六区导航；当前 Department；当前办公室；Workspace 导航；「办公室配置」入口（非固定栏） | 不放历史/资产/详情 |
| **Context**（Adaptive） | **仅当前工作上下文**：当前 Thread/阶段；责任链 已完成/当前/下一；团队 Presence 简要(P2) | **禁止**全量历史/Knowledge/配置/员工详情/Conversation |
| **Main**（必有） | ① 进入具体员工→Conversation-first Workstation(§3.1)；② 办公室总览→Business Home（现在发生什么 + 历史/资产/配置入口）；③ Office Profile/配置（独立 Domain 表面） | 禁止 Dashboard 堆砌；禁止固定右栏 |
| **Utility**（Adaptive） | 选中对象详情：Result/Artifact 全文(P6)；Employee Detail(§3.14)；资产预览；配置项详情 | 禁止 Conversation；禁止常驻工具墙 |
| **Search / History / Activity**（按需） | Company-wide Object Search(§1.5.4) 扩展：历史 Work/Conversation/Task、资产、Decision/Handoff/Recovery 事件、变更史 | 默认不占空间 |
| **办公室配置入口** | **Nav 入口 / Main 独立 Office Profile 表面 / Utility 详情**——**绝不是右侧固定「项目配置」栏** | 禁止固定右栏（违背 Adaptive Surface + 不常驻工具墙） |

> **特别裁定（用户指令）**：WorkBuddy 右侧固定「项目配置 / Artifacts / Files / Changes」栏**不得照搬**。Curis 的办公室配置走 Nav 入口或 Main 独立 Domain 表面（Office Profile），资产/详情走 Utility，历史/活动走 Search/History 按需。

---

## 7. Shared vs Domain 边界

**Shared（全局统一，不得因业务而变）**：
- 四栏职责与 Adaptive Surface 机制（Nav/Context/Main/Utility）。
- Context Isolation 原则（长期信息不自动注入员工 Context）。
- Employee 三概念（Presence=入口 / Workstation=Main·Conversation-first / Detail=Utility）。
- Result Reference(P6)：Conversation 轻量引用→Utility 全文。
- Company-wide Object Search(§1.5.4) 作为长期信息按需入口的基础。
- 「长期信息按需访问、不污染 Context」护栏（建议未来收口为 Shared Pattern，见 §8）。

**Domain（各 Workspace 自决）**：
- Business Home 的具体布局与「现在发生什么」的表达。
- 资产库语义（RD=代码/Diff；CG=笔记/内容库；SpaceEng=已交付办公室组合）。
- Office Profile / 配置表面的具体 UI 与字段。
- History/Activity/Change Log 的具体呈现。
- Knowledge 表面的具体形态。
- 「资产」如何由 Result/Artifact 沉淀（Domain 定义晋升规则）。

---

## 8. 是否需要修改 Frozen Authority？

**结论：现有 Frozen 已足够支撑机制与原则；长期信息表面属 Domain Extension；不强制修改 Blueprint/Shell/Shared。**

- **Blueprint**：已声明 Workspace = 真实业务办公室，含「资料与上下文、工作对象、成果、结果反馈和复盘」——长期信息层的**意图**已在，无需改 Blueprint 措辞。
- **Shell**：四栏、Adaptive Surface、Context Isolation、P6 Result Reference、Company-wide Object Search、Employee 三概念均已 Frozen，足以承载长期信息架构。
- **Shared Authority**：Operating Team / Employee / Responsibility / 配置语义已在 Shared Employee + Company OS Shared Authority 中。

**可选（非强制，未来轮次）**：在 Shell Layer 3 增一条 Shared Pattern「Office Long-term Information Access」（定义 History/Asset/Config/Change-Log 的**访问原则**：按需、不污染 Context、不固定栏），与 Employee Detail(§3.14) 同性质。本轮**不执行**，留作未来 Domain 实例固化时收口。

**因此本轮不修改任何 Frozen Authority。**

---

## 9. 对三个现有 Workspace 的影响

| Workspace | 长期信息层如何落地（Domain Extension） | 备注 |
|---|---|---|
| **RD** | Business Home=当前开发工作(Workstations)+近期 PR/结果；资产=代码/Diff/Test；历史=Git 提交/PR/Review；配置=Dev Rules/Capability；变更史=方法演进 | RD 天然有 git 历史可作 History 表面，缺口最小 |
| **Content Growth** | Business Home=八问经营视图（**现在**）；增补：资产=已发布笔记/内容库；历史=过往选题/活动；配置=内容策略/规则；变更史=策略调整 | 八问偏「现在经营」，须与「过去历史/资产」分离，新增按需表面而非堆进八问 |
| **Workspace Engineering** | 是**交付型支持部门**（非持续经营）：其长期信息=**已交付办公室组合（portfolio）+ 建设方法演进 + 建设历史**；交付后办公室归 Operating Team，不在 SpaceEng 常驻经营 | 不需类 CG 的永久 Business Home；其长期层=交付作品集 + 方法沉淀 |

---

## 10. 最终八答汇总

1. **WorkBuddy 最值得 Curis 借鉴的机制**：
   - Project 作「共享配置 + 共享上下文 + 资产沉淀 + 动态（活动）」的长期容器；
   - Task=对话会话、可重开可继续（历史不丢）；
   - 产物可手动沉淀为资产；
   - 配置变更进入「项目动态」活动流（变更可见）；
   - 多会话共享「引用级」长期上下文（非全量倾倒）的思路。

2. **明确不应该照搬的部分**：
   - ❌ 项目配置/资料库/个人记忆**自动注入每个任务上下文**（违反 Curis Context Isolation）；
   - ❌ 右侧固定「项目配置 / Artifacts / Files / Changes / Preview」常驻栏（违反 Adaptive Surface + 不常驻工具墙）；
   - ❌ 把「临时对话」与「长期业务」混为同一层级（Curis 明确临时 Conversation/Task 不强制升级为 Business）。

3. **Curis 当前长期 Workspace IA 的真实缺口**：
   - 机制层（四栏/Context Isolation/P6/Search/Employee 三概念）**已 Frozen 足够**；
   - **信息架构层未定义**：① History/Activity 表面 ② 业务资产库 ③ Office Profile/配置（Operating Strategy/Rules/Capability/Connector/Automation）④ 配置与经营方法变更历史（Change Log）。这四类属 Domain Extension，需各 Workspace 实例定义，并受一条 Shared 护栏约束。

4. **建议的 Curis Workspace 长期信息模型**：
   - 每间办公室一份长期信息层 = Office Profile/配置 + Business Home（现在）+ History/Activity（过去）+ Asset Library + Knowledge（按需）；
   - 14 类信息按 §5.2 归属；核心是「**现在**走 Business Home、**过去/资产/配置/变更**走按需表面」。

5. **四栏信息归属建议**：
   - Nav=在哪里（含办公室配置入口，非固定栏）；Context=仅当前工作上下文（禁历史/知识/配置）；Main=Workstation 或 Business Home 或 Office Profile；Utility=选中对象详情（禁 Conversation）；Search/History/Activity=按需长期信息入口；**办公室配置绝不做固定右栏**。

6. **Shared vs Domain**：
   - Shared=四栏机制、Context Isolation、Employee 三概念、P6、Search、按需访问护栏；
   - Domain=Business Home 布局、资产语义、Office Profile UI、History/Asset/Change-Log 呈现、Knowledge 形态、资产晋升规则。

7. **是否需要修改 Blueprint / Shell / Shared Authority**：
   - **否**（本轮不修改）。现有 Frozen 已足够支撑机制与原则；长期信息表面属 Domain Extension；可选未来在 Shell Layer 3 增「Office Long-term Information Access」Shared Pattern（非强制、非本轮）。

8. **对 RD / Content Growth / Workspace Engineering 的影响**：
   - RD：git 历史即 History 表面，缺口最小；
   - Content Growth：八问=「现在」，须分离出历史/资产/配置/变更史的按需表面；
   - Workspace Engineering：交付型部门，长期层=已交付办公室组合 + 建设方法演进，不需永久 Business Home。

---

*本文件为 WorkBuddy→Curis 长期 IA 参考研究 · 2026-08-16（RESEARCH + GAP REVIEW · 非 Frozen / 非视觉 / 非代码 / 不修改高保真 / 不设计页面）*
