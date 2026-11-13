> **📌 Status: HISTORICAL（2026-08-17 设计文档整合）** — 本 Visual Closure 记录高保真重制过程，属**历史审批证据**；当前视觉以 Frozen 视觉系统（`Curis_UI_Frozen_Spec_2026-08-04.md` + `_system/tokens.css`）与 Frozen Shell Contract 为准。新 Agent **无需必读**；旧原型 HTML 仅作 **VISUAL QUALITY REFERENCE — NOT AUTHORITY**。

# Workspace Engineering · 高保真重制 Visual Closure（Remake Visual Closure · Delta-X9）

> **Status**：VISUAL CLOSURE（高保真重制完成 · Bounded UX Simplification 已落 · 停止 Review）
> **纪律**：不写正式产品代码（仅原型 mock）；不修改 Frozen（P1–P7）/Shared Contract/§9；不创建 P8；不暴露 Agent/Router/DAG/Package/Gate 内部原语。
> **消费依据**：`CURIS_SHARED_BUSINESS_WORKSPACE_MAIN_COMPOSITION_CLOSURE.md`（APPROVED · 已回写 Frozen Delta-X9）+ `Curis_Workspace_Shell_Contract_And_Shared_Patterns.md`（Frozen · Delta-X9 回写）+ `WORKSPACE_ENGINEERING_FINAL_IA_CLOSURE.md`（含 2 项语义修正）+ Frozen 视觉系统（`curis-ui-prototype/_system/tokens.css` · `canonical-nav.js` · `Curis_UI_Frozen_Spec_2026-08-04.md`）。

---

## 0. 本次重制目标

在 **Shared Main Composition Closure（APPROVED，已回写 Frozen Delta-X9）** 批准后，直接重制空间工程部高保真原型。核心新增约束（相对 Final IA 版）：

- **真实 Curis Desktop 四独立 Pane Shell**：Nav(220px, T1 全收) + Context(T2, 默认收起) + Main(必有) + Utility(T3, 默认收起, ↗最大化)；四 Pane 顶部齐平、各自 Pane-local Header；**无全局 Topbar**。
- **进行中屏 Main = Domain Business Surface(上) + 工作区(下)**：
  - 上半 = 当前建设任务的 Domain Business Surface（任务目标 / 当前总体进度 / 当前阶段 / 当前问题·Blocker / 最近重要成果 / 是否 Needs CEO），轻量非 Dashboard；「业务展示区」仅内部架构名，非强制 UI 标题。
  - 下半固定 = **工作区**（统一名）= Employee Workstation List；每 Employee 固定轻量卡（头像+姓名+岗位+当前职责+当前状态+展开/收起），展开后统一显示 Frozen Conversation-first Workstation；**Runtime 状态 ≠ UI 折叠状态**。
- **唯一默认展开行为**：从办公室外部进入且存在单一当前 working Employee 时，该 Employee Workstation 默认展开（此处 = 「小录」）。CEO 进入后可自由展开/收起任意员工；收起不改变员工真实工作状态。
- **Main must stand on its own**：Context/Utility 全关时 CEO 仍能理解业务整体状态并完成主要工作。
- **原型评审控件不得伪装产品 Topbar**：屏幕跳转器为左下角可折叠浮层，标注「PROTOTYPE / 示例数据 / 仅评审用」。

---

## 1. 交付物

| 产出 | 路径 | 说明 |
|---|---|---|
| **新高保真原型** | `docs/03_Design/Curis_Workspace_Engineering_High_Fidelity_Remake.html` | 单文件、内联 `<style>` + 原生 JS、零外部依赖；消费 Frozen `--ui-*` 令牌（顶栏 52px / 侧栏 220px / 圆角 4·8·12·999 / 间距 6 档 / 字阶 7 档 / 12px 下限）；真实四独立 Pane，无全局 Topbar；原型导航器为左下角标注「PROTOTYPE/示例数据/仅评审用」的浮层。 |
| 本 Visual Closure | `docs/03_Design/WORKSPACE_ENGINEERING_VISUAL_DESIGN_REMAKE_CLOSURE.md` | 收口记录（Delta-X9 版）。 |

> 旧高保真 `Curis_Workspace_Engineering_CEO_Journey_High_Fidelity.html` **保留未动**，作为对比基线。

---

## 1.5 本轮 Bounded UX Simplification（2026-08-17 · 在 Delta-X9 重制之上继续收敛，不重新研究 Main Composition）

Visual Review 仍不通过后，做有界 UX 收敛。**不改 Frozen Main Composition、不写产品代码**。五点落地：

1. **Context 产品语言与职责**：Context 仅保留为内部 Shell 名称（代码/契约仍用 `Context`），**产品 UI 不直接显示「上下文 / Context」**。它改为按需取用的辅助资源栏。本轮给出 3 个普通用户可理解的中文候选名并选定：
   - 候选：① **资料台**（推荐）② 参考台 ③ 资源台
   - 选定：**资料台**（动词感弱、强调「按需取用的辅助资源台」，与「工作区」并列不冲突；「资料库」因与六区导航「资料库」重名弃用）。
   - 内部 Context Authority 名称未改（代码标识符 `ctx` / `pane-ctx` / `has-ctx` / `toggleCtx` 全部保留）。
2. **删除 Context 中重复的员工 / 流程信息**：进行中屏 Context 删除 责任链、团队 Presence、Employee 入口、当前阶段 等已由 Main 表达的核心业务状态。Context 改为仅展示按需项目资料：已确认需求/目标、行业研究、Operating Model、Workspace IA/Design 输入、参考资料/Knowledge；每项可点击 → Utility 看全文。
3. **工作区去 Card 化**：保持 Employee Workstation List 语义，但视觉改为简洁列表行（头像 | 姓名 | 岗位 | 当前职责 | 当前状态 | 展开/收起），用自然分隔线（border-bottom）替代每个员工的大型 Card。
4. **Workstation 回归普通 AI Conversation**：展开员工后仅 自然消息流 + 必要时单行轻量过程状态行 + Result/Artifact 轻量引用 + 普通 Composer。**删除独立「AI 工作状态」大块**（当前步骤/持有者/等待原因/下一步）与「对话/严谨/快速」模式按钮**。Tool/工作过程仅在真实发生时作为消息流内的轻量状态行出现，不做 Dashboard；Result/Artifact 用轻量引用，点击 → Utility 全文，不放大 Artifact Card。
5. **保持不变**：Main 上部 Domain 业务展示、Main 下部固定「工作区」、Runtime ≠ UI 折叠、外部进入且单一 working Employee 默认展开、Employee Detail → Utility、Result/Artifact 详情 → Utility、Context/Utility 默认收起、Main must stand on its own。

---

## 2. 八屏与四栏对齐

| # | 屏 | 四栏要点（已落实） |
|---|---|---|
| 1 | 空间工程部首页 | Nav=六区+部门高亮+历史/配置入口（仅「首页」可达，其余 muted 上下文）；Context=收起；Main=轻量概览（进行中/近期交付/部门入口+发起入口，**无八问/Dashboard**）；Utility=收起 |
| 2 | 历史建设任务列表 | Main=列表视图；点选 → 状态 6 回顾 |
| 3 | **进行中建设任务（CORE）** | **Main = Domain Business Surface(上：任务目标/进度/阶段/Blocker/成果/Needs CEO 轻量非 Dashboard) + 工作区(下：Employee Workstation List，简洁列表行·去 Card 化)**；Context=**资料台**（按需项目资料：已确认需求/目标·行业研究·Operating Model·Design 输入·参考；点击 → Utility 全文；默认收起，无责任链/Presence/Employee 入口）；Utility=点 Employee/Result/Artifact 展开详情（默认收起，↗最大化） |
| 4 | Shared Employee Detail | Utility=六字段（个人信息/组织关系/长期责任/当前 Responsibility/能力·工作方式/最近结果），**无 Conversation**；Main 停留工作区 |
| 5 | Artifact / Result 全文 | Main=轻量引用卡；Utility=全文详情（无 Conversation） |
| 6 | 已完成建设任务回顾 | Context=已完成摘要+只读责任链（无 live Presence）；Main=回顾性聚合（无实时 Workstation/Dashboard）；Utility=点交付物看全文 |
| 7 | 部门配置 | Nav=部门配置/建设方法入口；Main=配置专业面（**不固定右栏**）；Utility=点条目看 Change Log 详情 |
| 8 | 建设方法 | Main=建设方法专业面；同状态 7 规则 |

**工作区（屏 3 下半）编排**：Employee Workstation List 去 Card 化 → 简洁列表行（头像 | 姓名 | 岗位 | 当前职责 | 当前状态 pill | 展开/收起 chevron + 详情）；展开 = 普通 AI Conversation（自然消息流 + 单行轻量过程状态行 + Result/Artifact 轻量引用 + 普通 Composer，无「AI 工作状态」四格大块、无模式按钮）；默认仅展开单一 working 员工「小录」；Runtime 状态 ≠ UI 折叠；CEO 可自由覆盖展开/收起。

---

## 3. 语义修正的落地验证（沿用 Final IA 2 项 + Delta-X9 补强）

- **Result flow ≠ P5 Handoff**：当前责任员工（小录）完成 Result 后，仅当真实 Responsibility Holder 转移才触发 P5。员工顺序推进不强行标 P5。
- **Audit 收窄**：Change Log 仅记 business-significant 变更；普通配置/对话/routine 不永久保存（fixture 显式声明）。
- **Delta-X9 Main 组合**：Main = Domain Business Surface + 工作区；Employee Workstation ∈ Main.WorkArea（≠ 整个 Main）；「业务展示区」仅内部架构名，可见标题为任务名，非强制 UI 标题。
- **工作区 = Employee Workstation List**：编排不与 Runtime 绑定；唯一默认展开 = 外部进入 + 单一 working Employee；多 Employee 并行默认展开策略本轮不定义。

---

## 4. 纪律遵守

- ✅ 真实四独立 Pane Shell（Nav 220px/T1 全收 + Context/T2 + Main 必有 + Utility/T3·↗），四 Pane 顶部齐平、各自 Pane-local Header，**无全局 Topbar**
- ✅ 原型评审导航器为左下角可折叠浮层，标注「PROTOTYPE/示例数据/仅评审用」，**不伪装产品 Topbar**
- ✅ 进行中屏 Main = Domain Business Surface(上) + 工作区(下)；业务展示区非强制 UI 标题
- ✅ 工作区 = Employee Workstation List；**去 Card 化**为简洁列表行（头像 | 姓名 | 岗位 | 当前职责 | 当前状态 | 展开/收起）；展开 = 普通 AI Conversation（自然消息流 + 单行轻量过程状态行 + Result/Artifact 轻量引用 + 普通 Composer，无「AI 工作状态」四格、无模式按钮）；Runtime ≠ UI 折叠；默认仅展开单一 working 员工「小录」
- ✅ Main must stand on its own（Context/Utility 全关自成立）
- ✅ **Context 产品名 = 资料台**（内部 Shell 名仍为 `Context`，未被修改；产品 UI 不再出现「上下文 / Context」字样）
- ✅ 进行中屏 Context 仅展示按需项目资料（已确认需求/目标·行业研究·Operating Model·Design 输入·参考），**无**责任链 / 团队 Presence / Employee 入口 / 当前阶段 等已被 Main 表达的核心状态；资料点击 → Utility 全文
- ✅ Context/Utility 默认收起、按需钻取；配置/方法走 Nav+Main 专业面，不固定右栏
- ✅ §3.12 禁止：Conversation 仅 Main，不进 Context/Utility；Utility Detail 六字段无 Conversation
- ✅ 未暴露 Agent/Router/DAG/Package/Gate 内部原语（UI 文案一律业务化）
- ✅ 未写正式产品代码（仅原型 mock）；未改 Frozen/P1–P7/Shared Contract/§9；未创建 P8；不重定义 Employee Workstation

---

## 5. 质量审查结论

- **筑原型（prototype-builder）**：运行期冒烟测试通过（8 屏 + 切换 / Utility 钻取 / 工作区展开收起全部无报错）；单文件零依赖，`node --check` JS 语法校验通过。
- **质量审查（critique-reviewer，fresh-eyes）**：**APPROVE-WITH-NOTES**。
  - 6 项绑定规则 **全部 PASS**：① 真实四栏 Shell 无伪装 Topbar ② Main = 业务展示区(上)+工作区(下) ③ 工作区 = Employee Workstation List 且 Runtime ≠ UI 折叠、默认仅展开单一 working 员工 ④ Context/Utility 默认收起按需钻取 ⑤ 未暴露内部原语 / Utility 无 Conversation / 配置走 Nav+Main ⑥ 八屏各自专业面全覆盖。
  - **违规项 = 0**（无伪造 Topbar、无 Agent/Router/DAG/Package/Gate 暴露、无 Utility 内 Conversation）。
  - 1 项非阻塞 note：Workstation 体内「工作过程」原渲染在 Conversation 之前，与 Frozen「Conversation-first」顺序略有偏差 → **已修复**（重排为 `msgs` 在 `aiStatus` 之前，Conversation 真正置首）。

---

## 5.1 本轮 Bounded UX Simplification 验证（2026-08-17）

- **JS 语法**：抽取 `<script>` 经 `node --check` 通过。
- **渲染冒烟（模拟 DOM 调 `screenS3()` / `screenS1()`）**：
  - 进行中屏 Main 仍含 `biz-surface` + `workspace-section`（业务展示区 + 工作区）。
  - 进行中屏 Context 含「资料台」、**不含** 责任链 / Presence / 当前阶段；含行业研究报告等可点击资料引用。
  - 进行中屏 Workstation 不含 `ai-status` 大块、不含「严谨 / 快速」模式按钮；含单行 `ws-status-line` 轻量过程状态行。
  - 首页 Context 不再出现「额外上下文」（改为「额外资料」）。
- **悬挂引用检查**：`aiStatus` / `empCardP2` / `data-enter-ws` / `.ai-status` / `.ais-*` / `.emp` / `presence-dot` / `.modes` / `.mode` 全部已从文件移除；保留的 `data-detail-ws`（工作区「详情」→ Utility 六字段）为既定 Employee Detail 路径，符合点 5。
- **纪律守住**：未改 Frozen Main Composition；未写产品代码；未暴露内部原语；四栏 Shell / 无伪装 Topbar / Main must stand on its own / Context·Utility 默认收起 全部维持。

### 5.2 最终一轮（Shared Employee Work Area + Composer · Delta-X10 对齐 · 2026-08-17）

据 `CURIS_SHARED_EMPLOYEE_WORK_AREA_AND_COMPOSER_CONTRACT_CLOSURE.md`（APPROVED · 修正 3 点）最后一轮重制，未重做 Main / 四栏 / 资料台：

- **Employee Row 两行结构**：头像（居中跨两行）+ 行1 姓名+岗位 + 行2 当前职责 + UI Status pill + 展开箭头；**点击头像/姓名 → Utility Employee Detail，无独立「详情」按钮**（`data-detail-ws` 由头像与姓名共用，stopPropagation 不触发展开）。
- **Shared Employee UI Status（Runtime Truth 投影）**：`空闲`（5 名已完成/等待上游员工）/ `工作中 · 产品设计`（小录，唯一默认展开）；`阻塞·<cause>` 槽位保留但示例数据无真实阻塞事实故不投影；**现有 Runtime State Schema 不动、不新增 Primitive**；对话内 `ws-status-line` 跟随投影（live/blocked/idle 三态），不再硬编码「待命/已完成」。
- **Conversation Surface**：`ws-conv` 居中（`max-width:760px; margin:0 auto`）、Bounded·Responsive（min 320 / max 760 readable width，不写死 px）；`ws-body` `resize:vertical; min-height:240px; max-height:68vh` 支持右下角拖拽调高；展开/收起只改 UI 不改 Runtime。
- **Shared Composer Shell**：Input + 底栏左（`＋` Add / `访问权限 ▾` / `工作模式 ▾` / chips）+ 底栏右（`执行选择 ▾` / `🎙` Voice / `发送`）；Desktop 推荐此左右分组（响应式 `flex-wrap` 可重排）；`＋` 入口语义冻结、文案不冻结。
- **验证**：`node --check` 通过；模拟 `screenS3()` 渲染——`ws-id` 两行结构存在、无「详情」按钮、`ws-av`/`ws-id` 均带 `data-detail-ws`、`空闲`×5 + `工作中 · 产品设计`、`c-add`/`访问权限`/`工作模式`/`执行选择`/`c-voice` 全部落位、s3.main 不含「待命」、`.ws-conv` 居中 + `.ws-body` 可拖拽 CSS 落位。
- **纪律守住**：未改 Frozen Shell/Shared Authority（本轮仅为消费方）；未写产品代码；未暴露 Agent/Router/DAG/Package/Gate；四栏 / 无伪装 Topbar / §3.12·§3.14 禁止项 / Main must stand on its own 全部维持。

### 5.3 最终简化（Delta-X11 · 彻底去 Card + 统一 Surface · 2026-08-17）

用户裁定视觉仍不通过，要求最后一次 simplification（不再研究，严格按已确认规则执行）：

1. **Employee Row 彻底去 Card**：`.ws-item.open` 不再有 `background: var(--ui-surface)`；Row 改为真正单行列表行（头像 | 姓名·岗位 | UI Status 轻量文本靠右 | ▸ | 当前职责）；删除 `.ws-head-main` 两行容器和 `.ws-actions` 包裹；UI Status 从 `pill.live/warn` 改为 `.ws-status` 轻量文本（空闲/工作中·<desc>/阻塞·<cause>），不用 pill/card。
2. **Conversation 彻底回归纯 AI 对话**：删除 `wsStatusLine()` 函数及其全部 CSS（`.dot-live/.dot-warn/.dot-idle/.ws-status-line/.ws-status-idle`）；Conversation 内不再展示当前步骤/Holder/暂无进行中的工作/工作中状态块/下一步——Employee 状态已在 Row 右侧表达，Conversation 只保留自然消息流 + Runtime 真实发生时的轻量过程 + Result/Artifact 轻量引用 + Composer。
3. **Result/Artifact 去 Card**：`resultCard()` 大卡片（`.result` 含 thumb/info/rt/rd/rk）替换为 `artRef()` 轻量行内引用（`📄 标题 ↗`，`.art-ref`）；Conversation 内不显示摘要/类型/缩略图等大块信息；Utility 内部完整展示不受限制。
4. **Composer 统一圆角输入 Surface**：不再是 textarea Card + toolbar 两层视觉；改为统一圆角 Surface（`border: 1px solid; border-radius: var(--ui-r-lg)`）：上部自然多行输入（`background: transparent; border: 0`）+ 底部图标/文本入口行（`.c-entry`：`background: transparent`，非 pill 卡片）；Shared 语义槽位不变（＋ | 访问权限 | 工作模式 | 已选资源 | 执行选择 | Voice | Send）。
5. **去掉 Workstation 大外框**：`.ws-body` 删除 `border-top: 1px solid var(--ui-line)` 和 `overflow:auto; resize:vertical; min-height:240px; max-height:68vh`；展开后视觉 = Employee Row ↓ 自然 Conversation Surface（仅 `padding` 间距分隔），非 Employee Card { Header + Conversation + Composer }。
6. **清理 HTML 顶部旧规则**：注释从「高保真重制 (High-Fidelity Remake)」更新为「最终简化 (Delta-X11)」；删除「每个员工固定轻量卡」「工作状态 + Result 轻量引用」等已被 Shared Contract 替代的旧纪律行；`<title>` 同步更新。

**验证**：`node --check` JS 语法通过；19/20 字符串级检查 PASS（唯一 `.pill.live/warn` CSS 残留为业务表面/Artifact 元数据使用，非员工状态）。

---

## 6. 停止态

```text
WORKSPACE ENGINEERING HIGH-FIDELITY REMAKE — VISUAL CLOSURE (Delta-X9 + Bounded + Delta-X10 + Delta-X11 最终简化)
→ 输入：Shared Main Composition Closure（APPROVED）+ Bounded UX Simplification 五点
  + Shared Employee Work Area + Composer Closure（APPROVED · 修正3点）+ Delta-X11 最终简化六点
→ 交付：Curis_Workspace_Engineering_High_Fidelity_Remake.html（8 屏，单文件零依赖，真实四独立 Pane）
→ 最终态：Employee Row 单行列表(去Card, uiStatusText轻量, 点头像/姓名→Utility)
  / Conversation 纯对话(删wsStatusLine, artRef轻量引用)
  / Composer 统一圆角Surface(非textarea+toolbar两层) / 无Workstation大外框
  / HTML头部旧规则已清理(Delta-X11)
→ 纪律：未写产品代码 / 未改 Frozen 真源 / 未新增 Runtime Primitive / 未暴露内部原语
→ 审查：node --check PASS; 字符串级 19/20 PASS（.pill.live/warn 残留为业务表面用，非员工状态）
→ 停止 Review（STOP FOR REVIEW · 用户指令：完成后停止 Review）
```

*本文件为 Workspace Engineering 高保真重制 Visual Closure（Delta-X9 Shared Main Composition 对齐版）· 2026-08-17 · 非 Frozen / 非产品代码 / 不重定义既有 Authority · 由设计原型专家团 prototype-builder(筑原型) + critique-reviewer(严过审) 产出。*

**prototype-builder 两项假设（已落盘，供后续裁决）**：
1. 六区导航仅「首页」可达，其余 muted 上下文（评审阶段无真实其他业务空间数据）。
2. 进行中屏默认仅展开单一 working 员工「小录」（符合 Delta-X9 唯一默认展开行为）。
