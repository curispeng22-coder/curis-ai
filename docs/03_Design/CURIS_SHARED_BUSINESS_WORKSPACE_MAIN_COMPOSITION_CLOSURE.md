# Curis · Shared Business Workspace Main Composition Closure

> **Status**：SHARED MAIN COMPOSITION CLOSURE（APPROVED · 已回写 Frozen 最小澄清 · 2026-08-17 · Delta-X9）
> **本阶段纪律**：不修改 Frozen Shell / P1–P7 / Employee Workstation Pattern / 任何高保真 HTML、不写产品代码、不创建 P8、不重定义 Employee Workstation、不暴露 Agent/Router/DAG/Package/Gate 内部原语。
> **消费依据**：`Curis_Workspace_Shell_Contract_And_Shared_Patterns.md`（Frozen · S1–S7 + P1–P7 + Delta-S1/S2/S3 已回写）+ `CURIS_SHARED_EMPLOYEE_WORKSTATION_PATTERN_CLOSURE.md`（本 Closure 是其**超集扩展**：在已锁定的 Employee Workstation Pattern 之上，补齐 Main 的完整组合视图）。

---

## 0. 结论先行（TL;DR）

- **Main = 业务展示区 + 工作区** 应成为所有**含 AI Employee 的**长期 Business Workspace 的 **Shared 组合规则**（无 AI Employee 的 Workspace 其 Main 可仅含业务展示区，与 Frozen §0.1 一致）。
- **业务展示区**：意图（"回答业务现在整体怎么样"）、容器名、维度候选集为 **Shared**；具体展示哪些维度 / 字段 / 形式由 **Domain** 决定。空间工程、RD、Content Growth、客服**不必长成相同 Dashboard**。
- **工作区**：固定名"工作区" + Conversation-first Workstation 基础范式 + Presence→Workstation→过程→Result/Artifact→Composer 流序为 **Shared**；哪些员工 / 谁当前·完成·等待 / 顺序或并行 / Responsibility / Tool / Result 类型 / 折叠-展开-轻量编排策略为 **Domain 编排**。
- **四栏**：Context / Utility 默认收起已被 Frozen 充分表达；但"**Main 必须独立成立 / Context 不得承载关闭后导致 Main 无法理解业务的核心信息**"需最小显式补充。
- **Frozen Shell S1 歧义**：S1「Employee Workstation = Main / Conversation-first」句主语易滑读为「Main = Employee Workstation」。最小澄清（不建 P8、不改 P1–P7、不重定义 Workstation）：**Employee Workstation ∈ Main.WorkArea（工作区）；Main = Domain Business Surface（业务展示区）+ Shared Work Area（工作区）**。
- **对当前 Workspace Engineering 高保真（前向说明，本轮不改）**：当前 Main 仅 = 当前员工 Workstation，缺独立业务展示区；须补 Business Display Area，Main 改为「业务展示区(上) + 工作区(下)」双区结构。

---

## 1. 核心裁定：Main = 业务展示区 + 工作区（Shared 规则）

所有**含 AI Employee 的**长期 Business Workspace 的 **Main** 统一由两部分组成（无 AI Employee 的 Workspace 其 Main 可仅含业务展示区，与 Frozen §0.1「Workstation = Available Capability 非 Required」一致）：

```
Main = 业务展示区 (Domain Business Surface)  +  工作区 (Shared Work Area)
         ↑ Domain-specific                       ↑ Company OS / Shell Shared 范式
```

- 这是**组合规则**（Main 的构成），不是新 Pattern、不是新 P 编号。它与已 Frozen 的 Employee Workstation Pattern（Delta-S1/S2/S3）**相容且互补**：Workstation Pattern 锁定"进入具体员工后 Main 的 Workstation 形态"，本 Closure 补齐"Main 除了 Workstation 还必须有独立的业务展示区"，二者共同构成完整 Main。
- Employee Workstation 属于 Main 的**工作区**，但 **≠ 整个 Main**。

---

## 2. 业务展示区（Domain-specific）

回答："**这个业务现在整体怎么样？**"

| 维度 | Shared / Domain | 说明 |
|---|---|---|
| **展示意图** | **Shared** | Main 必须能回答"业务现在整体状态"，这是所有 Business Workspace 的共同责任 |
| **容器名「业务展示区」** | **Shared** | 统一语义容器（可随 Workspace 视觉呈现，但概念名共享） |
| **维度候选集** | **Shared（候选）** | 目标 / 业务状态 / 关键业务对象 / 进度 / 关键结果 / 问题·Blocker / 需 CEO 关注或决定事项 |
| **具体展示哪些维度** | **Domain** | 由行业研究 / Operating Model 决定（交付型、经营型、研发型、服务型的关注点不同） |
| **具体字段 / 指标 / 对象** | **Domain** | 字段与取值由业务语义定义 |
| **呈现形式（卡片/列表/时间轴/看板）** | **Domain** | 由 Workspace 视觉与信息密度决定 |

**不同业务可完全不同（不要求同 Dashboard）**：
- 空间工程（交付型）：进行中建设任务 / 近期交付办公室 / 关键 Blocker / 需 CEO 拍板事项。
- RD（研发型）：在研项目 / 构建·测试状态 / 关键里程碑 / 技术风险。
- Content Growth（经营型）：内容经营 Business Home（经营方向 / 连续内容流 / 关键结果）。
- 客服（服务型）：工单量 / SLA / 待处理 / 升级事项。

> 关键：业务展示区是 **Domain 专业业务界面**，不是 Employee Workstation 的变体。它与 Workstation Pattern Closure §3 的"Domain Extension"一致——变化的只是被打开的内容，Employee Workstation 基础范式跨业务不变。

---

## 3. 工作区（Shared Work Area · Company OS / Shell）

固定名：**工作区**。

### 3.1 Shared 基础范式（全局统一，不得因业务而变）

| 项 | Shared 内容 |
|---|---|
| **固定名** | 统一叫"工作区" |
| **基础范式** | Conversation-first Employee Workstation（自然 Conversation + 工作状态 + Tool/Action 状态 + Result/Artifact 引用 + Composer） |
| **流序** | Employee Presence → Workstation → 工作过程 → Result / Artifact → Composer |
| **CEO 介入** | 可进入任一在岗员工继续讨论（责任未真变不新建线程） |

> 依据 Frozen：`Curis_Workspace_Shell_Contract_And_Shared_Patterns.md` §3.1（Employee Workstation = Main / Conversation-first，Delta-S1 全局统一约束）+ P2(Presence) / P5(Handoff) / P6(Result Reference) / P7(Needs CEO)。Employee Workstation 本身**不重新定义、不改写**。

### 3.2 Domain 编排（允许，但不改变 Workstation 基础范式）

| 项 | Domain 决定示例 |
|---|---|
| **哪些员工属此业务** | 空间工程=行业研究/经营方法/产品设计/搭建实施/质量验收；RD=Developer/Reviewer；客服=接待/处理 |
| **谁当前 / 完成 / 等待** | 实时责任状态由业务运行决定 |
| **顺序 or 并行** | 空间工程=顺序交付型；Content Growth=多员工持续/并行；RD=按 Developer/Reviewer 分工 |
| **Responsibility** | 各员工当前责任阶段 |
| **Tool 类型** | RD=代码/Diff/测试；Content Growth（小红书 / XHS）=图文预览/审核；客服=工单操作 |
| **Result / Artifact 类型** | RD=代码变更；Content Growth（小红书 / XHS）=已发布笔记；空间工程=研究报告/Operating Model/Design/Acceptance |
| **编排策略（折叠-展开-轻量）** | 默认呈现策略示例：已完成员工 Workstation 默认折叠、当前员工默认展开、等待员工默认轻量显示——**仅为建议默认呈现，非状态绑定规则**；CEO 可自由覆盖（见回写 Frozen §3.1「工作区编排约定」） |

**铁律**：顺序交付 / 多员工并行 / 按角色分工 等差异，属于**工作区编排差异**，不是 Employee Workstation 基础范式差异。Employee Workstation 在所有部门完全一致；变化的只是它周边被打开的 Tool / Artifact / Responsibility / 协作拓扑。

---

## 4. 四栏进一步明确（默认 Desktop）

```
Nav  +  Main                              （常驻）
Context / Utility  =  Adaptive On-demand Pane（默认收起）
```

| Pane | 语义 | 默认态 |
|---|---|---|
| **Nav** | 我在哪里 | 常驻 |
| **Context** | 当前工作**按需取用**的额外上下文 | Adaptive，默认收起 |
| **Main** | 业务展示区 + 工作区 | 常驻；**必须能独立成立** |
| **Utility** | 当前选中对象详情 / 预览 | Adaptive，默认收起 |

**Main must stand on its own**：Context / Utility 全关时，CEO 仍能理解业务整体状态并完成主要工作。Context **不得承载**"关闭后导致 Main 无法理解业务"的核心信息。

### 4.1 Frozen 充分性审查

- **"默认收起"已充分表达**：
  - §0.1 边界修正 1：「不叫四栏固定……Context / Utility 都是 Adaptive Surface，按需出现、展开、收起，默认态不占空间」。
  - §2.1（Adaptive Surface）：默认均收起、主区满宽、可全关。
  - §3.12：Context 仅答工作上下文，不含完整员工详情 / Conversation。
- **"Main 必须独立成立 / Context 不得承载核心业务信息"未作为首类原则显式**：现有条款散见于 §3.12（Context 不含核心），但缺少一句把"Main 自成立"作为 Main 设计的硬约束显式写出。

> 建议最小补充（落 §0.1 或 §1.1，与现有条款一致、非新架构）：
> 「Context / Utility 全关时 CEO 仍能理解业务整体状态并完成主要工作；Context 仅答按需上下文，不得承载关闭后导致 Main 无法理解业务的核心信息。」

---

## 5. Frozen Shell 审查与最小澄清（S1 歧义）

### 5.1 现状引文（已回写 S1）
> §0.1 边界修正 2 Clarification + §3.1 Global Shared Rule（Delta-S1）：「CEO 进入任意具体 AI Employee 后，Main 统一 Conversation-first Employee Workstation；Workspace 默认 Main 可保持 Domain-specific 专业业务界面，但任何存在 AI Employee 的 Workspace 都必须支持进入该 Employee 的 Shared Workstation。」

### 5.2 歧义
句主语"Main 统一呈现其 Workstation"**易滑读为「Main = Employee Workstation」**——尤其当某 Workspace 把 Main 默认就渲染成单个 Workstation 时，会进一步强化"Main 即 Workstation"的误读。

### 5.3 最小澄清（不建 P8、不改 P1–P7、不重定义 Workstation）
> **Employee Workstation ∈ Main.WorkArea（工作区）；Main = Domain Business Surface（业务展示区）+ Shared Work Area（工作区）。**
> 钻取进具体员工时，Main 的**工作区局部**呈现该员工的 Conversation-first Workstation；这不改变 Main 还包含独立的业务展示区。Workspace 默认 Main 可声明自身 Domain 业务展示区，Workstation 只是其中"工作区"部分的统一范式。

- 落点建议：与 Delta-S1 同层，在 §0.1 边界修正 2 Clarification 追加一句 + §3.1 note 补"Workstation ∈ Main.WorkArea"；**不新开 P 编号、不重复定义 Workstation**。
- 与 `CURIS_SHARED_EMPLOYEE_WORKSTATION_PATTERN_CLOSURE.md` §7 约束一致（"即便在经营型 Workspace 的 Business Home，点员工 → Main 同样切到其 Workstation"），本 Closure 仅把它从"员工维度"推广为"Main 组合维度"的显式表述。

---

## 6. 对当前 Workspace Engineering 高保真的前向修改（本轮不改）

> 本 Closure 已批准并回写 Frozen（Delta-X9）；**Workspace Engineering 高保真已据本 Closure 重制**，新 Main = 业务展示区(上) + 工作区(下)，详见 Visual Closure 与交付物 `Curis_Workspace_Engineering_High_Fidelity_Remake.html`。

- **当前 Main（进行中建设任务屏）= 仅当前员工 Workstation**（build-progress + AI 工作状态 + Conversation + Result/Artifact + Composer），**缺独立的业务展示区**。
- **须改**：Main = **业务展示区(上) + 工作区(下)** 双区结构。
  - 空间工程 Domain 业务展示区 = **交付型概览**：进行中建设任务 / 近期交付办公室 / 关键 Blocker / 需 CEO 关注或决定事项。
  - 当前顶部 `build-progress` 责任链归入业务展示区的"**进度**"维度（Domain 展示内容），Conversation / Composer 留在工作区。
  - 确保 Context / Utility 全关时，Main（业务展示区 + 工作区）**自成立**。
- **纪律不变**：不引入 Dashboard / 八问 / 指标卡 / 大型 Timeline / 固定右栏 / 重设计聊天框；业务展示区用轻量 Domain 概览，工作区维持 Conversation-first Workstation。

---

## 7. 最终回答（用户六问）

**Q1 — Main = 业务展示区 + 工作区 是否应成为长期 Business Workspace Shared 规则？**
**是（限定含 AI Employee 的 Workspace）。** 它是跨所有**含 AI Employee 的**长期 Business Workspace 的 Main 组合规则，与已 Frozen 的 Employee Workstation Pattern 相容互补，不新建 Pattern / 不建 P8；无 AI Employee 的 Workspace 其 Main 可仅含业务展示区（Frozen §0.1 Workstation = Available Capability 非 Required）。

**Q2 — 业务展示区哪些 Shared、哪些 Domain-specific？**
- **Shared**：展示意图（回答"业务现在整体怎么样"）、容器名"业务展示区"、维度候选集（目标/状态/关键对象/进度/关键结果/Blocker/需 CEO 关注）。
- **Domain-specific**：具体展示哪些维度、具体字段/指标/对象、呈现形式（卡片/列表/时间轴）。空间工程、RD、Content Growth、客服不必同 Dashboard。

**Q3 — 工作区哪些 Shared、哪些允许 Domain 编排？**
- **Shared**：固定名"工作区"、Conversation-first Workstation 基础范式、流序 Presence→Workstation→过程→Result/Artifact→Composer、CEO 可进任一员工续议（Frozen §3.1 / P2/P5/P6/P7）。
- **Domain 编排**：哪些员工、谁当前/完成/等待、顺序或并行、Responsibility、Tool 类型、Result/Artifact 类型、折叠-展开-轻量编排策略。顺序交付 / 并行持续 / 按角色分工属编排差异，不改 Workstation 范式。

**Q4 — Context/Utility 默认收起 + Main must stand on its own 是否已被现有 Frozen 充分表达？**
- "默认收起"**已充分**（§0.1 边界修正1 + §2.1 + §3.12）。
- "Main 必须独立成立 / Context 不得承载核心业务信息"**需最小显式补充**（建议落 §0.1 或 §1.1 一句，与现有条款一致）。

**Q5 — Frozen Shell 需要哪些最小文字澄清？**
1. **S1 歧义澄清**：Employee Workstation ∈ Main.WorkArea；Main = Domain Business Surface + Shared Work Area（钻取进员工时工作区局部呈现其 Workstation，不改变 Main 还含业务展示区）。不建 P8、不改 P1–P7、不重定义 Workstation。
2. **四栏显式一句**：Context/Utility 全关时 CEO 仍能理解业务整体状态并完成主要工作；Context 不得承载关闭后导致 Main 无法理解业务的核心信息。

**Q6 — 对 Workspace Engineering 当前高保真必须产生哪些修改？**
当前 Main 仅 = 当前员工 Workstation，缺独立业务展示区。须补 Business Display Area，Main 改为「业务展示区(上) + 工作区(下)」双区结构；空间工程 Domain 业务展示区 = 交付型概览（进行中/近期交付/关键 Blocker/需 CEO 关注事项），build-progress 责任链归入"进度"维度，Conversation/Composer 留工作区；确保 Context/Utility 全关时 Main 自成立。**已据本 Closure 批准并重制高保真（见交付物）。**

---

## 8. 纪律与停止态

```text
CURIS SHARED BUSINESS WORKSPACE MAIN COMPOSITION CLOSURE — APPROVED · WRITTEN-BACK
→ Main = 业务展示区(Domain) + 工作区(Shared) 定为长期 Business Workspace Shared 规则（已回写 Frozen Delta-X9）
→ 业务展示区：意图/容器/维度候选集 Shared；具体字段/形式 Domain（"业务展示区"为内部架构名，非强制 UI 标题）
→ 工作区：固定名+Workstation范式+流序 Shared；员工/当前/完成等待/顺序并行/Responsibility/Tool/Result/编排 Domain
→ 四栏：默认收起已充分；新增 Main must stand on its own（已回写 Frozen）
→ Frozen S1 最小澄清：Workstation ∈ Main.WorkArea；Main = Domain Business Surface + Shared Work Area（已回写）
→ 工作区 = Employee Workstation List；Runtime 状态 ≠ UI 折叠；唯一默认展开 = 外部进入且单一 working Employee（已回写）
→ 高保真已据本 Closure 重制（新 Main = 业务展示区(上) + 工作区(下)）
→ 纪律：未新建 P8；未改 P1–P7；未重定义 Workstation；未暴露内部原语
→ 停止 Review（STOP FOR REVIEW）
```

*本文件为 Curis Shared Business Workspace Main Composition Closure · 2026-08-17（APPROVED · 已回写 Frozen Delta-X9 · 非视觉 / 非代码 / 不创建 P8 · 为 Shared Employee Workstation Pattern Closure 的超集扩展）· 经设计原型专家团 Phase1(许明需) IA 发现 + Phase4(严过审) 审查流程产出 · 高保真已据本 Closure 重制*
