# Curis Content Growth — Core Interaction Review

**Status**: CONTENT GROWTH CORE INTERACTION · APPROVED CANDIDATE（FINAL REVIEW 通过 · CLOSED · 等待 Operating Strategy Expert 交接 · 未进高保真）
**阶段**: PRODUCT / WORKSPACE DESIGN — Core Interaction（3 个核心场景 · 已批准 APPROVED CANDIDATE · 当前 Closure Review）
**上位依据（均未修改）**:
- `Curis_Company_OS_Shared_Authority.md`（Frozen）
- `Curis_Content_Growth_Domain_Authority.md`（Frozen）
- `Curis_Workspace_Shell_Contract_And_Shared_Patterns.md`（Frozen · P1–P7 · 四独立 Pane · 无 Global Topbar）
- `Curis_Content_Growth_Product_Model_Closure.md`（PRODUCT MODEL RECOMMENDATION · 已 APPROVED）
- `Curis_Content_Growth_Core_Interaction_Spec.md`（本轮配套规范）

**本轮交付物**:
1. `Curis_Content_Growth_Core_Interaction_Spec.md` — 结构稿 + 交互规范（设计依据）
2. `Curis_Content_Growth_First_Run_Wireframe.html` — 场景 A 中保真结构稿（可打开）
3. `Curis_Content_Growth_Home_Wireframe.html` — 场景 B 中保真结构稿（可打开）
4. `Curis_Content_Growth_Content_Journey_Wireframe.html` — 场景 C 中保真结构稿（可打开，本轮最重要）
5. 本 Review 文档

---

## 1. 本轮覆盖回顾

### 1.1 三个核心场景 × 真实 CASE
| 场景 | 覆盖 | 关键判定 |
|---|---|---|
| **A. First-Run / Account Setup** | CASE A（单账号·极简·零暴露「经营方向」）/ B（同平台 2 账号·定位不同·AI 建议分开）/ C（多平台同定位·AI 建议同一经营方向）/ D（大量账号·AI 建议分组·拖动调整） | 单账号完全隐去 Office 层；分组建议可确认可调整，非自动落定；OAuth 失效仅标「授权已过期·可重连」，不静默删账号与历史 |
| **B. Content Growth Business Home** | 5 秒信息优先级 + 视觉层级（Decision Banner > Attention 高亮卡 > 普通行）+ 单账号隐去切换器 / 多经营方向轻量切换 | Decision / Attention 天然比普通 Activity 突出；不机械做成 7 个等大 Dashboard |
| **C. Continuous Content Journey** | 完整一条内容流（AI 发现 → 为什么值得做 → 接受 → 发到哪里三源合并 → 分别制作 → 各账号状态 → 发布 → 数据回流）+ 示例主题跨 4 账号 | 用户一眼看到「同一条内容在不同账号的进展」，不是 4 个独立任务列表；复用行为化、禁词已落实 |

### 1.2 Frozen Shell 四 Pane 落实
- **Navigation（SHELL·T1）**：六区导航固定不增不减；业务空间子项下进入「内容增长」；三份结构稿导航完全一致。
- **Main（SHELL）**：承载各场景 CG 内容；Pane Header 含 Breadcrumb + T2（左）+ T3（右）+ 无 Global Topbar。
- **Context（SHELL·CG 选题库/信号 · T2）**：Home / Journey 按需开合（演示 HTML 提供 T2 开关验证）。
- **Utility（SHELL·CG 数据看板/预览 · T3）**：Home 增长反馈、Journey 数据回流按需开合（演示 HTML 提供 T3 开关验证）。
- **Adaptive Surface 行为**：默认收起、点开才占空间、可拖拽调宽、↗ 最大化（Frozen S6），由 Instance 声明；均无 Global Topbar。

### 1.3 AI Employee Presence（跨场景自然出现，无独立 Dashboard）
- 出现于 Home「AI 在做什么」紧凑列表、Journey 各账号制作卡上方 Responsibility。
- 显示：Identity（名+角色）+ 正在做 + 状态；**不显示** Router / Assignment / Queue / Capacity（⑨ 未 Frozen，仍 VISION/RESERVED）。

### 1.4 Professional Workspace 按需进入（I3：Main 切入，非 Modal）
- 点「编辑抖音版本」→ **Main 切入 Content Production 专业工作状态**（非弹窗）；Breadcrumb 保持内容语境（业务空间 / 内容增长 / AI浏览器 / 抖音版本）；点「返回内容流」即回连续内容流；
- 点「查看小红书发布详情」→ **Main 切入 XHS Channel Operations 专业工作状态**（复用现有 XHS，不修改）；
- 机制 = Shell Adaptive Surface / Deep Link 的 **Main 切换**，Context/Utility 按专业面重声明；**不感知跳办公室**；本轮不设计其内部布局。Wireframe 已由此前的 Modal 占位改为 Main-switch 实现。

---

## 2. 与 Frozen / Closure 的对应校验

| 用户面（本轮） | Frozen / Closure 语义 | 是否暴露原词 |
|---|---|---|
| 添加你要经营的账号 | Channel Account / OfficeAccountBinding（②） | 否 |
| 经营方向（多账号时） | Office（①） | 否（内部词完整） |
| 今天值得做 / AI 发现选题 | Content Opportunity / Intent（③） | 否 |
| 发到哪里（默认+AI+手动） | Target Account Set（④，三源合并） | 否 |
| 各账号分别制作 / 已自动复用 | Variant / Publication（⑤）+ reuse 行为化 | 否（禁 HIGH_REUSE/FULL_DIVERGENCE/Variant） |
| 暂不发 TikTok / 等全部准备好再发 | Distribution Execution Policy（④） | 否（自然语言） |
| 谁在负责 / 正在做 | Responsibility Requirement（⑥）+ Routing（⑦）+ Employee（⑧） | 否 |
| 用了哪些资料（Journey 左侧「为什么值得做」） | Context Isolation Truth Boundary | 否（按需可追溯，默认隐藏） |
| 需要 CEO 决策（仅重大事由） | Needs CEO（Frozen P7） | 否（仅占位呈现 8 要素语义） |
| 数据回流（T3） | System Activity 自动 Analytics（P3）+ Result Reference（P6）+ Receipt Evidence | 否 |

**校验结论**：所有用户面完全消费 Frozen Authority 语义，仅做翻译与渐进披露；**未修改、未新增任何 Primitive**；Product Model Closure 推荐骨架（Business Home + 经营方向 + 连续内容流 + 按需专业面）已逐一落地为可评审结构。

---

## 2.5 本轮 Closure 应用的 Interaction DELTA（I1–I4）

Review 批准时附 4 个 Interaction DELTA，已在 5 份文档就地应用（不新增文档、不 Frozen、不开发）：

- **I1 — Opportunity ≠ 每次人工批准**（对齐 Frozen P4 Automation by default）：三路径
  - A. **DEFAULT AUTO**：符合经营节奏/策略/预算/风险边界的选题，Curis 自动进入制作；Home「正在生产」显示「已按节奏自动开始 + 为什么做」，可查看/暂停/调整，无需先批准；
  - B. **USER-INITIATED**：「今天值得做」= 机会面（Opportunity Surface），非审批队列；点「做这个」即制作；
  - C. **DECISION REQUIRED**：仅品牌方向/超策略/合规版权/高成本/重大定位变化进 Frozen P7（见 Home 顶部 Decision Banner）。普通 Opportunity 不得全变 Gate。
- **I2 — Publishing/Scheduling 默认自动**：账号有正常规则 + 内容符合 + 平台允许 + 无异常 → AI 自动排期/发布；Home 显示「小红书 · 今晚20:00 自动发布」+[调整]，非[确认]；仅异常（多账号须同步但 Blocked / 平台异常 / 超策略 / 重大活动 / 额外预算 / 风险）才 CEO Decision。
- **I3 — Professional Workspace ≠ Modal**：Wireframe 中 Modal 仅为早期占位，已改为 **Main 切入专业工作状态** + Breadcrumb 保持内容语境 + [返回内容流]，非弹窗（见 §1.4、各 HTML legend）。
- **I4 — CEO Operating Rules（I4.1–I4.10，仅 Design Candidate）**：Automation by default ≠ AI 随意搜/制/发，也 ≠ CEO 逐条批；模型 = CEO 制定日常经营规则 → AI 规则内自主运行 → 数据回流 → AI 提优化建议 → CEO 决定 → 新规则成后续依据。含采集规则、生产节奏、每账号发布规则、规则层级（方向默认→账号覆盖→单次临时）、自动执行边界、AI 建议改规则、禁静默改长期规则、First-Run 不复杂化（I4.8）、Home 加「当前经营节奏」轻量入口（I4.9）、I1/I2 与 Operating Rules 合并为统一循环。Operating Rules 仅作 Design Candidate，不 Frozen、不新增 Primitive。

**KEEP（未改动）**：First-Run CASE A/B/C/D、单账号隐藏经营方向、AI 建议分组、Home=Attention+Light Ops、Decision 最高优先级、Continuous Content Journey、同主题多账号状态、分别制作、自动复用行为化、AI Employee Presence、Context 按需追溯、Utility 数据回流、四 Pane Shell、T1/T2/T3、无 Global Topbar、内部术语全隐藏、XHS 不改、Queue/Bottleneck 仍 VISION/RESERVED。

---

## 3. 未在本轮设计（明确留给后续轮次）

- **Professional Workspace 内部布局与高保真**：Content Production / 各平台 Channel Operations（XHS 已实现部分复用，不修改）的内部结构（进入机制已定为 Main-switch，见 §1.4 / I3；内部布局本轮不设计）。
- **Closure §6 其余 7 个界面**：
  1. 经营方向容器与切换器细节（本轮仅 Home 轻量切换占位）
  2. Connected Accounts 管理面完整（增/删/改定位/跨经营方向移动/N:N 预留）
  3. 增员轻入口细节（主动 + Curis 建议，指标全隐藏，VISION）
  4. Context 可追溯入口细节（「用了哪些资料 / 依据哪些 Knowledge」按 Context Isolation Truth Boundary）
  5. Needs CEO 完整呈现（沿用 P7，本轮仅占位）
  6. XHS 当前实例未来纳入 IA 草图（XHS Note Workspace → 内容增长 → 小红书经营方向）
  7. 单账号隐去层之外的多经营方向深编辑
- **Operating Context**（仍 RESERVED/DEFERRED）、**N:N 共享账号复杂 UX**（首版 1 Account : 1 Primary 经营方向）、**Queue/Bottleneck 指标呈现**（⑨ 未 Frozen）。

---

## 4. 纪律遵守声明

✅ 未修改 Frozen Authority / Product Blueprint / Shell / P1–P7 / XHS·RD Instance。
✅ 未写正式前端、未开发 Runtime / Connector、未进 Figma、未做最终视觉高保真。
✅ 未继续研究架构；仅把已 Frozen 的模型翻译为结构与交互。
✅ 三份结构稿均实际可打开（HTML + 轻量交互：CASE 切换 / T2·T3 开合 / Professional Workspace 为 Main 切入专业工作状态，非 Modal），并显式标注 Navigation/Context/Main/Utility 与 `SHELL` / `CG` 区分。
✅ 全部禁词已落实：HIGH_REUSE / FULL_DIVERGENCE / Variant / Target Set / OfficeAccountBinding / Office（内部语义完整，用户面零暴露）。
✅ Queue/Bottleneck 仍 VISION/RESERVED，未把 Candidate 画成确定功能。

---

## 5. 停止状态

```
CONTENT GROWTH CORE INTERACTION CLOSED
WAITING FOR OPERATING STRATEGY EXPERT HANDOFF
NO HIGH-FIDELITY YET
```

（Core Interaction 三场景已 Review 批准为 **APPROVED CANDIDATE**，并就地应用 I1/I2/I3/I4；本轮 DOCUMENT CONSISTENCY CLEANUP 修正残留旧表述（§3.1 待发布语义 / §7 C-1 进入制作路径 / §4 去「专业面弹层」Modal 表述 / §3 「P8 边界」→ Context Isolation Truth Boundary）。**CLOSED**：不再继续设计、不进高保真，等待 Operating Strategy Expert 交接。未越界、未 Frozen、未开发。）
