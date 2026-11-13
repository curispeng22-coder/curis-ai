# Curis · Workspace Engineering — Visual Design Closure（视觉设计收口）

**Status**: WORKSPACE ENGINEERING VISUAL DESIGN — **CLOSURE CANDIDATE**（Team Operating Model Delta 已应用 · Review 修正完成 · 不写正式产品代码）
**阶段**: PRODUCT / WORKSPACE DESIGN — Final High-Fidelity Design（承接《Company Integration Product Delta》→《CEO Journey High-Fidelity》）
**日期**: 2026-08-16
**交付物**: `Curis_Workspace_Engineering_CEO_Journey_High_Fidelity.html`（单文件自包含 Frozen 高保真 HTML）

**上位依据**:
- `Curis_Workspace_Engineering_Product_Translation.md`（APPROVED CANDIDATE）
- `Curis_Workspace_Engineering_Technical_Reality_Delta_Review.md`（GO FOR VISUAL）
- `Curis_Workspace_Engineering_Company_Integration_Product_Delta.md`（COMPLETE → 直接进入高保真）
- `Curis_Workspace_Shell_Contract_And_Shared_Patterns.md`（Frozen · S1–S7 + P1–P7）
- `_system/tokens.css`（Frozen 设计令牌唯一真源）

---

## 1. 交付物清单

| 文件 | 内容 | 状态 |
|---|---|---|
| `Curis_Workspace_Engineering_Company_Integration_Product_Delta.md` | P0.5 Operating 层 Company Integration 小 Delta：6 条产品语义铁律 | COMPLETE |
| `Curis_Workspace_Engineering_CEO_Journey_High_Fidelity.html` | 完整 CEO Journey 高保真（10 帧，Frozen Shell 四 Pane，dark/light 双主题） | DELIVERED |
| 本文档 | 视觉设计收口：锁定 / 合规 / 边界 / 停止态 | CLOSURE |

---

## 2. Frozen 合规声明

### 2.1 Shell 结构合规

| Frozen 要求 | 高保真实现 |
|---|---|
| 四独立 Pane（Nav / Context / Main / Utility） | ✅ CSS Grid 四列；Nav 固定 220px，Context/Utility Adaptive（T2/T3 开合） |
| 无 Global Topbar | ✅ 无顶部全局栏；窗口控制（macOS traffic lights）在 Nav Header 内 |
| T1 Navigation Toggle | ✅ Nav Header 右侧；折叠后可重新展开 |
| T2 Context Toggle | ✅ Main Header 左侧常驻 |
| T3 Utility Toggle | ✅ Main Header 右侧条件显示；展开后转移至 Utility Header |
| Pane-local Header | ✅ 每个 Pane 各自独立 Header（品牌/搜索/面包屑/标题/模式名） |

### 2.2 设计令牌合规

| 令牌层 | 使用情况 |
|---|---|
| 颜色（Dark/Light 双主题） | ✅ 全部使用 `--ui-*` 变量；无硬编码色值；默认 Dark（Frozen 默认）；Light 经 data-theme 切换 |
| 字阶（7 档，下限 12px） | ✅ 全部使用 `--ui-fs-1..7`；无 <12px 文字 |
| 间距（8 档，4px 基数） | ✅ 全部使用 `--ui-sp-1..8` |
| 圆角（5 档） | ✅ 全部使用 `--ui-r-xs/pill/sm/md/lg` |
| 层级（6 档） | ✅ z-index 使用 `--ui-z-*` |
| 动效（3 档时长 + 缓动） | ✅ transition 使用 `--ui-dur-*` + `--ui-ease-*` |
| 控件高度（触达下限 32px） | ✅ 所有按钮/控件 ≥ `var(--ui-tap-min)` |
| 焦点环 | ✅ 统一 `focus-visible` outline |
| 减少动态效果偏好 | ✅ `prefers-reduced-motion` 归零 |

### 2.3 Surface 注册表合规

高保真中使用的 Surface（全部来自 Handoff §11.2 注册表 9 种，**不新增类型**）：

| Surface | 出现位置 | 对应旅程阶段 |
|---|---|---|
| status-owner summary | Business Home 经营概览 | 步骤 8·9 |
| object list | 经营总览业务空间列表 | 步骤 0 |
| activity timeline | Curis 准备进度 / Context 动态 | 步骤 2·3 |
| Employee Presence（P2） | 员工在场 / 负任 / 工作方式 | 步骤 7·8·9 |
| Result Reference list（P6） | 结果卡片 | 步骤 8·10 |
| Evidence list | 验收证据 / Utility | 步骤 2·4·5·7·8（独立 Surface，**不归类为 P5**） |
| empty-failure-gap card | 能力缺口 / 异常 | 步骤 4·10 |
| field editor | 表达意图输入框 | 步骤 1 |
| object detail | Proposal 文档结构 | 步骤 3 |

### 2.4 P1–P7 共享模式合规

| 模式 | 落地位置 | 说明 |
|---|---|---|
| P1 三层责任语义 | Employee Presence 区分「在场/负责/执行」 | 不用 Object Owner 替代 Current Responsibility |
| P2 Employee Presence | Business Home + Context「员工工作方式」扩展 | Shared Employee Detail 内自然语言呈现 |
| P3 System Activity | 正在执行的工作（Task/Execution 进度条） | 非 Employee Runtime 的系统活动 |
| P4 Automation by default | 全程自动化背景阶段（准备、执行、复盘） | CEO 仅在决策点出现 |
| P5 Handoff Event（责任交接事件） | **NOT TRIGGERED / NOT REQUIRED** | 本旅程在办公室创建时即确定真实 Responsibility（P0.5），无后续责任转移事件；验收证据（Evidence list）是独立 Surface，**不归类为 P5** |
| P6 Result Reference | 结果引用（P6）+ Utility 按需查看 | 结果已生成时展示 |
| P7 CEO Decision Package Pattern | Needs CEO 决策包（Layer 0 Banner + Layer 1 Plain + Layer 2 Evidence） | 仅在真实结构性变化时出现（步骤 10），非固定步骤 |

---

## 3. CEO Journey 覆盖矩阵

| # | 旅程阶段 | 高保真帧 | 关键设计元素 | P0/P0.5 技术基础 |
|---|---|---|---|---|
| 0 | 经营总览（起点） | Frame 0 | 业务列表 + status-owner + 「创办新业务」入口；空间工程部 coord note（非唯一入口） | — |
| 1 | 表达经营意图 | Frame 1 | 自然语言输入 + 方向选项 chip；委托路径说明（直接 / 经 Assistant 转交空间工程部） | — |
| 2 | 委托与澄清 | Frame 2 | **空间工程部**作为真实核心 Department 出现（dept card）；Assistant 协调转交；CEO↔Leader Conversation 澄清目标/成功/范围/Non-goals | Frozen Team Operating Model |
| 3 | 团队工作过程 | Frame 3 | **6 真实责任分工**（Leader/行业研究/经营方法/产品设计/搭建实施/质量验收），每阶段真实结果+交接推进，不画流程/DAG；resp 可点击进入 Workstation | Frozen Team Operating Model |
| 4 | Workspace Proposal | Frame 4 | 6 答 + **由谁负责/怎么工作/需要什么能力**（Operating Team Leader 长期负责，空间工程退出）；Proposal 来源 = Leader 提交 | P0.5 real Employee/Responsibility |
| 5 | 适配·连接 | Frame 5 | 能力三分类卡（Required for Activation / Specific Action / Optional） | P0 F7（权限 request 非 grant） |
| 6 | 激活 | Frame 6 | 「确认启用」→ **「已经可以经营」**（铁律文案） | P0 F1+F6（安装+保留） |
| 7 | 进入公司 · 交付 | Frame 7 | 导航动态出现新办公室；**Build Team→Operating Team 交付 Handoff**（初始指派，非 P5）；空间工程退出日常经营；员工可点击进 Workstation | P0.5 real Company identity + Frozen TOM |
| 8 | 员工开始工作 | Frame 8 | Operating Team 负责（空间工程已退出）；Employee Presence(P2) 可点击进 Workstation；coord note：CEO 默认不管理内部流程 | P0.5 real Employee/Task/Execution |
| 9 | Business Home 运营 | Frame 9 | 八问模型 + 真实员工/责任/执行/结果/证据 + 进化通知；员工可点击进 Workstation | P0.5 full Operating chain |
| 10 | 结果·异常·Needs CEO | Frame 10 | Result Reference(P6) + gap 卡 + P7 决策包（仅真实需要） | P0.5 Artifact/Evidence/Result |

**完整覆盖用户指令的十一帧旅程**：表达经营意图 → 委托空间工程部·目标澄清 → 团队工作过程 → Workspace Proposal → 必要适配/能力连接 → 激活 → 进入公司·交付 → 员工开始工作 → Business Home 运营 → 结果/异常/Needs CEO。

---

## 4. P0.5 Company Integration Delta 在高保真中的落地

以下 6 条铁律已在高保真中逐一实现：

| # | 铁律 | 高保真落地点 |
|---|---|---|
| 1 | 进入公司，非独立 App | 步骤 6：导航「办公室」分组动态出现 + 公司身份；用户面「已经加入公司，可以开始经营」，以真实员工在场/责任/能力连接/工作状态体现成功（不出现任何内部 Acceptance 术语） |
| 2 | Proposal 三问自然语言 | 步骤 3：Proposal 第 5 栏「由谁负责 / 怎么工作 / 需要什么能力」（角色+循环+能力三分类），不暴露 Primitive |
| 3 | Business Home = 真实运营真相 | 步骤 7·8·9：Employee Presence(P2) 显示真实员工在场/责任/执行；Result/Evidence 为真实运营产出 |
| 4 | 能力缺口三分类沿用 | 步骤 4：三张 capability 卡（act/spec/opt）+ 步骤 9 gap 卡诚实呈现 |
| 5 | Handoff / P7 仅真实需要时出现 | 步骤 9：P7 决策包仅在「建议调整教程占比」这一真实结构性变化时出现；Context 解释为何出现 |
| 6 | 激活文案 =「已经可以经营」 | 步骤 5：banner 写「已为你启用 · 现在可以经营」，注释明确不写「Package 安装成功」 |

---

## 5. 边界与排除项（硬约束）

本批高保真**不包含**以下内容（均未由 P0/P0.5 覆盖，须新 bounded Issue）：

| 排除项 | 状态 | 说明 |
|---|---|---|
| Package update / migration / rollback UX | **STILL POST-P3** | P0 Remaining boundary 明确 remain unimplemented |
| 签名 / Marketplace / 第三方信任 UX | **STILL POST-P3** | 同上 |
| arbitrary extension（任意代码扩展） | **未覆盖** | P0 明确 Package 不能携带任意代码 |
| XHS·RD·TTK migration UX | **未覆盖** | P0 仅 two bounded integration seams；既有业务未迁移 |
| Evolvable（进化 = Package 升级） | **NOT IMPLEMENTED** | 进化 = 运营学习驱动的 method 进化（§2.C），不是 Package 版本变更 |
| Content Growth 运营示例数据（已发布 / 阅读 / 线索 / 自动发布 等） | **DESIGN FIXTURE / FUTURE OPERATING EXAMPLE** | 高保真中出现的 Content Growth 运营数据未连接真实外部平台能力，不得作为 Current Runtime Truth；Content Growth 各设计文档同性质示例数据亦适用 |

**高保真内不得暗示以上任何能力可用。**

---

## 5.1 Review 修正记录（PASS WITH REQUIRED FIXES）

| # | 修正项 | 落实位置 | 结果 |
|---|---|---|---|
| 1 | **P5 修正** | 高保真 Frame 8 Context「责任与员工」卡 + 本文 §2.4 | P5 = Responsibility Handoff Event → 标记 **NOT TRIGGERED / NOT REQUIRED**（本旅程无真实责任转移，责任在办公室创建时即确定）；Evidence list 明确**不归类为 P5**（是独立 Surface） |
| 2 | **删除 CEO UI 内部术语** | 高保真 Frame 6（进入公司） | 移除 Installed / Operational / Company Integrated / Operating / Evolvable；用户面仅表达「已经加入公司，可以开始经营」，成功以真实员工在场 / 责任 / 能力连接 / 工作状态体现 |
| 3 | **Content Growth 运营数据标注** | 高保真 Frame 8·9（`已发布 / 阅读 / 线索 / 自动发布` 等） | 标记为 **DESIGN FIXTURE / FUTURE OPERATING EXAMPLE**，未连接真实外部平台能力，非 Current Runtime Truth |

---

## 5.2 Team Operating Model Delta 记录（Frozen Company OS TOM 落地）

| # | 修正项（10 条） | 落实位置 | 结果 |
|---|---|---|---|
| **1** | **空间工程部 = 真实核心 Department** | Frame 0 coord note / Frame 2 dept card（"Curis 组织 · 真实核心建设部门"，含 Leader + 6 角色 pills） | 不再表现为后台「Curis 自动准备」功能；明确非唯一入口 |
| **2** | **委托路径：CEO 直接 / Assistant 协调转交** | Frame 1 coord（委托路径说明）+ Frame 2 coord（Assistant 已理解需求并转交） | Assistant 协调/监督/汇报但不替代实施 |
| **3** | **CEO↔Leader Conversation 澄清目标** | Frame 2 Conversation（3 条 msg：Leader 问目标/成功/范围/Non-goals → CEO 答 → Leader 确认组织团队） | 目标/成功标准/范围/Non-goals 经 Conversation 确认后才组织团队 |
| **4** | **6 真实责任分工（Result + Handoff，不画 DAG）** | Frame 3：6 个 resp 卡（Leader→行业研究→经营方法→产品设计→搭建实施→质量验收），每卡含负责/产出(真实结果)；handoff 箭头「不是后台黑箱，也不画成流程图」 | CEO 默认不管理内部流程；resp 可点击进 Workstation |
| **5** | **CEO 随时点击员工 → Workstation/Conversation** | sEmployee clickable(true) in Frames 7·8·9；Context pane Workstation overlay（employee card + 当前工作/结果 + Evidence + Conversation thread + 输入框）；openWorkstation() + render() override ctx | 满足 correction 5 完整实现 |
| **6** | **Build Team → Operating Team 交付 Handoff** | Frame 7 dept card：「建设交付 · 空间工程部 → 内容增长 Operating Team」+ Leader 汇报完成 + 退出日常经营 + 可再委托 | 标注为初始责任指派（**非 P5 转移事件**），P5 仍 NOT TRIGGERED |
| **7** | **Operating Team 长期负责 / 空间工程退出** | Frame 4 Proposal（Operating Team 长期负责）、Frame 8（"Operating Team 负责 · 空间工程部已退出" pill）、Frame 9 同 | 与 correction 8 一致 |
| **8** | **渐近工作原则（空间工程不是唯一入口）** | Frame 0 coord（"但不是唯一入口——CEO 自建、Assistant 协调、临时团队升级等路径同样开放"） | Frozen TOM 渐进原则落地 |
| **9** | **不暴露内部原语** | 全文无 Agent/Router/DAG/Package/Gate 出现在 CEO UI；framePrepare（含 "Package 校验通过"）已删除 | correction 10 合规 |
| **10** | **保留 Frozen Shell / Company Integration / 能力三分类 / Failure Truth / P5 NOT TRIGGERED / P7 正确语义** | 全部保留并验证通过 | 零回退 |

---

## 6. 停止状态

```text
WORKSPACE ENGINEERING VISUAL DESIGN — CLOSURE CANDIDATE
→ STOP FOR REVIEW（不写正式产品代码 · Review 修正：P5 / 内部术语 / Content Growth 标注
  + Team Operating Model Delta：空间工程部真实 Department / 委托路径 / Conversation 澄清 /
    6 责任分工 Result+Handoff / Build→Operating 交付 / Workstation/Conversation 介入）
```

（Workspace Engineering 产品线至此完成：Product Translation APPROVED CANDIDATE → Technical Reality Delta GO FOR VISUAL → Company Integration Product Delta COMPLETE → Final High-Fidelity DELIVERED → Visual Design Closure COMPLETE → **Team Operating Model Delta APPLIED**。三份文档 + 一份高保真 HTML 构成完整交付。保持 Frozen/Blueprint/Shell/P1-P7/XHS-RD/Runtime/Connector/代码/UI 零修改。内部语义零重定义。Evolvable=NOT IMPLEMENTED。POST-P3 排除项明确标注。Content Growth 运营示例数据已标注 DESIGN FIXTURE。Review 修正（P5 NOT TRIGGERED / 删除内部 Acceptance 术语 / Content Growth 数据标注）+ Team Operating Model Delta（10 条 Frozen TOM 落地）均已落实，状态升为 CLOSURE CANDIDATE；待最终 Review 通过后决定是否进入前端工程。）

---

*Curis Workspace Engineering Visual Design Closure · 2026-08-16（CLOSURE · 非产品代码 · 非Runtime · 非新架构 · Team Operating Model Delta APPLIED）*
