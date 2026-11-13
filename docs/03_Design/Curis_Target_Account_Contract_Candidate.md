# Curis · Target Account Contract Candidate

> **状态**：APPROVED CANDIDATE（Batch A — Operating Foundation · 经 DELTA A1/A2 修正，未 Frozen）
> **类型**：Content Growth Domain
> **纪律**：不 Frozen / 不改 Product Blueprint / 不改 P1–P7 / 不改 XHS·RD Instance / 不开发 Runtime / 不开发 Connector / 不画 UI
> **前置**：`CONTENT_GROWTH_SHARED_CONTRACT_PLAN.md`（契约 4）、用户约束 4（Target=Account 非 Platform；Office Default + AI Recommendation + Manual Override → Effective Set）
> **本轮修正**：DELTA A1（生命周期降复杂度，移除 proposed→…→executed 小状态机）、DELTA A2（Target 与 Eligibility 分离 + Distribution Execution Policy）
> **FROZEN 指针（2026-08-16）**：④ Target Account Set / Distribution Targets 语义已正式冻结于 `Curis_Content_Growth_Domain_Authority.md` §1.4。本 Candidate 保留作 **Design Record / Reference**，不删除、不覆盖。

---

## 0. 本契约的目的与边界

固化「**这次具体针对哪些账号**」的载体 —— **Target Account Set / Distribution Targets**。

**核心纠正**（继承前序 + 用户约束 4）：
- Target **必须是 Account，不是 Platform**。
- 绑定 N 个账号 **≠ 每条内容必须群发所有账号**（CASE 3 验证）。
- 用户**不需要每条手工选择**：支持 Office Default Set + AI Recommendation + Manual Override → **Effective Target Account Set**。

本契约只定义对象语义 / 关系 / 归属 / 生命周期 / 必填·可选 / 不变量 / 跨对象引用 / 失败·未知 / 场景验证。**不进入** DB table / SQL / ORM / API / frontend state / 实现类 / migration。

---

## 1. Target Account Set / Distribution Targets（Content Growth Domain）

### Object semantics
某一次**内容实例**所针对的**具体账号子集**。由 Intent + 相关 Office 的 Account Pool 经选择推导得出，是「在哪经营（具体账号）」的落点。

### Identity
- `content_intent_id`（FK → Content Intent；或更高层 content_instance_id）
- `selected_accounts[]`（每项为一个 Channel Account id）

### Composition（核心字段）
- `selected_accounts[]`：最终入选的 Channel Account id 列表（**账号粒度**，即「业务/用户想发哪里」的 Target）
- `selection_basis`：选择来源
  - `DEFAULT_SET`（来自 Office 默认目标账号集）
  - `AI_RECOMMENDED`（AI 基于内容/历史表现推荐）
  - `MANUAL_OVERRIDE`（用户手动覆盖）
- `effective_target_account_set`：解析后的最终集合（三者合并裁决结果）
- `distribution_execution_policy`：本次分发的执行策略（见 §Eligibility 分离），默认来自 Office，可被任务覆盖
  - `BEST_EFFORT`（默认推荐）：可用账号继续发布，不可用账号保持 Blocked，不阻断其他
  - `ALL_REQUIRED`：任一 Target 账号当前不可执行 → 本次 Distribution 暂停，待全部可用再执行
- `production_requirements`（由 selected_accounts 推导，见 §派生）：
  - `ratio_union`（各账号 ratio 并集 / 下限）
  - `duration_lower_bound`（时长下限）
  - `copyright_placeholder`（版权占位，按平台要求）
  - `disclosure_dictionary`（AI 披露字典，按平台政策）
  - `publish_at_placeholder`（各平台 scheduling 支持度条件化，POLICY VERIFICATION REQUIRED，不写死强规则）

### Required / Optional information
**必填**：`content_intent_id`（ref）、`selected_accounts[]`（每个为 Channel Account id）
**可选**：`selection_basis`、`effective_target_account_set`、`production_requirements`、`override_reason`

### Relationships
- `Target Account Set *—1 Content Intent`（父意图）
- `Target Account Set *—* Channel Account`（来自相关 Office Account Pool 的子集）
- `Target Account Set → Content Variant / Publication`（驱动后续账号级变体与发布，契约 5 后续 Batch）

### Ownership
- 属于**一次内容实例**（由 Intent + Office 派生），非 Office 独占、非 Channel 独占。

### Lifecycle（DELTA A1 · 降复杂度）
Target Account Set **不是独立 Workflow**，不暗示每次需用户确认、不与 Publication 执行状态重复、不给简单选择集制造小状态机。

- **收敛为**：`DRAFT`（草稿/构建中）→ `EFFECTIVE`（当前生效的目标账号解析结果）→ `SUPERSEDED`（被新的解析结果取代）。
- 若 Content Intent 自身的 revision 已足以表达「目标账号变更」，则 Target Account Set **可进一步不持独立生命周期**，仅作为 Intent 当前生效解析的**派生视图**（推荐默认解读）。
- **发布是否执行 / 成功，属于 Publication（契约 5 后续），不属于 Target Account Set**。
- **Automation by default 保持不变**：默认集 / AI 推荐自动生效，不要求用户逐条确认。

### Invariants（硬约束）
1. **Target = Account，永不为 Platform**。选择粒度是账号。
2. **绑 N 账号 ≠ 群发所有**。每次内容实例仅从 Account Pool **选子集**（CASE 3）。
3. 三源合并裁决：
   - `Office.default_target_account_set` 提供默认；
   - AI 可推荐增删（基于内容语义 / 历史表现）；
   - 用户可手动覆盖（增 / 删 / 改）；
   - 最终 = **Effective Target Account Set**。
4. **无默认群发**：不要求用户每条机械勾选，但也绝不自动全量群发。
5. **Target 与 Eligibility 分离**（DELTA A2）：Target 表达「业务/用户想发哪里」；Eligibility 表达「当前技术上能不能发」。二者必须分开——账号失效时**仍是 Target，只是 BLOCKED**，不得静默从 Target 删除。
6. **Distribution Execution Policy 决定降级行为**（见 §Eligibility）：`BEST_EFFORT`=可用继续/不可用 Blocked；`ALL_REQUIRED`=任一不可用则本次暂停。普通用户不配此枚举，Office 有默认、任务可覆盖，UI 仅白话表达。

### Cross-object references
- → Content Intent（契约 3，父）
- → Office.default_target_account_set（契约 1，默认来源）
- → Channel Account / Account Pool（契约 2，候选来源）
- → Content Variant / Publication（契约 5 后续，消费方；**发布执行/成功状态在此，不在本契约**）
- → Account Eligibility（见 §Eligibility，运行期派生，非本契约持久化对象）

### Failure / Unknown semantics（DELTA A2 · Eligibility 分离）
- **Target 不因 Eligibility 失效而被删除**：某 `selected_account` 为 `EXPIRED` / `REVOKED`（CASE 5）→ 它**仍是 Target**，但其 Eligibility = `BLOCKED`；按 `distribution_execution_policy` 决定行为：
  - `BEST_EFFORT`：其余 Available 账号继续发布，BLOCKED 账号跳过并保持 Target；
  - `ALL_REQUIRED`：本次 Distribution 暂停，待该账号恢复 Available 再执行。
- 账号与历史**保留**；**不静默从用户业务 Target 中删除、不默认继续即丢**。
- 若某选中账号其 Channel 能力为 `UNKNOWN` → `production_requirements` 中对应项标记缺口，不静默继续。

### Example scenarios
- **CASE 2（多平台同定位 → 单 Office 4 账号）**：
  - `Office · Curis AI` Account Pool = `{ Douyin, XHS, Bilibili, TikTok }`
  - Intent 经 Target Account Set 选择子集。
- **CASE 3（4 账号，仅选 3）**：
  - Content #101 → `{Douyin ✓, XHS ✓, Bilibili ✓, TikTok ✕}`
  - Content #102 → `{Douyin ✓, XHS ✕, Bilibili ✕, TikTok ✓}`
  - 说明：绑定多账号 **≠** 每条内容群发所有账号。
- **CASE 5（OAuth 失效 · Target/Eligibility 分离）**：
  - `Bilibili · Curis AI` OAuth 过期 → Bilibili **仍是 Target**，但 Eligibility = `BLOCKED`；
  - 按 `BEST_EFFORT`（Office 默认）：Douyin / XHS / TikTok 继续发布，Bilibili 保持 Blocked；
  - UI 白话：「B站授权已过期。抖音和小红书仍可继续发布。」——用户无需理解内部 Policy 枚举。

---

## 1b. Account Eligibility 与 Distribution Execution Policy（DELTA A2 · 核心分离）

**Target ≠ Eligibility**。两者必须分开建模：

| 维度 | 表达什么 | 来源 |
|------|----------|------|
| **Target Account Set** | 业务 / 用户**想发哪里** | 用户/Office 默认/AI 推荐（业务意图） |
| **Account Eligibility** | 当前**技术上能不能发** | 运行期派生（OAuth 状态 / Scope / 平台能力） |

- **Target 不因 Eligibility 失效而消失**：账号 `EXPIRED`/`REVOKED` 时，它**仍是 Target**，只是 Eligibility 置 `BLOCKED`。
- **禁止**：OAuth 失效 → 静默从用户业务 Target 中删除 → 默认继续其他平台。该行为混淆了「意图」与「能力」。

**Distribution Execution Policy**（决定 BLOCKED 账号如何影响本次分发；普通用户不配枚举，Office 有默认、任务可覆盖）：

| Policy | 行为 | 适用 |
|--------|------|------|
| `BEST_EFFORT`（推荐默认） | 可用账号继续发布；不可用（BLOCKED）账号保持 Target 并跳过 | 多数内容分发 |
| `ALL_REQUIRED` | 任一 Target 账号当前不可执行 → 本次 Distribution **暂停**，待全部可用再执行 | 强一致/全渠道联动发布 |

- **UI 白话表达**（不暴露内部枚举）：「B站授权已过期。抖音和小红书仍可继续发布。」
- Eligibility 为**运行期派生视图**（基于 Channel Account `authorization_state` + Channel 能力状态），非本契约持久化对象；具体判定规则在 Runtime / Connector 设计期裁定。

---

## 2. 派生规则（production_requirements 推导原则 · 仅声明，细节留契约 5）

`production_requirements` 由各 `selected_account`（经其 Channel 约束）**合并推导**：
- ratio / duration / resolution：取各账号要求的**并集或下限**（不抹平差异，见前序 G 节平台差异模型）。
- copyright / disclosure：按各平台政策字典分别生成。
- scheduling (`publish_at`)：按各平台支持度**条件化**——YouTube `VERIFIED` 可定时；抖音官方 API `UNKNOWN` 暂不支持（POLICY VERIFICATION REQUIRED，不写死「每次必须人工点击」强规则）。

> 具体合并算法与字段级规则在 **契约 5（Content Variant / Publication）** 设计期裁定，不在本 Batch A 固化。

---

## 3. 归属层

| 对象 | 归属层 |
|------|--------|
| Target Account Set / Distribution Targets | Content Growth Domain |

---

## 4. 与现有权威文档的关系

- **P1–P7**：不冲突。本契约为业务对象（账号选择集），与责任/员工语义正交。
- **XHS Instance**：当前 XHS 实例为单一 XHS 账号，其 Target Account Set 退化为单账号；新模型支持其未来扩展为多账号选择。当前实例不变。
- **契约 1/2/3 依赖**：Target Account Set 依赖 Office 默认集（契约 1）、Account Pool（契约 2）、Content Intent（契约 3）；被契约 5（Variant/Publication）消费。
- **DELTA A1/A2 已应用**：生命周期降为 DRAFT→EFFECTIVE→SUPERSEDED（或作为 Intent 派生视图）；新增 Target/Eligibility 分离与 Distribution Execution Policy，发布执行状态归属 Publication（契约 5）。

---

*本文件为 Contract Candidate，经 Batch A Review 批准为 **APPROVED CANDIDATE**，未 Frozen。以后续 Batch / Frozen 裁定为准。*

---

*CONTENT GROWTH CONTRACT BATCH A — APPROVED CANDIDATE*
