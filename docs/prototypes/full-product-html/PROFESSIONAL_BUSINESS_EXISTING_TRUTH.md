# PROFESSIONAL_BUSINESS_EXISTING_TRUTH

> 用途声明：本文是 HTML 设计原型（Content Growth 与 RD professional workspace fixtures）的**输入摘要**，仅汇编既有项目权威与原型证据；不是新 Product Truth，不得据此发明产品规则。所有结论以引用路径的原文为准。路径根 = `/Users/yy/Documents/Curis AI Workspace/`。

## 权威优先级速览

- 最高结构权威：`docs/01_Product/CURIS_PRODUCT_STRUCTURE_BASELINE_PRE_DESIGN_RESEARCH.md`（CURRENT / Frozen / Structure Authority，2026-09-10；§15：下游设计研究必须先读本基线，冲突时 STOP / REPORT）。
- 跨业务共享语义：`docs/03_Design/Curis_Company_OS_Shared_Authority.md`（Frozen §0–§9 + 2026-09-09/09-10 顶部 Current 修订段）。
- Content Growth 域：`docs/03_Design/Curis_Content_Growth_Domain_Authority.md`（Frozen，高于 Instance Spec、低于 Shared Authority）。
- 视觉：**FINAL UI MASTER: PAUSED — COMPETITIVE DESIGN RESEARCH REQUIRED**（Structure Baseline §13）；任何原型不得宣称视觉已批准。

---

## A. Content Growth / 内容增长

### A1. Department / Business / Workspace 命名与关系（fixture 应使用的名字）

- 产品层级固定 `Company → Department → Business → Workspace`；Workspace 是唯一 canonical user/product identity。来源：`docs/03_Design/Curis_Company_OS_Shared_Authority.md` §9 + 2026-08-24 CEO reconciliation（`docs/reviews/CONTENT_GROWTH_CEO_AUTHORITY_DECISION_RECONCILIATION.md` §1）；`docs/03_Design/Curis_Content_Growth_Domain_Authority.md` §0.1/§1.1。
- `Office` 已退出当前用户产品语义，仅历史/迁移 provenance；`office_id`、`OfficeAccountBinding` 不迁移（Domain Authority §0.1、§3 `OFFICE_UNDER_COMPANY_AND_NOT_ORG`）。
- 内容增长是 **Professional Workspace Candidate**，不是 Verified Professional Workspace（CEO Reconciliation §1.2）。
- XHS / 抖音 / TikTok / YouTube / Bilibili 是 **Channel**，具体账号是 **Channel Account**；`Channel ≠ Workspace ≠ Channel Account`（Domain Authority §1.2）。fixture 中不要把「小红书」写成 Workspace 身份。
- D 代原型（2026-08-18，七区时代）使用的命名，fixture 应沿用：
  - Department：**内容增长部**（「一组内容类业务的最小管理单位」）。
  - Businesses：**小红书运营**（母业务）、抖音运营（占位）、公众号运营（维护中）。来源：`curis-ui-prototype/department-business-work-surface-2026-08-18/CURIS_DEPARTMENT_BUSINESS_WORK_SURFACE_UX_EXPLORATION.html` state-2/state-4。
  - Workspace 实例（D 代 coverage 原型）：**AI 科技**（小红书运营业务下的工作空间，Leader 陈真）。来源：`curis-ui-prototype/coverage-exploration-2026-08-17/09-xhs-workspace.html`。

### A2. Team / Leader / 成员

- Leader 语义：Leader 是普通 Employee 的 Leadership Role（`Employee × Role × Scope` Assignment），不是新 Employee 类型；Workspace Leader 同时承担业务领导力（a）与「仅异常介入任务路由」（b）两层正交语义。来源：Shared Authority §0.1、§9.1A、§9.2。
- 关系链：Department Leader 周宁 → Business Leader 陈真（小红书业务负责人）→ Workspace Leader 陈真（AI 科技工作空间负责人）。同一 Employee 可兼任多 Scope（Shared Authority §0.1）。
- 成员 fixture 名（来自 D 代原型，均为 **DESIGN FIXTURE**，项目未给正式员工花名册）：
  - 周宁 · 内容增长部部长 · 跨平台节奏统一/公私域联动（dept HTML state-2）
  - 陈真 · 资深运营 / 小红书业务负责人 / AI 科技工作空间负责人（dept HTML state-2/state-4；09-xhs-workspace.html）
  - 苏晴 · 视觉（封面 + 排版）（dept HTML state-4）
  - 何川 · 数据分析 · 选题归因（dept HTML state-4）
  - 林月 · 排版助理（跨 Workspace 复用）；在 09-xhs-workspace.html 里兼 调研/文案 两工位行
- 早期研究文档的另一组角色词汇：王颖(Research&Intel)·李想(Producer)·陈帆(Channel Operator)·周明(Strategist)（`docs/Content_Growth_Professional_Workspace_Research/CONTENT_GROWTH_CEO_OPERATING_STATE_MODEL.md` 头注）。**两组名字并存属于原型 mock 差异，非权威冲突**；fixture 建议统一用 D 代（2026-08-18）一组。

### A3. 每成员 Responsibility（一句一条）

- 周宁：跨平台节奏统一、公私域联动（dept HTML state-2「当前责任」）。
- 陈真（业务/Workspace Leader）：统筹 AI 科技工作空间目标、内容节奏、团队结果与下一轮经营（09-xhs-workspace.html）；业务级：8 月种草节奏、选题 vs 转化归因（dept HTML state-4）。
- 林月：AI 工具实测数据收集（调研）；AI 工具测评稿文案起草（文案）（09-xhs-workspace.html emp-row）。
- 苏晴：封面风格、视觉规范（09-xhs-workspace.html；dept HTML「视觉 · 封面 + 排版」）。
- 何川：数据分析、选题归因（dept HTML state-4）。
- 结构规则：Surface/流程只声明 Responsibility，不直接绑 Employee；WHO 由 ⑥Requirement→⑦Routing→⑧Service 解析（Shared Authority §1–§3、§9.2 `SURFACE_DECLARES_RESPONSIBILITY_NOT_EMPLOYEE`）。

### A4. Operating Model / Work lifecycle

- Frozen 主价值链（唯一权威措辞）：**Opportunity → Intent → Target Account Set → Content Variant → Publication**。`docs/03_Design/Curis_Content_Growth_Domain_Authority.md` §1.3–§1.5、§2。
  - Content Opportunity（信号，source/topic/score）；Content Intent（WHY/WHAT/GOAL，禁存推理/Prompt/CoT/中间草稿）；Target Account Set（账号粒度，Effective = Default Set + AI Recommendation + Manual Override；Target ≠ Eligibility）；Content Variant（per-Account，HIGH_REUSE / FULL_DIVERGENCE）；Publication（per-Account 唯一真相源，回执来自 Connector）。
  - 关键 Invariants：`INTENT_EXCLUDES_INFERENCE`、`TARGET_NE_ELIGIBILITY`、`PUBLICATION_PER_ACCOUNT_TRUTH`、`FACT_NOT_ROLLED_BACK`、`DISTRIBUTION_POLICY_IS_UNIQUE_SOURCE`（BEST_EFFORT/ALL_REQUIRED）、`OAUTH_FAILURE_KEEPS_ACCOUNT`、`NO_CROSS_ACCOUNT_CONTEXT_LEAK`、`SCHEDULING_IS_CONDITIONAL`、`UNKNOWN 是合法事实状态`（Domain Authority §3、§5）。
- 团队运转（Team Operating）默认流程的产品语言（D 代原型原文）：**选题 → 调研 → 文案 → 视觉 → 发布**（09-xhs-workspace.html `.team-op`；`A→B` 只表示默认下一 Responsibility，不是强制 DAG——`docs/reviews/BUSINESS_WORK_SURFACE_PAGE_CONTRACT.md` §5）。
- 早期 Reference 八阶段闭环（Growth Intelligence → Opportunity → Strategy/Intent → Target Account Routing → Account-aware Production → Channel Operations → Unified Growth Feedback → Next Cycle）：`docs/03_Design/Curis_Content_Growth_Operating_Model.md` §G。该文属于 Reference 时代（仍用 Office 词汇），fixture 只可借用阶段词汇，不得把 Office 画成产品身份。

### A5. Professional Surfaces 清单与每 Surface 的 Main / Context / Utility

权威 Surface 列表（B 代 multi-surface 原型，产品层级为 业务空间/内容增长部/小红书运营）：

- 列表：**经营总览 / 研究与洞察 / 内容运营 / 增长与评估 / 反馈 / 商业化**。定义与评审：`docs/reviews/CURIS_MULTI_SURFACE_PROFESSIONAL_WORKSPACE_UX_REVIEW.md`（Status: Review / DESIGN CANDIDATE, 2026-08-22, STOP FOR CEO VISUAL REVIEW）；截图证据 `docs/reviews/multi-surface-workspace-screenshots/`（01-research…16-prototype-1280）与 `docs/reviews/multi-surface-workspace-screenshots/prototype/`；独立确认：`docs/research/system_competitive_research/CURIS_CURRENT_UI_AUDIT.md` §「B 代」。
- 结构规则：Main = selected Professional Surface + Shared Work Area；Domain Navigation 仅在 Context Pane 出现，Main Header 不重复 Surface Tabs；Context 收起后用 context-recovery 条恢复（UX Review §1/§3）。
- 每 Surface 的 Main 对象 / Context / Utility（综合 UX Review 状态表 + 截图 + D 代 09-xhs-workspace.html）：
  - 经营总览：Main = 当前经营五要素（经营状态/本轮重点/最新判断/下一步/需要关注，09-xhs-workspace.html `.ws-shell-op`）+ CEO Operating Result 投影；Context = Workspace/Surface indicator；Utility = Employee Quick Panel。
  - 研究与洞察：Main = 趋势/竞品/受众对象卡 + 可点击 Handoff（「交接至 内容运营：生成 3 个实测选题」）；Context = 信号/选题库；Utility = Employee Quick Panel。
  - 内容运营：Main = 对象列表/日历 View switch，对象卡含 stage/owner/status（内容排期周视图：文案中/选题中/待视觉/待发布/已发布）；Context = 素材 + 内容日历；Utility = 图文预览 / 审核 / 数据。
  - 增长与评估：Main = 数据看板（阅读/互动/转化 EST 标注）+ 归因任务；B 代截图状态。
  - 反馈：B 代截图状态；细节字段 UNKNOWN。
  - 商业化：UX Review §2.2-11 明确为 Optional。
- Presence 规则：所有 Presence Chip/头像/姓名可点击打开 Utility Employee Quick Panel（一步直达协作）。
- D 代（09-xhs-workspace.html）页面 anatomy：导航七区 → Main 顺序 = Workspace Shell（负责人/目标/规则与配置）→ 当前经营 → Domain Primary Work Surface（内容排期，月/周/日 switch）→ 团队运转（默认流程 pill 行 + 原位编辑）→ 工作区（Employee 列表，Leader 固定第一工位，展开 = Conversation + Composer）；Context Pane = 选题库（信号/素材/内容日历）；Utility Pane = 图文预览/审核/数据。
- 注意：**B 代 6-Surface 列表与 D 代「Domain Primary Surface + Shared Work Area」两代原型并存**；权威合同仅为「Main = selected Professional Surface + Shared Work Area」。fixture 消费 B 代 Surface 列表作为 Domain Navigation、D 代 Shell/工作区作为骨架，并在交付说明标注这是设计组合而非已验收整体（DESIGN FIXTURE）。

### A6. Conversation / Result / Evidence / Decision 关系

- Work → Execution → Result / Evidence → Decision / next Work 是 canonical continuity；Viewed ≠ Accepted（Structure Baseline §7）。
- Conversation anchored to work（Shared Authority §9.2 `CONVERSATION_ANCHORED_TO_WORK`）；CEO 可直接进入任一 Employee Conversation（`CEO_CAN_DIVE_INTO_EMPLOYEE`）。
- CEO Decision：高风险/不可逆（如生产发布）进 CEO Decision Slot；白话 Decision + 同一 Decision Reference，技术证据进 Utility/Result Reference（`docs/03_Design/Curis_RD_Design_Phase_Closeout_2026-08-15.md` §2）。Escalation 链 `Employee → Workspace Leader → Business Leader → Department Leader → CEO`（Shared Authority §0.1）。
- Content Growth 特有：发布证据 `publish_receipt` 只能来自 Capability·Connector，原型不得伪造（Domain Authority §3 `RECEIPT_FROM_CONNECTOR`）。

### A7. 已验收 UX 基线

- 无任何已验收视觉。B 代 multi-surface 原型 = Review / DESIGN CANDIDATE（STOP FOR CEO VISUAL REVIEW）。D 代 coverage-exploration 与 department-business-work-surface 为探索原型。
- 结构已验收/权威的是：Frozen Shell Contract & Shared Patterns（`docs/03_Design/Curis_Workspace_Shell_Contract_And_Shared_Patterns.md`）、`docs/reviews/BUSINESS_WORK_SURFACE_PAGE_CONTRACT.md`（Review）、Structure Baseline §8 Four-Pane。
- Content Growth 整体仍待 Channel Capability Evidence 与 Autonomy Guardrail Gate 才能谈 Verified（CEO Reconciliation §5）。

### A8. 开放的 Visual 问题

- FINAL UI MASTER PAUSED；Typography/spacing/Composer/Employee 呈现等全部开放（Structure Baseline §13–§14）。
- 多套视觉语言并存（P0）：`docs/research/system_competitive_research/CURIS_CURRENT_UI_AUDIT.md` S1–S6（accent #806BE5 vs 旧 #32f08c 绿；A 代使用已废弃「办公室」词汇——fixture 禁用「办公室」一词）。
- Dark theme：D 代默认 dark；B 代截图为浅色 1440 + 1280x800。Dark/1024 无权威定稿（UNKNOWN）。
- `--ui-syntax-*` 语法高亮色值未冻结（DESIGN GAP #2）（`docs/03_Design/Curis_RD_Workspace_Instance_Spec_v1.md` §11）。

---

## B. RD / 研发

### B1. Department / Business / Workspace 命名与关系

- Department：**研发部**；Businesses：**Curis 产品研发**（主营）、Curis 内部工具研发、数据中台研发（dept HTML state-3）。Workspace：**Curis 研发**（08-rd-workspace.html）。均 DESIGN FIXTURE（D 代原型）。原装部门只有空间工程部与数据分析部——RD/内容增长部均为用户启用的 Business 示例（Structure Baseline §5；Shared Authority 2026-09-09 段）。

### B2/B3. Team / Leader / Employees 与 Responsibility

- 林涛 · 研发部部长 / Tech Lead（业务负责人）；孙浩 · 工作空间负责人（统筹版本节奏、联调收口与发布质量）——**部门 Leader（林涛）与 Workspace 负责人（孙浩）两名并存**，fixture 需二选一或明确两级 Leader（DESIGN FIXTURE 决策）。
- 王琳 · 产品经理 · 需求澄清与验收标准
- 周岚 · 开发工程师 · 登录接口联调与异常分支修复
- 赵敏 · QA · 等待联调完成后回归测试
- RD Instance Spec 另一组 mock（陈真/李翔/王磊）与 D 代名字冲突属 mock 层差异（见 E）。

### B4. 阶段 / 方法论（按项目实际措辞）

- RD 已验收执行链（G3 Phase 0/1 accepted 口径）：`Project / Cycle → Task → Responsibility / Employee → Codex → declared-file change → Artifact / Evidence → Result Reference → restart / failure truth`（`docs/reviews/CURIS_WORKTREE_CLEANUP_FINAL.md` §G3）。
- D 代「当前研发」状态行：**产品/需求 → 架构 → Runtime → Frontend Adapter → Test → Review**；Team Operating 默认流程：**产品 → 架构 → 开发 → 测试**（08-rd-workspace.html）。fixture 按这些原文措辞。
- 四概念责任语义：Responsibility / Responsibility Holder / Current Executor / Status（working/waiting/needs_ceo/completed/failed/idle）；`waiting` ≠ idle（Instance Spec §1a；Closeout §1）。
- 方法论缺口（背景，不给原型当设计指令）：`docs/05_Workspace_Engineering/Curis_RD_Methodology_Gap_Review.md`。

### B5. 08-rd-workspace.html 页面 anatomy（提取）

- 四 Pane 可切换（nav / context / main / utility）。
- Main 顺序：page-head → Workspace Shell（负责人/目标/规则与配置）→ Conditional CEO Decision Slot（灰度发布 banner：发生了什么/为何 AI 不能自决/员工推荐/你只需做 + [查看方案][暂缓]）→ 当前经营（五要素）→ Domain Primary Work Surface「当前研发」（状态行 + 当前 Blocker + 最近 Result + 需要你）→ 团队运转（默认流程 pills）→ 工作区（Employee 列表：Leader 行高亮 + `Assignment · Employee × Role × Scope`，展开 = Conversation + Composer）。
- Context Pane：文件树（product-platform/src/auth/login.ts 等）+ Responsibility + Recent Work / Object。
- Utility Pane：tabs = **Diff / Source / Preview**；Diff 显示变更归属责任 + diff block + [提交变更 / 请求协审]。
- Composer chips：+ 添加 / 访问权限 / 工作模式 / 执行·Codex / 发送。
- mock：登录模块重构 · v1.3 灰度、联调通过率 96%、Test 22 passed / 0 failed、Frontend Adapter 80%。

### B6. 已验收边界

- **RD Phase 0/1 = accepted bounded real execution slice**；Phase 2A design fidelity pass 但 long-running reliability = REVIEW REQUIRED（`issues/RD-WORKSPACE-INSTANCE-001.md`；`docs/reviews/CURIS_WORKTREE_CLEANUP_FINAL.md` §G3）。
- RD INSTANCE APPROVED（`docs/03_Design/Curis_RD_Workspace_Instance_Spec_v1.md` §13）；Design Phase COMPLETE（Closeout）。

---

## C. New Business / Generic Workspace activation

### C1. 标准步骤（权威措辞）

- Structure Baseline §5：`CEO intent → Company → reuse / propose Business → necessary Decision Gate → canonical Department → canonical Business → first Workspace → Team / Responsibility → Operating`；CEO 可直接创建或委托空间工程团队；Generic Workspace 是合法真实工作环境，Professional 不是强制前置（2026-09-09 scoped amendment SUPERSEDED 旧 §9）。
- Create Business Flow 合同（Review）：`CEO 意图 → Curis 理解 →（必要时）研究与能力发现 → Operating Proposal → 必要 CEO Gate → Bootstrap / Reuse / Compose → 合法 Leader 承责 → 开始经营`；默认入口是 Conversation（`docs/reviews/CURIS_CREATE_BUSINESS_FLOW_CONTRACT.md` §1）。
- 委托空间工程路径（Frozen）：CEO/Assistant → 空间工程部承接 → Leader 澄清需求 → Research/Operating/Design/Build/Quality → 同时组建 Operating Team → Build Team Handoff → 新团队经营（Shared Authority §9.5）。
- 未知业务诚实路径：`USE EXISTING → COMPOSE EXISTING → RESEARCH / ADAPT → BUILD / ACQUIRE → ESCALATE → REFUSE / CANNOT OPERATE YET`（Structure Baseline §11）。

### C2. Generic Workspace 原型 anatomy（fixture 参照）

- `curis-ui-prototype/coverage-exploration-2026-08-17/10-generic-workspace.html`：实例 = **宠物寄养工作空间**；Main = page-head + 当前工作 + 工作区（Leader 固定第一工位、默认收起）。
- Business Work Surface 结构（通用）：Part1 Business Definition（含 Leader Workstation）→ Part2 Operating Status → Part3 Workspace Directory → Part4 Business Team（`docs/reviews/BUSINESS_WORK_SURFACE_PAGE_CONTRACT.md` §4）。

### C3. fixture 建议

- 中性示例业务沿用项目已出现的**宠物寄养**（10-generic-workspace / dept state-7），标注 DESIGN FIXTURE。须满足：Business 归属 Department、长期 Business ≥1 Workspace、Team = Leader + 成员 + 职责、不伪造 Verified 状态。

---

## D. Fixture 数据建议表

| 对象类型 | fixture 值 | 语义来源路径 |
|---|---|---|
| Department（内容） | 内容增长部 | curis-ui-prototype/department-business-work-surface-2026-08-18/... state-2 |
| Department（研发） | 研发部 | 同上 state-3 |
| Business（内容） | 小红书运营（母业务）；抖音/公众号 占位 | 同上 state-2/state-4 |
| Business（研发） | Curis 产品研发；内部工具/数据中台 占位 | 同上 state-3/state-5 |
| Workspace（内容） | AI 科技（小红书运营业务下） | curis-ui-prototype/coverage-exploration-2026-08-17/09-xhs-workspace.html |
| Workspace（研发） | Curis 研发（Curis 产品研发业务下） | 08-rd-workspace.html |
| 内容员工 | 周宁(部长)、陈真(业务/Workspace Leader)、苏晴(视觉)、何川(数据分析)、林月(排版/调研/文案) | dept HTML state-2/state-4；09-xhs-workspace.html（均 DESIGN FIXTURE） |
| 研发员工 | 林涛(部长/Tech Lead)、王琳(产品经理)、周岚(开发)、赵敏(QA)、孙浩(Workspace 负责人/发布门禁) | dept HTML state-3；08-rd-workspace.html（DESIGN FIXTURE） |
| 内容 Team 默认流程 | 选题→调研→文案→视觉→发布 | 09-xhs-workspace.html .team-op |
| 研发 Team 默认流程 | 产品→架构→开发→测试 | 08-rd-workspace.html .team-op |
| 典型 Work（内容） | 「AI 工具测评·极简风」：文案中→待审核→待视觉→待发布→已发布 | 09-xhs-workspace.html 内容排期周视图 |
| 典型 Work（研发） | 登录模块重构 v1.3：产品/需求已确认→架构完成→Runtime 完成→Frontend Adapter 80%→Test 22 passed→Review 待验收 | 08-rd-workspace.html .dev-status-list |
| 典型 Result / Evidence（内容） | 数据看板（EST 标注）+ 归因任务；回执只能来自 Connector | 09-xhs Utility「数据」；Domain Authority §3 |
| 典型 Result / Evidence（研发） | 联调通过率 96%、Diff (+34/-93)、登录页预览 | 08-rd-workspace.html Utility |
| 典型 Decision（内容域） | 定位调整建议待证据门槛（Approved Strategy Envelope 内） | 09-xhs Leader Conversation |
| 典型 Decision（研发） | 灰度发布 Banner：①发生了什么②为何不能自决⑤员工推荐⑦你只需做 | 08-rd-workspace.html decision-banner |
| Context（内容/研发） | 信号/素材/内容日历；文件树 + Responsibility + Recent | 09-xhs / 08-rd Context Pane |
| Generic 业务 fixture | 宠物寄养工作空间（业务刚创建） | 10-generic-workspace.html；dept state-7 |

---

## E. AUTHORITY CONFLICT 记录

未发现需 CEO 裁决的**同级权威冲突**。需注意的已裁定/低层事项：

1. Office vs Workspace 等：已于 2026-08-24 由 CEO 裁决（CONTENT_GROWTH_CEO_AUTHORITY_DECISION_RECONCILIATION.md §6）。原型不得回退。
2. 「长期 Workspace 必须 Professional」：已被 2026-09-09 scoped amendment SUPERSEDED。
3. mock 员工名不一致（两代原型）为 fixture 层差异；fixture 统一用 D 代一组并标注 DESIGN FIXTURE。
4. B 代 6-Surface 与 D 代 Domain-Primary-Surface 并存：组合方式是设计决策，须显式声明。
5. `CONTENT_GROWTH_PROFESSIONAL_WORKSPACE_RECONCILIATION*` 不存在（UNKNOWN）；最近对应物为 `CONTENT_GROWTH_PRE_IA_AUTHORITY_RECONCILIATION.md` 与 `CONTENT_GROWTH_AUTONOMY_GUARDRAIL_CALIBRATION_AUDIT.md`。
6. 8 Operating States / 4 Cognitive Buckets 仅为 Research / Accepted Candidate，fixture 不得画成固定栏目。
