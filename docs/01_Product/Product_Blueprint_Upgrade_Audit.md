# Curis Product Blueprint 升级审计工作稿

**Status: Review**  
**日期：2026-08-14**  
**性质：唯一 Product Blueprint 的升级审计工作稿，不是第二份 Blueprint，不是开发规范。**

## 1. 审计范围与权威关系

本审计先于 Blueprint 修改完成，使用以下材料：

1. 唯一正式产品定义：`docs/01_Product/Curis_Product_Blueprint.html`
2. 产品重新推导：`docs/01_Product/Curis_Product_Rethink_Reasoning_2026-08-13.md`
3. 产品母版：`docs/01_Product/Curis_Product_Master_Map.md`
4. 页面地图：`docs/01_Product/Curis_Product_Page_Map_v1.0.md`
5. 现有 UI 依赖识别：`docs/01_Product/Curis_Product_UI_Blueprint.html`
6. 上位约束：`docs/01_Product/Curis_Product_Context.md`、`docs/00_Context/CURRENT_STATE.md`、`docs/08_Change_Log/CHANGE_LOG.md`
7. 人才市场：`Curis_Talent_Market_Product_Map.md`、`Curis_Talent_Market_Integration_Contract.md`、`Curis_Talent_Market_Resource_Audit.md`

权威关系保持：

```text
产品重新推导 → Master Map → Page Map → 唯一 Product Blueprint → 唯一 UI Blueprint → Code
```

本轮不改变 Runtime、数据库或代码；UI Blueprint 只用于识别依赖，不在本轮修改。

## 2. 结论先行

当前 Blueprint 5.0 不是废弃品，经营闭环、结果真实性、Assistant、Workspace 和安全边界仍然正确；但它仍然以“公司经营系统 / Runtime 说明书”为主要阅读方式，尚未完整吸收 2026-08-14 的普通用户 Desktop App 重定基线。

本次升级的核心不是增加更多能力，而是重新排序产品真相：

```text
一级产品与用户动作
→ 页面与工作空间
→ AI 自动承担什么
→ 最后才是 Runtime、能力、状态和审计支撑
```

升级后，唯一 Blueprint 必须让普通用户先看懂 Curis 是什么、从哪里开始、六个区域各自负责什么；同时让设计和开发知道底层严谨性仍然存在，只是不能统治默认产品语言。

## 3. 差异审计

### 3.1 仍然正确，应保留

| 原定义 | 保留原因 | 升级处理 |
| --- | --- | --- |
| Curis 帮 CEO 建立、经营和发展 AI 公司 | 仍是产品身份和差异化核心 | 置于 Blueprint 首屏和主用户路径 |
| 单一 CEO、多个 AI 员工、Local Desktop 不等于低配 | 明确当前交付方式不能删能力 | 保留，改成普通用户可理解的产品承诺 |
| CEO Assistant 是第一位 AI 员工 | 是 Curis 与普通 Agent 工具的关键差异 | 作为全局公司角色和默认首页伙伴 |
| Company / Business / Workspace / Employee / Outcome 关系 | 形成公司经营连续性 | 保留为 Company OS 固定语义 |
| Workspace 是业务办公室、每个业务可有独立工作方式 | 是 Curis 的核心差异层 | 从“统一 Runtime 约束”改成“开放数字办公室契约” |
| 外部结果、证据、人工回填、CEO 验收 | 防止内部运行冒充业务成功 | 保留为每个业务的结果真实性底线 |
| 权限、外部副作用、失败回退、责任连续性 | 是可用产品而非演示壳的基础 | 下沉到高级说明和每个工作空间的启动 / 恢复契约 |
| 会议 → Decision → Commitment → 后续执行 | 公司经营闭环仍需要 | 用普通语言先表达，内部对象后置 |
| 公司成长、能力调整、知识沉淀 | 保证 Curis 不只是一次性 Agent 调用 | 放入公司长期循环和资料库 / 组织调整 |
| 成熟产品优先复用的方向 | 减少重复建设 | 新增正式复用原则和边界 |

### 3.2 已经过时，需要修改

| 旧表现 | 问题 | 新定义 |
| --- | --- | --- |
| 一级导航仍是“今日经营 / 经营 / 业务 / 公司 / 工作空间 / 公司资产 / 经营工具” | 与 Master Map 的六个一级区域冲突，且“公司资产”已过时 | 首页/CEO 工作台、业务空间、组织中心、人才市场、资料库、会议；设置下沉头像菜单 |
| 能力中心作为一级产品 | 能力中心是重要维护能力，但不是普通用户第一层心智 | 能力通过人才市场发现、上下文缺口进入、头像菜单设置维护 |
| “公司资产” | 把资料、成果、知识、经验、外部资料混成资产后台 | 统一改为“资料库” |
| 组织先有部门，再有岗位 / 员工 | 违背渐进式组织和人才市场契约 | Department 可选；员工可直接属于 Company，部门由重复责任触发 |
| 专家 / 员工 / Agent 交替使用 | 普通用户不知道外部专家何时成为公司成员 | 外部专家先是市场候选；招募并取得公司身份后才是 Employee |
| Skill 只是能力中心的普通资源 | 没有表达职业能力和岗位组合价值 | 加入“职业能力组合 / 岗位能力包”与人才模板 |
| 招聘与 Workspace 组队边界不够突出 | 容易复制身份或把市场候选当员工 | 招聘=外部专家→公司员工；组队=已有员工→Workspace 团队 |
| Workspace 仍用统一 Runtime / Stage / Cycle 组织首屏 | 产品看起来像统一任务流或控制台 | 只共享公司契约；每个 Workspace 拥有自己的 UI、工作对象、节奏、协作方式和结果窗口 |
| Runtime / Simulation / Gate 在主导航和主叙事中可见 | 内部可靠性模型反向定义产品 | 保留为高级 / 审计 / 实现层，普通用户使用“准备、工作、结果、问题、确认、下一步” |
| 产品由底层能力反推页面 | 容易变成先做能力货架 | 固定“一级产品→用户动作→页面→AI 自动化→底层能力” |

### 3.3 与 Master Map / Page Map 的冲突

| 发现 | 严重度 | 处理 |
| --- | --- | --- |
| 旧七项导航与六个一级工作区域不一致 | P0 | 以六区域为唯一正式导航，四个 CEO 意图入口只作为心智分组，不另起导航 |
| Blueprint 使用“公司资产”，母版使用“资料库” | P0 | 全文改为资料库；成果、经验和知识作为资料库来源 / 类型 |
| Blueprint 把能力中心写成一级中心，母版将人才发现与设置维护分开 | P0 | 人才市场负责发现；设置负责授权 / 维护；工作现场提供缺口返回入口 |
| Blueprint 的组织关系允许 Department / Office，未明确部门非强制 | P0 | 明确第一天可直接创建公司级员工，Department 按真实重复责任形成 |
| Blueprint 的 Employee / Professional AI / Workspace AI 有混用 | P0 | 固定“员工是具有公司身份的专家 / Agent”；Workspace AI 是员工在某办公室承担的工作视图，不是第二种员工 |
| Blueprint 的 Workspace Studio 偏统一阶段装配 | P1 | 保留装配、能力检查和 CEO 确认，但将运行现场定义为独立专业办公室 |
| Page Map 的“固定一级侧栏 + 上下文侧栏 + 主工作区 + 右侧检查器”尚未成为产品空间模型 | P1 | 正式加入 Blueprint，像素细节留给 UI Blueprint |
| Master Map 的成熟产品复用原则在 Blueprint 只有 EvoFlow 单一矩阵 | P1 | 扩展为成熟产品优先复用，同时保留来源、许可证、授权和 Adapter 边界 |

### 3.4 当前缺少的产品定义

Blueprint 需要新增以下正式章节：

1. 普通用户打开 App 的主路径，而不是先配置公司的工程路径。
2. 六个一级区域、头像设置菜单和四个全局入口的关系。
3. 人才市场作为公司外部能力生态，以及专家 / Skill / Connector 三个内部分区。
4. 外部专家→招募→公司身份→Employee 的完整路径。
5. Skill→岗位能力包→人才模板→员工能力→真实工作→成长的职业能力链。
6. 招聘与组队的明确分离。
7. 资料库替代公司资产后的来源、索引、引用、权限和自动沉淀职责。
8. Workspace 作为独立专业产品容器，而非统一 Runtime 页面。
9. 固定 Desktop 空间模型：一级侧栏、上下文侧栏、自由主工作区、按需检查器。
10. 产品反推能力方法，防止从底层对象反推页面。
11. 成熟产品优先复用矩阵和 Curis 自己必须建设的差异层。
12. 普通用户语言、高级 / 审计语言、内部实现语言三层术语边界。

### 3.5 过度工程化内容

以下内容不能删除，但不再应主导 Blueprint 首屏、一级导航或普通用户路径：

| 内部概念 | 继续保留的位置 | 普通用户默认说法 |
| --- | --- | --- |
| Runtime | 架构 / 高级详情 / 实现契约 | 工作正在进行、等待、失败、恢复 |
| Workflow | Workspace 内的自动协作实现 | 自动协作方式 |
| Gate / Capability Supply Check | 启动检查、设置和审计 | 现在还缺什么、怎么补 |
| Simulation | 高级装配和质量验证 | 开始前试运行 |
| Commitment | 结果和会议上下文 | 这轮答应做到什么 |
| RoleSlot / Position | 员工详情和工作责任映射 | 谁负责这件事 |
| Cycle | Workspace 内部工作轮次 | 这一轮工作 |
| Handoff | 责任交接证据 | 已交给谁、是否接住 |
| Acceptance | 结果确认 | 这次结果算不算数 |
| DecisionPacket | Assistant 的高影响决策材料 | 现在需要 CEO 判断什么 |
| Capability Supply | 高级能力供给检查 | 需要什么能力才能开始 |
| Truth / Change | 来源与公司变化审计 | 事实来源、发生了什么变化 |

## 4. 对现有 UI / 开发的影响

本轮不修改 UI 或代码，但 Blueprint 升级会成为后续拆 Issue 的产品依据：

### UI 影响

- 主导航需要从旧七项迁移到六个一级区域，设置移入头像菜单。
- “公司资产”页面命名和信息架构需要迁移为资料库。
- 人才市场必须成为独立一级入口；能力发现不能继续只藏在能力中心。
- Workspace 入口必须允许不同业务进入不同的专业 UI，不能用同一 Runtime 看板套壳。
- 全局布局遵循“左边我在哪里，中间我正在做什么，右边我正在看 / 修改什么”。
- 技术状态、内部 ID 和运行对象进入高级详情，不再占据默认首屏。

### 开发影响

- 后续开发队列应先实现六区域壳层和首个可感知价值，再补各类 Workspace 的专业工作面。
- 人才市场、组织中心、Workspace 的 Issue 必须分别定义发现、招募、员工化、组队和运行结果，不得合并为 Agent/Task 中心。
- 能力中心继续存在，但作为设置与上下文缺口入口；它不能单独代表员工已能工作。
- 旧 Project/Task-first 实现只能通过正式迁移 Issue 逐步替换，不能把 Blueprint 目标当作已交付事实。
- 所有外部专家、Skill、Connector 仍需来源、许可证、授权、健康、权限和真实结果边界；成熟复用不等于复制私有内容。

## 5. REVIEW REQUIRED：尚需 CEO 明确的真实冲突

以下不是本轮自行创造的新方案，而是材料之间仍需确认或后续冻结的选择：

1. **Blueprint 状态**：Master Map / Page Map 仍为 `REVIEW REQUIRED`，因此升级后的唯一 Blueprint 继续保持 `Status: Review`，不能宣称新产品方向已 Frozen。
2. **成熟产品复用边界**：可以复用公开接口、开源适配器和已授权连接；Workbuddy / Coze 等闭源私有专家、Prompt、知识和内部 API 不可直接复制。需要 CEO 后续决定每个外部来源采用“参考、Adapter 接入或官方连接”的策略。
3. **首批 Workspace 的产品化顺序**：研发、小红书、抖音仍是首批模板，但每个模板应独立形成专业工作面；具体先做哪个垂直工作面不在本轮擅自排序。
4. **四个 CEO 意图入口与六个一级区域**：本审计采用“六区是导航、四入口是心智分组”的解释；若 CEO 要求四入口直接成为导航，需要另行产品决策，不能在实现时自行混合。
5. **Talent Market 的外部来源深度**：公开 Agent / Skill / Connector 的发现和导入可进入产品，但具体来源白名单、许可证、更新策略和安全扫描门禁需在后续 Talent Market 设计 / Issue 中冻结。

## 6. 升级后的验收问题

唯一 Product Blueprint 修改后必须直接回答：

1. Curis 是什么；
2. 普通用户打开后从哪里开始；
3. 六个一级区域分别解决什么问题；
4. 专家从哪里来，如何成为员工；
5. 员工如何获得职业能力；
6. 员工如何加入多个 Workspace 组成团队；
7. 资料如何进入、被引用并自动沉淀；
8. 不同 Workspace 如何使用各自专业工作方式；
9. 公司如何得到真实结果并处理缺口；
10. 如何复盘员工、业务和能力并推动公司成长；
11. 哪些成熟能力直接复用，哪些能力由 Curis 建设；
12. 哪些内部状态只用于高级 / 审计 / 实现层。

## 7. 审计结论与执行结果

审计结论为：**可以升级唯一 Product Blueprint，不需要创建新 Blueprint，也不需要推翻原有经营闭环。**升级重点是产品入口、普通用户语言、人才市场、员工化、Workspace 开放性和资料库；结果真实性、权限、恢复、责任连续性和审计继续保留。

已在原文件 `docs/01_Product/Curis_Product_Blueprint.html` 内完成 v5.1 正式升级。本工作稿仍只保留差异依据和 `REVIEW REQUIRED` 项，不承担正式产品定义职责。

## 8. Workspace 产品模型追加审计（2026-08-14）

在 v5.1 冻结后，CEO 进一步明确 Workspace 的核心原语。该变化已原位合并进唯一 Blueprint，未创建 Workspace Blueprint 或 Automation Blueprint：

| 原表达 | 新正式表达 | 受影响的 UI / 产品语义 |
| --- | --- | --- |
| Workspace 是独立业务办公室，内部关系未展开 | Workspace = 专业业务应用 + 多 Employee Workstation + 责任驱动的 Agent Handoff | 研发、小红书、短视频必须拥有不同专业工作界面 |
| 员工是 Workspace 成员，Conversation 容易被理解为中央群聊 | 员工在 Workspace 拥有持续 Workstation；Conversation 分为 Assistant、Employee、Meeting、Workspace Thread | Workstation 位于 Main Workspace，可多个同时存在 |
| Context Sidebar 可承载员工或统一上下文 | Context Sidebar 只承载项目、Thread、资料、文件和业务对象；员工工作不进入侧栏 | Flexible Utility Pane 按当前对象变化，不是固定 Inspector |
| 自动化容易被理解为用户画 Workflow | Organization / Role / Responsibility 天然驱动 Agent Handoff | 用户看到责任、进度、等待原因和下一步，不画 DAG |
| 自动运行与手动操作是两种模式 | 自动流转与 CEO 介入共用同一 Employee Session | 可串行、并行、回退、重新分配、请求帮助和等待 CEO |
| Meeting 与运行链路分离 | Meeting / Decision 可中断并重新驱动来源 Workspace | Decision 产生 Action、Owner、Checkpoint 并回到办公室 |

本追加使 Blueprint 当前保持 `Status: Review`，并将 Workspace Model 标为 `Review Required`；UI Blueprint 只在产品语义确认后同步，不在本工作稿中授权开发。

## 9. 历史能力回收追加审计（2026-08-14）

依据 `docs/reviews/Curis_Capability_Recovery_Audit_2026-08-14.md`，本轮只把仍符合当前产品路线的能力补回唯一 Blueprint：

| 判定 | 处理 |
| --- | --- |
| 已完整承接 | 公司经营闭环、真实结果、权限、责任连续性、来源、CEO 确认、失败恢复、Handoff、Acceptance、审计，以及 Workspace 的开放专业 UI 与 Employee Workstation 模型不重复改写。 |
| 本轮补齐 | 结构化会议的 Question / Conflict / Evidence Source / 多员工观点与 Proposal 来源；Meeting → Decision → Assignment → Workstation → Result / Evidence → Review / Learning；Studio 的创建、复制、修改、扩展、影响预览、测试、升级与回退；Goal / Result / Review / Learning 的 Company / Business / Workspace 归属；Schedule、Notification、Handoff、Recovery 的用户表达。 |
| 继续下沉 | Runtime、Workflow、Gate、Simulation Engine、Task Graph、State Machine、Adapter、Trace、Retry Policy、DecisionPacket、RoleSlot、Capability Binding、Evolution Governor。它们支撑真实性、权限、恢复和审计，不成为一级产品入口。 |
| 明确不恢复 | Project / Task-first 入口、Runtime / Workflow Console、自由 DAG / 拖拽装修画布、旧 Meeting Room、独立 Memory / Evolution Center、旧 Admin / Workspace 双系统。 |

结果：唯一 Blueprint 仍为 v5.1、`Status: Review`；本轮未修改 UI Blueprint、Prototype、Runtime、Schema、数据库或代码。下一步只有在 CEO Review 通过后，才把受影响语义同步到 UI Blueprint，并另行形成实现 Issue。
