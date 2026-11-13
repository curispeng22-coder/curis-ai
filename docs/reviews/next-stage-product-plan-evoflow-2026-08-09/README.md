# Curis 下一阶段产品计划：EvoFlow 研究转译

日期：2026-08-09  
Status: Review  
Decision: `PASS_TO_RUNTIME_FOUNDATION_REVIEW`  

本文件是下一阶段产品计划与产品决策记录，不是新的产品真相，也不替代
`docs/01_Product/Curis_Product_Blueprint.html`。唯一产品真相仍是 Blueprint；运行完成标准仍由
`docs/07_Decisions/ADR-0041-business-runtime-completion-standard.md` 冻结；当前实现事实仍以
`docs/00_Context/CURRENT_STATE.md` 为准。

研究依据：`/Users/yy/Documents/大魔王知识库/资料/EvoFlow 深度产品研究：Curis 可借鉴能力、体验与终局形态.md`。
本计划吸收该研究中已经真实观察到的表达、动线和治理问题，不复制 EvoFlow 的代码、技术栈、
Agent/Task 中心或未经授权的资源包。

---

## 1. 这次研究改变了什么判断

EvoFlow 暴露的不是 Curis 缺少几个页面，而是一个更根本的产品差距：Curis 已有不少
Company OS / Runtime 概念和后端基础，但用户还不能用很短的路径理解、装配、批准和管理一位
真正承担责任的 AI 员工。

因此下一阶段不把 Curis 改造成 Agent 控制台，而是完成下面的转译：

```text
EvoFlow：把能力做成用户看得懂、装得上、调得动的产品
Curis：把这些能力放进 CEO 的公司经营闭环，能够承担责任、产生证据、接受验收、被复盘和回滚
```

保留的 Curis 不变量：

1. `Company OS 固定，Workspace 开放`；业务差异只能进入 Workspace Blueprint / Runtime。
2. CEO 是唯一真实人类用户；CEO Assistant 是 Company 级第一位 AI 员工。
3. Business、Outcome、Commitment、Evidence、Acceptance、Decision 是经营语言。
4. Agent、Skill、MCP、Model、Connector 是 Company Resource，不是一级经营导航。
5. Task、Workflow、Run 只能作为 Workspace 内部执行基座，不得成为产品默认入口。
6. 任何“安装、雇佣、自动化、会议、交付”都必须经过权限、成本、责任、模拟、审批、激活和回滚。
7. Runtime v1.6 的产品门禁仍适用于尚未通过的产品切片；Runtime Foundation、三业务 Backend Simulation、Runtime API、First Arrival、Company 物化和 Workspace Foundation 已分别通过带基线阻塞的 Review，但这些证据不等于 UI 或 Desktop 完成。研究转译不能解除剩余实现门禁。

## 2. EvoFlow 能借鉴什么，放到 Curis 哪里

| EvoFlow 的可借鉴机制 | Curis 的产品转译 | 放置位置 | 明确不复制的部分 |
| --- | --- | --- | --- |
| Agent / Skill / Connector 卡片 | AI Workforce Card Contract：身份、岗位、责任、输入/输出、能力、权限、成本、结果、Workspace、Owner、状态、主要动作 | AI Team、Company Resources、Workspace 详情 | 不建立 Agent Center 作为 CEO 默认首页，不把提示词卡片当员工 |
| Agent 与 AI 员工分离 | Agent 是能力执行器；AIEmployee / RoleSlot 是责任主体；CEO Assistant 是 Company-level 特殊 AIEmployee | Business Runtime v1.6 组织契约 | 不允许平级 Agent 卡片承担公司责任 |
| 组织树、经理与直属关系 | CEO → CEO Assistant → Professional AIEmployee → Workspace RoleSlot → Workspace AI；汇报、授权、验收和升级可追溯 | AI Team + Runtime 组织版本 | 不做立即生效的关系编辑；变更必须产生新 `orgVersion` 并使旧 Simulation 失效 |
| 雇佣、安装和来源审查 | 对话式“雇佣与能力装配”：识别岗位/结果 → 发现资源 → 展示来源/权限/数据流/成本 → 形成 Role Contract / Workspace Blueprint → Simulation → CEO 批准 → 激活 | CEO Assistant、AI Team、Company Resources | 不做未经审核的一键市场安装、默认 Full Auto 或 Unlimited Budget |
| 员工健康、Token、预算 | AI 成本健康度：成本/Accepted Outcome、返工、失败、空转、预算速度、异常调用、边际收益 | CEO Desk、AI Team、公司脉搏 | 不做孤立的技术监控或只显示 Token 总数 |
| 全局 Assistant Workbench / Chat / Meeting | 一个共享浮层运行体：主动汇报、待决策、待输入、失败恢复、召集员工、会议入口 | Global CEO Assistant Overlay | 不增加固定秘书侧栏或第三列，不复制聊天机器人入口 |
| 多 Agent 会议轮次与点名 | 事实/观点/建议的自然讨论 → Decision Proposal → CEO 批准/修改/拒绝 → Commitment + Owner + DueDate + Evidence → Workspace 执行 | Company Meeting / Workspace Meeting | 讨论本身不能自动成为公司决策，不做科幻舞台代替业务语义 |
| 自然语言 Cron / 下一次运行预览 | 业务节奏与事件规则：谁在何时依据哪些数据执行，预计成本，完成后交给谁；预览后才激活 | Workspace Studio、Cycle、Operating Day | 不把通用 Workflow/Cron 放成一级平台入口 |
| 任务沉淀为可复用 App / 模板 | 先完成一次业务结果，再在 Workspace Studio 沉淀 Blueprint 版本；新版本必须重新模拟和审批 | Workspace Studio | 不把画布节点和 App 货架当成 Curis 的产品核心 |
| 失败、缺模型、权限不足的可恢复路径 | 允许先保存公司设计、Role Contract 和 Simulation 草稿；只有激活执行时才阻断并给出替代方案 | First Arrival、Company Resources、Assistant | 不因未配置模型而阻断所有公司设计，也不把失败吞成“运行中” |

## 3. 下一阶段目标形态

下一阶段只围绕下面这条 CEO 动线建立产品，不增加平行中心：

```text
CEO Desk
  → 看见公司状态、AI 团队健康、待决策和异常
  → Global CEO Assistant 解释并准备行动
  → AI Team / Company Resources 形成责任和能力方案
  → Workspace Studio 把业务目标装配成 Business Execution Space
  → Workspace Runtime 产生外部结果与证据
  → Meeting / Decision / Acceptance 形成公司事实
  → CEO 决策，Assistant 跟进，组织和 Workspace 进入下一周期
```

导航原则：

- `CEO Desk`、`Business`、`AI Team`、`Workspaces`、`Company Resources` 是经营语义入口。
- `Meeting`、`Decision`、`Cost Health`、`Knowledge`、`Calendar` 作为上下文视图或二级工具出现，不能再次形成一套平行公司。
- `Agent`、`Skill`、`MCP`、`Task`、`Workflow`、`Run` 在需要时由 Assistant 或 Workspace 引出。
- 同一个对象只能有一个权威状态与一个 Owner；卡片是可读表达，不是第二套数据模型。

## 4. 分阶段产品计划

### Gate 0：Runtime v1.6 产品评审（当前）

**目标**：确认 CEO Assistant、AIEmployee、RoleSlot、CapabilityBinding、组织版本、First Arrival、
Workspace、Cycle、DecisionPacket、Acceptance、SimulationRun 的边界已经足以进入 Runtime Foundation。

**交付物**：

- Runtime Definition v1.6 的产品负责人 Review 结论；
- `FIRST-ARRIVAL`、`ORG`、研发 / 小红书 / 抖音三业务 Simulation 的通过条件；
- 本计划与 Blueprint 的一致性确认。

**停止条件**：没有 Review PASS，不创建代码 Issue，不做 UI 重排，不把 EvoFlow 研究直接变成实现需求。

### P0-R：Runtime Foundation（Review 通过后）

这是下一步唯一可创建的运行时实现边界，候选 Issue 仍为 `RUNTIME-FOUNDATION-001`。范围最小化为：

1. `FoundingRun → Company → CEOAssistant → Business → Workspace → Cycle` 的可恢复证据链；
2. CEOAssistant 作为 Company-level 特殊 AIEmployee，含身份、触发、输出、动作边界、升级和回滚；
3. `AIEmployee / RoleSlot / CapabilityBinding` 的责任、汇报、授权、容量和组织版本；
4. `Commitment / Handoff / DecisionPacket / Acceptance / Evidence` 的状态和闭环；
5. `SimulationRun`、失败出口、CEO 批准和组织变更失效规则；
6. 研发工作台首个任务“完善 Curis”、小红书、抖音共享内核的三条最小 Simulation。

**退出证据**：运行时状态可持久化、可恢复、可回放；三条业务的 Owner、输入、输出、下一阶段、外部结果和 CEO 验收均可追溯；没有任何静态原型、fixture 或旧 Project/Task 聚合被当作通过证据。

### P0-E：把 Runtime 变成可理解的产品（P0-R 通过后）

此阶段才进入 UI / 交互 Issue，优先做最短的三条动线：

**A. AI Team / Workforce Card Contract**

- 公司级首屏看见 Assistant、专业员工、岗位空缺、在岗/等待/阻塞、最近结果、成本和风险；
- 员工详情回答“他负责什么、凭什么执行、最近产出什么、花了多少、遇到问题交给谁”；
- 组织关系通过树和汇报路径表达，变更先生成预览和 Simulation，不直接改变生产责任。

**B. 对话式雇佣与能力装配**

CEO 可以说：

> 我需要一个小红书市场研究员工，每天找五个增长机会，发布前确认，每日预算 20 元。

Assistant 必须将这句话转换为：岗位目标、Role Contract、所需 Capability / Connector / Knowledge、权限、数据流、预计成本、风险、Workspace 归属、Simulation 和待 CEO 批准项。批准前只保存草稿，批准后才绑定并激活。

**C. CEO Assistant Operating Overlay**

- 共享浮层有 Workbench / 对话 / 会议三种模式，但内容是经营事实；
- 主动汇报异常、待决策、待输入、待验收和即将发生的节奏；
- 能召集 AI 员工、创建 Decision Proposal、拆出 Commitment、跟进 Evidence，并在失败时解释恢复路径；
- 不遮挡主内容、不成为固定导航栏、不再创建第二个 Task 系统。

**退出证据**：CEO 不打开 Agent/Task 管理页，也能完成“提出需求 → 形成岗位/能力方案 → 审查 → 模拟 → 批准 → 激活 → 查看结果 → 回滚”全链路。

### P1：公司运行闭环

1. **Meeting Runtime**：事实和议题准备 → 召集员工 → 结构化讨论 → Decision Proposal → CEO 决定 → Commitments → Workspace 执行 → Evidence / Acceptance。
2. **Workspace Studio**：从真实完成的业务结果反推 Blueprint；配置岗位、能力、工具、知识、数据窗口、节奏和验收；模拟后交付运行版本。
3. **Business Cadence / Event Runtime**：周期、阈值和外部事件均显示下一次动作、数据来源、Owner、预计成本和交付对象；暂停、重试、转人工均可见。
4. **AI Cost Health**：把调用成本挂到员工、岗位、能力、业务和 Accepted Outcome；提供预算超速、返工、空转和高成本低产出预警。
5. **组织与 Workspace 版本**：岗位、能力、权限、Blueprint 变化生成版本差异，旧 Simulation 自动失效，CEO 重新批准后才进入运行。

**退出证据**：一个业务周期从异常或机会开始，经过 Assistant / Meeting / Workspace / Acceptance，最终形成 CEO 可审计的 Decision 和下一周期调整；不需要 CEO 手工在多个中心搬运状态。

### P2：受控生态与跨端能力

只有 P0/P1 的经营闭环稳定后，才考虑：

- 受控 Skill / MCP / Agent / Workspace 模板市场；
- 来源、版本、供应链评分和一键撤销；
- IM 通知、远程审批、跨设备 Assistant；
- 租户 / Admin 物理拆分、计费与商业化。

这些能力必须沿用 P0 的权限、成本、模拟、审批、回滚和审计，不得因为市场化重新引入“安装即运行”。

## 5. 第一条可验收产品切片

下一阶段不以“做完某个页面”为完成标准，而以 CEO 能否完成下面的故事为标准：

1. CEO 在 CEO Desk 说出一个业务需要或结果缺口；
2. Assistant 识别问题，汇报事实，提出岗位、能力、Workspace 和成本方案；
3. CEO 查看来源、权限、数据流、责任边界和风险；
4. Curis 生成 Role Contract / Workspace Blueprint，并运行隔离 Simulation；
5. CEO 批准、修改或拒绝；
6. 系统激活对应 AI 员工和 Workspace，进入真实 Cycle；
7. AI 员工提交 Evidence，外部结果可 API 回传或由 CEO 手动录入并标记来源/新鲜度；
8. Assistant 汇报 Accepted / Unknown / Failed / Blocked，必要时召集 Meeting；
9. CEO 形成 Decision，系统创建 Commitment、Owner、DueDate 和下一阶段；
10. 组织、能力或 Workspace 的变化触发新版本和重新模拟，不污染旧运行证据。

研发工作台、小红书运营工作台、抖音 / TikTok 运营工作台必须共享这条切片，只在外部结果、平台授权、内容对象和反馈窗口上不同。第一个研发任务仍是“完善 Curis”，但业务名称是“研发工作台”。

## 6. 明确不做的事

- 不把 EvoFlow 的 Agent / Task / Workflow 菜单复制为 Curis 一级导航。
- 不为了模仿 UI 重写 Curis 后端、数据模型或桌面技术栈。
- 不把静态员工卡、组织图、聊天记录或示例成本称为 Runtime 已运行。
- 不在 Runtime Review 前修改业务代码、页面路由或数据库。
- 不默认 Full Auto、Unlimited Budget、无审批发布或无来源安装。
- 不把会议讨论、模型调用、任务完成等同于 Decision、Accepted Outcome 或公司闭环。

## 7. 当前决策与下一步

产品负责人已对本计划给出 `PASS`，含义是进入 Runtime Foundation 评审，而不是直接批准代码实现。后续仍应由
`docs/reviews/runtime-foundation-review-2026-08-09/README.md` 记录 Runtime 评审结果。结论应明确：

- `PASS`：允许创建 `RUNTIME-FOUNDATION-001`，仍需独立 Issue、精确文件清单和实现授权；
- `CHANGES_REQUESTED`：只修改 Product / Runtime 文档，不改代码；
- `BLOCKED`：保留当前门禁，补齐缺失的状态、Owner、证据或 Simulation。

在得到 `PASS` 和明确 Issue 之前，前端继续作为 Project/Task-first 交付基线维护，
不得把本计划中的目标态截图、页面或演示数据写成已完成能力。

## 8. 2026-08-09 研究转译复核增补

本次复核不是把 EvoFlow 的功能逐项搬进 Curis，而是检查研究结论是否已经进入唯一
Blueprint，并把仍缺少的经营约束补成可实现、可验证的产品契约。

### 已吸收并写入 Blueprint 4.13

- `AI Workforce Card Contract`：卡片统一显示身份、责任、汇报、输入 / 输出、能力、权限、成本、容量、结果、证据、下一检查点和主要动作；卡片是只读投影，不是新的 Agent 对象。
- 对话式雇佣与能力装配：意图 → 岗位 / 结果 → 来源与权限审查 → Role Contract / Workspace Blueprint → 隔离 Simulation → CEO 批准 → 激活；未批准只能保存草案。
- 分阶段能力门禁：规划、执行、发布三阶段分别开放读取 / 模拟、批准写入、外部副作用；缺模型或权限时保存设计但激活 fail-closed。
- AI 团队健康与成本：成本与 Accepted Outcome、返工、失败、空转、审批等待和容量关联，避免退化成 Token 看板。
- Meeting Runtime 收束：事实 / 观点 / 建议 / 异议只构成讨论；Decision Proposal 经 CEO 决定后才产生 Commitment、Owner、DueDate、Evidence 和 Workspace 交接。
- Workspace Studio、业务节奏和运行恢复：加入 Blueprint 装配、下一动作预览、checkpoint、暂停 / 恢复 / 重试 / 局部重规划和错误可恢复性。

### 明确不吸收

不新增 Agent Center、Task / Workflow 一级平台、开放资源市场、科幻会议舞台、默认
Full Auto、Unlimited Budget、无来源一键安装，也不把讨论或运行日志当成 Decision / Accepted Outcome。

### 阶段事实校正

- `P0-R Runtime Foundation`：已完成并通过独立 Review；三业务 Simulation、Runtime API、Company 物化、First Arrival、Workspace Foundation 均已有独立证据，但 Backend 全量仍保留既有基线失败。
- `P0-E UI`：`THREE-BUSINESS-WORKSPACE-UI-001` 已获授权并正在实施，范围仅为现有 Runtime 安全投影、三业务 Workspace 与共享 Assistant Context；不扩展到 Backend、Desktop、prototype、活动库或旧链。
- `Desktop Packaging`：仍为 Draft，尚未形成可交付桌面包；不能把本计划或 UI 证据写成最终产品完成。

本增补的判断优先级高于本文件前文中“尚未进入 Runtime Foundation”的历史叙述；若与
`docs/00_Context/CURRENT_STATE.md` 冲突，以 Current State 的最新事实为准。

`Curis_Business_Runtime_Definition_v0.1.md` 仍以 v1.6 作为当前 Runtime Foundation 基线。
本次新增的机制先作为 Blueprint 4.13 的产品约束和 P1/P2 候选，不自动改写已通过的
Foundation，也不直接解锁新的代码 Issue；进入运行时前仍需单独的 Runtime Review、Simulation
和明确授权。

## 9. 证据与关联文档

- 唯一产品真相：`docs/01_Product/Curis_Product_Blueprint.html`（v4.13，Review）
- Business Runtime：`docs/01_Product/Curis_Business_Runtime_Definition_v0.1.md`（v1.6，Draft）
- 当前交付事实：`docs/00_Context/CURRENT_STATE.md`
- Runtime 完成标准：`docs/07_Decisions/ADR-0041-business-runtime-completion-standard.md`
- 当前 Runtime Review：`docs/reviews/content-workspace-runtime-review-2026-08-09/README.md`
- 三业务 Simulation：`docs/reviews/three-business-runtime-simulation-plan-2026-08-09/README.md`
- 前端目标对齐：`docs/reviews/frontend-target-alignment-2026-08-09/README.md`
- EvoFlow 研究原文：`/Users/yy/Documents/大魔王知识库/资料/EvoFlow 深度产品研究：Curis 可借鉴能力、体验与终局形态.md`
