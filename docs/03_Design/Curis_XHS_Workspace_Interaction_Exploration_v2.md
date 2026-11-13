# Curis XHS Workspace Interaction Exploration v2

**Status**: **XHS INTERACTION REVIEW REQUIRED**  
**研究序位**: Reference Research（READY FOR DESIGN）→ Design Brief → Exploration v1（Round 1 三方案）→ **本探索（Round 2 交互低保真）**  
**方向确认（Round 1 已通过）**：不采用纯 A / B / C，采用渐进混合方案 ——
- **默认**：Calendar 是 Main 主视图，第一眼只看内容节奏与状态；
- **选 Note**：不打开窄 Drawer；Calendar 自然压缩为「时间上下文」，Content Object 展开成为主要工作面（Split Working）；
- **关闭 / 完成 Note**：恢复 Calendar-Dominant；
- **C · Object-First** 保留为未来 Focus Mode，**不作默认状态**。

**本轮边界（强约束）**:
1. **只做低保真状态与交互**：ASCII 线框 + 状态说明 + 交互流转，**不做高保真视觉**（无色值/字体/间距精修）；
2. **不增加新功能**：所有出现的 Pattern 均来自 Reference Research / Design Brief（Calendar、Note、Context=选题库/信号、Utility=预览/数据/审核、Review Gate、Needs CEO、Handoff、Result Reference、Employee Workstation、Publishing Queue），仅做空间与交互编排；
3. **不修改 Shell Contract**；
4. **不写代码**；
5. 动效引用 Frozen `--ui-dur-3`(320ms) + `--ui-ease-standard`，仅作交互说明，不出 CSS。

---

## 0. 核心交互原则（混合模型）

```
默认态：  Nav + Main(Canvas=Calendar 满宽)
选 Note： Nav + Main(时间上下文压缩 | Content Object 主工作面)   ← Re-partition，非 Drawer
开Ctx：   Nav + [Context 自适应面] + Main(时间上下文 | Note)      ← 瞬态，可关
开Util：  Nav + Main(时间上下文 | Note) + [Utility 自适应面]      ← 瞬态，可关
审/阻塞： 顶部橙色 Decision Banner + Note 旁员工 Workstation 浮现   ← 节点事件，非常驻
发布后：  Nav + Main(Calendar 满宽)，卡片带 Result Reference 链接
```

**关键**：Main 始终是「Nav + 一个弹性 Main」；Context/Utility 是叠加的 **Adaptive Surface 层**（默认收起、按需开、可关），它们出现时可能临时加宽布局，但**不是 Shell 的固定第四/五栏**。关闭即回到 Nav + Main 两区。

---

## 1. 低保真状态总览

| # | 状态 | 一句话 | 验证焦点 |
|---|---|---|---|
| 1 | Default Calendar | 满宽日历 + 状态卡片，第一眼只看节奏 | 第一眼简单 |
| 2 | Note Selected → Split Working | 日历压缩为时间上下文，Note 成为主工作面 | Calendar→Split 是否自然 / Note 如何成为当前对象 |
| 3 | Context Open → Topic/Signal | 左开选题库/信号（瞬态 Adaptive） | Context 接入不变成固定四栏 |
| 4 | Utility Open → Note Preview | 右开图文预览（瞬态 Adaptive） | Utility 接入不变成固定四栏 |
| 5 | Review Gate / Needs CEO | 审核闸 + 橙色 Banner + 员工 Workstation 浮现 | 员工「浮现」非常驻 / Handoff 落位 |
| 6 | Publishing / Published / Review Result | 发布→已发布，卡片带 Result Reference | Result Reference 落在内容流 |

### 状态流转图

```
[1 Default Calendar]
      │ 点卡片选 Note
      ▼
[2 Split Working] ──────────── 关 Note ───────────┐
      │ 开 Context(选题库/信号)                    │
      ▼                                           │
[3 + Topic/Signal] ─── 关 Context ──► [2 Split]    │
      │ 开 Utility(图文预览)                      │
      ▼                                           │
[4 + Note Preview] ─── 关 Utility ──► [2 Split]    │
      │ 提交审核                                   │
      ▼                                           │
[5 Review Gate / Needs CEO]                        │
      │ 通过 → 发布                                │
      ▼                                           │
[6 Publishing→Published (+Result Ref)] ───────────┘ (关 Note → 回 [1])
```

---

## 2. 状态 1 — Default Calendar（Calendar-Dominant）

```
┌ Topbar 52px ────────────────────────────────────────────────┐
├ Primary Nav 220 │ Main: Calendar-Dominant                    │
│                  │ [月▾][周]   [+ 新建笔记]   图例 🟡制作 ⚪待审 🔵已发 │
│                  │ ┌────┐┌────┐┌────┐┌────┐┌────┐┌────┐       │
│                  │ │周一││周二││周三││周四││周五││周六│ ...    │
│                  │ │🟡  ││🟢  ││⚪  ││🔵  ││🟡  ││⚪  │       │
│                  │ │[封]││[封]││[封]││[封]││[封]││[封]│       │
│                  │ │标题││标题││标题││标题││标题││标题│       │
│                  │ └────┘└────┘└────┘└────┘└────┘└────┘       │
│                  │ (Context / Utility 默认收起；无员工常驻)    │
└──────────────────┴───────────────────────────────────────────┘
```

**交互**：
- 主区满宽 = Content Calendar；每格一张 Note 卡片（状态色点 + 3:4 缩略 + 标题）。
- 第一眼只有「内容节奏 + 状态」，无编辑器、无员工。
- 点卡片 → 进入状态 2；点「+ 新建笔记」→ 新建后也进入状态 2。

**验证了什么**：Low Surface Complexity 达标——第一眼只剩日历与状态。

---

## 3. 状态 2 — Note Selected → Split Working

```
┌ Topbar 52px ────────────────────────────────────────────────┐
├ Primary Nav 220 │ Main: Split Working                        │
│                  │ ┌时间上下文─┐┌── Content Object（主工作面）─┐│
│                  │ │[周]       ││ ● Note: 夏日穿搭合集         ││
│                  │ │周一 🟡    ││ 状态: 制作中                 ││
│                  │ │周二 🟢    ││ ┌────────┐ 标题[ input ]     ││
│                  │ │周三 ⚪    ││ │封面 3:4│ 正文[ 编辑器 ]     ││
│                  │ │周四 🔵    ││ │        │ 标签[+大词][+长尾] ││
│                  │ │(选日过滤) ││ └────────┘ 状态[ 制作中 ▾ ]  ││
│                  │ │           ││ [保存][提交审核][📊数据▸]     ││
│                  │ └───────────┘└───────────────────────────┘│
└──────────────────┴───────────────────────────────────────────┘
```

**交互（关键空间变化）**：
- 选 Note **不是**开 Drawer；而是 Main 内部 **re-partition**：左栏 = Calendar 压缩成「时间上下文」窄条（周列表/迷你月，选日可过滤右栏），右栏 = Content Object 工作台。
- 变化用 `--ui-dur-3`(320ms) + `--ui-ease-standard` 过渡；日历格「流」成时间条，同一 Main 重分区，不是新覆盖层 → **自然**。
- Note 成为「当前工作对象」：右栏顶部 `● Note: 标题` + 状态，明确当前对象身份；左时间条退为上下文。
- 关 Note（关闭/完成）→ 右栏收，左时间条重新展开为满宽日历 → 回到状态 1。

**验证了什么**：
- Calendar → Split 空间变化自然（re-partition，非 drawer）；
- Note 经由「选中 = 设为当前对象 + 工作台展开」成为主工作对象。

---

## 4. 状态 3 — Context Open → Topic / Signal

```
┌ Topbar 52px ────────────────────────────────────────────────┐
├ Nav220│Ctx(选题/信号)│时间│Content Object                     │
│       │🔥热门话题  │周一│ ● Note: 夏日穿搭合集                │
│       │💬评论提问  │周二│ 标题[ input ] 正文[ 编辑器 ]        │
│       │📌选题库    │周三│ 标签[+大词][+长尾]                  │
│       │(点选→引用) │    │ [保存][提交审核]                    │
│       │           │    │                                     │
└───────┴───────────┴────┴─────────────────────────────────────┘
```

**交互**：
- Context Surface（左 · Adaptive）按需开：在 Note 工作台点「选题库」或引用信号时触发；内容 = Topic & Signal Library（热门/评论/选题库）。
- **它是瞬态 Adaptive Surface，不是固定第四栏**：默认收起；打开时临时出现在 Nav 右侧；有关闭入口；关闭即回到 `Nav | 时间上下文 | Note` 三区，日历仍是压缩态、Note 仍是主工作面。
- 不把页面变「固定四栏」的关键：Context 是**叠加层/可推层**，非 Shell 结构列；它的存在是临时的、可被用户随时消解。

**验证了什么**：Context 接入不固化四栏——Adaptive Surface 语义（Shell Contract §2.2）成立。

---

## 5. 状态 4 — Utility Open → Note Preview

```
┌ Topbar 52px ────────────────────────────────────────────────┐
├ Nav220│时间│Content Object        │Utility(右·预览)           │
│       │周一│ ● Note: 夏日穿搭合集 │ ┌──────────────────┐      │
│       │周二│ 标题[ ] 正文[ ]      │ │ 封面 3:4 真实渲染│      │
│       │周三│ 标签[+][+]           │ │ 标题(读者视角)   │      │
│       │    │ [保存][提交审核]     │ │ 正文渲染         │      │
│       │    │                     │ │ 标签展示         │      │
│       │    │                     │ └──────────────────┘      │
└───────┴────┴─────────────────────┴──────────────────────────┘
```

**交互**：
- Utility Surface（右 · Adaptive）按需开：点 Note 工作台的「预览」或 Result Reference `📊/✅` 时触发；本状态内容 = Note Preview（读者视角 3:4 渲染）。
- 同样瞬态、可关；关闭回到 `Nav | 时间 | Note`。
- 与状态 3 对称：左 Context、右 Utility 各自独立、可单开/双开/全关，均不固化栏位。

**验证了什么**：Utility 接入不固化四栏——与 Context 同构的 Adaptive Surface 语义成立。

---

## 6. 状态 5 — Review Gate / Needs CEO

```
┌ Topbar 52px ────────────────────────────────────────────────┐
├ Nav220│⚠ 需要 CEO 决策 [✓执行][⛔驳回][暂缓]  (橙色 Banner)   │
│       │时间│Content Object (待审核)                          │
│       │周一│ ● Note: 夏日穿搭合集  状态:待审核               │
│       │    │ ⇄ Handoff: 策划→审核 (轻量)                     │
│       │    │ ┌────────┐ [审核详情▸] (开 Utility/抽屉)        │
│       │    │ │封面3:4 │ 违禁词:0  人设:一致                  │
│       │    │ │        │ [通过→发布][升级CEO]                 │
│       │    │ └────────┘                                      │
│       │    │ 🟣 审核员工 Workstation (needs_ceo 浮现)         │
│       │    │    状态: needs_ceo · 等待品牌确认                │
└───────┴────┴─────────────────────────────────────────────────┘
```

**交互**：
- Note 提交审核 → 进入 Review Gate：Note 工作台显示审核态，可点「审核详情▸」开 Utility（或抽屉）看违禁词/人设报告。
- **Handoff（策划→审核）** 以轻量事件 `⇄ 策划→审核` 出现在 Note 工作台内，不阻断主流程。
- **Needs CEO**：若品牌/敏感表达需确认 → 顶部橙色 Decision Banner（Workspace 级，独立横幅，不占双轴空间）；同时审核员工 Workstation 以 `needs_ceo` 状态**浮现**在 Note 旁（非独立侧栏、非常驻），保留其责任状态。
- **员工「浮现」而非「常驻」**：仅在制作中/审核阻塞/Handoff 节点出现；**needs_ceo 员工不固定「默认折叠」，保留当前展开/折叠状态**（与 Shared Pattern §3.1 一致），由顶部 Decision Banner 承载 Workspace 级注意力；展开时显当前工作/阻塞原因；日常浏览日历、看预览时不出现。

**验证了什么**：
- Employee Workstation 在节点浮现非常驻；
- Handoff / Needs CEO 落在内容工作流中（轻量事件 + 顶部 Banner），不另起一套结构。

---

## 7. 状态 6 — Publishing / Published / Review Result

```
┌ Topbar 52px ────────────────────────────────────────────────┐
├ Nav220│Main: Calendar-Dominant (发布后回到节奏视图)           │
│       │ [月▾] 周三🔵已发布   ✅笔记已发布▸  📊数据看板▸       │
│       │ ┌────┐┌────┐┌────┐┌────┐ ...                        │
│       │ │周一││周二││周三🔵││周四│ ...                       │
│       │ │🟡  ││🟢  ││[封] ││🟡  │                            │
│       │ └────┘└────┘└────┘└────┘                             │
│       │ (点 📊数据看板▸ → 开 Utility Analytics)              │
│       │ (点笔记卡片 → 回状态 2 Split Working)                │
└───────┴──────────────────────────────────────────────────────┘
```

**交互**：
- 审核通过 → 进入 Publishing Queue（日历格显示 🕒定时 或 🔵已发布）；发布后回到 Calendar-Dominant（状态 1 形态）。
- 已发布笔记卡片带 **Result Reference**：`✅ 笔记已发布 ▸` / `📊 数据看板 ▸`；点 → 开 Utility Analytics（复用在状态 4 的同族 Adaptive Surface，内容切到数据看板）。
- **Result Reference 落在内容流**：链接在日历卡片 / Note 工作台内，点击才开 Utility，对话/卡片内不铺完整数据表（符合 Shell Contract §3.4）。

**验证了什么**：Handoff/Result Reference 自然落在内容工作流——链接驱动 Utility，而非嵌入大块数据。

---

## 8. 焦点验证逐项回答

| 验证焦点 | 结论 |
|---|---|
| **Calendar → Split 空间变化是否自然** | 是。选 Note 是 Main 内部 re-partition（日历格流成时间上下文条 + Note 工作台展开），非 Drawer 覆盖；320ms 缓动过渡，同一 Main 重分区，认知连续。 |
| **Note 如何成为当前工作对象** | 选中 = 设为 active Content Object：右栏顶部 `● Note + 标题 + 状态` 标识当前对象，左时间条退为上下文；关闭即解除。 |
| **Employee Workstation 如何「浮现」非常驻** | 仅在制作中/审核阻塞/Handoff 节点出现；needs_ceo 员工保留当前展开状态（不固定默认折叠），Decision Banner 负责 Workspace 级注意力；日常浏览日历/预览时不出现，无常驻员工栏。 |
| **Context/Utility 如何接入而不固化四栏** | 二者均为默认收起、按需开、可关的 **Adaptive Surface 层**；出现时临时加宽布局但可消解，非 Shell 固定列；关闭即回 `Nav + Main` 两区。 |
| **Handoff / Result Reference 如何落在内容工作流** | Handoff 以轻量 `⇄` 事件出现在 Note 工作台；Result Reference 以 `📊/✅` 链接出现在卡片/工作台，点击开 Utility；均不嵌入大块内容。 |

---

## 9. 不变式 / 禁止项（本轮约束）

- ❌ 新增功能：所有 Pattern 均来自 Reference Research / Design Brief，仅做编排；
- ❌ 修改 Shell Contract：本探索不改动 Contract 正文；
- ❌ 写代码 / 高保真视觉：仅低保真 ASCII + 交互说明；
- ❌ 固定四栏：Context/Utility 不得固化为 Shell 结构列；
- ❌ 窄 Drawer 当 Note 主工作面：选 Note 必须走 Split Working re-partition；
- ❌ 员工常驻栏 / 顶部员工 tab；
- ❌ C · Object-First 作为默认态（仅保留为未来 Focus Mode）。
- ❌ XHS Main 接入 CEO 队列：XHS 仅使用 Needs CEO / Decision Pattern；全局 CEO 待处理汇总属于 CEO 工作台，不属于 XHS Main。

---

## 10. 开放问题 / 下一步

1. 时间上下文条的最小可用宽度与折叠阈值？（关联 Shell Delta-X5 Resizable）
2. Context/Utility 同时开时，Main 剩余宽度低于 usable width 如何自适应（Overlay/Focus）？（Delta-X5 已登记）
3. 「保存 / 提交审核」保持业务对象动作，不由 Composer 接管（已确认：Composer 仅在员工展开 Conversation 时出，制作动作走业务对象按钮）。
4. 多 Note 并行制作（Split 内多标签页）— **暂不引入**（已确认：按单当前对象）。

**下一步**：Review 通过后进入 Round 3 高保真视觉（先画 Default Calendar 与 Note Selected → Split Working 两状态；**XHS Main 不含 CEO 队列**，CEO 待处理汇总归属 CEO 工作台，XHS 仅用 Needs CEO / Decision Pattern）。Shell Delta-X5 已批准回写。

---

**UI Designer**: UI Designer（像素君）  
**文档日期**: 2026-08-15  
**阶段**: XHS Design Exploration · Round 2（交互低保真，无代码、无高保真视觉）  
**状态**: **XHS INTERACTION REVIEW REQUIRED**
