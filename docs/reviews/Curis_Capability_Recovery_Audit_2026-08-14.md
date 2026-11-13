# Curis 历史能力回收审计

Status: REVIEW INPUT  
Date: 2026-08-14  
Baseline: `main @ c0e1855f446a55aa3a384006cfcfed9877130338`

> 本文只是历史能力审计与决策输入，不是 Product Blueprint、UI Blueprint、Prototype、Runtime Blueprint，也不拥有产品定义权。
>
> 本轮不是恢复旧架构或旧 UI，而是：**旧能力回收，新产品重新安置**。

## 1. 审计范围与边界

本轮为只读历史能力审计，不是开发任务。未修改 Product Blueprint、UI Blueprint、Prototype、正式代码、Runtime、Schema、数据库、活动数据或当前产品结构。

扫描范围包括：

- 当前 `docs/`、历史 docs、归档 / Deprecated 文档；
- Product Blueprint 历史版本、Master Map、Page Map、Product Rethink、UI 探索、HTML Prototype；
- `frontend/`、`backend/`、Runtime、数据库定义、测试和脚本；
- Git 历史、已删除文件路径和仍可由 Git 追溯的实现证据；
- Meeting、Decision、Fact、Opinion、Evidence、Proposal、Assignment、Task、Owner、Action、引用、结果回写；
- Workspace Studio、Space Engineering、Workspace Builder、Workspace Template、Workspace Config、Workspace Renderer；
- Goal、Review、Retrospective、Evolution、Memory、Learning、Result、Outcome、Approval、Intervention、Handoff、Notification、Recovery、Schedule、Automation。

当前权威边界：

- 当前事实以 `docs/00_Context/CURRENT_STATE.md` 为准；
- 当前冻结方向以 `docs/07_Decisions/ADR-0045-ordinary-user-desktop-product-rebaseline.md` 为准；
- 当前唯一 Blueprint 仍是 `docs/01_Product/Curis_Product_Blueprint.html`；
- 当前产品方向是普通用户优先的 Desktop App，Runtime、Simulation、Gate、Evidence、Acceptance、Decision 和 Rollback 继续保留为真实性与恢复支撑，但不作为普通用户默认入口语言；
- 当前工作树在审计开始时已有 dirty 文件，本次保留原状，不清理、不覆盖、不回滚。

## 2. 状态定义

| 状态 | 含义 |
|---|---|
| ACTIVE | 当前仍完整存在，或作为底层可靠性能力持续使用 |
| WEAKENED | 能力仍有部分实现或产品表达，但相较历史形态明显被简化、断链或降级 |
| MISSING | 当前产品定义或 UI 中已消失，当前未找到足够实现证据 |
| LEGACY_ONLY | 只存在历史文档、归档原型或旧实现，不属于当前产品事实 |
| REJECTED | 已明确不应恢复，通常是旧工程化架构或旧产品入口 |
| UNKNOWN | 现有证据不足以确认状态 |

## 3. 历史能力清单

| 能力 | 最早 / 最成熟出现位置 | 用户问题 | 历史呈现 | 当前代码 / 数据 / API / 测试证据 | 当前 Blueprint / Prototype / 正式代码 | 状态 | 当前判断 |
|---|---|---|---|---|---|---|---|
| 结构化会议 | `docs/01_Product/Curis 产品梳理 1.0_副本/Curis Development Specification v1.0/14 会议室开发规格（Meeting Room Specification）.md:9`；`34 会议与决策智能系统增强规范（Meeting Intelligence System）.md:9` | 复杂问题需要多人分析、记录决定并转执行 | 会议列表、创建、详情、历史会议；实时会议与后台研讨 | 当前存在 Runtime Meeting API、持久化 Runtime 实体和 `backend/tests/test_meeting_runtime.py:46` 起的测试 | 当前 Page Map 仍有会议区域；当前 `/ceo-office/meeting` 仍是规划占位页；正式代码保留部分 Runtime | WEAKENED | 会议能力不是从未存在，而是后端保留、前台被压缩 |
| Fact / Opinion / Evidence / Question / Risk | `34 会议与决策智能系统`；当前测试仍写入 `label: FACT` | 讨论不能只是消息流，需要区分事实、观点、未知和风险 | 多角色观点、辩论、评审和依据追踪 | 当前可写入 FACT；Evidence、DecisionPacket 等 Runtime 对象存在，但没有完整会议级独立类型链 | 当前产品保留 Evidence / Decision 语义，未保留完整用户级结构 | WEAKENED | 恢复为会议内部结构和来源链，不直接恢复旧标签控制台 |
| Proposal / Decision | `34 会议与决策智能系统:47`；`backend/tests/test_meeting_runtime.py:73` | 讨论必须形成可审阅提案，由 CEO 作最终选择 | 提案、采用、修改、暂停、转任务 | 当前 Runtime 可生成 Proposal，且 CEO 决策后才生成 Commitment；测试覆盖 APPROVE / REJECT / DEFER | 当前 Page Map 有会议结论与决定；正式前台未完整接线 | WEAKENED | 高价值能力，应回收为 CEO 决策链 |
| Action / Assignment / Owner / Deadline / Checkpoint | `14 会议室开发规格:200` 起、`Product Bible 09 会议室:198` 起 | 决策后谁做、何时做、如何反馈 | 会议结论转项目任务，指定负责人和执行反馈 | 当前 Commitment、Cycle Assignment、Handoff 和 Owner 机制存在；会议页未完整接通 | 当前 CEO 工作台和 Workspace 定义了负责人、下一检查点和责任 | WEAKENED | 回收为 CEO 待处理事项和 Workspace 责任，不回到 Task-first 一级入口 |
| 引用资料 / 会议上下文 | `Product Bible 09 会议室:137` 起；`34 会议与决策智能系统:195` 起 | 会议必须基于项目资料、Memory、Knowledge、数据和历史决定 | 会前自动准备背景、资料、风险和历史会议 | Memory / Knowledge 服务和引用测试存在；未发现会议专属自动上下文与完整引用展示 | 当前 Page Map 保留资料引用；正式会议 UI 未完成 | WEAKENED | 候选恢复，挂接资料库、来源和会议检查器 |
| 多员工讨论 / 辩论 / Reviewer / Moderator | `34 会议与决策智能系统:245` 起 | 不同 AI 员工需要提出、质疑和评审方案 | Meeting Moderator Agent、观点模式、辩论模式、评审模式 | 未发现当前完整 Moderator / Debate / Reviewer 会议 Runtime；Strategy Room 主要启动 Task 简报 | 仅历史规格、原型和目标性描述 | MISSING / LEGACY_ONLY | 只恢复“多角色分析”用户价值，不恢复多 Agent 控制台架构 |
| 会议结果回写 | `34 会议与决策智能系统:47` 起 | 决策需要进入执行、反馈和历史追踪 | Decision → Task → 执行反馈 | Workspace Runtime 已有 Evidence、Acceptance、Decision、Handoff；Meeting → Result → 下一轮调整尚未闭合 | 当前产品保留结果、反馈、复盘方向，会议页未闭环 | WEAKENED | P0 候选，必须能回到来源 Workspace 和 CEO 工作台 |
| Workspace Studio | `docs/01_Product/Curis_Product_Reasoning_Record.md:731` 起 | 用户 / 业务工程需要把业务意图变成可运行办公室 | `Discover → Blueprint → Compose → Bind → Staff → Simulate → Approve → Operate` | 当前 `frontend/app/ceo-office/workspace/studio/page.js:21` 起有生命周期、模板、岗位、能力、证据、失败路径；真实 Runtime Workspace API；`frontend/tests/runtimeWorkspaceUi.test.mjs:108` 起有验证 | 当前 Page Map、Visual Master Map 和正式代码均保留 | WEAKENED | 能力并未消失，但目前主要完成 Draft 创建和候选装配 |
| Workspace Builder / Renderer | `Product Bible v1.0/19 工作区渲染引擎（Workspace Renderer）.md:9` | 不同行业需要不同工作对象、模块、布局和节奏 | Business Definition → Project Template → Renderer → Workspace | 当前 RD / XHS / TTK 模板可生成阶段、岗位、能力和模拟场景；当前共享 Runtime View 和对应测试存在 | 当前 Blueprint / Master Map 保留“Workspace 可以不同”；历史通用 Renderer 只部分保留 | WEAKENED | 回收为业务 Workspace 装配能力，不恢复旧 Project Workspace |
| Workspace 修改 / 扩展 / 升级 / 回滚 | `Curis_Business_Runtime_Definition_v0.1.md:689` 起，尤其 `:718` | 已运行办公室需要安全修改，且不破坏当前运行版本 | Draft Version / Active Version、影响分析、重新模拟、批准、14 天回滚 | 当前已有 Workspace Version、Approval、Rollback 和相关测试；Studio 前台主要仍是一次创建入口 | 当前产品方向保留版本、差异、模拟和恢复原则 | WEAKENED | P0 候选，补齐持续装配和演进闭环 |
| Goal / Outcome / Review | `Curis_Business_Runtime_Definition_v0.1.md`、历史 Project / Goal 规格 | 用户要知道目标、结果、是否达成以及下一步 | Goal → 工作 → 结果 → 验收 → Review | 当前 Workspace Cycle、Acceptance、Decision 和内容复盘部分存在 | 当前产品已将 Outcome、Result、Review 纳入业务语言 | WEAKENED | 统一到 Workspace 结果链，不恢复旧 Goal / Project 控制台 |
| Memory / Learning / Lessons | `Product Bible v1.0/22 Memory 系统`、`docs/01_Product/Curis_Product_Reasoning_Record.md`、历史 Evolution 规格 | 公司要从结果和失败中变好 | 经验、历史决定、执行模式和可复用 Lesson | 当前 `backend/app/memory_service.py`、`backend/app/memory_api.py`、`lesson_memory.py`、`capability_lessons`、Evolution Governor 和测试存在 | 当前资料库 / 记忆区存在；面向 CEO 的复盘后改进入口仍弱 | WEAKENED | P1 候选，连接结果、复盘、知识和下一轮经营 |
| Handoff / Continuity | 历史 AI Secretary、长任务和项目记忆规格 | 责任不能因异步执行、跨员工或中断而丢失 | 交接快照、责任转移、上下文连续性 | 当前 Runtime Handoff、Task Handoff、Recovery 和 Workspace Cycle 证据存在 | 当前 Page Map 定义交接、返回和恢复；前台仍需普通用户化表达 | ACTIVE（下沉） | 继续保留底层，不新增技术一级入口 |
| Notification / Intervention | 历史 AI Secretary、后台研讨和长任务规格 | 用户应在需要决定、接管、恢复或查看时被通知 | 完成通知、风险通知、人工接管和提醒 | 当前 Global Assistant、通知状态、Pending Decision、Handoff 机制存在；`strategy-room` 有待开始 / 进行中 / 已结束状态 | 当前 Page Map 保留通知 / 待处理 | WEAKENED | P1 候选，统一进入 CEO 待处理 |
| Recovery | 历史自动推进、超时、重试、人工接管和恢复门禁规格 | 失败不能伪装成成功，用户需要知道如何恢复 | 重试、暂停、人工接管、降级和返回原上下文 | 当前 Runtime Recovery、Cycle Resume、Rollback、Task Execution Control 存在 | 当前产品明确失败、恢复、回退是完整能力 | ACTIVE（下沉） | 保留机制，面向用户显示原因、影响、负责人和恢复动作 |
| Schedule / Automation | 历史 Scheduler、Task Graph、后台研讨和会议通知设计 | 工作可稍后运行，完成或失败后继续处理 | scheduled / event / condition、后台执行、完成通知 | 当前 `backend/app/scheduler.py`、`task_graph.py`、strategy meeting status 和通知底座存在 | 当前 Page Map 有日历、通知与待处理；会议自动化链未完整 | WEAKENED | P2 候选，先支持延后、提醒、完成通知和失败接管 |
| Project / Task / Workflow execution substrate | 历史 MVP 和大量当前实现 | 需要真实执行、任务状态、结果和审计 | Project → Task → Workflow → Artifact | 当前正式代码、数据库、API、测试均大量存在 | 当前产品明确 Task 是内部执行事实，不是默认入口 | ACTIVE（底层） | KEEP INTERNAL；不作为历史能力回收的一级产品入口 |
| 自由拖拽装修画布 / Runtime 控制台 | 历史 UI / 工程化设计 | 主要解决工程配置和内部观测问题 | 画布、状态机、Gate、Simulation 控制面 | 无需恢复；当前 Studio 已采用受业务语义约束的装配器 | 当前产品原则明确 Runtime 下沉，Studio 不是自由画布 | REJECTED | DO NOT RESTORE |

## 4. 结构化会议专项结论

### 4.1 历史会议不是普通聊天

历史 Meeting Room 与 Meeting Intelligence 规格都明确规定：

```text
复杂问题
→ 召集参与者
→ 多角色分析
→ 事实 / 观点 / 证据 / 风险
→ 提案
→ CEO 决策
→ 责任与任务
→ 执行反馈
→ 结果回写与下一轮调整
```

历史能力覆盖：

- Conversation / 讨论；
- Fact、Opinion、Question、Risk；
- Evidence 与引用资料；
- Proposal；
- Decision；
- Action、Assignment、Owner、Deadline / Checkpoint；
- 参与员工、@员工和会议上下文；
- Company Meeting 与 Workspace Meeting；
- 结果、反馈、任务生成和历史追踪；
- 实时会议与后台研讨。

### 4.2 当前实现证据

- `backend/tests/test_meeting_runtime.py:46-83`：创建会议、准备、开始讨论、写入 `FACT`、生成 Proposal；
- `backend/tests/test_meeting_runtime.py:86-115`：只有 CEO `APPROVE` 才产生 Commitment，`REJECT` 不产生 Commitment；
- `backend/tests/test_meeting_runtime.py:117-141`：Proposal 可保持开放，`DEFER` 不产生 Commitment；
- 当前 Runtime 实体类型包含 `EVIDENCE`、`HANDOFF`、`ACCEPTANCE`、`DECISION_PACKET`、`MEETING`、`COMMITMENT`；
- `backend/app/database.py:5997-6077`：仍存在 tenant-scoped `strategy_meetings` 的保存、查询和列表 API 数据层；
- `frontend/app/ceo-office/strategy-room/page.js:18-24`：战略会议室可读取真实后端会议数据，并通过 `TaskLauncher` 执行 AI 简报；
- `frontend/app/ceo-office/meeting/page.js:6-16`：当前普通会议入口仍是“规划中 / v1 暂不建设”的占位页。

### 4.3 会议专项判定

结论：**WEAKENED，不是 MISSING**。

会议后端已经保留了 Proposal、CEO Decision、Commitment 的一部分业务链；但前台没有呈现结构化讨论，也没有完成资料引用、参与员工、多角色分析、行动责任和结果回写。因此不能把当前 Meeting Runtime 测试或 Strategy Room 页面描述为完整会议产品。

建议回收：

- 先恢复“事实、证据、提案、决定、责任、反馈”的连续性；
- 再恢复多角色分析和后台研讨；
- 会议主语义使用普通用户可理解的“讨论、依据、建议、决定、负责人、下一步”；
- Fact / Opinion / Evidence 等作为结构和来源层，不强迫 CEO 学习内部对象名；
- 会议结果必须回到来源 Workspace / CEO 工作台，并显示下一检查点。

## 5. Workspace Studio 专项结论

### 5.1 能力没有被删除

当前 Studio 页面保留：

- `Discover → Blueprint → Compose → Bind → Staff → Simulate → Approve → Operate`；
- RD / XHS / TTK 三类 Workspace 模板；
- Stage、Role Slot、Capability Binding；
- Evidence Rule；
- Failure Policy 与人工备用路径；
- Simulation Scenarios；
- CEO Explicit Approval Gate；
- Draft、候选岗位、未授权能力需求和 Runtime API 写入。

证据：

- `frontend/app/ceo-office/workspace/studio/page.js:21-131`；
- `frontend/app/ceo-office/workspace/studio/page.js:151-212`；
- `frontend/tests/runtimeWorkspaceUi.test.mjs:108-135`；
- `backend/app/runtime/workspace.py:76-130`：Workspace、Version 和候选组织的持久化；
- `backend/tests/test_p1_workspace_studio_runtime.py`；
- `backend/tests/test_wsp2_workspace_studio_versioning.py`；
- `backend/tests/test_runtime_workspace_foundation.py`。

### 5.2 当前缺口

当前 Studio 仍主要完成“创建第一份 Draft”，以下历史能力没有形成可持续产品闭环：

- 修改已有 Workspace；
- 复制或扩展 Workspace；
- Draft Version 与 Operating Version 的差异查看；
- 影响范围预览；
- 修改后自动使旧 Simulation 失效；
- 重新 Simulation、CEO Review、批准升级；
- 失败后恢复原 Operating Version；
- 由结果和复盘反向修改 Workspace；
- 将“业务工程装配”翻译为普通用户可理解的“这个办公室怎么工作”。

结论：**WEAKENED**。

这不是恢复旧 Workspace Renderer 页面，而是恢复 Workspace 的持续装配和演进能力。Studio 应成为业务空间的创建、修改、扩展、验证和升级入口；Runtime、Simulation、Role Slot、Capability Binding 和 Version 仍是底层实现与高级详情。

## 6. Goal / Result / Review

历史产品曾把 Goal、Project、Task、Workflow、Artifact、Review 分成多个工程对象。当前产品重定基线后，仍必须保留用户问题：

```text
用户要达成什么
→ 谁负责
→ 做了什么
→ 产生什么真实结果
→ 证据是否足够
→ CEO 是否接受
→ 下一轮改变什么
```

当前 Workspace Runtime 已有 Cycle、Evidence、Handoff、Acceptance、Decision 和关闭链；内容 Workspace 还存在发布回执、互动和结果反馈。但 Meeting → Result → Review → 下一轮经营尚未完整接线。

判定：**WEAKENED**。

重新安置位置：CEO 工作台、业务 Workspace、结果详情、会议和资料库；不恢复旧 Project / Task-first 一级导航。

## 7. Memory / Learning

历史资料中的 Memory、Lesson、Learning、Evolution 解决的是公司如何从执行结果变强，而不是模型私自训练。

当前证据包括：

- `backend/app/memory_service.py`；
- `backend/app/memory_api.py`；
- `frontend/app/ceo-office/knowledge/memory/page.js`；
- `backend/app/lesson_memory.py`；
- `backend/app/evolution_governor.py`；
- `backend/app/database.py:1421-1439` 的 `capability_lessons` 表；
- `backend/tests/test_mvp_phase6_s11_basic_memory_context.py`；
- `backend/tests/test_execution_engine.py:573-835` 的 Evolution Decision / Simulation 测试。

判定：**WEAKENED**。

当前底层能力真实存在，但产品没有完整表达：

- 哪个结果产生了什么经验；
- 哪条经验被复用；
- 哪次复盘改变了员工、能力、Workspace 或节奏；
- 哪些建议仍是未知或未验证。

建议 P1 回收为“结果复盘 → 经验沉淀 → 下一轮调整”，不恢复自动改码或自动演进控制台。

## 8. Handoff / Notification / Recovery

这些能力不应被误判为消失：

- Runtime Workspace 有 Handoff、Evidence、Acceptance 和 Recovery；
- `backend/app/task_execution_control.py` 有人工接管、接收、转派机制；
- `backend/app/runtime/workspace.py:1258-1696` 有 Handoff、Evidence、Acceptance、Resume 和恢复路径；
- Global Assistant 有通知状态和上下文；
- Pending Decision 有持久化、过期和 fail-closed 决策状态；
- Page Map 已定义“补充、批准、修改、接管、恢复、暂停、稍后处理”。

判定：**ACTIVE（底层能力）/ WEAKENED（用户表达）**。

建议 KEEP INTERNAL 作为 Runtime 机制，但前台统一表达为：

- 当前发生了什么；
- 影响是什么；
- 谁负责；
- 为什么等待或失败；
- 用户可以补充、批准、接管、恢复还是暂停；
- 完成后回到哪个业务 Workspace。

## 9. Schedule / Automation

当前存在：

- `backend/app/scheduler.py`；
- `backend/app/task_graph.py` 的 scheduled / event / condition 触发；
- Strategy Meeting 的 scheduled / active / closed 状态；
- Assistant 通知和待处理机制；
- 历史后台研讨、完成通知、超时、重试和恢复规格。

但没有证据证明当前已经形成完整的会议自动化产品链。因此判定为：**WEAKENED**。

建议 P2 只恢复最小用户价值：延后运行、完成通知、失败通知、人工接管和下一检查点。不要恢复一个新的 Automation 控制台或调度工程平台。

## 10. 分级建议

### P0：必须优先回收

1. 结构化会议主链：事实 / 依据 / 提案 / CEO 决策 / 责任 / 结果回写；
2. Workspace Studio 的持续演进：修改、版本差异、影响分析、重新模拟、批准升级、回滚；
3. 会议与 Workspace / CEO 工作台之间的来源、结果、责任和返回链；
4. 会议结果不能只停留在 Conversation 或 Proposal，必须产生可追踪的下一步。

### P1：完成公司经营连续性

1. 会议上下文自动准备：资料、Memory、Knowledge、历史决定、经营数据；
2. Goal / Outcome → Result → Evidence → Review → 下一轮调整；
3. Memory / Learning / Lesson 的结果驱动沉淀；
4. Handoff、Notification、Intervention、Recovery 统一进入 CEO 待处理；
5. 多员工分析、观点冲突和依据补充，但以普通用户语言呈现。

### P2：在主闭环稳定后补齐

1. 后台研讨和异步会议；
2. Schedule、Automation、提醒和完成通知；
3. 会议模板、Workspace 模板复制和业务变体；
4. 更丰富的历史搜索、引用和会议复用。

### KEEP INTERNAL

- Runtime；
- Workflow；
- Simulation；
- Gate；
- Role Slot；
- Capability Binding；
- Transition Log；
- Handoff 内部协议；
- Version / Rollback 实现细节；
- Task / Project / Workflow 执行底座；
- Evolution Governor 和自动改进安全门禁。

这些能力继续为真实性、权限、失败恢复和审计服务，但不恢复为普通用户的一级导航或默认操作对象。

### DO NOT RESTORE

- 旧 Project / Task-first 产品入口；
- 旧统一 Runtime 控制台；
- 自由拖拽装修画布；
- 要求 CEO 直接管理 Role Slot、Capability Binding、Simulation 状态机的 UI；
- 旧 Admin / Workspace 双系统；
- 以静态 Mock、Draft、API 200、Simulation 或候选构建冒充产品完成；
- 自动改码、自动演进或未经 CEO 决策的业务结构变化；
- 未经来源、授权、许可证和真实验证的外部 Agent 直接进入会议或 Workspace。

## 11. 建议重新安置位置

| 历史能力 | 当前产品位置 | 普通用户表达 |
|---|---|---|
| 结构化会议 | 会议 | 讨论、依据、建议、决定、负责人、下一步 |
| Fact / Opinion / Evidence | 会议详情 / 资料库 / 结果检查器 | 已知事实、不同看法、引用依据、仍未知 |
| Proposal / Decision | CEO 工作台 / 会议 / 决策室 | 建议方案、影响、请 CEO 决定 |
| Assignment / Owner / Checkpoint | CEO 工作台 / Workspace | 谁负责、做到哪、下一次检查 |
| 结果回写 | 来源 Workspace / 结果详情 | 结果是否达成、外部反馈、下一轮调整 |
| Workspace Builder | Workspace Studio | 创建或修改办公室怎么工作 |
| Workspace Renderer | 独立 Workspace 运行现场 | 不同业务拥有自己的工作对象和布局 |
| Memory / Learning | 资料库 / 结果复盘 / CEO 工作台 | 这次学到了什么、下次改变什么 |
| Handoff / Notification / Recovery | 待处理 / 异常 / Assistant | 需要补充、批准、接管或恢复什么 |
| Schedule / Automation | 日历 / 待处理 / Workspace | 何时运行、完成后通知谁 |

## 12. 最终判定

本次历史扫描确认：

1. Curis 过去确实设计过更完整的会议系统；当前会议能力是 **WEAKENED**，不是不存在。
2. Curis 过去确实设计过 Workspace Studio / Renderer；当前 Studio 底座仍在，但持续修改、扩展和升级能力未形成完整产品闭环。
3. 当前保留的 Runtime、Evidence、Acceptance、Decision、Handoff、Recovery、Memory 和 Version 能力不应被删除，也不应重新搬回技术控制台。
4. 当前真正需要回收的是业务连续性：讨论如何形成决定，决定如何产生责任，责任如何产生结果，结果如何推动 Workspace 和公司下一轮变化。
5. 所有恢复都必须经过当前普通用户产品原则重新安置，并重新区分“当前已实现事实”“目标产品契约”和“历史设计输入”。

最终原则：

> **不是恢复旧 UI，而是旧能力回收、新产品重新安置。**

本文件只作为后续产品架构 Review 的输入，不直接授权 Blueprint、UI、Runtime 或代码变更。
