# Curis · RD Workspace Methodology Gap Review（研发工作台方法论缺口审查）

**Status**: `Review`
**Methodology State**: `WORKSPACE ENGINEERING METHODOLOGY APPROVED CANDIDATE`
**类型**: 方法论 · Gap 审查（**仅判定缺口，不重新设计 RD**）
**日期**: 2026-08-16
**上位**: `Curis_Workspace_Engineering_Methodology.md` · Lifecycle · Gates
**配套**: Content Growth Case Study（Doc 5）
**真实素材**（均不修改，仅引用）:
- `docs/01_Product/Curis_RD_Workspace_Design_Brief.md`（Status: Review · READY FOR DESIGN REVIEW）
- `docs/01_Product/Curis_RD_Workspace_Reference_Synthesis.md`（Status: Review · 产品参考研究）
- `docs/03_Design/Curis_RD_Workspace_Instance_Spec_v1.md`（Status: **RD INSTANCE APPROVED**）
- `docs/00_Context/CURRENT_STATE.md`（RD INSTANCE APPROVED · READY FOR IMPLEMENTATION PLANNING）

---

## 0. 阅读指引（范围铁律）

> **本文只做 Gap 判定，不重新设计 RD。**

用户提出的核心问题：
> RD Workspace 是否跳过了「优秀软件研发组织到底如何经营研发业务」这一 **Domain Expert Research** 阶段？

本文据此做**缺口审查**，给出 present / weak / missing 判定、证据、潜在影响与建议。**不**补 Operating Model、**不**补 Handoff、**不**改 Instance Spec、**不**进代码。

---

## 1. RD Workspace 实际走过的链路

根据源文档，RD Workspace 的方法论链路是：

```text
[Reference Synthesis]  Codex / Claude Code / Cursor / VS Code / Linear / Relevance AI
                       → 产品 UI 交互模式研究（CONFIRMED/INFERRED/UNVERIFIED 分类）
        ↓
[Design Brief]         由参考研究衍生的「设计-AI 输入」：页面目标/信息层级/空间结构/
                       员工工作站/Composer/Handoff/Needs CEO/失败恢复/参考产品映射
        ↓
[Instance Spec v1]     固化第一个 Professional Workspace Instance（RD INSTANCE APPROVED）
```

即：**工具交互研究 → 设计简报 → 实例规范**。这是一条**以「界面/交互」为起点**的链路。

---

## 2. 对照 Lifecycle 的逐环判定

| Lifecycle 步骤 | RD 实际情况 | 判定 |
|---|---|---|
| 1 BUSINESS INTENT | RD 目标：CEO 监督多 AI 员工真实研发（Design Brief §1） | ✅ present（范围清晰） |
| 2 DOMAIN EXPERT RESEARCH | 研究的是**开发工具的产品 UI 交互模式**，非「研发组织如何经营研发业务」 | ⚠️ **weak / mis-scoped**（研究对象错位） |
| 3 OPERATING MODEL | 无独立 Operating Model 文档（八步飞轮/五层归属等效物缺失） | ❌ **missing**（被 Design Brief 的 UI 要求替代） |
| 4 PRODUCT HANDOFF | 无收敛单份 Handoff（Design Brief 是设计输入，非业务方法 Handoff） | ⚠️ weak（无业务方法收敛层） |
| 5 PRODUCT TRANSLATION | Instance Spec 内部分隐藏（如内部原语）做得较好 | ✅ present（在 Instance 层） |
| 6 CAPABILITY REVIEW | 采用 Frozen Shell / Shared Patterns（P1–P7），未私造 Primitive | ✅ present（设计层复用达标） |
| 7 COMPOSITION | Main/Context/Utility 四 Pane + 员工工作站栈 | ✅ present |
| 8 SEMANTIC MODEL + WORKSPACE DESIGN | RD Instance Spec v1 **APPROVED**；显式研发业务 Semantic Model 仍偏弱 | ⚠️ Design present / Semantic Model weak |
| 9 PACKAGE COMPOSITION | 无可安装 RD Workspace Package | ❌ Target Runtime `NOT IMPLEMENTED`；当前 RD 为源码内置交付 |
| 10–14 | Expressibility / 验收 / 激活 / 学习 / 进化 | ⏳ 当前只按已授权 Issue / Review 推进，不代表 Package 路径 |

**结论**：RD 在**设计层（步骤 5–8）做得扎实且已 APPROVED**；缺口集中在**业务方法层（步骤 2–4）**——尤其步骤 2 的研究对象与步骤 3 的 Operating Model 缺失。

---

## 3. 核心缺口：缺失的 Domain Expert Research 阶段

Lifecycle 步骤 2 要求：
> 先找真正的行业专家 / Expert / Skill，研究：**现实世界里这项业务到底怎么经营**。

对 RD 而言，「这项业务」= **软件研发业务的经营**。真实问题应是：
> 优秀软件研发组织到底如何**经营**研发业务？

应包含（举例，非设计）：经营目标设定、需求/发现与规划、架构与估算、质量门禁、技术债务管理、发布与运维节奏、事故与恢复、研发产出如何回流产品/经营决策、研发组织的学习与进化。

**RD 的实际研究没有覆盖这一层。** 它的《Reference Synthesis》研究的是 *如何用工具做开发*（composer/diff/terminal/test/git/handoff 的交互契约），而不是 *研发组织如何经营研发*。前者是**工具交互**，后者是**业务经营**——两者不等价。

> 类比：Content Growth 若只研究了「小红书/抖音 App 的按钮怎么点」，却没研究「矩阵号内容团队怎么经营增长」，就等同于 RD 现在的状态。Content Growth 正确链的关键是先有 Social Media Growth Expert 的真实经营研究（步骤 2），RD 缺这一环。

---

## 4. 证据：RD Reference Synthesis 的研究对象是什么

《Reference Synthesis》§1 证据边界与 §13 Sources 显示，其研究对象全部是**产品/工具及其 UI 交互**：

| 研究来源 | 性质 | 属于 |
|---|---|---|
| OpenAI Codex app/docs | 产品功能与交互 | 工具交互 |
| Anthropic Claude Code docs | CLI/工作流/子代理 | 工具交互 |
| Cursor Agent/docs | 模式/上下文/后台代理 | 工具交互 |
| VS Code Source Control/GitHub | IDE 源码控制交互 | 工具交互 |
| Linear docs | 项目管理 UI（search/overview/status） | 工具交互 |
| Relevance AI Workforces | 多 agent 状态/审批/升级 | 工具交互 |
| Curis 内部 Authority（CURRENT_STATE 等） | 既有 Curis 语义 | Curis 内部 |

其 §2 任务矩阵（Task A–F）按「开始开发工作 / 给 agent 任务 / agent 开发中 / 检视输出 / 完成 Git / 多 agent 协作」组织——**这是「使用开发工具的任务流」，不是「研发组织的经营方法」**。

**无任何来源**指向：软件工程管理学、研发组织运营模式、研发效能/价值流、技术战略与组合管理、研发业务闭环等「经营研究」文献。这构成步骤 2 研究对象错位的直接证据。

---

## 5. 缺口的潜在影响（风险）

缺口不是「RD 不能用」，而是「RD 的业务经营层可能先天偏薄」：

| 风险点 | 说明 | 关联 Gate |
|---|---|---|
| **Business Truth 偏工具化** | RD 当前中心是代码/Diff/Test/Git/Handoff 等**工具活动真相**；研发工作的**业务真相**（对齐哪个公司/业务目标？研发产出如何回流经营决策？）可能未被建模 | Acceptance ① Business Truth |
| **Operating Model 缺失 → 无 Operating Learning 锚点** | 没有「研发业务如何长期运行并变更好」的模型，步骤 13 运营学习容易退化成「只看工具活动指标」，而非判断经营方法进化 | Gate 6 OPERATING LEARNING |
| **Employee Method 未从经营方法推导** | RD 员工（工程/审核/运行 AI）的职责来自工具链直觉，而非「研发业务经营方法」推导；未来增员/路由时可能缺乏经营层依据 | Lifecycle 步骤 3 |
| **Instance 设计扎实但语义地基薄** | Instance Spec APPROVED 是设计事实正确；但其上游尚缺显式的研发业务对象 / 关系 / 状态 / 责任 / 关键业务真相模型。该缺口应先由局部 Semantic Model / Package Domain Schema 承载，不默认要求像 Content Growth 一样 Frozen 全局 Authority | Lifecycle 步骤 6–8 |

> 重要澄清：**这不构成「RD 实例错误」的结论。** RD Instance 作为「监督 AI 员工做研发的界面」已 APPROVED 且可用。缺口是**方法层面的上游缺失**，会在 RD 未来**进化**（尤其真实研发工具闭环、研发 Business Runtime、研发经营闭环）时显形。

---

## 6. 结论与建议

### 6.1 判定

| 项 | 结论 |
|---|---|
| RD 是否跳过了「优秀研发组织如何经营研发业务」的 Domain Expert Research？ | **是（步骤 2 mis-scoped / missing）** |
| RD 设计层（步骤 5–8）是否达标？ | **是（Instance APPROVED）** |
| 是否现在重新设计 RD？ | **否（本次仅 Gap 判定）** |

### 6.2 建议（供 Review 与未来演进参考，非本次执行）

1. **在 RD 进一步进化前**，补一轮真正的 Domain Expert Research：优秀软件研发组织如何经营研发业务（经营目标/规划/质量/技术债/发布/事故/学习闭环）。
2. 据此补一份 RD **Operating Model**（步骤 3）、收敛 **Product Handoff**（步骤 4）与显式 **Semantic Model**（步骤 8），再评估是否需要演进 Workspace Design / Package Domain Schema。
3. 明确 RD 的 **Business Truth** 范围：除了工具活动真相，是否建模研发工作与公司/业务目标的对齐与回流。
4. 为 RD 的 **Operating Learning Gate（Gate 6）** 预设判据：什么算「研发经营方法需要进化」，而非只看工具活动指标。
5. 只有 RD 语义跨多个 Instance 复用、成为官方 Domain 标准、影响 Company OS 或需要长期兼容保证时，才进入 Domain Authority / Frozen；不得把 Content Growth 的升格路径机械复制到 RD。

### 6.3 不做什么（铁律）

- ❌ 不补 Operating Model / Handoff（本次只判定）
- ❌ 不改 RD Instance Spec（已 APPROVED）
- ❌ 不进代码 / Runtime / Blueprint / Frozen 文档
- ❌ 不把本 Gap 判定曲解为「RD 实例无效」
- ❌ 不把当前 RD 源码实现 / 重建验收写成 Dynamic Workspace Package Runtime 已实现

---

## 7. 状态

```text
RD METHODOLOGY GAP APPROVED CANDIDATE — DOMAIN EXPERT RESEARCH (STEP 2) GAP CONFIRMED · NO REDESIGN THIS ROUND
```

*Curis RD Workspace Methodology Gap Review · APPROVED CANDIDATE / Review（非 Frozen · 仅缺口判定 · 不重新设计 RD）*
