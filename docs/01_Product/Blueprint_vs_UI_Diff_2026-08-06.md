# Blueprint × UI 原型 差异清单（2026-08-06）

Status: Deprecated

> 本文是 2026-08-06 的历史差异快照。当前 UI 证据以 `docs/01_Product/Curis_UI_Evidence_Alignment_2026-08-09.md` 为准，产品定义以 Blueprint 5.0 为准。

> 目的：在不动任何代码/文档的前提下，逐条坐实「Blueprint 与 UI 原型脱节」的具体差异、证据与影响面，供总控决策席选定治理方向。
> 状态：**仅诊断，未改动**。

> 术语校正（2026-08-09）：文中“Curis 自我研发”应理解为“研发工作台中的第一个任务：完善 Curis”，
> 不是一个独立业务名称。当前三条业务是研发工作台、小红书运营工作台和抖音 / TikTok 运营工作台。

## 0. 权威链与结论摘要

```
Blueprint (v4.4 · Single Current · 声称唯一真相源)
   └─→ docs/03_Design/Curis_Design_System.md §3.1   ← 设计文档（非产品文档）
          └─→ curis-ui-prototype/_system/canonical-nav.js
                 （自身第 4 行标注「规范来源：Curis_Design_System.md §3.1」）
                 └─→ 桌面 frontend/components/terra/TerraNavData.js
```

**核心结论**：UI 原型以「设计文档」为源，而该设计文档 §3.1 是 Blueprint 表面模型的**平行版本**，从未回合进 Blueprint（违反 memory #4「Blueprint 唯一真相源、禁止平行版本」）。漂移集中在三处：① 工具/资源分组被提升为独立导航；② 硬编码垂直办公室与演示业务；③ 首页状态机被简化。

## 1. 导航结构差异（Blueprint ↔ 设计文档/UI ↔ 桌面）

| # | 分组/项 | Blueprint 立场（证据） | UI 原型/设计文档（证据） | 桌面现状（证据） | 严重度 |
|---|---------|------------------------|--------------------------|------------------|--------|
| 1.1 | 主入口 5 项（CEO工作台/经营/业务/AI团队/工作空间） | §09 四入口投影模型（L113-128） | canonical-nav NAV_MODEL.primary（L29-35）；设计文档 §3.1 L71 | TerraNavData 同 5 项 | ✅ 一致 |
| 1.2 | 「经营工具」分组（会议工作台/决策室） | §09「Meeting、Knowledge、Assistant、Analysis 是**跨切机制，不是独立导航项**」（L113） | 设计文档 §3.1 L72 提升为分组；canonical-nav NAV_MODEL.tools（L36-39） | 桌面有 `meeting`/`decisions` 页 | 🔴 高 |
| 1.3 | 「公司资源」分组（成果库/知识库/财务/日历） | §09 未列这些为独立导航；Knowledge 为跨切；§09 L127「Operating Timeline 不是日历复制品」 | 设计文档 §3.1 L74 提升为分组；canonical-nav NAV_MODEL.resources（L46-51） | 桌面有 `assets?`(缺失)/`knowledge`/`finance`/`calendar` | 🔴 高 |
| 1.4 | 办公室生成方式 | §07「Workspace 由已配置业务空间**生成**」，通用、无固定垂直 | canonical-nav NAV_MODEL.offices **硬编码 4 个具体垂直办公室**（L40-45） | 桌面 `workspace/{software,xhs,shortvideo,department}` 占位页 | 🔴 高 |
| 1.5 | 底部（设置/帮助） | 未明确反对 | canonical-nav NAV_MODEL.footer（L52-55），按钮打开 Assistant 浮层 | 桌面同 | ✅ 基本一致 |
| 1.6 | Assistant 形态 | §09/§11「Assistant 是第一位 AI 员工，不做固定第三栏/侧栏卡片，以 CEO Desk 主内容+浮层出现」 | Frozen 规范 L284「设置/帮助改为打开 CEO 助理」 | 待确认（大概率一致） | ✅ 一致 |

## 2. 硬编码演示业务 vs Blueprint 业务模型（🔴 最关键）

| 证据 | 内容 | 与 Blueprint 冲突点 |
|------|------|---------------------|
| `business.html` L237 | `/* 当前本机验证范围：软件开发、小红书、抖音 / TikTok。历史实验不进入当前业务版图。 */` | Blueprint §00/§04：业务由 CEO 创建；首条验证业务是研发工作台，首个任务是“完善 Curis”；业务不是预置清单 |
| `business.html` L355-458 | 3 张固定 `biz-card`：software-dev（运行中）、content-growth（扩大中）、short-video（Experiment） | Blueprint §09「业务」入口是关于价值/赌注/客户结果的判断，不是写死的 3 卡 |
| `ceo-desk.html` L450 | 「根据**软件开发 工作空间** 与**短视频内容 工作空间**的运行数据，我已将事项按优先级分组」 | Blueprint：工作空间由已配置业务生成，不应预置 2 个特定垂直空间 |
| 桌面 `projects` 页 | 当前为空（从零创建，见 E2E 验证） | 与 UI 的 3 预置业务直接矛盾 |

**影响**：整个 UI 原型是围着 3 个写死的垂直业务搭的 demo，与 Blueprint「从零创建三类工作台、研发工作台的首个任务为完善 Curis」的产品范式冲突。后续所有围绕这 3 业务的页面（business / workspace-runtime-* / ceo-desk 假设）都建立在固定预置业务前提上。

## 3. 页面清单不对等（UI 原型 ↔ 桌面）

**桌面缺失 UI 原型页（应建未建）：**
| UI 页 | 含义 | Blueprint 依据 | 严重度 |
|-------|------|----------------|--------|
| `founding-flow.html` | 首次创建公司（5 步） | §00/§09「公司为空→Founding Brief」是首屏核心路径 | 🔴 高（onboarding 缺失） |
| `assets.html`（成果库） | 输出物/证据 | §07 Artifact 是 Workspace 内部实现手段，但是否独立沉淀页 Blueprint 未禁止；UI 有、桌面无 | 🟡 中 |

**桌面重命名（语义偏移）：**
| UI 页 | 桌面路由 | 偏移 |
|-------|----------|------|
| `operating.html`（经营） | `/ceo-office/analytics` | 命名从「经营运行」→「分析」，弱化了控制面语义 |
| `business.html`（业务版图） | `/ceo-office/projects` | 语义从「价值/赌注」→「项目对象」，与 Blueprint §09「不能用 Project 列表代表业务价值」相悖 |
| `ai-organization.html`（AI 团队） | `/ceo-office/organization` + `/ceo-office/capabilities` | 拆分，但 capability 本属 AI 团队/Workspace 装修，拆分后边界模糊 |

**桌面多出 UI 原型没有的页（自创 IA，正是此前用户愤怒点）：**
| 桌面路由 | 性质 | Blueprint 立场 |
|----------|------|----------------|
| `brainstorm` / `brainstorm/sessions/[id]` | 头脑风暴室 | 不在 UI 原型导航；疑似自创 |
| `reports` / `reports/[id]` | 重要汇报 | 不在 UI 原型导航；疑似自创 |
| `execution` / `execution/runs/[id]` / `execution/tasks/[id]` | 执行/任务 | §07「Project、Task、Workflow 只在 Workspace **内部**作为实现手段，不能取代 Outcome/Commitment/Evidence」——提升为顶层导航违反此条 |
| `runtime-trace` | 运行追踪 | 不在 UI 原型导航；Workspace 内部机制 |
| `company-runtime` | 公司运行 | 与「成果库 assets」关系不清，疑似自创替身 |

## 4. 首页状态机

| 维度 | Blueprint §09（L115） | UI `index.html`（Frozen 规范 L234） | 桌面 |
|------|------------------------|--------------------------------------|------|
| 状态数 | **4 态**：公司为空→Founding Brief / 配置中→Company Design / 业务运行→Company Now / 重构中→Change Mode | **2 态**：有 companyName→ceo-desk，否则 founding-flow | 待确认（大概率 2 态或最简） |
| 严重度 | — | 🟡 中（简化了治理态，但功能可渐进补） | — |

## 5. 一致部分（不必动）

- 主入口 4/5 项结构（§1.1）
- 「办公室动态生成」原则（虽 UI 实现成了硬编码，原则本身一致）
- Assistant 浮层不占固定第三栏（§1.6）
- CEO Desk 6 组件骨架：ceo-desk.html 含 Brief Header / Assistant Brief / Company Pulse / Matters / Operating Timeline / Handoffs（L425-702），与 Blueprint §09 L127 的 6 组件定义一致

## 6. 影响面汇总（供治理决策参考）

| 治理动作 | 涉及文件/路由 | 工作量 |
|----------|---------------|--------|
| 回退/合并「经营工具」「公司资源」分组 | canonical-nav、TerraNavData、meeting/decisions/knowledge/finance/calendar 路由归属 | 中 |
| 去除硬编码垂直办公室/业务 | business.html、ceo-desk.html、workspace-runtime-*、桌面 workspace/* 占位页 | 高（牵动 demo 数据） |
| 补 founding-flow / assets | 桌面缺页 | 中 |
| 清理自创 IA（brainstorm/reports/execution*/runtime-trace/company-runtime） | 桌面多余路由 | 中（此前用户已要求清理） |
| 首页 4 态恢复 | index / 桌面入口逻辑 | 中 |
| 业务语义纠正（projects→业务版图） | 桌面 projects 页 + 后端 project 模型对齐 Blueprint「价值赌注」 | 高 |

> 下一步：由总控决策席在以下方向中选定，再启动改动——
> A) 以 Blueprint 为准，将 UI 超出的部分回退或合并进 Blueprint 再审；
> B) 反向把 UI 决策正式写入 Blueprint（升版 v4.5）；
> C) 维持现状仅做清单备案（不推荐，违背单一真相源红线）。
