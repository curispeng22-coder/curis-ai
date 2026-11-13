# Curis · CEO Decision Pattern Review

> **类型**：独立产品设计专项（只研究 CEO Decision，不研究 Agent Computer Access）
> **输入真源**：`Curis_Workspace_Shell_Contract_And_Shared_Patterns.md`（Frozen · §3.3 Needs CEO / Decision、§3.12 边界、P4 Automation、P6 Result Reference）
> **参考实例**：RD Instance Spec §7（Banner 当前内容结构）、XHS Visual v4 状态 C（已较白话的示例）
> **目标**：把 Needs CEO 从「专业技术审批」升级为**普通 CEO 能理解的白话决策包**。
> **纪律**：本文件**不修改** Frozen Shared Pattern，也**不修改**任何 High-Fidelity 高保真。原提出的 Candidate Shared Pattern Delta（DP-CEO-1）已 FINAL REVIEW APPROVED 并回写为 Frozen §3.13 CEO Decision Package（P7）；本文件现为**研究记录 / Reference Only**，权威定义以 Frozen §3.13 为准。

**状态**：Reference Only — 研究记录，已回写为 Frozen §3.13 CEO Decision Package（P7）

---

## 1. 问题：当前 Needs CEO 仍是「技术审批」视角

Frozen §3.3 已定义 Needs CEO / Decision 是 **Workspace 级阻断性决策面**（橙色 Decision Banner，三动作：✓执行 / ⛔驳回 / 暂缓）。这解决了「在哪决策、谁决策」的问题，但**没解决「决策界面讲什么语言」**。

当前实例的实际写法仍是技术视角：

| 来源 | 当前 Decision 文案 | 问题 |
|------|-------------------|------|
| RD Instance §7 / HF 状态 `needs-ceo` | 「数据迁移 **ALTER TABLE** 操作需**主表执行权**，**不可逆**」 | 假定 CEO 懂 SQL / 数据库执行权 / 回滚窗口 |
| RD HF Banner | 「需要 CEO 决策 — 数据迁移 ALTER TABLE 操作需主表执行权，不可逆」 | 同上，且把「不可逆」当理由，CEO 不知不可逆对业务意味着什么 |
| XHS Visual v4 状态 C | 「文案含绝对化用语「最便宜」」 | ✅ 已是白话方向，但**尚未结构化**为统一决策包 |

这与产品铁律 **P4 · Automation by default / Human action only at Decision Gates** 冲突：决策闸本应让人类「很便宜地做判断」，现在却要求 CEO 先读懂技术语境才能决策——等于把技术债转嫁给人。

**结论**：Decision 主界面只讲 CEO 能理解的语言；专业证据通过 Result Reference / Utility 按需查看（P6）。

---

## 2. Pattern 结构：CEO Decision Package（8 要素是「必备语义」，不是「固定 UI 区块」）

每次 Needs CEO **必须**在语义上覆盖以下 8 个要素。前 6 个是「让 CEO 看懂」，第 7 个是「让 CEO 只做一件事」，第 8 个是「让 AI 自动继续」。

| # | 要素 | 内容 | 语言要求 |
|---|------|------|---------|
| 1 | **发生了什么** | 一句话业务事件（而非技术事件） | CEO 能懂；❌ 禁 SQL/CLI/Stack/API 原文 |
| 2 | **为什么 AI 不能自行决定** | 业务/合规/不可逆/范围原因 | 业务语言；❌ 只讲「后果」不讲「机制」 |
| 3 | **可选方案** | 2–4 个互斥方案 | 业务语言；❌ 方案名不加技术后缀 |
| 4 | **每个方案的业务影响 / 风险 / 代价** | 每方案三列 | 业务语言；⚠️ 仅代价可用极简术语（「需停机约 30 分钟」），且须带 Provenance |
| 5 | **Employee 推荐哪个方案** | 明确标注推荐项 | 直接 |
| 6 | **推荐理由** | 业务理由（非技术） | 业务语言；❌ |
| 7 | **CEO 只需要做出的选择** | 简化到 1 个动作族 | 极简 |
| 8 | **选择后 AI 如何自动继续** | 决策后自动流描述 | CEO 能懂；❌ |

> **关键修正（方向批准，本轮回写）**：8 要素是 **Decision Packet 的必备语义**，❌ **不等于** UI 必须固定展示 8 张卡 / 8 个标题。
>
> **原则：Low Surface Complexity, High Functional Density（低表面复杂度，高功能密度）。**
> - UI 必须允许按**复杂度压缩表达**：简单的决策用段落/紧凑行自然组合 8 要素；复杂的才展开为表格/分区。
> - Layer 1 应**优先自然、紧凑地组合** 8 要素（例如「发生了什么 + 为何你拍板」合并为一段导言；方案与影响/风险/代价合并为一张对比表；推荐+理由合并为一行；CEO 选择 + 自动继续各一行），**禁止为了满足规范机械堆 8 个区块**。
> - 语义覆盖可用清单/脚注/合并段落表达，不强制 1:1 标题映射。

**红线（不变）**：要素 1/2/5/6/7/8 主界面**不得出现** SQL / CLI / Stack / API / 内部架构原文。专业证据只进 **Layer 2（按需）**。

---

## 3. 信息层级（三层）+ Layer 0 动作规则

三层，注意力递减、专业度递增。CEO 默认只接触 Layer 0 + Layer 1；Layer 2 永远可选。

```
┌─────────────────────────────────────────────────────────────┐
│ Layer 0 · DECISION BANNER（Workspace 级，常驻顶部，Frozen §3.3）│
│   ⚠ 一句话「发生了什么」 + 复杂度感知动作 + 展开详情            │
│   —— 仅承载注意力 + 动作，不承载理解                               │
└─────────────────────────────────────────────────────────────┘
                            ↓ 展开详情
┌─────────────────────────────────────────────────────────────┐
│ Layer 1 · PLAIN DECISION PACKAGE（8 要素，CEO 语言，紧凑组合）  │
│   导言(1+2) / 方案×影响风险代价表(3+4，带 Provenance)           │
│   / 推荐+理由(5+6) / CEO选择(7) / 自动继续(8)                   │
│   —— 让 CEO 在不看任何技术细节下做出判断                          │
└─────────────────────────────────────────────────────────────┘
                            ↓ （最底部，默认收起）
┌─────────────────────────────────────────────────────────────┐
│ Layer 2 · PROFESSIONAL EVIDENCE（按需，P6 Result Reference）    │
│   「查看技术证据 ▸」→ Source / Diff / Preview / Test / Logs     │
│   —— 只给想核实的技术决策者；CEO 可完全不看                       │
└─────────────────────────────────────────────────────────────┘
```

### 3.1 Layer 0 动作规则（Complexity-aware · 本次修正）

> **关键修正（方向批准，本轮回写）**：❌ **不冻结**「所有 Decision Banner 都直接显示 `[批准推荐] [驳回] [暂缓]`」。改为**复杂度感知**。

| 复杂度 | 判定信号 | Banner 显示动作 | CEO 可否 Layer 0 直接决策 |
|--------|---------|----------------|--------------------------|
| **简单 · 低歧义 · 影响明确** | 单推荐路径、无业务取舍、风险低 | `[按建议处理] [其他方案] [暂缓]` | ✅ 可以 |
| **有业务取舍 / 高风险 / 不可逆** | 多方案各有损益、不可逆、影响范围不确定 | `[查看方案] [暂缓]` | ❌ 必须进 Layer 1 看清方案/影响/推荐后再执行具体 Choice |
| **高风险 / 不可逆专项** | 不可逆对外变更、涉及资金/合规 | **禁止** Layer 0 一句话直接批准 | ❌ 强制走 `[查看方案]` → Layer 1 → CEO Choice |

- **简单类**（如 XHS 改合规标题）：推荐路径清晰、风险低，CEO 可在 Layer 0 直接 `[按建议处理]`。
- **高风险/不可逆类**（如 RD 数据迁移）：Banner **只负责提醒**，`[查看方案] [暂缓]`；进入 Layer 1 看清方案、影响、推荐理由后，才出现具体 `[批准推荐] / [选其他] / [驳回]` 等 Choice。**严禁仅凭 Layer 0 一句话批准不可逆操作**。

**映射 Frozen**：
- Layer 0 = §3.3 Decision Banner（橙色 `--ui-warning` 横幅，Workspace 级）
- Layer 1 = 本 Pattern 新增的「内容结构」层（不修改 §3.3 定义，只扩展其 Banner 描述）
- Layer 2 = P6 Result Reference（对话/决策内仅放引用行，完整证据按需查看）+ RD Utility（Source/Diff/Preview）

---

## 4. Decision Provenance / Confidence 硬约束（本次新增）

Decision Package 中以下字段**必须可追溯来源**，禁止「为了让决策看起来完整」而编造：

**必须带 Provenance 的字段**：Impact（影响）、Risk（风险）、Cost（代价）、Recommendation（推荐）、Recommendation Reason（推荐理由）。

**来源类型（至少区分以下五类）**：

| 标记 | 含义 | 示例 |
|------|------|------|
| `(FACT)` | 已验证客观事实（系统/数据可查） | 「结构已就绪」「你承担合规责任」 |
| `(POLICY)` | 平台/公司明文规则 | 「绝对化用语违反平台规范」「灰度即小流量验证」 |
| `(EVIDENCE→L2)` | 具体可查证据，指向 Layer 2 技术/业务详情 | 「切换脚本已通过测试（报告见技术证据）」 |
| `(EST)` | **Employee Estimate** — 员工基于经验的判断，**非事实** | 「约停服 30 分钟」「上线延后 1–2 天」 |
| `(UNK)` | 尚未验证 / 未知 | 「影响全体用户的概率未做全量演练，未知」 |

**硬约束（强制）**：
1. Impact / Risk / Cost / Recommendation / Recommendation Reason **每个断言都须带 Provenance 标记**。
2. **禁止编造**：时间、成本、风险概率、业务影响、流量变化等数字/结论，无依据不得填写。
3. 不知道 → **显式 `(UNK) 尚未验证`**，不得留空暗示「已知」或填一个看似合理的数。
4. `(EST)` **必须让用户知道这是员工判断**，不得伪装成 `(FACT)` 或 `(EVIDENCE)`。
5. 专业来源仍走 Layer 2 按需查看，**不要求 CEO 默认阅读技术证据**；Provenance 标记本身用 CEO 语言（如「员工估算」「尚未验证」），不暴露内部术语。

> 该约束只新增「内容可信度层」，不修改 §2 的 8 要素语义，也不修改 Frozen §3.3 / §3.12。

---

## 5. RD 示例（含 Provenance 修正）

### 5.1 Before（当前技术视角 · 不推荐）
> Banner：「需要 CEO 决策 — 数据迁移 **ALTER TABLE** 操作需**主表执行权**，**不可逆**」

问题：CEO 必须懂「ALTER TABLE / 主表执行权 / 不可逆」才能判断。

### 5.2 After（CEO Decision Package · 紧凑 Layer 1 + Provenance）

**Layer 0（不可逆类 → 仅提醒）**
> ⚠ 用户数据搬家最后一步需要你拍板（会改动线上结构、不可直接回退）　`[查看方案] [暂缓]`

**Layer 1（展开后 · 8 要素紧凑组合）**

> **发生了什么 + 为何你拍板**：用户数据从旧库搬到新库已准备就绪，但最后一步「真正切换」会改动线上用户表结构（POLICY：不可逆对外变更），按规则必须由你确认（POLICY：Decision Authority）。
>
> **方案与影响 / 风险 / 代价**（每个断言带来源）
>
> | 方案 | 业务影响 | 风险 | 代价 |
> |------|---------|------|------|
> | A 现在执行（推荐） | 用户立即用上新结构（FACT：结构已就绪） | 若切换异常，影响全体线上用户（EST：影响范围与概率未知，未做全量故障演练） | 需停服约 30 分钟（EST） |
> | B 今晚低峰（02:00）执行 | 几乎无感切换（EST） | 异常影响极小（EST） | 等待至 02:00（FACT：时间确定） |
> | C 先灰度验证 | 最稳妥，小流量验证后全量（POLICY：灰度机制） | 极低（POLICY） | 上线延后 1–2 天（EST） |
>
> **推荐 + 理由**：推荐 **方案 A**——切换脚本已通过审核与测试（EVIDENCE→L2：测试报告），且当前为低流量时段。⚠ 但「当前低流量」是员工估算（EST：基于时段经验，未实时核验流量）；若你对该判断不确定，**方案 B 更稳妥**。
>
> **CEO 只需选**：`[批准现在执行] [改选 B 今晚] [改选 C 灰度] [驳回维持旧库] [暂缓]`
>
> **选择后 AI 自动继续**：批准后 AI 自动执行切换并持续监控（EVIDENCE→L2：执行日志），后续发布与数据观测自动进行，无需你再操作；若选驳回，AI 保留旧库并通知相关员工。

> 注：迁移脚本 `migration/users_2026.sql`、Diff、压测结果全部进入 Layer 2「查看技术证据 ▸」，主界面不出现。原示例中的「P95 120ms」「127/127 测试通过」等若无可查证据，不得作为 FACT 填入——此处以 `(EVIDENCE→L2)` 引用，具体数字留在 Layer 2 由技术证据支撑。

---

## 6. XHS 示例（含 Provenance 修正）

XHS Visual v4 状态 C 已接近白话方向（「文案含绝对化用语「最便宜」」），下面把它**结构化**为统一的 Decision Package，验证 Pattern 跨 Workspace 通用，并演示「简单类可在 Layer 0 直接决策」。

### 6.1 After（CEO Decision Package）

**Layer 0（简单 · 低风险推荐路径 → 可直接决策）**
> ⚠ 笔记标题用了「最便宜」这种绝对化用语，发布前需你确认　`[按建议处理] [其他方案] [暂缓]`

**Layer 1（展开后 · 8 要素紧凑组合）**

> **发生了什么 + 为何你拍板**：笔记《夏日通勤穿搭合集》已写好，AI 审核发现标题用了「最便宜」这类绝对化用语（FACT：AI 检出；POLICY：违反平台内容规范），发布前需你做品牌合规授权（POLICY：Decision Authority）。
>
> **方案与影响 / 风险 / 代价**
>
> | 方案 | 业务影响 | 风险 | 代价 |
> |------|---------|------|------|
> | A 批准原标题（你担责） | 按时发布，标题更吸睛（EST：吸睛收益未量化） | 若平台收紧，判违规下架（POLICY：平台规则；EST：判罚概率未知） | 你承担合规责任（FACT） |
> | B 改合规标题后发布（推荐） | 安全发布（POLICY） | 极低（POLICY） | 重写 1 个标题约 1 分钟（EST） |
> | C 驳回打回重写 | 最稳妥（POLICY） | 无（FACT） | 延后发布约半天（EST） |
>
> **推荐 + 理由**：推荐 **方案 B**——原标题吸睛收益有限（EST），而违规下架会中断笔记流量积累（POLICY：平台降权规则；EST：流量损失未量化）；改标题几乎无成本（EST）。
>
> **CEO 只需选**：`[按建议改标题发布] [A 坚持原标题(我担责)] [C 驳回重写] [暂缓]`
>
> **选择后 AI 自动继续**：选定后 AI 自动改标题（或保留）/ 发布，并进入数据观测闭环，无需你再操作。

> 注：命中词高亮、审核员王芳的判断过程、笔记正文预览进入 Layer 2「查看审核详情 ▸」。

---

## 7. Decision Banner → 展开详情 交互建议

### 7.1 Banner 本身（Layer 0，极简 · 复杂度感知）
- 位置：Main Pane Content 顶部（Frozen §3.3，橙色 `--ui-warning` 横幅），**不横跨** Context/Utility。
- 内容**只**有：⚠ 图标 + 一句话「发生了什么」（要素 1 的极简版）+ **复杂度感知动作**（见 §3.1）+ 一个 `展开详情 ▾` 链接。
- **不**在横幅里放影响范围/风险评估/技术描述（那些进 Layer 1/2）。
- 多 Responsibility 待决策时：每个 Responsibility 一个独立 Package；横幅可逐条出现，或与员工卡 `needs_ceo` 状态分离呈现（Frozen 修正 2）。

### 7.2 展开详情（Layer 1 + 2）
- 触发：`展开详情` 或点击横幅主体 → 内联展开面板（或 Overlay，与 Utility Maximize 同族 overlay 行为，**不新造 Shell 区域**）。
- 展开后**先显示 Plain Decision Package（8 要素紧凑组合）**，用业务语言，CEO 无需滚动即可决策；高风险/不可逆类此时才出现具体 `[批准推荐] / [选其他] / [驳回]` Choice（见 §3.1）。
- **技术证据放在最底部一个默认收起的「查看技术证据 ▸」区**（Layer 2），点击才展开 Source/Diff/Preview/Test/Logs（P6 Result Reference + RD Utility）。
- CEO 在 Layer 1 直接点动作之一即可完成决策；Layer 2 是给想核实的技术决策者（或 CEO 自己好奇）的可选项。

### 7.3 决策后
- CEO 动作后 → 横幅消失 / 转为「已批准·自动继续中」轻量状态；AI 按要素 8 自动继续（P4 Automation）。
- 不新建对话、不新建 Handoff（重申 **CEO Decision ≠ Handoff**，Frozen §3.12）。

---

## 8. Candidate Shared Pattern Delta

> **状态：APPROVED CANDIDATE（方向批准，待 FINAL REVIEW 后回写 Frozen）**。本 Delta 提议新增一个 Shared Pattern。

### DP-CEO-1：CEO Decision Package Pattern（Candidate）

- **定位**：建立在 Frozen §3.3（Needs CEO / Decision）之上，**补充其「内容结构」层**——§3.3 解决了「在哪/谁决策」，本 Pattern 解决「决策界面讲什么、怎么讲」。
- **8 要素语义（非 UI 区块）**：每次 Needs CEO 必须语义覆盖 §2 的 8 要素；UI 按复杂度压缩表达（Low Surface Complexity, High Functional Density），禁止机械堆 8 卡。
- **信息层级**：Layer 0 Decision Banner（注意力+复杂度感知动作）/ Layer 1 Plain Package（8 要素紧凑组合，CEO 语言）/ Layer 2 Professional Evidence（P6 Result Reference 按需）。
- **Layer 0 复杂度感知动作**：简单低歧义类 → `[按建议处理][其他方案][暂缓]`；有取舍/高风险/不可逆类 → `[查看方案][暂缓]`，禁止 Layer 0 直接批准不可逆操作。
- **Provenance / Confidence 硬约束**：Impact / Risk / Cost / Recommendation / Recommendation Reason 须带来源标记（FACT / POLICY / EVIDENCE→L2 / EST / UNK）；禁止编造，未知显式 `(UNK) 尚未验证`，`(EST)` 须明示为员工判断。
- **依赖的 Frozen 能力**：
  - P4 Automation by default / Human action only at Decision Gates（决策闸是人类唯一必要动作）
  - P6 Result Reference（专业证据通道，对话/决策内仅引用行）
  - §3.3 Needs CEO / Decision（Workspace 级横幅）
  - §3.12 边界：**CEO Decision ≠ Handoff**（本 Pattern 重申：决策后 AI 自动继续，不产生责任交接）
- **不修改**：Frozen §3.3 定义、§3.12 边界、P4/P6 内容；本 Candidate 只扩展 Banner 的描述从「标题+描述+元信息」细化为「8 要素白话包 + 分层证据 + Provenance」。
- **跨 Workspace 通用**：RD（数据迁移·不可逆类）、XHS（合规审核·简单类）、抖音（投放预算）、会议（方向确认）均复用同一结构与 Provenance 规则，仅领域内容不同。

### 红线（Candidate 内强制）
1. Decision 主界面不得出现专业技术细节原文。
2. 专业证据只能通过 Layer 2（Result Reference / Utility）按需查看。
3. CEO 决策后 AI 自动继续，不新建 Handoff、不新建对话。
4. Impact/Risk/Cost/Recommendation/Reason 必须带 Provenance；禁止编造，未知显式 `(UNK)`。

---

## 9. 与 Frozen 边界确认

| Frozen 条目 | 本 Review 的处理 |
|------------|----------------|
| §3.3 Needs CEO / Decision | **不修改定义**；仅补充内容结构（8 要素语义 + 分层证据 + Provenance）作为 Candidate |
| §3.12 CEO Decision ≠ Handoff | **重申并强化**：决策后自动继续，非责任交接 |
| P4 Automation by default | 作为 Pattern 的底层原则被引用 |
| P6 Result Reference | 作为 Layer 2 证据通道被引用 |
| Shell Contract / 高保真 | **未修改**；本文件为独立研究交付 |

**下一步**：若 FINAL REVIEW 批准 DP-CEO-1，再将其回写为 Frozen §3 新小节（如 §3.13 CEO Decision Package），并同步更新 RD / XHS Instance Spec 的 Decision Banner 描述与 High-Fidelity 文案（届时另开任务，不在本文件内）。

---

**UI Designer**：UiDesigner
**日期**：2026-08-15
**状态**：Reference Only — 研究记录，已回写为 Frozen §3.13 CEO Decision Package（P7）