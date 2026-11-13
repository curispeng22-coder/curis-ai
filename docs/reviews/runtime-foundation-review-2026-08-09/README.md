# Curis Runtime Foundation Review（2026-08-09）

Status: Review  
Decision: `PASS_WITH_BASELINE_BLOCKERS`  
Product owner gate: `PASS_TO_RUNTIME_FOUNDATION_REVIEW`  

本文件记录产品负责人已批准进入 Runtime Foundation 评审及封闭 Backend 实施。`RUNTIME-FOUNDATION-001` 已完成授权范围内实现，并通过独立聚焦验证；Backend 全量仍保留输入快照前的基线失败，因此不把全量回归写成 PASS。三业务 Simulation、UI 和 Desktop 仍未开始。

## 1. 评审基准与目标

| 层级 | 当前权威 | 本次用途 |
| --- | --- | --- |
| Product | `docs/01_Product/Curis_Product_Blueprint.html`（v4.12，Review） | 确认公司经营目标、CEO 使用路径和三业务边界 |
| Runtime | `docs/01_Product/Curis_Business_Runtime_Definition_v0.1.md`（v1.6，Draft） | 确认对象、状态、责任、证据和失败路径 |
| Completion | `docs/07_Decisions/ADR-0041-business-runtime-completion-standard.md`（Frozen） | 确认不能用页面、接口或单测替代完整业务运行 |
| Current fact | `docs/00_Context/CURRENT_STATE.md`（Frozen） | 区分目标态与当前 Project/Task-first 交付事实 |
| Simulation | `docs/reviews/three-business-runtime-simulation-plan-2026-08-09/README.md` | 确认 FIRST-ARRIVAL、ORG、RD、XHS、TTK 场景与失败证据 |
| Product transfer | `docs/reviews/next-stage-product-plan-evoflow-2026-08-09/README.md` | 确认能力表达和便捷动线只作为 Company OS 的体验增强 |

本次评审目标不是继续扩展页面，而是回答：

> Curis 是否已经把“CEO 创建公司 → Assistant 组织 AI 员工 → Workspace 运行 → 外部结果 / 手动反馈 → CEO 决策”的最小运行内核定义到可以被实现、模拟、回放和审计？

## 2. 不变量（评审通过后仍然必须保持）

1. Curis 是 CEO 的 AI Company Operating System，不是 Agent、Task 或 Workflow 控制台。
2. `Company OS 固定，Workspace 开放`；研发工作台、小红书运营工作台、抖音 / TikTok 运营工作台共享内核。
3. CEO 是唯一真实人类用户；CEO Assistant 是 Company-level 唯一的第一位 AI 员工。
4. `AIEmployee` 是责任主体，`RoleSlot` 是业务岗位，`CapabilityBinding` 是岗位能力授权；三者不能合并为 Agent 卡片。
5. `State` 是持久化业务事实；旧 `workflow_runs` / `content_workflow_runs` 只能作为 `executionRef`。
6. 所有外部结果必须有 API 回执或 CEO 手动反馈，不能用估算值伪装成已验证事实。
7. 高影响动作必须升级 CEO：对外发布、花钱、外部承诺、权限变更、不可逆操作和扩大业务范围。
8. Blueprint、Agent、Connector、平台约束、ReplyPolicy 或 Evidence Rule 发生变化，旧 Simulation 必须失效。
9. UI、桌面壳和打包是 Runtime 通过后的消费层，不得反过来定义业务事实。

## 3. Runtime Foundation 必须覆盖的对象边界

| 对象组 | 必须证明的事实 | 评审结论 |
| --- | --- | --- |
| First Arrival | `FoundingRun → Company → CEO → CEOAssistant` 可确认、恢复、拒绝、失败；未确认前不产生假 Company | 定义已存在；实现 / 重启证据缺失 |
| CEOAssistant | 身份、Company 唯一性、Context 版本、生命周期、主动汇报、动作边界、升级、升级与换责区分 | 定义已存在；当前 Global Assistant 仍是旧 Snapshot / Task 链 |
| AI Organization | `CEO → CEOAssistant → Professional AIEmployee → RoleSlot → Workspace AI` 汇报与升级关系 | 定义已存在；当前 Employee CRUD 不能证明目标组织 Runtime |
| CapabilityBinding | 岗位能力、授权状态、effect class、容量、撤权、缺能力和退回 | 定义已存在；目标 `orgVersion` 链仍无运行证据 |
| Business / Workspace | 三业务共享引擎，Workspace Blueprint / Stage 可版本化，运行版本与草稿分离 | 定义已存在；当前门户仍由 Project 派生 |
| Cycle / Handoff | 周期目标、输入、Owner、输出、下一 Owner、退回、失败和关闭 | 定义已存在；跨对象 Handoff 证据缺失 |
| DecisionPacket | 事实、观点、建议、风险、候选方案、CEO 决策、回滚原因 | 定义已存在；尚无目标 Runtime 记录 |
| Acceptance / Evidence | `verificationStatus` 与 `evidenceCondition` 正交；外部回执 / CEO 手动反馈带来源、时间、责任人 | 定义已存在；当前数据未形成统一证据链 |
| SimulationRun | 按 Company / Workspace / Scenario 查询、重启恢复、参与者、交接、失败、CEO 决策可回放 | 当前缺少目标聚合持久化 |
| Content Runtime | ContentItem、版本、审核、发布回执、互动和回复版本拥有独立状态与审计 | 当前旧内容运行链不能替代 |
| RD Runtime | 研发 Stage 业务状态独立于旧 workflow run；首个任务是“完善 Curis” | 当前旧研发运行链不能替代 |

### 3.1 当前现场证据（只读）

2026-08-09 对当前工作树与 `backend/data/curis.sqlite` 的核对结果：

| 证据 | 当前事实 | 对本评审的含义 |
| --- | --- | --- |
| `frontend/app/ceo-office/workspace/page.js` | Workspace 门户仍调用 `getProjects()`，并按 `project_type` 映射固定路由 | 当前页面不是目标 Workspace Runtime 的事实来源 |
| `frontend/app/ceo-office/page.js` 与 `frontend/components/assistant/GlobalAssistant.js` | CEO Desk / Assistant 仍以旧 Project、Task、Artifact 聚合为主要输入 | 可复用壳层与入口，但不能证明 CEOAssistant Runtime 已运行 |
| `backend/data/curis.sqlite` | `business_directions / commitments / workspaces / outcomes / assistant_identities / guide_sessions / runtime_transition_log` 均为 0；`employee_instances=1`、`department_instances=3` | 旧 CRUD 记录不能证明 AIEmployee / RoleSlot / CapabilityBinding 目标组织链 |
| 目标对象扫描 | 未发现目标 `SimulationRun`、`ContentItem`、`InteractionItem`、`FoundingRun` 持久化实现 | Foundation 仍是待实现的运行事实，不可用原型或空库补齐 |
| `desktop/target/release/bundle/macos/Curis.app` | 文件存在，最近现场时间为 2026-08-08 16:22；Tauri 壳仍启动本机 Node / Python sidecar | 只能证明已有打包路径，不能证明目标 Runtime 已进入可投入使用状态 |

现场证据与目标定义分离：本节不否定已有代码的可复用价值，只禁止将旧执行链、空表、静态原型或已有 `.app` 当作 Foundation 通过证据。

## 4. 状态与责任审查结果

### 4.1 状态入口

Runtime 必须只通过统一状态入口流转，禁止业务代码直接更新裸 `status`。每次流转至少保留：

```text
from → to → trigger → actor → at → reason → evidenceRefs → nextCheckAt
```

`actor` 只能是 `CEO / AI_EMPLOYEE / SYSTEM / EXTERNAL`。非法流转必须拒绝并可被测试验证。

### 4.2 正交状态

- `AIEmployee.lifecycleStatus`：雇佣关系和生命周期。
- `AIEmployee.presenceState`：可承接、工作中、等待 CEO、阻塞、暂停。
- `RoleSlot.status`：岗位配置与责任是否有效。
- `CapabilityBinding.status`：能力绑定、授权、撤权、过期。
- `Outcome.verificationStatus`：事实是否被采用。
- `Outcome.evidenceCondition`：证据新鲜度、冲突或缺失。

`BLOCKED` 不能被写成员工生命周期；`STALE` / `CONFLICT` 不能被写成成功结果；`WAITING_CEO` 不能被系统自动批准。

### 4.3 责任闭环

每条工作必须能够反查：

```text
CEOAssistant
→ RoleSlot
→ AIEmployee / CapabilityBinding
→ Cycle / Handoff
→ Stage / ContentItem
→ Evidence / ExternalReceipt
→ Acceptance
→ DecisionPacket
→ 下一周期
```

如果任一环节只能在聊天记录、页面状态或内存中存在，Foundation 不通过。

## 5. `RUNTIME-FOUNDATION-001` 评审范围

### 5.1 允许交付

1. First Arrival 与 Company Formation 的可持久化状态和恢复路径。
2. CEOAssistant、AIEmployee、RoleSlot、CapabilityBinding 的身份、汇报、授权、容量和版本关系。
3. 统一状态入口、审计日志、非法流转拒绝和迁移适配边界。
4. Cycle、Handoff、DecisionPacket、Acceptance、Evidence 的最小闭环。
5. SimulationRun 的创建、运行、失败、CEO 拒绝、恢复、重启和查询。
6. ContentItem / ContentVersion / ContentReview / PublicationReceipt / InteractionItem / InteractionResponse 的最小契约。
7. 研发 Stage Runtime 与内容 Stage Runtime 对旧执行链的 `executionRef` 适配。
8. Workspace Blueprint 版本、Simulation 失效和 Operating Version 分离。
9. FIRST-ARRIVAL-001、ORG-001、RD-001、XHS-001、TTK-001 的最小 fixture / 手动证据入口；fixture 结果必须保持 `UNVERIFIED`。
10. 针对上述对象的持久化、租户 / Company 隔离、重启恢复、状态、失败、回滚和反查测试。

### 5.2 明确不在本次范围

- 不改造 CEO Desk、AI Team、Workspace Studio 或运营办公室 UI。
- 不创建新的一级导航、第二套 Assistant、CRM 或 Agent 市场。
- 不接入真实小红书、抖音 / TikTok API。
- 不物理删除旧表、不迁移历史数据、不重写旧执行链。
- 不将 EvoFlow UI、代码、资源包或技术栈复制进 Curis。
- 不以桌面应用打包结果作为 Runtime 通过证据。

## 6. 评审门禁与决策

### 当前决策

产品负责人已给出：`PASS_TO_RUNTIME_FOUNDATION_REVIEW`。

这只代表允许开始本文件的产品 / Runtime 交叉评审，不代表允许立即开发。

### 评审通过条件

以下问题必须全部得到 `PASS`，才能创建正式实现 Issue：

| 检查项 | 必须回答 |
| --- | --- |
| 对象 | 每个对象的唯一性、Owner、输入、输出、下一阶段和归档规则是什么？ |
| 状态 | 每个状态的合法动作、触发者、拒绝和恢复路径是什么？ |
| 权限 | 哪些动作必须由 CEO 批准？AI 员工凭什么可以执行？ |
| 证据 | API 回执与手动反馈如何区分来源、新鲜度、验证等级和责任人？ |
| 版本 | 组织、能力、Workspace 或平台规则变化如何让旧 Simulation 失效？ |
| 失败 | 缺能力、过载、撤权、发布失败、外部数据延迟、CEO 拒绝如何结束？ |
| 隔离 | Company、Workspace、AI 员工和外部结果如何避免串租户、串业务？ |
| Simulation | FIRST-ARRIVAL、ORG、RD、XHS、TTK 各自的正常与失败证据如何生成？ |
| 迁移 | 旧 Project/Task/Workflow 如何仅作执行参考而不继续充当目标事实源？ |

### 评审结果枚举

- `PASS`：允许创建正式 `RUNTIME-FOUNDATION-001` Issue。
- `CHANGES_REQUESTED`：只修改 Blueprint / Runtime / Simulation 文档，不改代码。
- `BLOCKED`：保留门禁，补充缺失的定义、证据或授权。

## 7. 三业务 Simulation 顺序

Runtime Foundation 实现并通过独立 Review 后，按同一内核执行：

1. `FIRST-ARRIVAL-001`：空公司 → Company → CEOAssistant → 第一业务候选。
2. `ORG-001`：创建岗位、绑定能力、容量不足、撤权、退回、换责。
3. `RD-001`：研发工作台中的首个任务“完善 Curis”，包含提交、构建、测试、CEO 验收和失败。
4. `XHS-001`：小红书内容生产、CEO 审核、授权 / 手动发布、反馈回流和复盘。
5. `TTK-001`：抖音 / TikTok 视频生产、发布、结果回流或 CEO 手动录入、交易 / 价值反馈。

三业务必须各自产生 `SimulationRun`，但不能复制三套 Company OS、Assistant 或组织系统。

## 8. 桌面应用交付路线

桌面应用不是另一个产品层，而是 Curis Company Runtime 的本地交付壳。当前现场事实：

- `desktop/` 已存在 Tauri 2 工程；
- 当前存在 `desktop/target/release/bundle/macos/Curis.app`，但这只能证明曾经打包过；
- Tauri 壳当前通过本机 Node / Python sidecar 启动旧前端与后端；
- 当前 `frontend/` 仍是 Project/Task-first 基线，不能把现有 `.app` 描述为目标 Runtime 已投入使用。

正确交付顺序：

```text
Runtime Foundation Review PASS
→ 正式 Issue 授权
→ Foundation 实现与测试
→ 三业务 Simulation PASS
→ UI / 导航 / Assistant 迁移 Issue
→ 桌面壳接入目标前端与真实 Runtime
→ .app 启动、重启、数据隔离、升级、失败恢复验证
→ 可投入使用的桌面发布包
```

桌面发布的最终验收必须额外证明：

- 双击启动后前后端就绪，窗口不白屏；
- 关闭 / 崩溃后 sidecar 可回收，不留下孤儿进程；
- 数据目录、Company 身份、模型密钥引用和日志不泄漏；
- 目标前端来自已通过 Runtime / UI Review 的版本；
- 空公司首次进入、CEO Assistant、三 Workspace、结果反馈和恢复路径均可在 `.app` 内完成；
- 打包产物、启动脚本、版本号、数据库迁移和回滚说明可复现。

## 9. 当前下一步

现在进入 **Runtime Foundation 产品 / Runtime 交叉评审**。在评审结论产生前：

1. 继续补齐本文件中未回答的对象、状态、Owner、证据和失败定义；
2. 不改 `frontend/`、`backend/`、`desktop/` 业务实现；
3. 不把当前 `.app` 或原型截图写成目标产品已完成；
4. 评审通过后，再创建带明确文件清单、验收条件和回滚方式的正式 `RUNTIME-FOUNDATION-001` Issue。

## 10. 指定开发会话的只读交叉审查回传

指定代码会话 `019faa67-53e0-7f82-9f36-c04def66c63e` 已完成只读对照，并明确反馈“本轮未修改代码、数据库或文档”。回传结论已纳入本 Review：

### 10.1 新增的评审阻塞项

1. 当前工作树与批准基线不一致：批准基线为 `main @ c0e1855f446a55aa3a384006cfcfed9877130338`，现场 HEAD 为 `dd77c672428999b5d96868c0380313eab53f31f9`，且 Backend、Frontend、产品文档和 Desktop 均有未提交改动。
2. Blueprint、Runtime Definition、Current State 和本 Review 相关目录尚未冻结到一个可引用的 Git SHA；正式 Issue 不能只引用本地工作树。
3. Foundation 范围在不同文档中存在冲突：本 Review / Content Review 要求完整 First Arrival、AI Organization、CEOAssistant、Cycle、Content Runtime；Simulation Plan 的执行准备段曾缩小为内容对象和 SimulationRun。为保证 FIRST-ARRIVAL 与 ORG Simulation 有运行基础，本 Review 采用**完整 Foundation 范围**，以本文件 §5.1 和 Draft Issue 为准。
4. Runtime PASS 与 UI Browser Evidence 属于两个阶段：Foundation / 三业务阶段先证明状态、责任、证据和回放；UI 迁移后再补真实人类浏览器证据。两者均通过后，才可宣称产品能力完成。
5. 现有实现仍有契约漂移：`StageSlot` 历史注释称“9 槽位”（目标为 8 个语义槽位、Produce 可拆 1～N Stage）；`EvidenceGrade` 将 `ABNORMAL` 与验证等级混合（目标要求与 `evidenceCondition` 正交）；旧研发 / 内容链仍存在直接写 `status` 的路径。
6. 活动 `data/curis.sqlite` 当前不存在，`backend/data/curis.sqlite` 的目标运行表为空；实现前只能使用临时数据库完成 fresh / upgrade / restart 验证，不得直接修改现有数据库。

### 10.2 实现授权前的封闭文件清单

候选 Issue 已单独记录在 `issues/20260809_runtime_foundation_001.md`。其建议清单为：

- 现有：`backend/app/database.py`、`backend/app/runtime/__init__.py`、`models.py`、`states.py`、`state_machine.py`、`registry.py`、`store.py`；
- 新增：`backend/app/runtime/foundation.py`、`simulation.py`、`legacy_execution_adapter.py`；
- 新增测试：`backend/tests/test_runtime_foundation_state_contracts.py`、`persistence.py`、`isolation.py`、`simulation.py`、`legacy_adapter.py`；
- 治理同步：本 Review、`CURRENT_STATE.md`、`CHANGE_LOG.md`，以及正式 Review 记录。

清单外的 `backend/app/main.py`、`frontend/`、`curis-ui-prototype/`、`desktop/`、活动数据库、旧研发 / 内容运行模块和真实平台 API 均不在授权范围内；若适配器无法接入旧链，必须先提交 Issue Amendment。

### 10.3 当前 Review 结论

当前评审结论为 `PASS_WITH_BASELINE_BLOCKERS`。产品负责人此前的 `PASS_TO_RUNTIME_FOUNDATION_REVIEW` 已被执行为评审；完整 Foundation 范围、Runtime / UI 两阶段顺序、输入快照和封闭文件清单均已形成。指定代码会话已按授权清单完成 Foundation，实现席回传的聚焦回归为 27 passed；本地独立复核运行 11 项 Foundation 测试与兼容联合回归，结果为 27 passed。Backend 全量仍为 1267 passed、31 failed、2 skipped，失败属于输入快照前的 Model Gateway / `.env`、旧执行绑定及前端断言漂移，未纳入本 Issue。

- 不得修改 Issue 清单外文件；
- 不得把 Runtime 实现结果宣称为 UI 或桌面产品完成；
- 必须使用临时数据库并回传测试、Simulation 和恢复证据。

## 11. Backend Runtime Foundation 实施回传

2026-08-09，指定实现会话按最终 `INPUT_SNAPSHOT_2026-08-09.md` 完成封闭 Backend 实施：

- 增加持久化 Runtime Entity / Link / SimulationRun / Workspace Version 与统一审计字段；
- 增加 FoundingRun、CEOAssistant、AIEmployee、RoleSlot、CapabilityBinding、Cycle、Handoff、DecisionPacket、Acceptance、ContentItem、InteractionItem 和 SimulationRun 状态契约；
- Company 唯一 CEOAssistant 由数据库唯一索引保证；Company 创建、Assistant 创建、FoundingRun 流转和反查关系使用同一 SQLite 事务；
- `verificationStatus`、`evidenceCondition`、`exceptionStatus` 与生命周期分离；fixture 证据禁止升级为 `VERIFIED`，也不能使 Simulation 通过；
- 旧研发 / 内容执行只保存 `executionRef`，不会反写 Foundation 生命周期；
- Blueprint、Stage、Agent、Organization、Capability、Connector、平台约束、ReplyPolicy、Evidence Rule 变化会使旧 Simulation 失效，但不覆盖历史运行。

验证结果：

- 聚焦与兼容联合回归：`27 passed`；
- Backend 全量：`1267 passed, 31 failed, 2 skipped`。31 项失败集中于输入快照前既有 Model Gateway / `.env` 默认值漂移、旧数字员工绑定链、旧前端文案断言及相关联失败，均不在本 Issue 授权文件范围；不得在本 Review 中伪装为全量 PASS；
- 临时 SQLite：`/tmp/curis-runtime-foundation-acm2y3fg/`；fresh / upgrade 语义 schema 一致，重复初始化通过，两个数据库 `pragma integrity_check=ok`，重启反查和跨租户 fail-closed 通过；
- RD-001 Foundation-level Simulation 证据：`PASSED / PASS`，3 条聚合状态引用；五个批准场景的 fixture 入口由聚焦测试覆盖，fixture 始终 `UNVERIFIED`。

独立复核结论：`PASS_WITH_BASELINE_BLOCKERS`。允许进入下一阶段的 FIRST-ARRIVAL / ORG / RD / XHS / TTK Runtime Simulation；仍不得进入 UI / Desktop 迁移，直到五个场景形成独立 Simulation Review 证据。Backend 全量的 31 项基线失败保持原样，必须另立 Issue 才能修复。
