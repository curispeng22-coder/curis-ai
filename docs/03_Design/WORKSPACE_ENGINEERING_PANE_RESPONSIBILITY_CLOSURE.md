> **⚠️ Status: SUPERSEDED（2026-08-17 设计文档整合）** — 本文件已被 `WORKSPACE_ENGINEERING_FINAL_IA_CLOSURE.md`（2026-08-16 Final IA Closure）**收口替代**；新 Agent 请勿以本文件为权威，仅作历史审批证据保留。

# Workspace Engineering · 四栏信息职责 Closure

> **Status**：PANE RESPONSIBILITY CLOSURE · REVIEW INPUT（本轮只回答「什么内容应该出现在哪里」，不做视觉、不改高保真）
> **⚠️ 已替代**：本文件已被 `WORKSPACE_ENGINEERING_FINAL_IA_CLOSURE.md`（2026-08-16 Final IA Closure）**收口替代**。Final 版纳入 Frozen Shell 4 点 + 方法论 IA Composition/Retention + WorkBuddy IA Review 三项新依据，并新增「最终信息架构 / 七状态矩阵 / 长期 History·Asset·Config 归属 / 高保真整改清单 / 重制条件判定」。以 Final 版为准。
> **触发**：高保真 Review 不通过 —— 根因是**把空间工程当成了 Content Growth 式持续经营业务**，错误地用「Business Home 运营（八问/指标卡/Dashboard）」填充 Main，并把员工详情/Conversation 错放到 Context/Utility。本 Closure 重新锁定四 Pane 职责。
> **核心论断**：**空间工程是交付型支持部门，不是持续经营业务**。它的工作单位是**建设任务**，生命周期在「交付」处结束；其主工作面必须参照 **RD Employee Workstation**，而非 Content Growth Business Home。
> **纪律**：不重定义 Frozen Shell / P1–P7 / Shared Employee Contract；不设计视觉；不写产品代码；不暴露 Agent/Router/DAG/Package/Gate 内部原语。

---

## 0. 背景与失败归因

| 失败点 | 说明 | 纠正方向 |
|---|---|---|
| 误用经营模型 | 把「建设项目」画成 Content Growth 式 Business Home（八问模型 + 已发布/阅读/线索指标卡） | 建设任务有**明确终点（交付）**，主工作面是**当前责任员工的 Workstation（Conversation 驱动）**，不是运营 Dashboard |
| Context 越界 | 在 Context 放了完整员工详情 / 员工 Conversation | Context 只回答「这次工作是什么上下文」，放**团队 Presence 简要**，不放详情、不放 Conversation |
| Utility 越界 | 点击员工把 Conversation 放进了 Utility | 点击员工 → **Shared Employee Detail**（Utility）；Conversation 只在 **Main（Workstation）** |
| Main 越界 | 在 Main 堆 Timeline / 指标卡 / 多业务概览 | Main = 当前责任员工的**自然 Conversation + 工作现场**；上方最多轻量建设进度 |
| 混淆 Detail / Workstation | 把「这个人是谁」与「这个人现在怎么工作」混为一谈 | Employee Detail（Utility）≠ Employee Workstation（Main），见 §3 |

---

## 1. 空间工程建设任务的核心工作模型

空间工程承接的是**一次性建设任务**，不是持续经营循环。模型如下：

```
CEO / 空间工程 Leader 确认需求（目标·成功标准·范围·Non-goals）
  → 当前责任员工 以 Conversation 工作（消息流 + 工作状态 + Result/Artifact 卡）
  → 产出 Result / Artifact
  → 真实责任交接（Handoff · P5 · 自动触发，CEO 不点「下一步」）
  → 下一责任员工 接手（行业研究 → 经营方法 → 产品设计 → 搭建实施 → 质量验收）
  → 搭建完成、验收通过
  → 交付（Build Team → 新业务 Operating Team 的 Handoff）
  → 建设任务结束（空间工程部退出日常经营）
```

**关键边界**：
- **有终点**：交付后任务结束；新办公室转入**它自己的经营页面**（那才用 Content Growth 式经营模型，且属于新业务，不属于空间工程部）。
- **责任链是顺序交接，不是 Dashboard**：每个阶段由一名真实责任员工持有，Main 显示**当前持有者**的 Workstation；完成后自动 Handoff 到下一持有者，Main 随之切换。
- **参照 RD Workstation**：Main 是「当前员工 Workstation + 其活跃 Conversation」，不是业务概览页。

---

## 2. 四 Pane 职责总表（建设任务语境）

### Nav — 「我在哪里」
- **只回答**：我在哪个组织位置、当前在哪个建设项目、属于哪个 Workspace。
- **shows**：六区导航（首页/业务空间/组织中心/人才市场/资料库/会议）；当前 Department（空间工程部）；当前建设项目入口；Workspace 导航。
- **forbids**：不放工作进度、不放员工详情、不放 Conversation、不做业务指标。

### Context — 「这次工作是什么上下文」
- **只回答**：当前这个建设任务/Thread 处于什么状态。
- **shows**：
  - 当前建设项目 / Thread 名称
  - 当前阶段（行业研究 / 经营方法 / 产品设计 / 搭建 / 验收 / 交付）
  - 责任链状态：**已完成 / 当前 / 下一** 责任（对应 P5 Handoff 的真实阶段推进）
  - 团队 Presence 简要信息（P2 Employee Presence 轻量呈现：谁在场、当前责任、状态，可一键进 Workstation）
- **forbids**：**不放完整员工详情**；**不放员工 Conversation**（Conversation 只在 Main）；不做可滚动的长员工档案；不做权限中心 / 目录 / 工具目录。

### Main — 「当前责任员工怎么工作」
- **只回答**：此刻负责这项工作的员工，正在和 CEO 一起做什么。
- **shows**（遵循 ChatGPT / Codex 成熟范式，**不重新设计** Conversation）：
  - 当前 Responsibility Holder / Employee 的**自然 Conversation 工作现场**
  - 消息流（Message Stream）
  - 工作状态（当前步骤 / 持有者 / 等待原因 / 下一步 —— 禁止无 owner 的泛「运行中」）
  - Result / Artifact 卡（P6 Result Reference 轻量引用，点击进 Utility 看全文）
  - Composer（自然语言输入 + 必要模式/模型/发送；归属当前 Workstation Conversation）
  - 顶部最多保留**一条轻量建设进度**（当前阶段 + 责任链概览），不展开成块
- **forbids**：**不做 Dashboard**；**不堆 Timeline / 指标卡 / 多业务概览**；不把建设任务画成经营八问；不放完整员工档案；不放与当前责任无关的内容。

### Utility — 「我当前选中的对象是什么」
- **只回答**：当前选中的那个对象（Result/Artifact 或 Employee）的详情 / 预览。
- **shows**：
  - 点击 **Result / Artifact** → 查看其完整报告 / 策略 / 设计 / 验收结果（P6，保留 Conversation 锚点可返回）
  - 点击 **Employee** → 使用 **Shared Employee Detail**（见 §3）
- **forbids**：**点击员工不得把 Conversation 放进 Utility**（Conversation 只在 Main）；不常驻右侧工具墙；不做永久可见的全量工具列。

---

## 3. Employee Detail ≠ Employee Workstation（强制区分）

| 维度 | Employee Detail | Employee Workstation |
|---|---|---|
| 回答的问题 | 「这个人是谁、在组织里什么关系、负责什么」 | 「这个员工现在怎么和 CEO 一起工作」 |
| 所在 Pane | **Utility**（点击员工时展开） | **Main**（当前责任员工的主工作面） |
| 触发 | 点击员工「详情 / 是谁」 | 建设项目进行中、或点击员工「进入工作」 |
| 内容 | 个人信息 · Organization/Department/Team/Leader 关系 · 长期责任 · 当前 Responsibility · 能力/工作方式 · 最近结果 | 该员工的 Conversation 消息流 + 工作状态 + Result/Artifact 卡 + Composer |
| 是否含 Conversation | **否** | **是** |
| 来源契约 | Shared Employee Service Relation（Organization 轴 + 长期责任 + 执行期上下文分离） | RD Employee Workstation（provider-native Conversation，沿用不重设计） |

**铁律**：Utility 里的 Employee 视图**永远只是 Detail**，绝不承载 Conversation；Conversation 一旦出现，它属于 Main 的 Workstation。

### Utility · Shared Employee Detail 必含字段
1. **个人信息**：姓名 / 头像 / 岗位（Role）
2. **Organization 关系**：Company → Organization → Department / Team / Leader（组织轴，稳定隶属）
3. **长期责任**：该员工经 Responsibility Assignment 服务哪些 Office、承担哪些责任族（responsibility_types）
4. **当前 Responsibility**：此刻在该建设项目中的当前责任阶段（来自执行期上下文，瞬时）
5. **能力 / 工作方式**：capability / specialty / platform_experience / style / 稳定工具绑定
6. **最近结果**：近期 Result / Artifact 摘要（轻量，点进看全文走 P6）

> 注：Detail 展示「组织隶属（Organization 轴）」与「Office 服务（业务轴）」两正交轴，不得混淆；不把 Assignment 当成永久 Context 绑定（Shared Employee Contract Invariant #6/#7）。

---

## 4. 关键页面 · 四 Pane 逐页分解

> 约定：**建设项目主工作面（P-C）** 是核心；P-E/P-F 是其钻取状态，仍按四 Pane 描述。

### P-A · 经营总览 / 发起创办（Company OS CEO 工作台入口）
| Pane | 显示 | 禁止 |
|---|---|---|
| Nav | 六区导航；当前 Department 概览；「业务空间」分组 | 不放进度/员工详情 |
| Context | 收起或极简（本次无进行中建设任务时为空） | 不放员工 Conversation |
| Main | 经营方向聚合 + 「创办新业务」入口（发起委托空间工程的起点） | 不预渲染建设项目内容 |
| Utility | 收起 | 不放 Conversation |

### P-B · 委托空间工程部 / 表达意图
| Pane | 显示 | 禁止 |
|---|---|---|
| Nav | Department = 空间工程部；当前建设项目（草稿态） | 同 P-A |
| Context | 委托方式（CEO 直接 / CEO Assistant 协调转交）；目标·成功标准·范围·Non-goals 摘要（来自 CEO↔Leader Conversation） | 不放员工完整档案 |
| Main | 意图表达 + 与空间工程 Leader 的 Conversation（澄清需求） | 不做进度条 / Dashboard |
| Utility | 收起或目标摘要预览 | 不放员工 Conversation |

### P-C · 建设项目主工作面（CORE · RD Workstation 范式）★
| Pane | 显示 | 禁止 |
|---|---|---|
| Nav | Department = 空间工程部；**当前建设项目**高亮；Workspace 导航 | 不放工作进度 |
| Context | 当前 Thread；当前阶段；责任链 **已完成/当前/下一**；团队 Presence 简要（P2，可进 Workstation） | **不放完整员工详情**；**不放员工 Conversation**；不做员工目录 |
| Main | **当前责任员工的 Workstation**：Conversation 消息流 + 工作状态 + Result/Artifact 卡（P6）+ Composer；顶部一条轻量建设进度 | **不做 Dashboard**；**不堆 Timeline/指标卡**；不画八问经营模型；不放无关业务概览 |
| Utility | 点击 Result/Artifact → 报告/策略/设计/验收全文；点击 Employee → Shared Employee Detail（§3，无 Conversation） | 不常驻工具墙；点击员工不放 Conversation |

> 责任交接（P5，真实事件，P4 自动触发）：当前员工完成 → Main 自动切换到下一责任员工的 Workstation；Context 的「当前/下一」同步推进。CEO 不点「下一步」。

### P-D · 交付 / 进入公司 / Handoff（Build Team → Operating Team）
| Pane | 显示 | 禁止 |
|---|---|---|
| Nav | Department = 空间工程部；建设项目标记「已交付」；新办公室出现在「业务空间」 | 不放运营指标 |
| Context | 交付摘要：建设任务结束；责任从 Build Team 交接至 Operating Team；空间工程部退出日常经营 | 不放运营八问 |
| Main | 交付完成确认 + 新办公室「可以开始经营」的轻量说明（由真实员工/责任/能力/工作状态体现，不写「Package 安装成功」）；提供进入新办公室经营页的入口 | 不渲染建设进度；不做运营 Dashboard |
| Utility | 点击交付物/验收报告 → 全文（P6） | 不放 Conversation |

> 注：进入公司/交付是 **Build Team → Operating Team 的真实 Handoff**（P5）。交付后该建设项目任务结束；新办公室的**经营**属于新业务自己的页面（Content Growth 式经营模型），不在空间工程的建设主工作面内。

### P-E · 员工 Workstation 介入（钻取 · Main 变体）
| Pane | 显示 | 禁止 |
|---|---|---|
| Nav | 不变（Department / 当前建设项目） | — |
| Context | 不变（本次建设的责任链 + 团队 Presence） | 不放该员工完整档案 |
| Main | **该员工的 Workstation**：其 Conversation（沿用，不新建线程除非责任真变）+ 工作状态 + Result/Artifact + Composer | 不重设计 Conversation；不放 Dashboard |
| Utility | 点击其 Result/Artifact → 全文；点击「详情」→ Shared Employee Detail | 不放 Conversation |

### P-F · 员工 Detail（钻取 · Utility 变体）
| Pane | 显示 | 禁止 |
|---|---|---|
| Nav | 不变 | — |
| Context | 不变 | — |
| Main | 不变（仍显示建设项目当前责任员工 Workstation，或停留原 Main） | — |
| Utility | **Shared Employee Detail**（§3 六字段：**无 Conversation**） | **禁止 Conversation 进入 Utility**；禁放工作现场 |

---

## 5. Conversation 范式声明

- Conversation 本身**不重新设计**，遵循 ChatGPT / Codex 类成熟范式：消息流 + 工作状态 + Result/Artifact 卡 + Composer。
- Main 中的 Workstation Conversation 是「当前责任员工」的持续会话；责任未真变时不新建线程（RD Design Brief §10）。
- CEO Assistant / 空间工程 Leader / 责任员工之间的澄清、协调、汇报，都走各自 Conversation，**不**在 Context/Utility 以静态文本冒充。

---

## 6. 边界与禁止模式汇总（来自 RD Anti-pattern + Frozen）

| 禁止 | 依据 |
|---|---|
| 把建设任务画成 Business Home 运营（八问/指标卡/Dashboard） | 空间工程是交付部门，非持续经营 |
| Context 放完整员工详情 / 员工 Conversation | Context 只答「工作上下文」，见 §2 |
| Utility 点击员工放 Conversation | Employee Detail ≠ Workstation，见 §3 |
| Main 堆 Timeline / 指标卡 / 多业务概览 | Main = 当前员工 Workstation，见 §2 |
| 把员工 Workstation 做成导航侧栏 / 顶部 Tab | RD Design Brief §3：「Do not make Employee Workstations a navigation sidebar or top-level tabs」 |
| 把并行员工画成节点图 / DAG / 群聊 | RD：「Do not represent parallel employees as top tabs, an undifferentiated group chat, or a node graph」；CEO 要 ownership 不要编排拓扑 |
| Utility 常驻成右侧永久工具墙 | RD：「Do not create a permanent utility wall；open utilities from a concrete result or need」 |
| 泛「运行中」状态（无步骤/持有者/等待原因/下一步） | RD：「Generic 'running' status without current step, owner, wait reason, or next action」禁止 |
| DAG 画布作为 CEO 常态视图 | RD：「DAG canvas as the CEO's normal view of multi-agent work」禁止 |
| 暴露 Agent / Router / DAG / Package / Gate 内部原语 | 全程用户面自然语言 |

---

## 7. 与 Frozen / 既有契约的关系

- **Frozen Shell §1.1 四 Pane 职责表**：本 Closure 是其**建设任务语境的具体化**，未改 Shell 固定层。
- **P2 Employee Presence**：Context 的「团队 Presence 简要」即 P2 轻量呈现，不含完整详情/Conversation。
- **P5 Handoff**：建设责任链的真实交接；自动触发（P4），CEO 不操作；Context 的「已完成/当前/下一」反映之。
- **P6 Result Reference**：Main 中 Result/Artifact 轻量卡，点击进 Utility 全文。
- **P7 Needs CEO**：仅真实结构性变化/决策时出现，不固化进每个建设阶段。
- **Shared Employee Service Relation**：Utility 的 Employee Detail 字段来源；Organization 轴与 Office 服务轴正交，不混淆。

---

## 8. 停止状态

```text
WORKSPACE ENGINEERING PANE RESPONSIBILITY CLOSURE — COMPLETE (REVIEW INPUT)
→ 仅回答「什么内容出现在哪里」；不做视觉、不改高保真、不写产品代码
→ 下一步：依据本 Closure 修正高保真四 Pane 分配（尤其 Main 改 RD Workstation、Context 去员工详情、Utility 去员工 Conversation）
```

*本文件为 Workspace Engineering 四栏信息职责 Closure · 2026-08-16（非 Frozen / 非视觉 / 非代码 / 非新架构）*
