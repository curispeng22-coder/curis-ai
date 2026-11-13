# Batch A — Contract Review（Operating Foundation）

> **状态**：APPROVED CANDIDATE（Batch A — 经 DELTA A1 / A2 / A3 修正，未 Frozen）
> **范围**：契约 ① Office（直接挂 Company；Operating Context → RESERVED/DEFERRED） · ② Channel/Channel Account/Account Pool · ③ Content Opportunity/Intent · ④ Target Account（含 Eligibility 分离 + Distribution Execution Policy）
> **纪律**：不 Frozen / 不改 Product Blueprint / 不改 P1–P7 / 不改 XHS·RD Instance / 不开发 Runtime / 不开发 Connector / 不画 UI

---

## 0. 本轮交付清单

| 文件 | 契约 | 归属层 |
|------|------|--------|
| `Curis_Operating_Context_Office_Contract_Candidate.md` | ① Office（Operating Context → RESERVED/DEFERRED） | Office=CG Domain，直接挂 Company；Operating Context=RESERVED/DEFERRED CANDIDATE（不升 OS Shared） |
| `Curis_Channel_Account_Contract_Candidate.md` | ② Channel / Channel Account / Account Pool | Content Growth Domain |
| `Curis_Content_Intent_Contract_Candidate.md` | ③ Content Opportunity / Intent | Content Growth Domain |
| `Curis_Target_Account_Contract_Candidate.md` | ④ Target Account | Content Growth Domain |
| （本文件） | Batch A Review | — |

---

## 1. 四个契约之间的关系

```
Company
  ├─ Office (CG Domain) 1—* 直接挂 Company   [契约① · DELTA A3：删除 Operating Context 层]
  │        │  *—* Channel Account (CG Domain) 经 OfficeAccountBinding [契约②]
  │        │        └─ Channel Account 属 Channel (事实层) [契约②]
  │        └─ Office.default_target_account_set (引用 Account Pool 子集)
  │
  ├─ Content Opportunity (CG Domain) → 转化 → Content Intent (CG Domain) [契约③]
  │        └─ Intent *—* Office (弱服务链接，非所有权) [契约①③]
  │
  └─ Content Intent 1—* Target Account Set (CG Domain) [契约④]
           └─ selected_accounts[] 取自 相关 Office 的 Account Pool [契约②④]
           └─ Account Eligibility（运行期派生，非持久对象）+ Distribution Execution Policy [契约④ · DELTA A2]
                  └─ → 驱动 Content Variant / Publication (契约⑤，后续 Batch)

派生：Account Pool = Office 下 ACTIVE OfficeAccountBinding 指向的 Channel Account 全集 [契约②]
RESERVED/DEFERRED：Operating Context 本轮不升 OS Shared Primitive；未来上层 Business Context 优先对齐 Blueprint Business/业务空间 [契约① · DELTA A3]
```

**依赖顺序**（本 Batch 内部）：
- ① Office 是基础（经营单元）。
- ② Channel/Account 是「在哪里经营」的载体，经 Binding 服务于 Office。
- ③ Intent 是跨账号共享上游对象，弱链接 Office。
- ④ Target Account Set 消费 ① 的默认集 + ② 的 Account Pool + ③ 的 Intent，推导 production_requirements，向后传递至契约 5。

**四个契约共同构成「经营什么 → 在哪经营 → 准备讲什么 → 这次针对哪些账号」的完整上游链**，是后续 Batch（契约 5–9）与 Workspace 实例化的前置输入。

---

## 2. Unresolved Questions（待后续 Batch / Review 裁定）

1. ~~**Operating Context 是否每 Office 必有一个？**~~ **【DELTA A3 已解决】**
   - 原问题因「Company → Operating Context → Office」的过早抽象而提出。
   - DELTA A3 决定：**删除 Operating Context 层，Office 直接挂 Company**（`Company → Office` 与 `Company → Organization` 正交）。
   - 因此本问题不再成立；Operating Context 降为 **RESERVED / DEFERRED CANDIDATE**，未来若真实出现需管理多个 Office 的上层 Business Context，再从真实需求中抽象，且优先对齐 Blueprint 的 Business / 业务空间，避免重复造概念。

2. **Office 命名 vs XHS「运营办公室」Workspace 的混淆**
   - 当前 XHS Instance 称「小红书运营办公室」为 Workspace + Object Owner。
   - 新模型中 `Office` = 经营单元（业务概念），`Workspace` = 专业执行面（如 XHS Channel Operations Workspace 服务 Office）。
   - **不冲突**（不同层），但 **IA/UI 命名需澄清**（Office ≠ Workspace；一个 XHS Ops Workspace 可服务多个 Office）。建议留待 Workspace 实例化与导航设计期解决，不在契约层阻塞。

3. **Intent ↔ Office 弱链接的精确语义**
   - 设计定：Intent 属 Company Growth Context（共享），经 Target Account 再分流到 Office 账号；Intent **不被单一 Office 拥有**。
   - 待裁定：跨 Office 的 Intent 选择账号时，`selected_accounts` 如何跨多个 Office 的 Pool 聚合？（契约 ④ 已允许，规则留契约 5 细化）

4. **Account Pool 物化 vs 派生**
   - 建议：首版**派生**（从 OfficeAccountBinding 计算），不额外物化；仅性能需要再物化。

5. **production_requirements 合并算法**
   - 仅声明原则（并集/下限/按平台字典分别生成），**具体字段级合并规则留契约 5（Content Variant）** 设计期裁定。

6. **Capability 状态（VERIFIED/CONDITIONAL/UNKNOWN/UNAVAILABLE）的来源真源**
   - 建议：由 **Capability Registry**（Connector 提供、官方源验证）声明，不写死在 Channel 对象。
   - 待裁定：Registry 结构与 Connector 如何上报能力状态（Connector 设计期，不在本 Batch）。

7. **Office default_target_account_set 与 AI 推荐冲突时的用户否决权**
   - 建议：Effective Set = 默认 ∪ AI推荐 ∪ 手动覆盖，手动覆盖最高优先；用户可在确认环节整体接受/调整。
   - 待裁定：是否每次都需用户显式确认，还是默认集可直接进入生产（建议：默认集可直接生产，AI/手动变更才提示）。

---

## 3. 是否出现新 Primitive（与 Frozen 兼容检查）

**结论**：引入了**新的业务领域对象类型**（非 Shell/Shared/Org 新原语），与 Frozen P1–P7 **兼容、不冲突、不修改**。

新增对象类型（均属 Content Growth Domain 业务对象；**Operating Context 不升 OS Shared**）：
- Office（CG Domain 经营单元，直接挂 Company）
- Channel / Channel Account / OfficeAccountBinding / Account Pool（CG Domain 平台/账号）
- Content Opportunity / Content Intent（CG Domain 业务上游）
- Target Account Set（CG Domain 选择集，含运行期派生的 Account Eligibility + Distribution Execution Policy）
- ~~Operating Context（OS Shared 业务容器）~~ → **RESERVED / DEFERRED CANDIDATE**（DELTA A3：不 Frozen、不升 OS Shared；未来优先对齐 Blueprint Business/业务空间）

**它们不是**：
- 新的 Shell 原语（Pane/Search/Toggle 不变）
- 新的 Shared Pattern 原语（P1–P7 责任/员工/系统语义不变）
- 新的 Organization 原语（Department/Team/Employee 不变；Employee↔Office 服务关系由契约 8 后续 Batch 定义）

> 即：新对象是**业务内容对象**，叠加在已有的 Shell + Shared Pattern + Organization 之上，是「被管理的业务实体」，不是「新的运行机制」。运行机制的 Shared Pattern（P1–P7）完全不受影响。

---

## 4. 与现有 Blueprint / P1–P7 的冲突检查

| 权威文档 | 冲突？ | 说明 |
|----------|:------:|------|
| **P1 三层责任语义** | 无 | Office 可作为内容对象的 Object Owner 候选，与 P1「Object Owner = 稳定业务归属」兼容；责任语义本身不变。 |
| **P2 Employee Presence** | 无 | 员工在业务对象上的 Presence 不依赖 Office 结构。 |
| **P3 System Activity** | 无 | Analytics / 自动回流是 System Activity，与 Office/Account 业务对象正交。 |
| **P4 Automation by default** | 无 | Target Account 自动推导（默认集/AI推荐）符合「自动化默认」；人工仅在 Decision Gate（如发布前合规审核）。 |
| **P5 Handoff** | 无 | 责任交接在 Employee 层，与 Office/Intent 业务对象无关。 |
| **P6 Result Reference** | 无 | Publication/Analytics 结果引用机制不变。 |
| **P7 CEO Decision Package** | 无 | 发布合规/预算等 Decision 结构不变；仅领域内容新增。 |
| **Product Blueprint** | 无 | Office 是业务经营层概念，直接挂 Company；与 Blueprint「公司 → 部门 → 项目 → 员工」组织层及「业务空间 / Workspace」层级**正交**，不改 Blueprint。DELTA A3：若未来需上层 Business Context，优先对齐 Blueprint 的 **Business / 业务空间**，而非新造 Operating Context。 |

**结论**：Batch A 四个契约**不修改、不冲突**任何 Frozen 文档。

---

## 5. 对 XHS 当前实现的影响

**结论**：**ADDITIVE，非破坏性**。当前 XHS Instance（APPROVED）不变。

- 当前 XHS Instance = **单 Office · 单 XHS 账号** 的退化形态（「小红书运营办公室」既是 Workspace 也是 Object Owner，绑定一个 XHS 账号）。
- 新模型下，该实例可重新解读为：**一个 XHS Channel Operations Workspace，服务于（可能多个）Office，每个 Office 绑定一个 XHS 账号**。
- 当前实例**无需修改**；未来若扩展为多账号/多 Office XHS 经营，仅需在该 Workspace 实例内接入本 Batch 的 Office/Account/Target Account 契约，**不改变已 Approved 的 Calendar/Note/Analytics 专业能力**。
- Object Owner「小红书运营办公室」仍有效，可理解为「拥有该 XHS 账号的 Office」；与 P1 Object Owner 语义一致。

---

## 6. 对未来 Content Production / Channel Ops 的影响

本 Batch 四个契约是两层 Workspace 的**共享上游输入契约**：

### Content Production Workspace（平台无关，未来 Batch）
- 消费：Content Intent（契约 ③）+ Target Account Set 的 `production_requirements`（契约 ④）。
- 产出：Canonical Production Result → 账号级 Content Variant（契约 5 后续）。
- 不直接接触 Channel/Account 发布细节，只按 `production_requirements` 生产。

### Channel Operations Workspace（每平台一个，未来 Batch）
- 消费：Target Account Set（契约 ④）+ Content Variant（契约 5 后续）。
- 负责：Intake → Platform Adaptation → Review → Schedule → Publish → Engage → Analytics → Feedback。
- 账号级 Engagement / Analytics 以 **Publication（per Account）** 为真相源（契约 5 后续）。

**因此**：Batch A 契约是「上游共享契约」，Content Production 与 Channel Ops 两个 Workspace 都依赖它；未来 Batch（契约 5 Variant/Publication、契约 6–9 组织/路由/容量）在其下游扩展。

---

## 7. 五场景验证覆盖

| 场景 | 验证的契约 | 结论 |
|------|-----------|------|
| CASE 1 同平台不同定位 | ① Office + ② Channel Account | 拆为不同 Office，各绑不同定位账号 ✅ |
| CASE 2 多平台同定位 | ① Office + ② Account Pool | 单 Office 绑 N 账号 ✅ |
| CASE 3 4 账号仅选 3 | ④ Target Account | 选子集，不群发 ✅ |
| CASE 4 同 Intent 分歧生产 | ③ Intent + ④ | Intent 共享，Production 后续 Divergence ✅ |
| CASE 5 某账号 OAuth 失效 | ② Channel Account + ④ | 账号保留/历史保留；该账号**仍是 Target，仅 BLOCKED**（DELTA A2：禁止静默删除 Target）；按 Distribution Execution Policy 行为（BEST_EFFORT=可用账号继续，ALL_REQUIRED=本次暂停）；UI 白话「B站授权已过期。抖音和小红书仍可继续发布。」 ✅ |

---

## 8. 状态与下一步

**当前状态**：`CONTENT GROWTH CONTRACT BATCH A — APPROVED CANDIDATE`（未 Frozen）

**Review 结果**：总体 APPROVED WITH DELTAS。DELTA A1（Target 生命周期降复杂度）、DELTA A2（Target/Eligibility 分离 + Distribution Execution Policy）、DELTA A3（Operating Context 不升 OS Shared，Office 直接挂 Company）均已应用到对应契约文件。

**下一步（已批准）**：
1. 四个契约升为 **APPROVED CANDIDATE**（Office / Target 已标 DELTA；Channel Account / Content Intent 同步升 APPROVED CANDIDATE）。
2. 进入 **Batch B — COMPANY OS RESPONSIBILITY & ROUTING**：仅设计 ⑥ Responsibility Requirement · ⑧ Shared Employee Service Relation · ⑦ Organization Routing（暂不做 ⑤⑨、不 UI / Runtime / Connector）。目标稳定「Process asks WHAT / Organization decides WHO / Capability determines HOW」与「Employee 安全跨多 Office 服务而不产生固定 DAG」。
3. 后续 Batch C：契约 ⑤ Content Variant / Publication、⑨ Lightweight Queue·Bottleneck。

*本文件为 Batch A Review，未 Frozen。以 Review 批准后的修订版为准。*

---

*CONTENT GROWTH CONTRACT BATCH A — APPROVED CANDIDATE*
