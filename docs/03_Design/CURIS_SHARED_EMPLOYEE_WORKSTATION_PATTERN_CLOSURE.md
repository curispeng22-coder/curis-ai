# Curis · Shared Employee Workstation Pattern Closure

> **Status**：SHARED PATTERN CLOSURE · **APPROVED + DELTA-S1/S2/S3 已回写 Frozen Workspace Shell Contract**
> （Review 通过；最小 Delta 已回写，不创建 P8、不修改 P1–P7 语义；不改 Workspace Engineering 高保真、不写产品代码）
> **目标**：确认 Curis 所有 AI Employee 的实际工作工位是否统一采用 Conversation-first 范式，并审查现有 Frozen Authority 是否已足够表达。
> **纪律**：不重定义 Product Blueprint / Frozen Shell / P1–P7 / RD Instance / T5；引用为主、最小补强为辅；不暴露 Agent / Router / DAG / Package / Gate 内部原语。

---

## 0. 结论先行（TL;DR）

- **原则本身已经 80% 存在于 Frozen Authority**：Product Blueprint（v4.4 Single Current）已写明「员工 Workstation 必须位于 Main、不属于 Context Sidebar」「Workstation = 自然 Conversation + Composer + 持续 Session」；Frozen Shell §3.1 已把 Employee Workstation 定义为「自然 Agent Conversation + 底部锚定 Composer」的 Shared Company Pattern；RD Design Brief 已是第一个确认实例。
- **存在 2 个真实缺口**，但都「小」，不需要新 Pattern，只需在 **Frozen Workspace Shell Contract（Layer 3）做最小补充**：
  - **Gap A**：「进入**任意**具体员工（不限部门/业务）→ Main 统一回到 Conversation-first Workstation」这一**全局统一约束**尚未被单条显式 Shared 规则表述（Shell §0.1 反而把 Main 布局留给 Workspace、把 Employee Workstation 标为「Available Capability，非 Required」）。
  - **Gap B**：**Employee Detail（Utility）这一第三支柱根本不在 Frozen Shell 里**——它只存在于 Content Growth 的 T5 Candidate，Shell 只有 Presence(P2) + Workstation(§3.1)，没有 Detail。三概念统一规则因此缺一条腿。
- **建议**：把「Employee Workstation = Conversation-first Shared 全局规则」明确升级为 Company-wide 约束；在 Shell Layer 3 补「Employee Detail（Utility）」共享条目（引用 T5，不重复定义）；补一条显式禁止（Conversation 不得进入 Context、也不得进入 Detail/Utility）。**不创建 P8**。

---

## 1. 核心原则（待统一表述）

**所有 AI Employee Workstation 的基础工作方式统一。**

无论员工属于研发、内容增长、空间工程、销售、客服还是未来其他业务，**CEO 进入一个具体员工后，Main Workspace 默认都是**：

```
自然 Conversation
+ AI 工作过程（工作状态：当前步骤 / 持有者 / 等待原因 / 下一步）
+ 必要的 Tool / Action 状态
+ Result / Artifact（P6 轻量引用）
+ Composer
```

- 交互参考 **ChatGPT / Codex 类成熟 AI 工作范式**，**不为不同业务重新设计不同的「员工工作方式」**。
- **Domain-specific 的是 Workspace 自己的专业业务界面**，不是 Employee Workstation 基础范式：
  - 内容增长 Workspace 可以有发布日历、内容库、排期、账号数据、结果回收；
  - RD Workspace 可以有项目、代码、测试、Review；
  - 客服可以有工单、客户、SLA；
  - 但这些是 **Workspace 的 Main 专业业务布局（Domain Extension）**。当 CEO **点击进入其中任意具体 Employee** 时，Main 统一切到该员工的 **Conversation-first Workstation**。
- 精确边界（避免过宣称）：本规则约束的是「**进入具体员工**」这一动作后的 Main 形态，**不要求每个 Workspace 的默认 Main 永远只是一个 Workstation**。Workspace 的默认 Main 仍可有自己的领域业务布局（见 §3 Domain Extension）；钻取进员工才触发统一的 Workstation 形态。

---

## 2. 三概念严格区分（Presence / Workstation / Detail）

| 概念 | 回答的问题 | 所在 Pane | 是否含 Conversation | 当前 Authority 状态 |
|---|---|---|---|---|
| **Employee Presence** | 「谁在这里工作 / 谁当前负责」——只是员工**入口** | 贴在业务对象上（Note 卡 / 顶部 Presence 条），**持续可感知** | 否（只有「▸ 工作过程」入口） | **Frozen · P2（Shell §3.8）** |
| **Employee Workstation** | 「这个员工现在怎么和 CEO 一起工作」 | **Main Workspace**（CEO 进入具体员工时） | **是**（自然 Conversation + Composer） | **Frozen · Shell §3.1**（Shared Company Pattern） |
| **Employee Detail** | 「这个人是谁 / 组织关系 / 岗位 / 能力 / 长期责任 / 当前 Responsibility / 工作方式 / 最近结果」 | **Utility Pane**（点击员工「详情 / 是谁」时） | **否** | **仅 Candidate（Content Growth T5）—— 不在 Frozen Shell** ⚠️ |

**点击 Employee Presence 的两个动作（铁律）**：
- 「**进入员工工作**」→ Main 打开该 Employee **Workstation**（Conversation-first）。
- 「**查看员工详情** / 详情动作」→ Utility 打开 **Shared Employee Detail**。

**硬约束（三处不得混）**：
- Workstation / Conversation **不得塞进 Context**（Context 只答「这次工作是什么上下文」）。
- Workstation / Conversation **不得塞进 Employee Detail（Utility）**（Detail 永远只是「是谁」，不含会话）。
- Presence 只是入口，不等于 Workstation，也不等于 Detail。

---

## 3. Shared vs Domain Extension 边界

### Shared（全局统一，不得因业务而变）

| 项 | 说明 |
|---|---|
| **Conversation-first 基础范式** | 所有员工工位统一：消息流 + 工作状态 + Tool/Action 状态 + Result/Artifact + Composer |
| **Main = Employee Workstation** | CEO 进入具体员工后，Main 统一为 Conversation-first Workstation |
| **Composer** | 锚定在活跃 Workstation Conversation 底部；只显示改变当前运行契约的控件 |
| **工作过程表示** | 状态必须含 步骤 / 持有者 / 等待原因 / 下一步；禁止无 owner 的泛「运行中」 |
| **Result / Artifact 入口** | P6 轻量引用，对话内不铺全文；点击进 Utility 专业预览 |
| **CEO 持续介入同一 Session** | 责任未真变不新建线程；CEO 输入新上下文后员工继续当前 Session |
| **Employee Detail 使用 Shared Detail** | 点击员工「详情」→ Utility 统一用 Shared Employee Detail（六字段，见 §2） |

### Domain Extension（由 Workspace / 业务决定，不在 Shared 范围）

| 项 | 示例 |
|---|---|
| **Tool 类型** | RD=代码/Diff/测试；XHS=图文预览/审核；客服=工单操作 |
| **Artifact / Result 类型** | RD=代码变更；XHS=已发布笔记；客服=工单解决记录 |
| **专业工作状态** | RD=「构建中」；XHS=「创作中」；客服=「处理工单中」 |
| **Context 内容** | RD=文件树；XHS=选题库；客服=客户上下文 |
| **Utility 专业预览** | RD=Diff/Source；XHS=图文/数据看板；客服=工单详情 |
| **Workspace 其他专业业务 UI** | 发布日历、项目看板、工单队列、账号数据等 **Domain 业务主界面**（不属于 Employee Workstation 基础范式） |

> 关键：Domain Extension 是「Workspace 的 Main 专业业务布局」与「Utility 专业预览」，**不是** Employee Workstation 的变体。Employee Workstation 基础范式在所有部门完全一致；变化的只是它周边被打开的 Tool / Artifact / Context / Utility 内容。

---

## 4. 现有 Authority 审查（5 份）

### 4.1 Product Blueprint（v4.4 Single Current · Frozen）
**判定：已充分支持原则，是最高权威来源。**
- 第 145 行：「Workspace 是一间真正的专业业务办公室：它同时包含**业务自己的工作界面、多个 Employee Workstation**……它不是……只有一个 Conversation 的 Project。」→ **Domain 业务 UI 与 Employee Workstation 并存、且二者不同**，已奠定区分。
- 第 149 行：「员工 **Workstation 必须位于 Main Workspace，不属于 Context Sidebar**。」→ **显式 Frozen 规则：Workstation ∈ Main、∉ Context**。
- 第 153–160 行：Workstation = 「自然的员工工作窗口、当前责任和长期上下文」；Session = `Conversation / Current Context / Current Work / Progress / Working Memory`；紧凑态含「最近几轮 Conversation 和 Composer」；CEO 点击员工「展开当前 Session 输入新要求」。→ **Conversation-first + Composer + 持续 Session 已在 Frozen Blueprint**。
- 第 175 行：「CEO 随时可以进入正在工作的员工 Workstation，输入新上下文，员工继续当前 Session，后续 Handoff 不需要从头重跑。」→ **持续介入同一 Session**。

### 4.2 Frozen Workspace Shell Contract（Layer 3 · P1–P7 Frozen）
**判定：Workstation/Presence 已 Frozen，但缺「全局统一约束」与「Detail」两处。**
- §3.1 Employee Workstation（Collapsed/Expanded）：Anatomy = Header（头像/名/角色/状态/上下文标签/chevron）+ Body（**自然 Agent Conversation + 底部锚定 Compact Composer**）。→ **Conversation-first 已定义为 Shared Company Pattern**。
- §3.8 Employee Presence（**P2 Frozen**）：业务对象上的轻量责任存在；「Open Workstation 入口（▸ 工作过程）」展开 Workstation/Conversation；Presence ≠ Workstation 已明确。
- §3.4 Result Reference（**P6 Frozen**）：对话内仅轻量引用，点击开 Utility；对话内不铺全文。
- §3.5 Composer：锚定活跃 Workstation Conversation 底部。
- ⚠️ **§0.1 边界修正 2 的副作用**：它把 Main 定义为「专业业务主工作面，布局由 Workspace 决定」，并把 Employee Workstation 列入「Available Capability，**非 Required**」（§4 矩阵：研发✅ / 小红书⚪ / 抖音⚪ / 会议⚪）。这导致「进入任意具体员工 → Main 统一 Conversation-first」**未被单条显式 Shared 规则锁定**，容易被误读为「只有研发才以 Workstation 为核心」。
- ⚠️ **缺 Employee Detail**：Shell 只有 Presence(P2) + Workstation(§3.1)，**没有 Detail**，第三支柱悬空。

### 4.3 Shared P1–P7（Frozen）
**判定：不直接冲突，提供底座。**
- P2（Employee Presence）、P5（Handoff）、P6（Result Reference）、P7（Needs CEO）均支持本原则（Presence 入口、Result 轻量引用、Conversation 持续）。无一条禁止 Conversation-first。
- P1/P3/P4 三层责任语义、System Activity、Automation by default 与本原则正交、相容。

### 4.4 RD 已确认的 Employee Workstation
**判定：第一个确认实例，范式已被验证。**
- §2：Main = Employee Workstations + active employee Conversation；Context = 当前 Workspace/责任/相关文件/最近对象（**非 Session Manager / 员工目录 / 权限中心 / 工具目录**）；Utility = focus-switched 专业区。
- §3：「Do not make Employee Workstations a navigation sidebar or top-level tabs.」
- §4：展开 Workstation 打开真实 Agent Conversation，责任未真变不新建线程。
- §5：Composer 属于活跃 Workstation Conversation。
- §10：CEO 持续介入同一 Session；责任真变才新建。
- Anti-patterns：无 DAG 画布、无永久工具墙、无泛「运行中」状态。
- → **RD 是「统一范式」的首个实证**，不是「只适用于研发的特殊范式」。

### 4.5 Content Growth Business Home T5 · Shared Employee Detail
**判定：Detail 内容来源已就绪（Candidate），但未被 Shell 收编为 Shared。**
- T5（Shared Employee Service Relation Contract **Candidate**）定义了 Shared Employee Detail 六字段：个人信息 / Organization-Department-Team-Leader / 长期责任 / 当前 Responsibility / 能力·工作方式 / 最近结果；并区分 Organization 轴与 Office 服务轴正交。
- 但 T5 状态是 **APPROVED CANDIDATE（未 Frozen）**，且**仅存在于 Content Growth 语境**；Frozen Shell 未引用它，因此「点击员工 → Utility Shared Detail」目前只是 Candidate + 上一轮 Pane Closure 的约定，**不是 Shared 规则**。
- 其 §0 已声明 FROZEN 指针：语义已冻结于 `Curis_Company_OS_Shared_Authority.md` §1.2（作 Design Record）。→ 可由 Shell Layer 3 引用，无需重复定义。

---

## 5. 缺口判定（Gap）

| 缺口 | 描述 | 严重度 | 是否需要新 Pattern |
|---|---|---|---|
| **Gap A** | 「进入**任意**具体员工（不限部门）→ Main 统一 Conversation-first Workstation」**全局约束**未单条显式表述；Shell §0.1 把 Main 留给 Workspace、把 Workstation 标为「非 Required」，易被误读为「仅研发」 | 中 | 否——在 Shell §3.1 强化 + §0.1 澄清即可 |
| **Gap B** | **Employee Detail（Utility）不在 Frozen Shell**，只活在 T5 Candidate；三概念统一规则缺腿 | 中 | 否——在 Shell Layer 3 补一条引用 T5 的 Shared 条目即可 |
| **Gap C** | 「Conversation 不得进入 Context、也不得进入 Detail/Utility」未作为 **Shared 显式禁止**；目前只散见于 Pane Closure | 低 | 否——在 Shell Layer 3 补一条边界澄清即可 |

**结论：现有规则足够承载原则，仅需在 Frozen Shell 做 3 处最小补充（不新开 P 编号、不重复定义）。**

---

## 6. 最小 Shared Pattern Delta 提议（落点：Frozen Workspace Shell Contract · Layer 3）

> 以下为**提议文本**，不自行 Frozen；待 Review 批准后由 Shell 维护者回写。

**Delta-S1（强化 §3.1 / 澄清 §0.1）· 全局统一约束**
> 新增一条 Shared 约束：「**CEO 进入任意一个具体 Employee（不限部门/业务）后，Main Workspace 统一呈现该员工的 Conversation-first Workstation**（自然 Conversation + 工作状态 + Tool/Action 状态 + Result/Artifact 引用 + Composer）。此为基础范式，跨所有业务一致，不为不同部门重新设计。Workspace 的默认 Main 仍可声明自身领域业务布局（Domain Extension）；钻取进员工即触发统一 Workstation 形态。」
> 同步在 §0.1 边界修正 2 增加注：「Employee Workstation 虽为 Available Capability（非所有 Workspace 默认必备），但一旦 CEO 钻取进具体员工，其形态必须统一为 Conversation-first，不受所在业务域影响。」

**Delta-S2（新增 Layer 3 条目）· Employee Detail（Utility）**
> 新增 §3.x「Employee Detail（Shared · Utility）」：定义 = 「这个人是谁 / 组织关系 / 岗位 / 能力 / 长期责任 / 当前 Responsibility / 工作方式 / 最近结果」；**位于 Utility Pane**，由点击员工「详情 / 是谁」触发；**不含 Conversation**（Conversation 只属 Main Workstation）；内容字段引用 **T5 Shared Employee Service Relation（Design Record）**，不重复定义。与 §3.8(Presence) / §3.1(Workstation) 构成三概念统一。

**Delta-S3（新增 Layer 3 边界澄清）· Conversation 不得越界**
> 在 §3.12 边界澄清表追加：「**Employee Workstation / Conversation 不得进入 Context Pane（Context 只答工作上下文、含 Presence 简要）**」；「**Employee Workstation / Conversation 不得进入 Employee Detail / Utility Pane（Detail 永远只是『是谁』）**」。

> **不创建 P8**：上述均为 Layer 3 共享模式层补强，不新增 P 编号；P2/P5/P6/P7 不动。

---

## 7. 对上一轮 Workspace Engineering Pane Closure 的必须修正约束

（上一轮 Pane Closure 本轮**暂不 Review**、**不修改**；以下为它将来被 Review 时必须吸收的约束。）

1. **规则从「空间工程专属」升为「全局统一」**：上一轮把 Main 的 Workstation 表述为「参照 RD Workstation 范式」（§1/§2/§4 P-C）。须修正为：**Conversation-first Workstation 是全公司所有员工的统一基础范式**，RD 只是首个确认实例；Space Engineering 建设任务只是该范式的一个**领域变体**（有终点、责任链顺序交接），不是特例。
2. **Employee Detail 须显式标注「Shared 待收编」**：上一轮 §3 把 Detail 字段来源写作「Shared Employee Service Relation」，但 Frozen Shell 尚无 Detail 条目。须补充注明：该 Detail 当前仅为 T5 Candidate，正通过本 Closure 的 Delta-S2 提议收编为 Shell Layer 3 Shared 条目；在收编前，它是 Review-INPUT 级约定，非 Frozen 规则。
3. **禁止项补强为 Shared 来源**：上一轮 §6 禁止「Context 放员工 Conversation」「Utility 点击员工放 Conversation」目前只引用自身 Closure。须改引为 **Frozen Shell（Delta-S3 提议）**，使禁止项获得 Shared Authority 支撑，而非仅 Workspace Engineering 内部约定。
4. **P-C 的 Main 表述精确化**：上一轮 P-C 写「Main = 当前责任员工的 Workstation」，须补一句：**即便在内容增长等「经营型」Workspace 的 Business Home，CEO 点击其中任一在岗员工，Main 同样切到该员工的 Conversation-first Workstation**——证明规则跨经营型/建设型业务一致。

---

## 8. 最终回答（用户四问）

**Q1 — 是否建议 Employee Workstation = Conversation-first Shared Pattern 成为全局规则？**
**建议：是。** 它已是 Frozen Product Blueprint（第 149/153–160/175 行）与 Frozen Shell §3.1 的产品真相，RD 已实证；缺的只是「跨部门统一」的显式 Shared 表述（Gap A）。建议升级为 Company-wide 约束。

**Q2 — 应落在哪个现有 Frozen Authority？**
**Frozen Workspace Shell Contract（Layer 3 · Shared Company Patterns）**。具体：§3.1 强化 + §0.1 澄清（Delta-S1）、新增 Employee Detail 共享条目引用 T5（Delta-S2）、§3.12 补边界澄清（Delta-S3）。T5 升为被 Shell 引用的 Design Record（其语义已冻结于 `Curis_Company_OS_Shared_Authority.md` §1.2）。

**Q3 — 是否需要新的 Shared Pattern，还是现有规则最小补充即可？**
**现有规则最小补充即可，不需要全新 Shared Pattern，不创建 P8。** 缺口仅为「全局统一约束未显式化」「Detail 未收编进 Shell」「禁止项未升 Shared」三处小补强，均落在既有 Shell Layer 3，且 Detail 内容直接复用 T5，零重复定义。

**Q4 — 对上一轮 Pane Closure 会产生哪些必须修正的约束？**
见 §7 四条：① 规则升全局（RD 只是首例，Space Engineering 是变体）；② Detail 标注「Shared 待收编」；③ 禁止项改引 Frozen Shell；④ P-C Main 精确化为「跨经营型/建设型业务一致」。

---

## 9. 停止状态

```text
CURIS SHARED EMPLOYEE WORKSTATION PATTERN CLOSURE — APPROVED + DELTA-S1/S2/S3 已回写 Frozen Shell
→ 原则已确认：所有 AI Employee Workstation 统一 = Conversation-first（Main）
→ Review 通过；Delta-S1/S2/S3 已回写 Frozen Workspace Shell Contract（见 §10 Pointer）
→ 未创建 P8、未修改 P1–P7 语义、未改 Workspace Engineering 高保真、未写产品代码
```

---

## 10. 回写结果 · Change Log & Pointer（2026-08-16）

**批准**：Shared Employee Workstation Pattern Closure Review 通过，批准 Delta-S1 / S2 / S3。

**回写落点（Frozen Workspace Shell Contract · `docs/03_Design/Curis_Workspace_Shell_Contract_And_Shared_Patterns.md`）**：

| Delta | Shell 落点 | 内容 |
|---|---|---|
| **S1** | §0.1 边界修正 2 · Clarification + §3.1 · Global Shared Rule note | CEO 进入任意具体 AI Employee → Main 统一 Conversation-first Workstation；Workspace 默认 Main 可保持 Domain-specific 专业界面，但任何有 AI Employee 的 Workspace 必须支持进入该 Employee 的 Shared Workstation |
| **S2** | 新增 **§3.14 Employee Detail（Shared · Utility）** | Employee Detail 正式收编为 Shared Utility Pattern；引用 `Curis_Company_OS_Shared_Authority.md` §1.2 + T5，不重复定义；与 P2(Presence) / §3.1(Workstation) 构成三概念统一；§4 矩阵新增 Employee Detail 行 |
| **S3** | §3.12 边界澄清表 · 新增两行 | Employee Workstation / Conversation 禁止进入 Context Pane；禁止进入 Employee Detail / Utility Pane |
| 状态 | Status 头 + §7 新增 **Delta-X8** 回写记录 | 标注 2026-08-16 回写；注明不创建 P8、不修改 P1–P7 |

**Frozen 三概念（现已在 Shell 中完整锁定）**：
- **Employee Presence**（P2 · §3.8）= 员工入口（贴在业务对象，持续可感知）
- **Employee Workstation**（§3.1）= Main / Conversation-first
- **Employee Detail**（§3.14）= Utility / 这个员工是谁

**未改动**：Workspace Engineering 高保真 HTML（用户指令暂停）；P1–P7 既有语义；Product Blueprint；RD Instance；T5 内容（仅被引用）。

*本文件为 Curis Shared Employee Workstation Pattern Closure · 2026-08-16（APPROVED · Delta 已回写 Frozen Shell · 非视觉 / 非代码 / 非新架构 / 不创建 P8）*
