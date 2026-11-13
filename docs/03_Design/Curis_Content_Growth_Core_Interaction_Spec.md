# Curis Content Growth — Core Interaction Spec（结构稿 + 交互规范）

**Status**: CORE INTERACTION DESIGN · **APPROVED CANDIDATE** · **OPERATING STRATEGY INTEGRATION CANDIDATE**（设计建议 · 非 Frozen · 非高保真 · 非前端代码 · 非 Runtime/Connector）
**阶段**: PRODUCT / WORKSPACE DESIGN — Core Interaction（第一轮只设计 3 个核心场景）
**上位依据（不修改）**:
- `Curis_Company_OS_Shared_Authority.md`（Frozen · ⑥⑧⑦ + Context Isolation）
- `Curis_Content_Growth_Domain_Authority.md`（Frozen · ①②③④⑤ + Distribution Execution Policy + Capability Truth）
- `Curis_Workspace_Shell_Contract_And_Shared_Patterns.md`（Frozen · P1–P7 · 四独立 Pane · T1/T2/T3 · 无 Global Topbar）
- `Curis_Content_Growth_Product_Model_Closure.md`（PRODUCT MODEL RECOMMENDATION · 已 APPROVED）
- 5 份 Exploration + Closure 上游文档（均 DESIGN RECOMMENDATION）

**本轮边界（硬约束）**：
- 不修改 Frozen Authority / Shell / P1–P7 / Product Blueprint / XHS·RD Instance / Runtime / Connector / 代码 / UI。
- 本轮只做**结构稿 + 交互规范（中保真）**，不进最终视觉高保真、不进 Figma、不写前端。
- 本轮只设计 **3 个核心场景**：① First-Run / Account Setup ② Content Growth Business Home ③ Continuous Content Journey。Closure §6 的其余 7 个界面**不在本轮**（见 §9）。

**Review 结论（承接）**：Product Model Closure APPROVED → 推荐模型 = Content Growth Business Home + 经营方向 + Continuous Content Journey + Professional Workspace on demand。本轮把该模型落为可评审的结构与交互。

> **本轮 Review 更新（APPROVED CANDIDATE · 4 INTERACTION DELTA）**：承接 Core Interaction Review APPROVED，统一修正 **I1 Opportunity 默认自动（对齐 Frozen P4）/ I2 Publishing 默认自动 / I3 Professional Workspace ≠ Modal（Main 切入专业工作状态）/ I4 CEO Operating Rules（Design Candidate）**。5 份文档就地更新，未新增大量文档；Professional Workspace 仅改进入方式示意，仍不设计内部布局。详见 §3.2（I1/I2/I4.9）/ §4.1（I1）/ §4.4（I2）/ §6（I3）/ §10（I4）。

> **运营策略集成标记（OPERATING STRATEGY INTEGRATION CANDIDATE · 2026-08-16）**：承接《Operating Strategy Product Handoff · FINAL》，把运营专家定义的「真实经营方法」翻译为产品体验。本轮**不改动已批准的三场景**（First-Run / Business Home / Continuous Content Journey 仍为 APPROVED CANDIDATE），仅叠加运营策略翻译层，并补充 3 个关键新增场景的中保真结构稿。翻译总纲与分册：
> - `Curis_Content_Growth_Operating_Strategy_UX_Translation.md`（翻译总纲 · 第一原则/映射/纪律）
> - `Curis_Content_Growth_Strategy_Experience_Model.md`（Doc 2 · Home IA / 经营方式 / 方向 / 账号 / 机会 / 社区 / 首启 Goal）
> - `Curis_Content_Growth_Employee_Method_Experience.md`（Doc 3 · 员工方式 / 对话驱动 / 信息雷达 / Token / 不固定5员工）
> - `Curis_Content_Growth_Strategy_Evolution_Interaction.md`（Doc 4 · 进化三类 / 最近学到了什么 / 提案 vs CEO）
> - `Curis_Content_Growth_Wireframe_A_Strategy.html` / `_B_Employee.html` / `_C_Evolution.html`（A/B/C 中保真结构稿）
>
> 纪律延续：不修改 Frozen Authority / Blueprint / XHS·RD / Runtime / Connector / 代码 / UI；不进最终高保真；Platform Facts 四态不写死数字；Context Isolation 引用正确、无 P8；内部术语全隐藏；对话与直接编辑同一份经营方法。
>
> **Translation Closure（2026-08-16）**：运营策略 UX 翻译已于本轮 Closure 达到 **APPROVED CANDIDATE**，停止态 `CONTENT GROWTH OPERATING STRATEGY UX TRANSLATION CLOSED · VISUAL DESIGN DEFERRED · WAITING FOR WORKSPACE ENGINEERING REVIEW`；就地应用 **DELTA T1–T5**（T1 经营方式=聚合入口 / T2 CEO 主动命令不二次 P7 / T3 AI 自主微调须授权边界 / T4 Demo Evidence 明确标识 / T5 Employee Detail 保持 Shared 一致：沿用 Shared 露出方式、仅在 Detail 内加「工作方式」扩展、不改全局 Employee UI、Shared≠Shared Context、权威不足仅记 `SHARED EMPLOYEE DETAIL DELTA CANDIDATE`），三场景与翻译层均保持 APPROVED CANDIDATE 未动。

---

## 0. Shell 映射基线（引用 Frozen，不重定义）

> 四个 Pane 彼此独立、顶部齐平、各自 Pane Header；不采用 Global Topbar 横跨。Main 必有；Context/Utility 是 Adaptive Surface（默认收起、按需展开、Resizable、不占默认空间）。

| Pane | 固定/Adaptive | Pane Header 内容（Frozen 行为） | T 位置 | 本场景角色 |
|---|---|---|---|---|
| **Navigation** | 固定（可 T1 完全收起） | macOS 交通灯 + 🔍 Search + **T1**；六区导航 + 业务空间子项 | T1 = Nav Header 右（折叠转 Main Header 最左） | 全局定位 / 进入内容增长 |
| **Context**（左） | Adaptive（T2 开合） | 类型/名称 + 切换 + 对象动作（由 Instance 声明） | T2 = Main Header 左（常驻） | CG 声明：**选题库 / 信号** |
| **Main** | 固定（必有） | Breadcrumb + **T2**（左）+ **T3**（右，条件）+ More | — | 专业业务主工作面（本场景内容） |
| **Utility**（右） | Adaptive（T3 开合） | 模式名/子标题 + 模式切换 + ↗ Maximize + **T3** | T3 = Main Header 右（展开转 Utility Header 右） | CG 声明：**数据看板 / 图文预览 / 审核** |

**Frozen P1–P7 采用清单（本轮用到）**：
- **P1 三层责任**（Object Owner ≠ Current Responsibility ≠ Current Executor）：内容对象稳定归属「内容增长」；责任随 Handoff 转移；执行者可 none。
- **P2 Employee Presence**：业务对象上的轻量责任存在（谁负责 / 正在做 / 状态），持续可感知、不做常驻列表。
- **P3 System Activity**：Current Executor = none 时的非员工运行时（自动 Analytics / 复用循环），无头像、不冒充员工。
- **P4 Automation by default / Human action only at Decision Gates**：员工自动 Handoff；CEO/用户只在 Decision Gate 操作。
- **P5 Handoff Event**：责任交接轻量呈现。
- **P6 Result Reference**：对话/列表内轻量引用 → 开 Utility Surface（如 📊 数据看板 ▸）。
- **P7 CEO Decision Package**：Needs CEO 严格用 8 要素语义 + 三层信息层级 + Provenance（FACT/POLICY/EVIDENCE/EST/UNK），禁止编造。

> **标注约定（全套结构稿一致）**：在每个 HTML 结构稿中，Navigation/Context/Main/Utility 四 Pane 均显式标注；Pane 内凡是 Frozen Shell 机制标 `SHELL`，凡是 Content Growth 专业内容（Instance 声明）标 `CG`。

---

## 1. 三个核心场景 × Shell Pane 映射总表

| 场景 | Navigation | Main | Context（T2） | Utility（T3） |
|---|---|---|---|---|
| **A. First-Run / Account Setup** | 业务空间 → 内容增长（进入设置流） | 账号连接与分组引导流（空态→添加→授权→AI 建议→确认→进入） | 默认收起（首轮不强制） | 默认收起（OAuth 技术细节不设计） |
| **B. Content Growth Business Home** | 业务空间 → 内容增长（active） | Attention + Light Operations 聚合首屏 | **选题库 / 信号**（按需） | **数据看板 / 增长反馈**（按需） |
| **C. Continuous Content Journey** | 业务空间 → 内容增长 → [经营方向] | 一条内容的连续流（选题→发哪里→各账号制作→发布→回流） | **选题库 / 信号**（本主题） | **图文预览 / 数据**（本主题，含 Professional Workspace 深入入口） |

**一致规则**：Navigation 六区顺序固定不增不减；T1/T2/T3 位置跨场景完全一致；不存在 Global Topbar；Context/Utility 默认收起，点开才占空间（演示 HTML 提供开关验证）。

---

## 2. Scene A — First-Run / Account Setup

### 2.1 流程状态机（不含 OAuth 技术细节）
```
[空态：添加你要经营的账号]
   └─ + 添加账号
        └─ 平台选择（小红书 / 抖音 / B站 / TikTok / …）
             └─ 走平台授权（不设计弹窗/回调，仅“已连接”结果态）
                  └─ 生成【授权后账号卡】
                       └─ （多账号时）AI 分组建议气泡
                            └─ 用户确认 / 调整
                                 └─ [进入内容增长]
```
- **单账号**直接跳过分组，授权后即进入（无「经营方向」词）。
- **多账号**才出现 AI 建议 + 确认步骤。

### 2.2 授权后账号卡（字段，用户侧）
- 平台图标 + 平台名
- 账号昵称 / @handle
- 连接状态（已连接 / 授权已过期 · 可重连）
- 经营定位（轻量一句话，如「AI 科普」/「个人 IP」/「Curis 官方」）
- 当前所属（单账号：隐去；多账号：显示所属经营方向，可改）

### 2.3 四个真实 CASE（本轮必须覆盖）

**CASE A — 仅 1 个小红书账号（极简）**
- 空态 → + 添加账号 → 选小红书 → 授权 → 账号卡出现。
- **全程不出现「经营方向 / 绑定 / 账号矩阵」任何词**。
- 底部直接「进入内容增长」；Curis 内部记为「你的内容经营」（Office 语义完整，用户面零暴露）。

**CASE B — 同平台 2 账号、定位不同（抖音·AI科普 / 抖音·个人IP）**
- 连完第 2 个账号后，AI 白话建议：
  > 「这两个抖音账号讲的东西不太一样——一个偏 AI 科普，一个偏个人日常。建议分开经营，各自有独立选题和策略，互不干扰。要分开吗？」
- 选项：`分开经营（推荐）` / `放一起试试`。
- 选「分开」→ 建两个经营方向（用户面「经营方向」），各自独立选题库/策略。
- 选「放一起」→ 单经营方向（罕见，用户主动）。

**CASE C — 多平台、定位相同（抖音·Curis AI / 小红书·Curis AI / B站·Curis AI / TikTok·Curis AI）**
- 连完多平台同定位账号后，AI 建议：
  > 「这几个账号都在讲同一套内容（Curis AI 品牌），建议放进同一个经营方向，共享选题、资料和策略；需要时再为每个平台分别制作。」
- 选项：`放一起（推荐）` / `我想分开管理`。
- 选「放一起」→ 一个经营方向绑定 4 账号（Frozen：Office 绑 1..N 账号；同定位→同 Office）。

**CASE D — 大量账号、用户自己也不确定怎么分**
- 用户连完一批账号（如 8 个跨平台）。
- AI 读取账号基本信息 / 历史内容（能力允许时）→ 给出建议分组：
  > 「我按内容和定位先分了 3 组：① Curis AI 品牌（抖音+小红书+B站+TikTok）② 个人 IP（抖音+小红书）③ 数码测评（B站+抖音）。你可以直接采用，或拖动调整。」
- 用户操作：**拖动账号在组间移动** / 重命名组 / 合并或拆分组 / 删组。
- 确认后进入；后续仍可在「账号」管理面调整。

### 2.4 AI 分组建议的表达纪律
- 用自然语言 + 理由，不出现 `OfficeAccountBinding` / `Account Pool` / `Target Account Set`。
- 建议是**可确认/可调整**的，不是自动落定；用户始终有最终权。
- OAuth 失效：账号卡标「授权已过期」，保留账号与历史，**不静默删**；提供「重连」入口。

### 2.5 Shell 映射
- Navigation：进入「业务空间 → 内容增长」的设置流（Main 内呈现引导，不另开一级区）。
- Main：上述引导流（空态 / 添加 / 授权卡 / AI 建议 / 确认 / 进入）。
- Context / Utility：首轮默认收起，不强制；OAuth 技术细节不设计。

---

## 3. Scene B — Content Growth Business Home

### 3.1 5 秒信息优先级（用户每天打开应立刻知道）
1. **有没有 Needs CEO**（重大事项：品牌方向 / 预算 / 版权 / 合规 / 重要渠道变化 / 重大账号定位变化）→ 顶部橙色 Decision Banner（Frozen P7）。
2. **今天值得做什么**（AI 发现的值得做选题 / 待你确认的事）。
3. **正在生产什么**（进行中的内容流 + 各账号进度）。
4. **即将自动发布什么 / 哪些发布存在异常需要关注**（正常 Publishing 按规则自动排期发布，不默认等待人工确认；仅异常才需你关注）。
5. **账号是否异常**（OAuth 过期 / 限流 / 平台变动）。
6. **AI 员工正在做什么**（谁在负责、卡在哪）。
7. **最近增长反馈**（轻量指标，非重 Dashboard）。

> **不要**把这 7 项机械做成 7 个等大 Dashboard 模块。**Decision / Attention 天然比普通 Activity 更突出**（Banner > 卡片高亮 > 普通行）。

**自动化默认（对齐 Frozen P4 · Automation by default / Human action only at Decision Gates）**：Curis 按既定经营规则自主运行，普通 Opportunity 与 Publishing **不需要逐条人工批准 / 确认**（详见 §10 CEO Operating Rules）。Home 把「需要 CEO/你决定的」与「自动进行的」清晰分层——Decision Banner 仅重大事由；普通内容自动生产、自动发布，你随时可 查看 / 暂停 / 调整。

### 3.2 结构（视觉优先级，自上而下）
```
[ 可选 Decision Banner：需要 CEO 决策（仅重大事项）]   ← 最突出
[ 当前经营节奏（轻量入口 · I4.9）：今天收集几轮 / 今天计划几条 / 各账号自动发布时间 / [调整经营节奏] ]
[ Attention 组：今天值得做（1–3 张高亮卡）]
[ Light Ops 组：
    正在生产（内容流进度，含 DEFAULT AUTO 自动制作项）
    待发布（多为自动排期，仅异常需确认）
    账号动态（异常高亮）
    AI 在做什么（员工 Presence 紧凑列表）
    增长反馈（轻量指标条） ]
[ 经营方向切换器：多经营方向时出现；单账号隐藏 ]
```
- **单账号用户**：不显示经营方向切换器；整页聚焦「我的内容经营」。
- **多经营方向用户**：顶部或侧边出现轻量切换器（如分段标签 / 下拉），切换不离开 Home、不感知跳房间。
- **当前经营节奏（I4.9）**：Home 不常驻复杂设置表，顶部/侧边提供轻量「当前经营节奏」入口（今日采集轮次、计划条数、各账号自动发布时间），让 CEO 知道公司今天如何运行，不必盯每个 Task；点 [调整经营节奏] 才进入设置。

### 3.3 Shell 映射
- Navigation：业务空间 → 内容增长（active）。
- Main：上述 Home 结构。
- Context（T2，按需）：**选题库 / 信号**——点某选题卡 → 左开选题库看为什么值得做、来源信号。
- Utility（T3，按需）：**数据看板 / 增长反馈**——点增长反馈引用 → 右开数据面板。

---

## 4. Scene C — Continuous Content Journey（本轮最重要）

### 4.1 完整一条内容流（对齐 Frozen P4 · 默认自动，非每步人工 Gate）

> **I1 — Opportunity 默认自动**：普通选题**不是**每次都要用户先「接受」才制作。默认走 **A. DEFAULT AUTO**；仅用户主动或重大事项才打断。普通 Opportunity 不得全部变成人工 Gate。

```
AI 发现选题
  ↓ 为什么值得做（自然语言 + 信号）
[ 路径判定 · 对齐 Frozen P4 ]
  ├─ A. DEFAULT AUTO：符合经营方向 / 内容策略 / 预算 / 风险边界 → 自动进入制作（无需先批准）
  ├─ B. USER-INITIATED：你从「今天值得做」点 [做这个] → 立即进入制作（Opportunity Surface ≠ CEO 审批队列）
  └─ C. DECISION REQUIRED：品牌方向变化 / 超出既定策略 / 预算变化 / 合规·版权风险 / 高成本制作 / 重大账号定位影响 → Frozen P7
  ↓ Curis 建议发到哪些账号（默认 + AI 推荐 + 用户手动，三源合并）
针对账号分别制作（能复用的自动复用；需要不同的分别制作）
  ↓ 每账号当前状态（同一主题、不同进展）
发布（按账号发布规则**默认自动排期/发布**，见 I2；异常才进 Frozen P7）
  ↓ 结果 / 数据回流（System Activity 自动 Analytics）
```

### 4.2 示例主题：「AI 浏览器正在改变办公方式」
目标账号与状态（**同一主题、不同账号的进展**，不是 4 个独立任务列表）：

| 账号 | 制作格式 | 状态 | 在场员工（P2 Presence） |
|---|---|---|---|
| 抖音 · Curis AI | 30 秒口播 | 制作中 | 视频制作·陈真 · 正在制作抖音版本 |
| 小红书 · Curis AI | 图文笔记 | 已完成 | 内容创作·李婷 · 已完成（等待发布） |
| B站 · Curis AI | 8 分钟教程 | 等待制作 | （排队中，下一制作） |
| TikTok | — | Curis 建议暂不发布 | 解释气泡：「这个选题主要针对国内用户，暂不建议发 TikTok」 |

**连续性表达**：用户一眼看到「这是同一条内容在不同账号上的进展」——顶部是主题与统一进度条，下方是按账号展开的制作卡，归属于同一主题。

> 本示例采用 **A. DEFAULT AUTO** 路径：该选题符合 Curis AI 经营方向与品牌策略、风险正常，Curis 已自动进入制作，用户无需先「接受」；Home 与 Journey 均显示「正在制作 + 为什么做这个」，用户可随时 查看 / 暂停 / 调整。
**复用行为化（禁词）**：若小红书图文封面可复用为 B站 缩略图，UI 只显示「✓ 已自动复用封面」，不出现 `HIGH_REUSE` / `FULL_DIVERGENCE` / `Variant` / `reuse_mode`。需要不同的（抖音口播 vs 小红书图文）就分别制作，用户感知是「Curis 针对不同账号分别制作」。

### 4.3 发到哪里（三源合并，不机械勾选）
- **默认自动选择**：根据经营方向 + 平台适用性预选。
- **AI 推荐**：自然语言解释（如「这个选题主要针对国内用户，暂不建议发 TikTok」），用户可采纳。
- **手动调整**：增/减账号（如加 TikTok / 移除某账号），不要求每条机械勾选全部。
- 表达用自然语言选项代替 `BEST_EFFORT` / `ALL_REQUIRED`：「其他账号可以继续发布」/「需要全部账号都准备好再一起发布」。

### 4.4 Shell 映射 + Professional Workspace 按需进入
- Navigation：业务空间 → 内容增长 → [经营方向]。
- Main：连续内容流（主题 + 各账号制作卡 + 状态 + Presence）。
- Context（T2）：本主题的**选题库 / 信号**（为什么值得做、来源）。
- Utility（T3）：**图文预览 / 数据**（本主题）；点「查看小红书发布详情」→ Main 切入 **XHS Channel Operations** 专业工作状态（见 §6，非 Modal）。

**发布默认自动（I2 — 对齐 Frozen P4）**：各账号按既定发布规则**自动排期 / 发布**；Home / Journey 显示「XX · 今晚 20:00 自动发布」+ [调整]，而非默认 [确认]。仅异常（多账号须同步但某账号 Blocked / 平台异常 / 超发布策略 / 重大活动 / 额外预算 / 风险内容）才进 Frozen P7 CEO Decision。

---

## 5. AI Employee Presence（跨 3 场景自然出现）

**出现位置（仅 3 场景内，不额外设计员工管理 Dashboard）**：
- Scene B Home：「AI 在做什么」紧凑列表（谁负责 / 正在执行 / 当前状态）。
- Scene C Journey：每条账号制作卡上的 Presence（如 视频制作·陈真 · 正在制作抖音版本）。
- Scene A：不出现（尚未进入生产）。

**显示**：Identity（名+角色）+ Current Responsibility + Current Activity + Status（复用 §3.1 状态色）。
**不显示**：Router / Assignment Policy / Queue depth / Capacity score / routing score——这些概念本轮不暴露，⑨ Queue/Bottleneck 仍 VISION/RESERVED。

**增员路径（未来，本轮仅留入口形态）**：
- 主动增加：设置里「添加员工」。
- Curis 建议增加：以白话出现（如「最近视频常卡在字幕，建议加一名字幕员工」），用户只看「为什么需要 / 增加后变化 / 大致成本」，指标全隐藏。本轮不把 Candidate 画成确定功能，可作 VISION 探索。

---

## 6. Professional Workspace（按需进入 · 非 Modal · I3）

Content Growth **不是**超级 Workspace；深度工作由各自 Professional Workspace 承担，但**进入方式是 Main 切入专业工作状态，不是弹窗（Modal）**。

**正确进入模型（DELTA I3）**：
1. 用户在 Content Journey 点某账号版本（如「编辑抖音版本」）。
2. 当前内容语境保持（仍是「AI 浏览器」这条内容）。
3. Main 切入对应 Professional Workspace 的**工作状态**（如 Content Production · 抖音版本）。
4. Context / Utility 按专业面**重新声明**（Content Production：Context = 素材 / 品牌资料 / 平台要求；Utility = 预览 / Evidence / 发布要求）。
5. Breadcrumb 保持内容语境：`业务空间 / 内容增长 / AI浏览器 / 抖音版本`。
6. Main Header 提供 `[返回内容流]`；点后即回原 Content Journey，上下文连续。

**关键**：Professional Workspace 是深度专业工作面，**不是 Modal 弹层**。用户不感知在「内容增长」与「制作/渠道 Workspace」之间反复横跳为两个独立大房间 = **上下文连续**（同一内容语境贯穿），而非把专业能力塞进弹窗。

| 用户动作 | 进入的专业面（Main 切入） | 重新声明的 Context / Utility |
|---|---|---|
| 点「编辑抖音版本」 | Content Production · 抖音版本 | Context = 素材 / 品牌资料 / 平台要求 · Utility = 预览 / Evidence / 发布要求 |
| 点「查看小红书发布详情」 | XHS Channel Operations · 小红书版本 | Context = 发布状态 / 定时窗口 · Utility = 平台回执(Receipt) / Evidence |
| 未来：点「准备 B站 版本」 | Bilibili Channel Operations · B站版本 | 同上结构 |

**本轮不设计这些 Professional Workspace 的内部布局 / 高保真**（仅定义进入模型与触发点 + Context/Utility 重新声明）。

---

## 7. 关键交互点击路径（Interaction Spec）

**A-1 添加首个账号**：空态 `+ 添加账号` → 平台选择 → 授权（模拟）→ 账号卡 → `进入内容增长`。
**A-2 多账号 AI 分组**：第 2+ 账号授权后 → AI 建议气泡 → `分开/放一起` 或 `拖动调整` → 确认 → 进入。
**B-1 处理 Needs CEO**：Decision Banner `[按建议处理] [其他方案] [暂缓]`（复杂/不可逆类降级为 `[查看方案] [暂缓]`）→ 决策后 AI 自动继续（P4/P7）。
**B-2 看选题为什么值得做**：点 Attention 卡 → T2 开 Context（选题库/信号）。
**B-3 看增长数据**：点增长反馈引用 → T3 开 Utility（数据看板）。
**C-1 进入制作**：普通路径 = 符合经营规则 → 自动进入制作；或用户在机会面点 `[做这个]` → 进入制作；之后 → 「发到哪里」三源合并 → 分别制作。重大事项才走 P7。
**C-2 深入某账号制作**：点「编辑抖音版本」→ 展开 Content Production 专业面（同语境）。
**C-3 看发布详情**：点「查看小红书发布详情」→ 展开 XHS Channel Operations 专业面。
**C-4 看数据回流**：发布后 → System Activity 自动 Analytics → Result Reference 📊 数据看板 ▸（P3/P6）。

---

## 8. 颗粒度与纪律

- 本轮产出 = **结构稿 / Wireframe + Interaction Specification**（中保真，接近真实布局但不做最终视觉精修）。
- 重点检查：信息层级 / 点击路径 / Pane 关系 / 多账号表达 / 内容流连续性 / 用户认知。
- 所有结构稿标注 Navigation/Context/Main/Utility 与 `SHELL` / `CG` 区分。
- 不修改任何 Frozen 文档；不写正式前端；不开发 Runtime/Connector；不直接做最终视觉高保真；不继续研究架构。

---

## 9. 本轮不设计（留给后续轮次）

- Professional Workspace（Content Production / 各平台 Channel Operations）的**内部布局与高保真**：其**进入模型（I3 · Main 切入专业工作状态 + Breadcrumb 保持内容语境 + [返回内容流]）本轮已定义**，仅内部布局 / 高保真留给后续轮次。
- Closure §6 其余 7 个界面：经营方向容器与切换器细节、Connected Accounts 管理面完整、增员轻入口细节、Context 可追溯入口细节、Needs CEO 完整呈现（沿用 P7，已于 §3.1/§7 占位）、XHS 当前实例未来纳入 IA 草图。
- Operating Context（仍 RESERVED/DEFERRED）、N:N 共享账号复杂 UX（首版 1 Account : 1 Primary 经营方向）、Queue/Bottleneck 指标呈现（⑨ 未 Frozen）。
- **CEO Operating Rules 的具体数值 / 默认节奏**（I4.8 仅为示例，不 Frozen；§10 为 Design Candidate，不新增 Contract / Primitive）。

---

## 10. CEO Operating Rules（Design Candidate / Product Model Candidate · 非 Frozen · 非 Contract）

> **性质**：本节 Operating Rules 是 **Design Candidate**，仅记录产品模型设想；**不新增 Frozen Primitive / Contract**，不修改任何 Frozen Authority。下一阶段若批准，可升格为 Instance Spec 或 Design Record。

**核心模型（I4）**：Automation by default ≠ AI 任意搜索 / 制作 / 发布，也 ≠ CEO 逐条批准。正确模型：
> CEO 制定日常经营规则 → AI 在规则内自主运行 → 数据持续回流 → AI 发现更优策略 → 向 CEO 提出规则调整建议 → CEO 决定 → 新规则成为后续自动运行依据。

**与 I1 / I2 的统一（I4.10）**：
```
CEO Operating Rules
  → Opportunity Discovery
  → Production
  → Distribution
  → Publication
  → Analytics
  → AI Optimization Suggestion
  → CEO Rule Update（必要时）
```
- **I1**：普通 Opportunity 无需逐条批准，因为 AI 按 Operating Rules 决定是否自动进入制作。
- **I2**：普通 Publishing / Scheduling 无需逐条确认，因为 AI 按账号 Publishing Rules 自动排期。

**I4.1 信息 / 选题采集规则**：用户自然表达采集节奏（如「每天 09:00 / 15:00 / 21:00 收集」「每 4 小时一次」「重点关注哪些方向 / 来源」「每轮最多保留多少机会」「是否允许符合策略的高价值选题自动进入制作」）。AI 按节奏工作，非 24h 无限搜索。

**I4.2 内容生产节奏**：用户表达经营节奏 / 目标（如「Curis AI 经营方向：每天 2 条短视频 + 1 篇图文」「工作日 2 条 / 周末 1 条」），这是经营目标，非 Workflow / Task Scheduler / Routing 配置。

**I4.3 每账号发布规则**：不同账号可有独立发布节奏（如抖音每天 2 条 12:30 / 20:30；小红书每天 1 篇 20:00；B站 周二 / 周六 19:00；TikTok 暂不自动发布）。AI 在规则内自动排期，正常发布不逐条确认；随时可 查看 / 调整 / 暂停。

**I4.4 规则层级**：最简单继承——经营方向默认规则 ↓ 账号规则（可覆盖）↓ 单次内容临时调整。用户侧只自然表达「默认这样运行 / 这个账号单独设置 / 这一次例外」，不出现 Policy inheritance / Override hierarchy。

**I4.5 AI 自动执行边界**：符合现有经营规则 + 风险正常 + 能力可用 → 自动执行，不需 CEO 批准。突破经营规则 / 改变长期策略 / 额外预算 / 重大品牌影响 / 合规·版权风险 / 重要账号定位变化 → Frozen P7 CEO Decision。因此 **Operating Rules ≠ CEO Decision**：前者是 CEO 预先授权 AI 如何日常经营，后者是 AI 遇超界问题请求判断。

**I4.6 AI 建议修改规则**：数据回流后 AI 可提优化建议（如「抖音 20:30 发布播放量明显高于 12:30，建议调整下午档」），用户看到 为什么建议 / 依据什么数据 / 调整后会发生什么 → [按建议调整] / [其他方案] / [保持现在]。批准后改的是**后续经营规则**，非仅当前一条内容。

**I4.7 不允许 AI 静默改变长期经营规则**：AI 可在规则内自主优化执行，但长期经营规则明显变化（每天 1 条 → 5 条 / 国内 → 新增 TikTok 自动发布 / 内容方向改品牌定位 / 长期预算明显增加）必须让 CEO 知道，不得因「可能更好」静默永久修改。

**I4.8 First-Run 不复杂化**：新用户首次连账号不填几十项规则；Curis 提供推荐默认（如「我先按稳妥节奏运行：每天收集几次选题、每天准备一定数量内容、按账号常用时间自动发布；之后据数据给你调整建议」），用户 [就这样开始] / [调整一下]。具体次数 / 时间仅为 Wireframe 示例，不 Frozen。

**I4.9 Home 增加「当前经营节奏」**：Business Home 不常驻复杂设置表，增加轻量入口「当前经营节奏」（如「今天 09:00 已完成选题收集 · 15:00 下一轮 · 今天计划 2 条 · 抖音 20:30 自动发布 · 小红书 20:00 自动发布」+ [调整经营节奏]），让 CEO 知道公司今天怎么运行，不必盯每个 Task。

**I4.10** 见上「与 I1 / I2 的统一」。

---

*Curis Content Growth — Core Interaction Spec · APPROVED CANDIDATE · OPERATING STRATEGY INTEGRATION CANDIDATE（非 Frozen）*
