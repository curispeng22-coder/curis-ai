# CURIS PAGE CONTRACT FINAL REVIEW — 01 CEO DESK

**Authority Class:** REVIEW  
**Status:** Review  
**Disposition:** ACCEPTED CANDIDATE — READY FOR CROSS-PAGE REVIEW  
**日期：** 2026-08-18  
**范围：** 只定义 CEO Desk 的页面结构、信息、入口、返回和状态表达；不修改 Product Blueprint、Master Map、UI Blueprint、Frozen Shell、Runtime、Schema、数据库或代码。

## 0. 结论

### CEO DESK PAGE CONTRACT
**FINAL DELTA APPLIED — ACCEPTED CANDIDATE — READY FOR CROSS-PAGE REVIEW**

当前 Product Truth 足以形成完整 CEO Desk Page Contract，没有发现需要打开 Product Delta 的 Authority 冲突。这个合同把已有的 CEO 工作台、CEO Operating Day、CEO Decision Package、Result、经营洞察和 Assistant 语义组织成一个可交给 UI Design 的页面定义；它没有新增一级产品、OperatingDay Primitive、第二套通知/任务/决策系统。

本文件是已接受的 Page Contract Candidate，不是 Product Authority；可作为后续跨页面 Review 和 UI Blueprint 消费输入，但仍不得据此直接开发，必须另有 Approved Design 与正式 Issue。

## 1. 对当前 Authority 的页面审计

| 检查项 | 当前真源已有内容 | 本合同补齐的页面层内容 | 判断 |
|---|---|---|---|
| Mission | CEO Desk 负责简报、变化、结果、待处理、下一决定；经营洞察负责深度分析 | 明确首屏叙事、注意力排序和页面结束状态 | 保留并展开 |
| Entry / Return | 七区导航、Assistant、跨上下文返回原则 | 统一进入参数、返回上下文、焦点恢复 | 页面合同缺口 |
| Operating Day | `Brief → Matters → Handoff → Decision → Exception → Evidence → Learning → Closeout`，Day N → Day N+1 | 每一段在 Desk 的可见承载和消失条件 | 保留并落位 |
| Decision | Frozen P7 八要素和复杂度分层 | Desk 中从 Matter 进入 Decision Package 的唯一路径 | 保留并落位 |
| Result | Result / Evidence / Acceptance 归属原业务与 Workspace | Desk-worthy Result 的筛选和下钻 | 保留并落位 |
| Assistant | 全局身份、主动汇报、解释、路由和跟进 | Desk 内的 scoped 入口，不变成固定秘书栏 | 保留并限界 |
| State / provenance | Unknown、stale、manual、external、source/freshness 语义已存在 | 页面级 loading、partial failure、空态和恢复规则 | 保留并落位 |
| Pages boundary | 七个一级区域与各自职责已冻结 | Desk 与六个相邻空间的具体边界 | 保留并明确 |

**不属于 CEO Desk 的内容：**完整指标仪表盘、结果归档、完整组织图、业务后台、任务台、通知中心、项目中心、独立聊天首页。它们分别由经营洞察、资料库/来源空间、组织中心、业务空间、既有对象入口或全局能力承载。

## 2. Page Mission

CEO Desk 的唯一使命是：

> 让 CEO 在打开 Curis 后，用最少注意力成本知道公司今天发生了什么、什么值得现在打扰、什么需要自己决定、哪些责任必须继续跟进，以及决定之后公司会往哪里走。

页面职责由五个词组成：

1. **Brief**：把公司和业务变化压缩成今日经营简报；
2. **Attention**：只呈现需要 CEO 关注的 Matters；
3. **Decision**：在合法 Decision Package 上完成选择；
4. **Follow-up**：承接责任、交接、异常和未完成事项；
5. **Continuity**：把 Day N 未完成内容带入 Day N+1。

## 3. Entry / Return Contract

### 3.1 进入

| 场景 | 进入规则 | 首次焦点 |
|---|---|---|
| App 启动 | 已有 confirmed Local CEO Profile + Company 时进入 Desk；无 Company 时仍走 Founding，不伪造 Desk 数据 | 首个需要 CEO 注意的 Brief / Matter；没有事项时显示安静空态 |
| Founding 完成 | Welcome / First Business / Launch Check 完成后进入 Desk | 新公司状态、第一项业务、下一步经营动作 |
| 一级导航 | 从任意七区点击首页 / CEO 工作台 | 恢复该 Company 的当前经营日和上次焦点 |
| 其他页面返回 | 由 Business、Workspace、组织中心、人才与能力、资料库、会议或经营洞察返回 | 恢复来源对象、Matter、筛选、滚动位置和焦点 |
| Assistant 进入 | Assistant 识别 CEO 要查看的 Company / Business / Workspace / Employee / Matter，并带 scope 打开 Desk | 直接聚焦该范围的 Brief 或 Matter，不丢失原问题 |

### 3.2 进入参数

进入 Desk 的上下文应使用已有对象引用和页面上下文，不创建新的事实对象：

```text
companyRef
sourceSurface
sourceObjectRef (optional)
matterRef (optional)
scopeRef (optional)
period (optional)
returnContext (optional)
```

`returnContext` 只用于回到来源页面，不成为第二套导航或状态源。

### 3.3 返回

所有下钻均返回原来源，而不是统一回 Desk 根页面：

```text
CEO Desk → Business / Workspace / Employee / Decision Package / Result / Insights / Map / Meeting
           → 完成查看或处理
           → 原 Company + 原来源 + 原 Matter + 原筛选 + 原滚动/焦点
```

如果来源对象已变化或失效，返回时显示当前事实、变化原因和可恢复入口；不得把旧快照当成当前状态。

## 4. Information Hierarchy

以下是 **Information Responsibilities（信息职责）**，不是要求分别绘制成独立 Card、Dashboard Block 或固定首页区块。Decision、Exception、Handoff 优先作为 Matter 的类型、状态或下钻内容出现，避免重复的大型首页模块。页面目标是 **Low Surface Complexity / High Operating Information Density**。

CEO Desk 的主叙事顺序固定为：

```text
Desk Header / 当前公司与经营日
        ↓
Today Brief（公司发生了什么）
        ↓
Matters（现在值得打扰什么）
        ↓
Decision / Exception / Handoff（需要处理什么）
        ↓
Important Results（最近产生了什么真实结果）
        ↓
Follow-up / Closeout（接下来谁负责什么）
        ↓
Assistant（按需解释、路由、继续）
```

这不是固定卡片数量，也不是 Dashboard 网格。各职责可以合并、嵌套或按当前事项展开；空状态时只显示真实的下一步，无数据不以占位数字填满页面。

## 5. Sections / Page Contract

### 5.1 Desk Header

**Mission：**确认“我在哪里”和资料新鲜度，不承担全局 Topbar 或全量导航。

**必须显示：**Company 名称、当前经营日/最近更新标签、Brief 生成或读取时间、数据新鲜度、必要的返回来源。

**可用动作：**刷新当前事实、打开 Assistant、进入相应 scoped Insights。Header 只显示当前 Company；当前 Product Truth 未确认多 Company 前，不显示 Company Switcher，也不扩展多 Company 产品模型。

**禁止：**全局指标、通知总数、Task 总数、第二套搜索/聊天、跨页面固定工具栏。

### 5.2 Today Brief

**Mission：**回答“今天公司最重要的变化是什么”，而不是展示所有日志。

**内容优先级：**

1. Company 级经营摘要；
2. 重要 Business 变化；
3. 重要 Employee / Organization 变化；
4. 真实 Result；
5. Risk / Blocker / Exception；
6. Needs CEO；
7. Day N carry-over；
8. 已有真实来源的外部经营结果。

**筛选原则：**只有影响经营方向、外部承诺、责任连续性、风险、结果验收或 CEO 决策的变化进入 Brief。普通通知、所有 Task、全部指标、无来源的健康分数和重复状态不进入 Brief。

### 5.3 Matters / Attention

Matters 是 CEO 当前需要处理的经营事项，不是 Task List 或 Notification Center。

**允许的类别：**

- `Needs CEO`：事实不足以由 AI 自行决定；
- `Risk`：已有来源证明的经营风险；
- `Exception`：运行或责任链异常，需要 Owner / 恢复动作；
- `Important Result`：值得 CEO 验收或改变方向的结果；
- `Responsibility Follow-up`：责任、交接或承诺尚未闭合；
- `Opportunity`：仅当有合法来源和明确业务上下文时出现。

每个 Matter 至少回答：

| 字段 | 要求 |
|---|---|
| What happened | 发生了什么，使用 CEO 语言 |
| Why it matters | 为什么现在值得 CEO 关注 |
| Scope | Company / Business / Workspace / Employee 等来源范围 |
| Owner | Responsible Employee / Business / 当前责任主体 |
| Source | 原始对象、资料、运行、会议或外部回执 |
| Evidence | 可查证的 Evidence / Result / Receipt；没有则显式未知 |
| Current status | 当前真实状态和更新时间 |
| Recommended next action | AI 建议的下一动作及其影响 |
| Return | 处理后回原来源和上下文 |

不要只用红/黄/绿颜色表达严重程度；颜色不能替代事实、责任和下一步。

### 5.4 Decision Surface

Desk 只消费 Frozen CEO Decision Package Pattern，不重新发明 Decision UI：

```text
Needs CEO
  → Decision Banner / Matter
  → Decision Package（发生了什么、为何不能自决、方案、影响/风险/代价、推荐、推荐理由、CEO选择、选择后自动继续）
  → Evidence（按需）
  → CEO Choice
  → AI 按原责任继续
```

简单、低歧义、低影响事项可以在 Banner 提供明确选择；高风险、不可逆、资金、合规或外部副作用事项必须进入 Decision Package 后再选择。`CEO Decision ≠ Handoff`：决策不是责任交接，也不创建新对话或第二套承诺系统。

### 5.5 Important Results

Desk 只显示对经营方向、客户承诺、业务目标、员工责任或 CEO 验收有影响的近期/重要 Result，不显示 Result Archive。

每个 Desk-worthy Result 至少显示：标题、所属 Business / Workspace、责任 Employee、结果状态（例如 Accepted / Unreviewed）、发生时间、来源、Evidence / 外部结果引用、下一步或是否需要 CEO 验收。

- `Accepted`：已有 CEO 验收或明确业务验收来源；
- `Unreviewed`：真实产生但尚未验收；
- `Unknown / Not connected`：没有真实来源，不得显示成 0 或完成。

点击 Result 回到 Result / Evidence Source；完整历史留在来源 Workspace、资料库或经营洞察。Result 必须可回溯到 Business、Employee 和 Evidence。

### 5.6 Follow-up / Handoff / Closeout

该区不是责任管理后台，而是让 CEO 知道哪些事情仍然没有“着落”：

- 未完成 Responsibility；
- 未完成 Handoff；
- 未决 Decision；
- 未关闭 Risk / Exception；
- 外部承诺或验收待回填；
- 下一经营日需要继续关注的结果。

每项显示 Owner、当前原因、下一检查点、来源和关闭条件。完成、拒绝、转移、暂停或关闭后从当前列表消失，但历史、Evidence、Result、Learning 保留并可反查。

## 6. CEO Assistant Role on Desk

CEO Assistant 是首位 AI 员工，但在 Desk 上不占固定秘书栏，也不把页面变成聊天首页。它按需承担：

- 解释 Brief 和 Matter；
- 将注意力路由到真正需要 CEO 的对象；
- 查询公司、业务、员工、资料、结果和会议；
- 准备 Decision Package、会议材料和后续跟进；
- 找到合适 Employee / Workspace 并协调责任；
- 把自然语言意图路由到已有 Business、人才与能力、资料库、会议、经营洞察或 Workspace 能力。

Assistant 入口必须继承当前 Company / Scope / Matter；完成动作后回到原上下文。不能新建固定秘书面板、第二个 Task 系统、第二个 Decision 系统或把 Assistant 输出当成未经来源验证的 Company Truth。

## 7. Operating Day / Cross-day Continuity

Desk 以已有跨日语义承接，不创建 `OperatingDay` 页面或 Runtime Primitive：

```text
Day N
 → Brief
 → Matters
 → Handoff
 → Decision
 → Exception
 → Evidence
 → Learning
 → Closeout
 → Day N+1
```

### 7.1 Day N → Day N+1 的 carry-over

默认继续承接：未完成责任、未决 Decision、未完成 Handoff、Risk、Exception、Follow-up、重要但未验收 Result、外部结果等待回填。

### 7.2 Carry-over 消失条件

事项只有在其真实来源达到相应关闭条件后才从当前经营日消失：

- Responsibility：责任完成并有 Result / 交接记录；
- Decision：CEO 已选择且 AI/责任主体已继续；
- Risk / Exception：风险解除或被 CEO 明确接受/转移；
- Follow-up：检查点完成并记录结果；
- Result：已验收、被拒绝、或已明确转入下一周期；
- 外部回填：来源、时间和录入者已记录。

关闭不删除历史；只改变当前 Desk 的注意力归属。

## 8. Empty / Loading / Unknown / Error

### 8.1 New Company

显示“公司已经建立，今天从这里开始”及真实下一步（如建立第一项业务、查看 Assistant 建议或配置必要能力）。不显示收入、业务数量、员工负载或健康分数 0。

### 8.2 No Business

显示空公司说明和唯一清晰下一步：创建业务或让 Assistant 帮助定义第一项业务。入口回到合法 Company / Founding / Business 创建路径。

### 8.3 Business exists but no Result

显示业务存在、当前目标和“尚未记录真实结果”；提供进入 Business / Workspace、配置能力或等待外部回执的合法入口。不把无结果渲染为 0、完成或健康。

### 8.4 External data unavailable

显示 `未知 / 未连接 / 待人工回填 / 最近验证时间`，并提供原来源或设置入口；永远不以 0 代替未知。

### 8.5 No Needs CEO

显示“目前没有需要你立即决定的事项”，同时保留 Brief、最近重要结果和下一经营方向；不制造事项、不制造通知计数。

### 8.6 Loading

Desk Header、Brief、Matters、Results、Follow-up 分区独立加载。Skeleton 只能表示正在读取，不能显示示例数字；一个分区加载失败不阻塞其他分区。

### 8.7 Partial Failure / Runtime unavailable

失败区显示“当前事实读取失败”、失败范围、最近成功时间（如有）、错误原因的用户语言、负责人和“重新读取 / 返回来源 / 查看诊断”的入口。其余分区继续显示已验证数据，并标注新鲜度。恢复后重新读取同一 scope，不直接把失败变成完成。

### 8.8 Unknown / Stale / 来源不一致

`Unknown` 表示没有可验证来源；`Stale` 表示来源存在但已过期；多个来源不一致时显示“来源不一致 / 需要核实”，并进入既有 `Unknown / Review-needed` 语义。CEO Desk 不新增全局 `Conflict` 状态；若未来需要正式 Conflict State，必须另走 Product Delta。所有情况都显示原因、来源和下一步，不由 UI 猜测或合并。

## 9. Fields / Source Authority Contract

页面使用来源对象的引用和投影，不发明新的 Runtime 字段。建议字段合同如下：

| Section | 必须字段 | 可选 / Derived 字段 | Source Authority | Unknown / Freshness |
|---|---|---|---|---|
| Header | `companyRef`、当前来源、读取时间 | 经营日标签、最近更新 | Company Truth + 当前上下文 | 读取不到 Company 时 fail-closed |
| Brief | Company 摘要、变化引用、Result 引用、Risk / Exception 引用、Needs CEO 引用、carry-over 引用 | 外部结果摘要、重要程度排序 | Company / Business / Organization / Result / Evidence / Feedback | 每条带 source、freshness、unknownReason |
| Matter | Matter 类别、事实、范围、Owner、状态、source/evidence、下一步 | 推荐理由、影响摘要、更新时间 | 原始 Business / Workspace / Employee / Meeting / Decision / Exception | 无来源不得进入“已确认事实” |
| Decision | Frozen Decision Package 8 要素、Choice、Evidence 引用 | 复杂度标签、推荐呈现 | CEO Decision Package Pattern / Evidence | 高风险无完整包不得直接批准 |
| Result | `resultRef`、Business / Workspace、Owner、状态、时间、Evidence / 外部结果引用 | 简短质量反馈、下一步 | Result / Evidence / Acceptance / External Result | Accepted、Unreviewed、Unknown 分开 |
| Follow-up | Responsibility / Handoff / Risk / Exception 引用、Owner、检查点、关闭条件 | Learning、下周期建议 | Responsibility / Handoff / Commitment / Result | 未完成责任必须可回到原来源 |
| Assistant | 当前 scope、原问题、回答引用、下一动作 | 建议路由、待 CEO 选择 | CEO Assistant + 被引用的产品能力 | Assistant 不能凭空创建 Truth |

`source`、`freshness`、`verified`、`manual`、`unknown`、`stale`、`missing`、`external` 是用户可理解的可信度语义；不把内部 Runtime 名称直接当作普通用户主语言。

## 10. Actions

CEO Desk 只提供已有产品能力的入口：

| 动作 | 目标 | 约束 |
|---|---|---|
| 进入 Business | Business Detail / Operating Model | 保留 Company、Matter、焦点 |
| 查看 Matter | 原始 Business / Workspace / Employee / Meeting / Exception | 不打开万能 Drawer 替代来源 |
| 做 Decision | Frozen Decision Package | 高风险必须完整查看方案与证据 |
| 查看 Result | Result / Evidence Source | 不进入结果归档替代页 |
| 找 Employee | Employee Profile / Workstation | 员工状态来自 Frozen Shell 投影 |
| 问 Assistant | Scoped Assistant | 不新增第二聊天系统 |
| 创建 / 委派后续工作 | 通过 Assistant、Business、Workspace 或 Meeting 的已有入口 | 不创建 Desk 专属 Task 系统；责任、Owner、结果必须回到来源 |
| 进入经营洞察 | 当前 Company / Business / Workspace / Employee scoped Insights | 完成后返回 Desk 原 Matter |
| 进入公司版图 | Organization Center / Company Map | Desk 只显示组织异常，不复制组织图 |
| 进入会议 | Company / Business / Workspace Meeting | 从 Matter 带议题和来源，不把聊天直接当决定 |

## 11. Drill-down / Reverse Entry

| Desk 内容 | 点击目标 | 返回 Desk 时保留 |
|---|---|---|
| Business signal | Business Detail / Operating Model | Company、Business、Matter、滚动/焦点 |
| Employee signal | Employee Profile / Workstation | Employee、来源事项、工作面焦点 |
| Decision | Decision Package → Evidence | Decision、选项、原 Matter |
| Result | Result / Evidence / External Result | Result、Business、Owner、原筛选 |
| Trend / report teaser | scoped Operating Intelligence / Business Report | scope、period、比较条件、原 Matter |
| Organization issue | Company Map / Employee Directory | Department / Business / Role / Employee scope |
| Meeting follow-up | Meeting | 议题、参与人、承诺、原事项 |
| Assistant answer | 被引用的 Business / Workspace / Employee / 资料 / Meeting | 原问题、scope、Assistant focus |

不能所有内容都进入一个万能 Drawer；需要完整阅读、比较或编辑时，进入对应产品空间或 Focus View。

## 12. Cross-page Boundary

| 空间 | 它负责什么 | CEO Desk 只保留什么 |
|---|---|---|
| 业务空间 | 具体 Business、目标、办公室、专业工作、业务结果 | 公司级摘要、变化和需要 CEO 介入的信号 |
| 组织中心 | 公司版图、员工目录、Role / Staffing | 组织变化、空岗、责任风险摘要 |
| 人才与能力 | 专家、Skill、Connector 的发现、招募、纳入 | 能力缺口或需要 CEO 关注的请求 |
| 经营洞察 | 深度趋势、比较、归因、报告和经营评估 | 需要注意的结论入口，不复制图表分析 |
| 资料库 | 资料导入、索引、搜索、引用、沉淀 | 资料相关风险/证据引用 |
| 会议 | 讨论、事实/观点、Proposal、Decision、Commitment、跟进 | 会议决定和待跟进事项 |

## 13. Product → Implementation Gaps

这些是实现门，而不是本文件新增产品模型：

1. **CEO Desk Projection Gap**：现有实现需要提供按 Company / scope 聚合 Brief、Matters、Result、Follow-up 的同源投影；不能由页面自行拼第二套事实。
2. **Cross-day Read / Closeout Gap**：需要让 Day N 未完成责任、Decision、Exception、Evidence、Learning 在重启后仍能回到 Desk；不新增 OperatingDay 表即可通过现有责任/结果/审计关系承载。
3. **Attention Ranking Gap**：需要可解释的来源、Owner、影响和下一步排序；不以不可解释的分数制造“重要性”。
4. **Partial Failure Projection Gap**：分区读取、Unknown / Stale / 来源不一致 / Review-needed 和恢复入口需要前端/Runtime 协同；单个 Business 失败不能令全 Desk 失效。
5. **Decision Package Projection Gap**：Desk 必须读取 Frozen P7 结构并在高风险场景阻止一键批准；不能创建第二 Decision Entity / UI。
6. **Result Traceability Gap**：Desk-worthy Result 必须能追溯 Business / Workspace / Employee / Evidence / Acceptance / External Result；缺少来源时显示未知。
7. **Assistant Context Gap**：Assistant 从 Desk 发起的查询、决策和跟进必须继承 scope，并可回到原 Matter；不能另起任务或对话系统。

实现前应为上述 Gap 建立正式 Issue、Allowed Files、Simulation / Browser / Desktop 验收门；本 Review 不授权代码实现。

## 14. 已落定的页面决策

以下决策已由 CEO 在本轮确定，不再作为 Open Question：

1. Brief 以 CEO 所在时区的自然日为主，同时可提示“自上次查看以来的变化”。
2. Matter 使用可解释的系统排序；CEO 可以手动置顶或标记稍后处理。
3. External Result 只在 Desk 提示；实际回填进入 Business / Insights 来源页。
4. Important Result 的数量不写死，由 Design 按信息密度和窗口尺寸决定。
5. Assistant 主动打扰阈值和静默时间属于 Settings / Company Policy，不由 Desk 定义。
6. Closeout 默认由系统 / CEO Assistant 根据真实经营事实自动形成并持续更新；CEO 不执行每日“关闭经营日”。未完成 Responsibility、Decision、Risk、Follow-up 自动 Carry Forward；只有真实 Decision Gate、Responsibility Conflict 或 High-risk Exception 才要求 CEO 介入。

这些决策只细化页面承载和经营连续性表达，不新增 OperatingDay Primitive、Closeout 页面或全局 Conflict State。

## 15. Final Recommendation

建议将本文件作为 **CEO Desk 专项 Page Contract**，并进入跨页面 Review；它可作为 UI Blueprint 的下一步 Design 输入。后续顺序应为：

```text
CEO Acceptance
→ UI Blueprint 消费本合同（不反向改 Product Truth）
→ CEO Desk Design Brief / Wireframe
→ Approved Design
→ 独立 Issue / Runtime Projection
→ Browser + Desktop + restart + failure/recovery 验收
```

在 Approved Design 与正式 Issue 之前：不改三份 Current Product Truth，不修改 Frozen Shell，不建立第二套 Brief、Matter、Task、Notification 或 Decision 系统。

---

CURIS PAGE CONTRACT FINAL REVIEW  
— 01 CEO DESK FINAL DELTA APPLIED  
— ACCEPTED CANDIDATE  
— READY FOR CROSS-PAGE REVIEW
