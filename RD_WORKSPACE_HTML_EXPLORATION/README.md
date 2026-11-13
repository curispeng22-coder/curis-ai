# RD Professional Workspace — 视觉 / 交互 HTML 探索 · Review 材料

> **Status**: `EXPLORATION` / `CANDIDATE`（视觉探索产物，**非 Authority**、非设计终稿、非正式前端）
> **Round**: CURIS — RD + MUSIC VISUAL EXPLORATION（本目录为 **RD 线**，与 Music 线**分开设计 / 分开 HTML / 分开验证**）
> **Date**: 2026-09-19
> **结构输入（唯一）**: `Curis Business Research/product-translation/shared/RECONCILIATION_INDEX.md` + `rd/` 四份文档
> **视觉基线**: `curis-ui-prototype/_system/tokens.css`（Frozen 令牌，暗色为默认）
> **边界**: 未修改 Authority / Blueprint / Runtime / Backend / Database / 正式 Frontend；未 Figma；未 commit / push。

---

## 1. 页面结构说明

### 1.1 桌面四 Pane 骨架

```
┌─ window bar（标题 / Project 面包屑 / 主题切换 / CEO 视角）────────────────┐
├──────────┬─────────────┬──────────────────────────────┬─────────────────┤
│ 全局导航  │ 文件·最近对象 │ Main                          │ Utility          │
│ （七区）  │ （可折叠）    │ ① Project Operating Header    │ Diff / Test /    │
│          │             │ ② Decision Banner（内嵌）      │ PR / Build       │
│          │             │ ③ Employee Work Surface       │ （view-only）     │
└──────────┴─────────────┴──────────────────────────────┴─────────────────┘
```

- **全局左导航**：Curis 七区原样（CEO 工作台 / 业务空间 / 组织中心 / 人才与能力 / 经营洞察 / 资料库 / 会议），**未新增 Project 级导航**。点击七区为占位提示（本轮只探索 RD 工作区）。
- **Main 只有两块面**（对齐 `RD_PRODUCT_TRANSLATION §5` / `RD INSTANCE §1.1`）：
  - **① Project Operating Header** — 紧凑条带，回答 CEO 第一眼的四个问题：这个项目做什么 / 现在做到哪里 / 有没有问题 / 下一步是什么。组成：Project Name · Goal · 当前版本 · 当前阶段 · 本轮目标 · Work 计数（总数 / 进行中 / 已完成 / 阻塞 / 需 CEO）· 总进度 % · Leader 判断 · 下一步检查。**刻意不做成大 Dashboard**。
  - **② Employee Work Surface** — 本项目真正的核心。按**真实工作状态排序**（Working → Needs CEO → Review → Blocked → Waiting → Complete → Idle）：
    - `Working` → 展开持续工作面：Employee 身份 / Responsibility / 当前 Work / Provider / 执行状态 → 紧接 **Conversation + Result Reference + Composer**；
    - `Waiting` → 压成一行；
    - `Idle` → 不占主要空间。
    - **不是员工卡片墙**：信息密度靠排版与状态而非 Card 堆叠。
- **Decision（Needs CEO）内嵌 Main 顶部**（琥珀色 Banner），**没有独立「待裁决」页面**。含八要素：发生什么 / 为何 AI 不能自决（FACT）/ 影响（FACT）/ 风险（EST）/ Employee 建议（POLICY）/ 预计时间 / 证据标签 / 三个动作（批准 · 拒绝 · 提供指示）。
- **Utility 右栏**：按引用类型给 mode —— `diff → 差异 / 源码`，`test → 测试 / 预览`，`pr → PR`，`build → 构建`。底部固定「返回 Conversation」。**Utility 只负责查看**；任何修改都要回到 Conversation → Employee → Provider。
- **左二栏（Context）**：命名为「**文件 · 最近对象**」（**不叫「上下文」**），内容为当前 Project 的 25 个相关文件 + 10 条最近对象，顶部可 ✕ 折叠。

### 1.2 目录内容

| 文件 | 作用 |
|---|---|
| `index.html` | 开发版骨架（外链 styles.css / data.js / app.js） |
| `tokens.css` | **Frozen 设计令牌副本**（`curis-ui-prototype/_system/tokens.css` 原样复制，未改一个字节） |
| `styles.css` | 全部样式，`@import` tokens.css 后只消费 Frozen `--ui-*` 令牌，不新造调色板 |
| `data.js` | 全部 Mock 数据（3 Project / 6 Employee / **19 Work** / 17 Result Reference / 文件与最近对象） |
| `app.js` | 渲染与交互（Provider 异步执行、Conversation、Decision、Utility、Context） |
| `_build.js` | 零依赖打包：把 tokens.css + styles.css + 全部 JS 与 body 骨架内联为单文件 |
| **`RD Workspace.html`** | **单文件版**（由 `_build.js` 生成，**禁止手改**），零外链，双击即用 |
| `_check.js` | 真实浏览器点击自测脚本 |
| `_check.log` | 自测输出（断言 + Console 记录） |
| `_evidence/*.png` | 逐步截图证据（**14 张**） |
| `README.md` | 本文件 |

> **⚠️ 本轮修复记录（保真缺陷，非设计取舍）**：首次构建出的单文件版**缺失 Frozen 令牌**——`styles.css` 引用了 44 个 `--ui-*` 变量（`--ui-bg` / `--ui-text` / `--ui-sp-*` / `--ui-fs-*` …），但本目录既无 `tokens.css`，`_build.js` 也只内联了 `styles.css`。结果是 `background: var(--ui-bg)` 解析为空、页面**退化成无主题的白底默认样式**，Frozen 暗色基线完全丢失，而文本长度类断言**察觉不到**（只有实读截图才能发现）。
> 已修复：补入 `tokens.css`（Frozen 原件）+ `styles.css` 顶部 `@import` + `_build.js` 改为「tokens 先于业务样式」内联并剥离 `@import`。修复后复核：`--ui-bg/--ui-surface/--ui-line/--ui-text/--ui-accent` 均已有定义；RD 引用的 44 个 `--ui-*` 中**仅 7 个 `--ui-syntax-*` 由本探索自建**（源码高亮候选值，其余全部命中 Frozen 定义），**零悬空引用**。

---

## 2. 关键交互说明

| # | 交互 | 行为 |
|---|---|---|
| 1 | **Project 切换** | 顶栏 Project 选择器 → 切换 Project Context，Header 全量刷新，员工展开态按新 Project 的工作状态重建。**Project 只存在于本 Workspace 内部，不进全局导航**。 |
| 2 | **Employee 展开 / 折叠** | 点员工头即切换展开；展开后直接呈现 Work + Conversation + Composer。 |
| 3 | **多 Work 切换** | 徐川同时持 `W-231 Working·Codex` / `W-232 Working·Claude Code` / `W-236 Review`。点 Work 切换器 → **Conversation 上下文随 Work 切换，绝不串线**。 |
| 4 | **Conversation 双向** | Composer 输入 + Enter / 发送 → CEO 消息入列 → 员工按当前 Work 给出**真实研发回复**：若说「拆成两条并行」，员工回复「已拆成两个并行 Work：W-231 走 Codex、W-232 走 Claude Code」并触发执行。 |
| 5 | **Provider 异步执行** | 触发后 Provider 消息进入 `执行中… N.Ns` 实时计时（ticker 每 400ms），4.5s 后转为「执行完成」并**自动挂上 Result Reference**。**切到别的员工/Work 不会中断执行**（job 挂在全局 state，不在 DOM 上）。 |
| 6 | **Result Reference → Utility** | Main 内只有轻量引用（查看差异 / 测试结论 / PR / 构建）；点击 → 右栏 Utility 打开对应结果，可切换 `差异↔源码`、`测试↔预览`。 |
| 7 | **Decision 批准 / 拒绝 / 指示** | 批准：架构师 `W-233` 由 `needs_ceo`→`working`、下游测试 `W-240` 由 `waiting`→`working`、Project 进度 **+8%**，相关员工自动展开，Banner 消失，toast 说明。拒绝：写明退回理由并保留 blocker。指示：直接跳到该员工对话并预填指示文本。 |
| 8 | **Work 完成 → 计数变化** | Work 状态变化后 Header 的 Complete / Working 计数与进位同步反映。 |
| 9 | **Context 折叠 / 主题切换** | 「文件 · 最近对象」可整栏折叠；暗 / 亮主题切换（暗色为默认）。 |
| 10 | **Utility 关闭** | 底部「返回 Conversation」或 ✕ → Utility 收起，回到员工工作面。 |

---

## 3. 与 Product Translation 的对应关系

| 本探索的体现 | 结构来源 |
|---|---|
| Main = Project Operating Header + Employee Work Surface **两块面** | `RD_PRODUCT_TRANSLATION §5`；`RD_PROFESSIONAL_WORKSPACE_STRUCTURE_CANDIDATE §1` |
| Conversation 为主要工作表面，**无独立 Work Detail 页** | `RD_PRODUCT_TRANSLATION §4` |
| Decision（Needs CEO）**内嵌** Main 当前工作位置，无独立待裁决页 | `RECONCILIATION_RULINGS §4 R1–R4`；`RD_INSTANCE §7 P7` |
| Project = Workspace 内 Project Context，**不升格 canonical core asset**，不进全局导航 | `RECONCILIATION_RULINGS §4 **R1/R2/R3**`；`RECONCILIATION_INDEX §3` |
| 七区主导航不变 | 同上 **R3** |
| RD 达 Professional Workspace 门槛但**保持极简**（无 5 区域 / 8 页） | 同上 **R4**；`RECONCILIATION_INDEX §2.1` |
| Utility 仅 Diff / Test / PR / Build / 源码 / 预览，**view-only** | `RD_INSTANCE_APPROVED §3` |
| Employee / Responsibility / Provider 三元分离，Provider 明确标注（Codex / Claude Code / Copilot / GitHub Actions） | `RD_EMPLOYEE_AND_PROVIDER_EXECUTION_MODEL`；`RECONCILIATION_RULINGS §1` |
| Result Intake 四模式 `API_SYNC / COMPUTER_USE / IMPORT / MANUAL_ENTRY` | `RECONCILIATION_RULINGS §2`；`RD_RESULT_INTAKE_AND_CONTINUOUS_OPERATION` |
| Auth Stop Gate = 既有 `WAITING_FOR_USER`（GitHub Actions 等待类 Work、Work 六态中的等待态） | `RECONCILIATION_RULINGS §3`；G1 §3 |
| 一行 `lib/auth-stop-gate.ts` 差异里写明 `setState(WAITING_FOR_USER); // 对齐 G1 §3，不新造状态名` | 同上 |
| 六态 Working / Waiting / Blocked / Needs CEO / Review / Complete | `RD_INSTANCE_APPROVED §4` |

**明确未做（符合禁令）**：无 IDE / 代码编辑器 / Terminal / Git 客户端 / CI 流水线 / 部署工具；无 5 专业区域；无 8 页导航；无 Project Center；无 Task Console；无自由 DAG。

---

## 4. 本轮主动做出的视觉判断

1. **Context 栏的裁定（brief §9 专项）**：没有把它做成一个泛用的「上下文」面板。判断是 **RD 确实需要它，但它的语义是「当前 Project 的文件与最近对象」**，因此命名为「文件 · 最近对象」并按 Project 隔离 25 个文件 + 10 条最近对象，且**可整栏折叠**。理由：研发工作的定位行为（从文件/对象回到 Work）频次高，值得一个常驻列；但它**不是**一个抽象「上下文」容器，所以既不叫这个名字，也不硬塞 Project 切换等不属于它的东西（Project 切换留在顶栏）。
2. **Main 上半部按「条带」而非「卡片墙」设计**：进度、计数、Leader 判断、Next Check 压缩成一条，避免与下半部争视觉权重。CEO 一眼扫完即走。
3. **Conversation 被设计成「持续工作现场」而非聊天窗**：Work 头（Responsibility / Provider / 状态）常驻在对话上方，Provider 消息带实时计时与完成态，Result 以引用块挂在消息尾部 —— 让人读得出「这个员工一直在干活」，而不是「一个能聊天的机器人」。
4. **Decision 用证据标签区分事实与估计**：`FACT / EST / POLICY` 三色标签直接印在每段结论前，避免「AI 的建议看起来像事实」。
5. **Provider 用独立视觉身份（无头像、方块标记）** 与 Employee（圆头像）区分，从视觉上坐实「Provider 不是员工」。
6. **暗色为默认**：遵循 Curis Frozen 默认，同时提供亮色切换以便评估两种主题下的信息密度。
7. **不使用 Dashboard 模板**：没有卡片网格、没有环形图/KPI 大字块，层级完全靠分隔线、间距与字阶。

---

## 5. 暴露出的产品问题（诚实列出）

1. **Context 栏在大 Project 下的扩展性未验证**：25 个文件在 220px 宽列里已接近满屏；真实项目上千文件时，这一列要么需要过滤/搜索，要么应该改成按 Work 聚合。本轮未做，属**未解决问题**。
2. **「Work 完成」缺少一等入口**：本轮自测中「Work 完成」是由状态推进触发的；界面上没有一个明确的「验收通过 / 收尾」动作位。是否需要在 Conversation 内提供「Accept / Done」动作，属**待裁的产品决策**。
3. **Employee 与 Responsibility 的视觉区分偏弱**：一个员工承担多个 Responsibility（如徐川同时是 Development 与 Review）时，Responsibility 只作为 Work 上的标签出现，扫描性一般。
4. **「阻塞」缺少升级路径的承载位**：本轮已补入真实阻塞样本 `W-247 · 孙磊 · 生产灰度通道（1% 流量）开通`（外部依赖：云厂商工单 #CAS-88213 三天未回复），六态因此齐全。但界面只能**表达**阻塞，无法**处置**阻塞——「何时升级供应商工单 / 何时改用 B 方案 / 何时把它转成 CEO 决策」这一步在 UI 上没有任何位置。而其对话里恰好点出一个真实风险：员工说「B 方案要动发布策略，那个再向你汇报」——**即一个 Work 会从 Blocked 转成 Needs CEO**，当前结构没有表达这条转换的机制。
   > 附：修复过程中同时暴露一个**实现级不一致**（已修复）：紧凑行原本取 `e.works[0]`，而状态标签取「最紧急的 Work」，导致「阻塞」标签旁边可能显示另一个 Work 的标题。已统一为同一来源（`urgentWork()`），展开面默认选中的 Work 也改为同一依据。
5. **Progress 百分比的口径未定义**：64% 这个数字在本探索里是给定值，没有从 Work 推导的规则。进入产品化前需要定义「Project 进度」的计算口径，否则会变成装饰性数字。
6. **Provider 成本 / 计量不可见**：`RD_PRODUCT_TRANSLATION §2.1` 把「Provider Routing 与计量」列为 Curis 必须自有的 Surface，但本轮界面完全没有承载（无调用次数、无成本、无 BYOK 归属）。属**结构性缺口**。
7. **Conversation 的「引用块」与 Utility 的关系只做了单向**：从引用可打开 Utility，但 Utility 内没有「这条结果属于哪次对话轮次」的回链。

---

## 6. 哪些只是 Mock

| 项 | 性质 |
|---|---|
| 全部 Project / Employee / Work / Conversation 文本 | 虚构样例，非真实研发记录 |
| Provider「执行中 → 完成」 | **模拟**：4.5s 定时器 + ticker，未调用 Codex / Claude Code / Copilot 任何真实接口 |
| Diff / 源码 / 测试结果 / PR / 构建 | 静态 Mock 数据渲染，非真实 CI 输出 |
| Conversation 的员工回复 | 基于关键词的**本地规则**（`employeeReply()`），非模型生成 |
| Project 进度 %、Work 计数 | 由 Mock 数据计算，**不代表真实工程度量** |
| 全局七区导航 | 占位（点击仅提示），本轮不实现其他区 |
| 「分配新工作」「CEO 视图」 | 占位 toast，未实现表单/聚合 |
| 无后端、无网络 | 零请求、零持久化；刷新即回到初始状态 |

---

## 7. 哪些需要 CEO Review

| # | 待裁事项 | 为什么需要 CEO |
|---|---|---|
| C1 | **Context 栏是否保留为常驻列**（还是折叠为默认收起 / 改为按 Work 聚合） | 涉及「研发工作区是否需要一个常驻左二栏」的形态判断 |
| C2 | **是否需要在 Conversation 内提供「验收 / Work 完成」一等动作** | 属于「目标→执行→验收→返工→完成」闭环的完成侧定义 |
| C3 | **Project 进度的计算口径**（当前为给定值） | 一旦进入实现就是产品承诺，不能由设计层臆定 |
| C4 | **Provider 计量 / 成本 / BYOK 归属是否需要在本 Workspace 内可见** | `RD_PRODUCT_TRANSLATION §2.1` 将其列为 Curis 自有 Surface，但界面未承载 —— 需决定是本期做还是留到能力治理层 |
| C5 | **Blocked 态的表现是否需要在默认场景中刻意造样** | 影响视觉验收的可信度 |
| C6 | **多 Responsibility 员工的视觉表达方式** | 涉及 Responsibility 模型在 UI 上的正式表达 |
| C7 | **`Blocked → Needs CEO` 的转换是否要成为一等能力**（W-247 的 B 方案恰好触发这条路径：员工说「B 方案要动发布策略，那个再向你汇报」） | 决定「外部阻塞」与「CEO 决策」之间是否需要显式升级机制，还是仅由员工在对话里口头提出 |

---

## 8. 自测路径与结果

**执行方式**：`puppeteer-core` + 系统 Google Chrome（`--headless=new --no-sandbox --no-proxy-server`），以 `file://` 加载**单文件版**，**全部通过真实点击与键盘输入**驱动，逐步截图存证。

**执行命令**
```bash
cd "RD_WORKSPACE_HTML_EXPLORATION"
NODE_PATH=/Users/yy/.workbuddy/binaries/node/workspace/node_modules \
/Users/yy/.workbuddy/binaries/node/versions/22.22.2-3/bin/node _check.js
```

**执行链路**（对应 brief §10）
Project 首屏 → Project 切换（`p-default` → `p-internal` → 回 `p-default`）→ 徐川多 Work 展开 → Work 切换 `W-231↔W-232`（验证 Conversation 不串线）→ Conversation 发送「把这个继续推进，拆成两条并行的线」→ 员工拆分并行 Work 回复 → Provider 执行中 → **切到陈昊再切回，验证执行不中断** → Provider 结果返回 → 打开 Diff Utility → 打开 Test Result Utility → Needs CEO Banner 八要素 → **批准 Decision** → 王雨 `W-240` 由 Waiting → Working → 测试员工工作面可见 → Work 完成 → Project 计数与进度变化。

**结果**

| 指标 | 值 |
|---|---|
| 断言通过 | **20 / 20** |
| **Console Error** | **0**（含 `pageerror` / `requestfailed`） |
| 截图证据 | **14 张**（`_evidence/01…13` + `14-blocked-external.png`） |
| 关键观测 | 进度 `64% → 72%`；计数 `working 6→8, waiting 3→2, needs_ceo 1→0`；`complete 1→2` 且 Header 同步；`W-240.status = working`；初始六态 `working 6 / waiting 3 / blocked 1 / needs_ceo 1 / review 2 / complete 1` |
| 额外复核 | **构建新鲜度**：重建后单文件字节哈希不变（`_build.js` 产物与源文件一致）；**令牌完整性**：`--ui-*` 悬空引用 = 0；**阻塞渲染**：紧凑行与展开面均正确显示 `W-247` 阻塞原因，Console 依旧为 0 |
| 私有复核脚本 | `/tmp/curis-vis/blocked2.js`（阻塞态专项，非交付物） |

---

> 本目录为**视觉探索产物**，不是 Current Product Truth，也不是第二套 Blueprint / Master Map / UI Blueprint。
> 任何被接受的结论须由正式流程（Blueprint → Design → Code）吸收后方为有效。
