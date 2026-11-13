# Batch C — Contract Review（Content Production × Channel Ops 落点 + Runtime Observation）

> **状态**：**APPROVED CANDIDATE**（Batch C；已应用 DELTA C1 + DELTA C2；仍不 Frozen）
> **范围**：契约 ⑤ Content Variant / Publication · 契约 ⑨ Lightweight Queue / Bottleneck Candidate
> **本轮修订**：**DELTA C1** — Publication 必须服从 Distribution Execution Policy（区分 FACT CONSISTENCY / FUTURE EXECUTION POLICY，Policy 唯一定义在契约 ④）；**DELTA C2** — Bottleneck ≠ 一定缺员工（possible_cause 可 UNKNOWN、suggested_action 4 个最小候选、禁止编造原因、CEO 侧不暴露工程指标）
> **纪律**：不 Frozen / 不改 Product Blueprint / 不改 P1–P7 / 不改 XHS·RD Instance / 不开发 Runtime / 不开发 Connector / 不画 UI
> **前置**：Batch A（① Office / ② Channel·Account / ③ Intent / ④ Target Account，均 APPROVED CANDIDATE）、Batch B（⑥ Responsibility Requirement / ⑧ Shared Employee Service Relation / ⑦ Organization Routing，均 APPROVED CANDIDATE）、`Curis_Organization_Routing_Architecture.md`（H/I/§6 DELTA 3）、`Curis_Content_Growth_Company_Evolution_Model.md`（§5）、`Curis_Workspace_Shell_Contract_And_Shared_Patterns.md`（P1/P7 Frozen）

---

## 0. 本轮交付清单

| 文件 | 契约 | 归属层 |
|------|------|--------|
| `Curis_Content_Variant_Publication_Contract_Candidate.md` | ⑤ Content Variant / Publication | Content Growth Domain（Variant/Publication 记录）；执行 → Capability·Connector（仅引用） |
| `Curis_Lightweight_Queue_Bottleneck_Contract_Candidate.md` | ⑨ Lightweight Queue / Bottleneck Candidate | Company OS Shared（运行层观测，跨域） |
| （本文件） | Batch C Review | — |

---

## 1. 两个契约之间的关系与上游链路

```
Content Intent ③
  → Target Account Set ④        （选账号子集 + production_requirements
                                  + distribution_execution_policy ← 唯一定义方）
      → Content Variant ⑤        （每选中账号一份，账号级适配；reuse_mode HIGH_REUSE/FULL_DIVERGENCE）
          → Publication ⑤        （per-Account 真相源：状态/回执/时间；执行经 Connector）
              │  FACT CONSISTENCY：已发生事实不回滚（Invariant #1）
              │  FUTURE EXECUTION：尚未执行部分是否继续 → 读 ④ Policy（Invariant #5/#6 · DELTA C1）
              → Engagement / Analytics（per-Account，未来 Batch，非本轮）

Organization Routing ⑦ → Employee ⑧ 执行各 Responsibility ⑥
  → Runtime Fact ⑨              （per Responsibility 观测：queue_depth/oldest_wait/active_count/availability）
      → Bottleneck Candidate ⑨  （阈值越界 → 只主张「可能持续阻塞」· DELTA C2）
              signal / observed_since / affected_responsibility
              possible_cause（含 UNKNOWN，禁止编造）
              suggested_action ∈ {WAIT_AND_OBSERVE, REBALANCE_EXISTING,
                                  ADD_EMPLOYEE, ESCALATE_FOR_DIAGNOSIS}
          → CEO Assistant 白话二选一（Frozen P7）→ [按建议处理]/[其他方案]
              （CEO 不可见 queue_depth/oldest_wait/capacity/routing/score/枚举名）
```

**依赖顺序（本 Batch 内部）**：
- ⑤ Content Variant/Publication 是 Batch A ④ Target Account Set 的**下游落点**，消费 ③ Intent + ② Channel Account + ④ `distribution_execution_policy`（**只读，不重定义** · DELTA C1），执行经 Capability·Connector。
- ⑨ Lightweight Queue/Bottleneck 是运行层**观测**，依赖 ⑥ Responsibility + ⑧ Employee availability，感知 ⑦ Routing（不改），建议投递 P7；`REBALANCE_EXISTING` 被接受时仅调整 ⑧ Assignment（不新建 Employee）。
- 二者相对独立：⑤ 在内容生产/发布主轴，⑨ 在运行观测轴；共同闭合「内容从 Intent 到 per-Account 发布」+「组织负载自管」两条线。

**至此 9 契约全部达到 APPROVED CANDIDATE**：① ② ③ ④（Batch A）、⑥ ⑧ ⑦（Batch B，含 DELTA B1）、⑤ ⑨（Batch C，含 DELTA C1/C2）。**均未 Frozen。**

---

## 1b. 本轮 DELTA 落地记录

### DELTA C1 — Publication 必须服从 Distribution Execution Policy

| 关注点 | 落地位置（契约 ⑤） |
|--------|------------------|
| 区分 FACT CONSISTENCY / FUTURE EXECUTION POLICY | §0 核心纠正第 2 条 + Publication Invariant #1（事实不回滚）与 #5（后续执行服从 Policy） |
| 不重定义第二套 Policy | Publication Invariant #6（语义/默认/覆盖**唯一归属契约 ④**，本契约只读服从） |
| 只读追溯字段 | Publication Composition 新增 `applied_execution_policy_ref?`（只读引用快照，不定义语义） |
| Policy 未知时的行为 | Failure/Unknown：不猜测 → 取 ④ Office 默认 → 仍无法解析则暂停并升级（**不默认全量继续发布**） |
| 场景验证 | CASE C2 改为显式 `BEST_EFFORT`；新增 **CASE C7（ALL_REQUIRED）**：已发生的抖音 PUBLISHED 不回滚，尚未执行的 XHS 暂停 |

**语义澄清（本轮最重要一条）**：
> 「一账号失败不回滚其他」= **已经发生的 Publication 事实不被篡改**。
> 它 **不等于** 「无论业务意图如何，其他账号永远继续发布」。
> 尚未执行的部分是否继续，**只能**由契约 ④ `distribution_execution_policy` 决定。

### DELTA C2 — Bottleneck ≠ 一定缺员工

| 关注点 | 落地位置（契约 ⑨） |
|--------|------------------|
| 只能主张「可能持续阻塞」 | §2 Object semantics 改写 + Invariant #2（`ADD_EMPLOYEE` 不再是唯一/默认动作） |
| 保留最小字段 | Composition：`signal` / `observed_since` / `affected_responsibility` / `possible_cause` / `suggested_action` |
| 可能原因枚举（含 UNKNOWN） | `EMPLOYEE_CAPACITY` / `SHORT_TERM_SPIKE` / `TOOL_OR_CAPABILITY_UNAVAILABLE` / `EXTERNAL_DEPENDENCY` / `PRIORITY_CONFLICT` / `TASK_COMPLEXITY` / `NO_ELIGIBLE_EXECUTOR` / `UNKNOWN` |
| 4 个最小动作候选 | `WAIT_AND_OBSERVE` / `REBALANCE_EXISTING` / `ADD_EMPLOYEE` / `ESCALATE_FOR_DIAGNOSIS` |
| 禁止 AI 编造原因 | Invariant #7（事实不足**必须** UNKNOWN + ESCALATE_FOR_DIAGNOSIS 或 WAIT_AND_OBSERVE；禁自由文本归因） |
| 不建诊断引擎 | Invariant #8 + §5 明确不做（❌ 根因分析 / 依赖图推理 / 归因模型） |
| CEO 侧保持简单 | Invariant #9 + **新增 §2b 用户侧表达边界**（CEO 不可见 queue_depth/oldest_wait/capacity/routing/score/枚举名；只给白话 + 二选一，沿用 **Frozen P7**） |
| 场景验证 | CASE C4（证据不足→先观察）/ C4b（证据充分→增员）/ C4c（工具不可用→升级诊断，**不建议加人**）/ C4d（可再平衡→仅调 ⑧ Assignment） |

---

## 2. Unresolved Questions（待 Review 裁定）

1. **`scheduled_at` 平台支持度清单（POLICY VERIFICATION REQUIRED）**
   - 已知：YouTube `publishAt` ✅；抖音官方 API ❌（未知/不支持）；其余平台待官方文档核实。
   - 待裁定：各平台 scheduling 支持度表以**官方 open 文档**确认后，才写入任何 Frozen Product Rule；本轮只声明「条件化」不写死强规则。

2. **同一 Variant 多次 Publication 的语义**
   - 本契约已允许（重发/多版本），每次 per-Account 独立真相。
   - 待裁定：重发是否需用户显式确认（Decision Gate）还是自动化默认（P4）？建议：首次发布后重发属普通操作，可由自动化默认；但跨长期/重大改版重发建议轻量确认。留 Frozen 裁定。

3. **Bottleneck 阈值（静态 vs 自适应）**
   - DELTA 3 已定首版静态规则（简单常量）。
   - 待裁定：阈值常量取值（如 oldest_wait 多少分钟算越界）；自适应基线留未来 Batch。

4. **用户选择「其他方案」后的长期行为**
   - 本契约已定：非破坏式（不自动降级/不丢队列），可再检测。
   - 待裁定：持续越界是否需升级至 CEO Decision Package（P7）正式决策，还是仅周期性再建议？建议周期性再建议即可，不强制升级。

5. **`possible_cause` 的填充规则边界（DELTA C2 新增）**
   - 已定：只允许**简单事实规则**填充（如「Tool 调用连续失败 → TOOL_OR_CAPABILITY_UNAVAILABLE」「同责任存在未满负荷 Employee → PRIORITY_CONFLICT」），事实不足取 UNKNOWN。
   - 待裁定：每个枚举值对应的**最小事实条件清单**（首版可以极少，甚至只保留 UNKNOWN + EMPLOYEE_CAPACITY 两条规则）。**不得**为凑满枚举而引入推断逻辑。

6. **`observed_since` 的「持续」判定窗口（DELTA C2 新增）**
   - 已定：`observed_since` 用于区分「短期峰值」与「持续阻塞」。
   - 待裁定：多长时间算「持续」（首版建议静态常量，与 §2 #3 阈值一并裁定）。

---

## 3. 是否出现新 Primitive（与 Frozen 兼容检查）

**结论**：引入了**业务/运行层对象**，与 Frozen P1–P7 **兼容、不修改**。

新增对象：
- `Content Variant` / `Publication`（CG Domain 业务对象 / per-Account 记录）
- `Runtime Fact` / `Bottleneck Candidate`（Company OS Shared 运行观测，跨域）

**它们不是**：
- 新的 Shell 原语（Pane/Search/Toggle 不变）
- 对 P1–P7 的修改 —— P1 三层语义、P4 自动化默认、P7 CEO Decision Package 全部原样保留；Publication 是业务记录，Bottleneck 建议投递 P7 二选一，不改既定义。
- 新的 Organization 原语 —— ⑨ 观测既有的 ⑥/⑧，不新增组织节点。
- **第 10 个正式 Contract** —— Context Assembly（Batch B DELTA B1 记为 Future Company OS Shared Candidate）**不在本轮新建**；本 Batch 仍只 ⑤ + ⑨ 两份契约。

> 即：⑤ 是 Batch A 上游链的下游落点（把「选哪些账号」变成「每账号一份变体 + 每账号一份发布真相」）；⑨ 把 Company Evolution Model §5 / Routing §6 的「Runtime Facts → Bottleneck → 一键增员」固化为观测契约。二者均叠加在既有 Frozen Shared Pattern 之上。

---

## 4. 与现有 Blueprint / P1–P7 的冲突检查

| 权威文档 | 冲突？ | 说明 |
|----------|:------:|------|
| **P1 三层责任语义** | 无 | Publication / Variant 是业务对象记录，不涉及责任语义；Bottleneck 不改责任定义。 |
| **P2 Employee Presence** | 无 | 员工在执行变体/发布时的 Presence 仍由 P2 表达；本 Batch 不改。 |
| **P3 System Activity** | 无 | Publication 发布后自动 Analytics 属 System Activity；Runtime Fact 是观测快照，性质接近 P3 派生。 |
| **P4 Automation by default** | 无 | 变体生产/发布自动发生；仅 Decision Gate（如重大重发确认）需人介入，符合 P4。 |
| **P5 Handoff** | 无 | 责任交接在 Employee 层，与变体/发布对象无关。 |
| **P6 Result Reference** | 无 | Publication `publish_receipt` 是结果引用，与 P6 一致。 |
| **P7 CEO Decision Package** | 无 | Bottleneck 建议以 P7 风格二选一投递（[按建议处理]/[其他方案]）；§2b 用户侧表达边界**沿用** P7 语义，**不新增决策模式、不修改 P7**（DELTA C2）。 |
| **Product Blueprint** | 无 | Variant/Publication 是 Content Growth 业务对象；Bottleneck 是运行观测；均不改 Blueprint。 |

**结论**：Batch C 两个契约**不修改、不冲突**任何 Frozen 文档。

---

## 5. 对 XHS / RD 当前实现的影响

**结论**：**ADDITIVE，非破坏性**。当前 XHS / RD Instance（APPROVED）不变。

- 当前 XHS Instance = 单 Office·单 XHS 账号退化形态；其发布在该模型下退化为一 Variant + 一 Publication（per-Account）。新模型支持其未来扩展为多账号/多 Variant 发布，**不改变已 Approved 的 Calendar/Note/Analytics 专业能力**。
- 当前 RD Instance 同理；其专业化生产/发布在未来可接入本 Batch 的 Variant/Publication 契约，不改动既有专业能力。
- ⑨ Bottleneck 对当前单 Employee 实例基本无触发（无队列），但机制可透明存在；未来多 Employee/Team 时自然生效。

---

## 6. 场景验证覆盖（含 DELTA C1/C2 新增场景）

| 场景 | 验证的契约 | 结论 |
|------|-----------|------|
| CASE C1 同 Intent→N 账号级 Variant | ⑤ | Intent #101 选 3 账号→3 Variant，各绑单一账号，reuse_mode 各异 ✅ |
| CASE C2 Publication per-Account 真相（BEST_EFFORT） | ⑤ + ④ | 抖音/XHS 成功、B站 BLOCKED → 各自独立真相；Policy=BEST_EFFORT 其余继续 ✅ |
| **CASE C7 ALL_REQUIRED（DELTA C1 新增）** | ⑤ + ④ | 抖音已 PUBLISHED **不回滚**；B站 BLOCKED → **XHS 尚未执行部分暂停**并升级；白话「这次要求三平台同步，已暂停后续发布」✅ |
| CASE C3 scheduling 条件化 | ⑤ | YouTube 可定时、抖音官方 API 不支持→置空，POLICY VERIFICATION REQUIRED ✅ |
| **CASE C4 证据不足→先观察（DELTA C2 修正）** | ⑨ + P7 | observed_since 仅 1 天 → possible_cause=UNKNOWN、action=WAIT_AND_OBSERVE；白话含不确定性表达 ✅ |
| **CASE C4b 证据充分→增员（DELTA C2）** | ⑨ + ⑥ + ⑧ | 持续一周积压 + 长期满负荷 → EMPLOYEE_CAPACITY / ADD_EMPLOYEE → 二选一增员闭环 ✅ |
| **CASE C4c 工具不可用→升级诊断（DELTA C2）** | ⑨ | Tool 连续失败 → TOOL_OR_CAPABILITY_UNAVAILABLE / ESCALATE_FOR_DIAGNOSIS，**不建议加人** ✅ |
| **CASE C4d 可再平衡（DELTA C2）** | ⑨ + ⑧ | 同责任有未满负荷 Employee → PRIORITY_CONFLICT / REBALANCE_EXISTING；仅调 ⑧ Assignment，不新建 Employee ✅ |
| CASE C5 拒绝非破坏 | ⑨ | 用户 [其他方案]→关闭候选、不丢队列、可再检测 ✅ |
| CASE C6 per-Responsibility 跨 Office 聚合 | ⑨ + ⑧ | 字幕责任服务 3 Office→Fact 聚合、瓶颈对责任整体建议一次 ✅ |

**三条主线校验**：
- 「Intent → Target Account → 每账号 Variant → per-Account Publication 真相」闭环稳定（⑤ + ③④②）✅
- 「事实一致性 vs 后续执行策略」严格分离，Policy 单一定义方（⑤ 只读 ④）✅ **DELTA C1**
- 「Responsibility 执行 → Runtime Fact 观测 → Bottleneck 候选（可 UNKNOWN）→ 白话二选一」自管闭环稳定，且**不误判为缺员工**（⑨ + ⑥⑧⑦ + P7）✅ **DELTA C2**

---

## 7. 状态与下一步

**当前状态**：`CONTENT GROWTH CONTRACT BATCH C — APPROVED CANDIDATE`（DELTA C1 + C2 已应用；**仍未 Frozen**）

### 9 契约状态总表

| Batch | 契约 | 状态 | 已应用 DELTA |
|-------|------|------|--------------|
| A | ① Office（Operating Context = RESERVED） | APPROVED CANDIDATE | A3 |
| A | ② Channel / Channel Account / Account Pool | APPROVED CANDIDATE | — |
| A | ③ Content Opportunity / Intent | APPROVED CANDIDATE | — |
| A | ④ Target Account Set（+ Eligibility / Distribution Execution Policy） | APPROVED CANDIDATE | A1 / A2 |
| B | ⑥ Responsibility Requirement | APPROVED CANDIDATE | B1 |
| B | ⑧ Shared Employee Service Relation | APPROVED CANDIDATE | B1 |
| B | ⑦ Organization Routing | APPROVED CANDIDATE | B1 |
| C | ⑤ Content Variant / Publication | APPROVED CANDIDATE | **C1** |
| C | ⑨ Lightweight Queue / Bottleneck Candidate | APPROVED CANDIDATE | **C2** |

**保留候选（不新建正式契约）**：
- **Context Assembly = Future Company OS Shared Candidate**（Batch B DELTA B1 记录）—— **不建第 10 个契约**。
- **Operating Context = RESERVED / DEFERRED CANDIDATE**（Batch A DELTA A3）—— 未来优先对齐 Blueprint Business / 业务空间。

### 下一步（明确不做的事）
1. **不立即 Frozen**、**不立即起草最终权威 Contract Set** —— 归并需先经 **Authority Consolidation Review**。
2. 归并前需闭合的关键 Unresolved：§2 #1（平台 scheduling 官方核实）、#3/#6（阈值与持续窗口常量）、#5（possible_cause 最小事实规则）。
3. 仍**只做契约设计**：不开发 Runtime / Connector、不画 UI、不进 DB/SQL/API/前端。

*本文件为 APPROVED CANDIDATE，**未 Frozen**。Frozen 与归并需待 Authority Consolidation Review。*

---

*CONTENT GROWTH CONTRACT DESIGN COMPLETE · 9 CONTRACTS APPROVED CANDIDATE · AUTHORITY CONSOLIDATION REVIEW REQUIRED*
