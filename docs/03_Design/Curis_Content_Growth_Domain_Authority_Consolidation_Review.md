# Content Growth Domain — Authority Consolidation Review

> **状态**：AUTHORITY CONSOLIDATION REVIEW（未 Frozen · 本轮只评审不落定最终 Frozen 文档）
> **Review Record（2026-08-16 已落定 Frozen）**：本 Review 的评审结论已落定为 Frozen Authority —— `Curis_Content_Growth_Domain_Authority.md`（①②③④⑤）。本轮 DELTA（仅 Shared 侧）：⑦ 原 `ROUTING_IS_DETERMINISTIC` 过强，改为 `ROUTING_IS_POLICY_GOVERNED_AND_EXPLAINABLE`（五项原则）。本文件留作 **Review Record / Reference**，不删除、不覆盖。
> **范围**：候选集 B — ① Office · ② Channel / Channel Account / Account Pool · ③ Content Opportunity / Intent · ④ Target Account · ⑤ Content Variant / Publication
> **目标**：审查稳定业务语义，判定哪些升格为 **Content Growth Domain Authority**，哪些仍保持 Candidate；并明确**不 Frozen** 具体平台事实。
> **纪律**：不复制 Candidate 细节（见 §G）；不 Frozen 具体平台 API / ratio / duration / OAuth Scope / scheduling 能力（属 Capability Registry / Channel Facts）；不修改现有 Frozen Authority。
> **前置**：9 契约全部 APPROVED CANDIDATE；依赖 Company OS Shared（⑥⑧⑦，本轮判定升格）；`Curis_XHS_Workspace_Instance_Spec_v1.md` / `Curis_RD_Workspace_Instance_Spec_v1.md`（ADDITIVE 验证）。

---

## 1. 稳定业务语义审查（D 节）

以下语义经 Batch A（A1/A2/A3）+ Batch C（C1/C2）多轮 Delta 已稳定，属 Content Growth 核心业务定义：

| 语义 | 稳定性 | 说明 |
|---|---|---|
| Office ≠ Organization | ✅ | Office 经营单元，直接挂 Company（DELTA A3）；与 Organization 树严格正交 |
| Channel ≠ Account | ✅ | Channel=平台事实层；Channel Account=账号经营层 |
| Target = Account（非 Platform） | ✅ | Effective Target Account Set = Office Default + AI Recommendation + Manual Override |
| Intent 共享 WHY/WHAT/GOAL | ✅ | 跨账号上游对象；**禁止** Prompt/CoT/推理进入 Intent |
| HIGH REUSE + FULL DIVERGENCE | ✅ | 一 Intent → N 账号级变体，复用与发散并存 |
| Publication per-Account truth | ✅ | 逐账号独立真相；一账号失败不回滚其他（FACT 层） |
| Distribution Policy 控制未来执行 | ✅ | BEST_EFFORT / ALL_REQUIRED 读自 ④，⑤ 只读服从（DELTA C1） |
| Capability Truth | ✅ | Channel 只引用 VERIFIED/CONDITIONAL/UNKNOWN/UNAVAILABLE 能力 |

**明确不 Frozen（下放 Capability Registry / Channel Facts / 扩展点）**：
- 具体平台 API（Douyin/XHS/Bilibili/YouTube 接口形态）
- 具体 ratio（复用/发散比例常量）
- 具体 duration（scheduling 时长）
- 具体 OAuth Scope（各平台授权范围）
- 具体 scheduling 能力（哪些平台支持定时发布）—— 保持 Capability Truth 枚举，UNKNOWN 合法

---

## 2. 逐项判定

### 2.1 ① Office — 判定：**FREEZE NOW（Domain Authority）**

- Definition：Office = 经营单元（目标/定位/受众/内容策略/Knowledge/Account Pool/Growth Context），直接挂 Company，与 Organization 正交。
- Invariant：OFFICE ≠ ORG_MEMBER（Office 不因此变 Department）；OFFICE_UNDER_COMPANY（company_id FK）；OPERATING_CONTEXT_RESERVED（Operating Context 为 DEFERRED CANDIDATE，未来优先对齐 Blueprint Business）。
- 排除：Operating Context 升格（DELTA A3 已 DEFERRED）。

### 2.2 ② Channel / Channel Account / Account Pool — 判定：**FREEZE NOW（Domain Authority）**

- Definition：Channel（平台事实层，只引用已验证能力）；Channel Account（账号经营层，OAuth 失效仍保留账号+历史+执行降级）；OfficeAccountBinding（首版 1:1、结构 N:N）；Account Pool = 派生集合。
- Invariant：CHANNEL ≠ ACCOUNT；BINDING_DERIVES_POOL；OAUTH_FAILURE_KEEPS_ACCOUNT（保留账号与历史，执行降级）。
- 排除：具体 OAuth Scope / 平台 API / capability 具体事实（Capability Registry）。

### 2.3 ③ Content Opportunity / Intent — 判定：**FREEZE NOW（Domain Authority）**

- Definition：Content Opportunity（发现的选题/机会）→ 转化 → Content Intent（跨账号共享上游对象：why/what/goal）。
- Invariant：INTENT_EXCLUDES_INFERENCE（禁存推理/Prompt/CoT/中间草稿）；HIGH_REUSE_AND_FULL_DIVERGENCE；INTENT_SHARED_UPSTREAM（多账号共享 WHY/WHAT/GOAL）。
- Truth boundary：Intent 只承载长期业务语义，非执行草稿。

### 2.4 ④ Target Account — 判定：**FREEZE NOW（Domain Authority）**

- Definition：Target = Account 非 Platform；Effective Target Account Set = Office Default + AI Recommendation + Manual Override。
- Lifecycle（DELTA A1）：DRAFT → EFFECTIVE → SUPERSEDED（或 Intent 派生视图；发布执行属 Publication，不属此处）。
- Invariant（DELTA A2）：TARGET ≠ ELIGIBILITY（OAuth 失效仍保持 Target 仅 BLOCKED，禁静默删）；DISTRIBUTION_POLICY_PRESENT（BEST_EFFORT / ALL_REQUIRED，Office 有默认、任务可覆盖）。
- Truth boundary：Distribution Execution Policy 为**唯一真相源**（⑤ 只读服从，不重定义 —— DELTA C1）。

### 2.5 ⑤ Content Variant / Publication — 判定：**FREEZE NOW（Domain Authority）**

- Definition：Content Variant（每选中账号一份，绑单一 Channel Account；reuse_mode HIGH_REUSE/FULL_DIVERGENCE）；Publication（per-Account 真相源：状态/回执/时间逐账号独立）。
- Invariant（DELTA C1）：FACT_NOT_ROLLED_BACK（已发生 Publication 事实不回滚）；FUTURE_GOVERNED_BY_POLICY（未执行部分是否继续读 ④ distribution_execution_policy）；PUBLICATION_OBEYS_POLICY（不重定义第二套 Policy）；RECEIPT_FROM_CONNECTOR（回执由 Capability·Connector 回填，不伪造）。
- 排除：具体 scheduling 能力（保持 Capability Truth 条件化，UNKNOWN 合法）；具体平台发布 API。

---

## 3. Cross-cutting Truth Boundaries（跨域，暂不升 Shared）

两个边界当前在 Domain 内稳定，但本质**跨业务**，标记未来可能升格 Company OS Shared（本轮**不升**，保持 Domain 引用）：

| 边界 | 当前归属 | 未来可能 | 理由 |
|---|---|---|---|
| Capability Truth（VERIFIED/CONDITIONAL/UNKNOWN/UNAVAILABLE） | Domain（Channel 引用） | Company OS Shared | RD 工具亦有 capability truth，属跨业务真理边界 |
| Distribution Execution Policy（BEST_EFFORT/ALL_REQUIRED） | Domain（④ 定义、⑤ 服从） | Company OS Shared | 任何「多目标分发」业务（如多客服渠道）都可能用 |

**本轮处理**：保持 Domain 引用，不在 Shared 重复定义；待未来确有第二业务需要时分出 Shared。

---

## 4. 冲突检查（F 节）

| 现有 Authority | 关系 | 说明 |
|---|---|---|
| Product Blueprint | NO CONFLICT | Office 挂 Company 与 Blueprint 业务空间层级正交；Operating Context DEFERRED 对齐 Blueprint Business |
| Frozen P1–P7 | NO CONFLICT / EXTENDS | Domain 契约消费 ⑥⑧⑦（Shared 升格后）；不修改 P1–P7 |
| Agent Adapter Contract | NO CONFLICT | Publication 回执经 Connector 回填，未重定义 Adapter 内部 |
| ADR-0046（Computer Access） | NO CONFLICT | 不涉及本机电脑访问 |
| XHS Approved Instance | EXTENDS / NO CONFLICT | 9 契约对 XHS ADDITIVE（单 Office·单账号退化） |
| RD Approved Instance | EXTENDS / NO CONFLICT | RD 责任模型映射 ⑥；ADDITIVE |
| Current Runtime Foundation | NO CONFLICT | 仅语义层，未实现 Runtime |

**结论：无 REQUIRES DELTA，无现有 Authority 需修改。**

---

## 5. 三项非阻塞问题（E 节）确认

1. **平台 Scheduling 核实**：保持 Capability Truth 枚举，UNKNOWN 合法；不 Frozen 具体事实（⑤ 落实）。
2. **Bottleneck 阈值/窗口**：属 Runtime Policy，不影响 Domain 升格。
3. **possible_cause 最小事实规则**：属 ⑨（Shared Candidate），不影响 Domain。

---

## 6. 建议的最终 Content Growth Domain Authority 文档结构（本轮不创建）

```
Curis_Content_Growth_Domain_Authority.md（未来）
├ §1 Definitions
│   ├ Office（经营单元，挂 Company，≠ Organization）
│   ├ Channel / Channel Account / OfficeAccountBinding / Account Pool
│   ├ Content Opportunity / Content Intent
│   ├ Target Account Set
│   └ Content Variant / Publication
├ §2 Relationships
│   ├ Company → Office（*—1）
│   ├ Office →* Channel Account（经 OfficeAccountBinding）
│   ├ Content Opportunity → Content Intent →* Target Account Set →* Content Variant → Publication
│   └ Domain 消费 Shared：⑥（Requirement）→ ⑦（Routing）→ ⑧（Employee 执行）
├ §3 Invariants
│   ├ OFFICE ≠ ORG；CHANNEL ≠ ACCOUNT；TARGET = ACCOUNT
│   ├ INTENT_EXCLUDES_INFERENCE；HIGH_REUSE + FULL_DIVERGENCE
│   ├ PUBLICATION_PER_ACCOUNT_TRUTH；FACT_NOT_ROLLED_BACK
│   └ TARGET ≠ ELIGIBILITY；PUBLICATION_OBEYS_POLICY
├ §4 Ownership（Office 归 Company；Intent 语义归 Process；Publication 真相归 per-Account）
├ §5 Truth Boundaries
│   ├ Capability Truth（cross-ref，未来可能升 Shared）
│   └ Distribution Execution Policy（④ 唯一源，⑤ 服从）
├ §6 Cross-domain rules（Domain 不得重定义 Shared 的 Responsibility/Routing/Employee 语义）
├ §7 Extension points
│   ├ 具体平台 API / OAuth Scope / scheduling 能力 → Capability Registry
│   ├ ratio / duration 常量 → Channel Facts / Runtime Config
│   └ responsibility_type 词汇 → Shared 扩展点
```

**Author 短、稳定**（G 节）：§1–§6 只留核心；平台事实/常量/场景全部下放 §7 或留 Candidate/Review 作 Reference。

---

## 7. 升格清单（H 节 · 候选集 B）

| 契约 | 判定 | 理由摘要 |
|---|---|---|
| ① Office | **FREEZE NOW** | 经营单元语义稳定，DELTA A3 已收口 |
| ② Channel / Channel Account / Account Pool | **FREEZE NOW** | Channel≠Account / Binding 派生 Pool / OAuth 失效保留，稳定 |
| ③ Content Opportunity / Intent | **FREEZE NOW** | Intent 排除推理 + HIGH REUSE/FULL DIVERGENCE，稳定真理边界 |
| ④ Target Account | **FREEZE NOW** | Target=Account + Eligibility 分离 + Distribution Policy，稳定 |
| ⑤ Content Variant / Publication | **FREEZE NOW** | per-Account 真相 + 服从 Policy（DELTA C1），稳定 |

**DEFER / REJECT / KEEP CANDIDATE**：候选集 B 内无（5 项均成熟到 Domain Authority）。具体平台事实已排除至扩展点，不影响升格。

---

## 8. 综合回答（H 节 · 6 问）

**1. 哪些 Company OS 语义值得现在 Frozen？**
⑥ Responsibility Requirement（「Process 声明 WHAT，不指名 WHO」抽象）、⑧ Shared Employee Service Relation（Employee∈Org、经 Assignment 服务多 Office、服务≠隶属/≠上下文所有权）、⑦ Organization Routing（确定性调度机制 + 异常升级边界）。三者均为跨业务通用模式，且已通过 DELTA 1/2/3 + B1 收口。

**2. 哪些 Company OS 语义还太早？**
⑨ Lightweight Queue / Bottleneck —— 概念属 Shared 但过新：阈值/持续窗口/`possible_cause` 最小事实规则均未校准（属未来 Runtime Policy），无运行时验证。**保持 APPROVED SHARED CANDIDATE，不强 Frozen**。此外，以下明确**不 Frozen**（作扩展点）：具体 routing 算法/权重/阈值、responsibility_type 词汇表、Bottleneck 常量、Context Assembly（Future Candidate，不建第 10 契约）。

**3. 哪些 Content Growth 语义值得现在 Frozen？**
全部 5 项核心关系/不变量语义：① Office、② Channel/Channel Account/Account Pool、③ Content Opportunity/Intent、④ Target Account、⑤ Content Variant/Publication。均经多轮 Delta 稳定。

**4. 哪些仍应保持 Domain Candidate？**
候选集 B 内无（5 项均成熟）。但须强调：**具体平台事实**（API / OAuth Scope / scheduling 能力 / ratio / duration）**不 Frozen**，下放 Capability Registry / Channel Facts / Runtime Config。另两个跨域边界（Capability Truth、Distribution Execution Policy）当前保持 Domain 引用，标记未来可能升 Shared，**本轮不升**。

**5. 是否需要修改任何现有 Frozen Authority？**
**不需要。** 冲突检查结论：9 契约对 Product Blueprint / Frozen P1–P7 / Agent Adapter Contract / ADR-0046 / XHS·RD Instance / Runtime Foundation 均为 NO CONFLICT 或 EXTENDS（扩展不修改）。**无 REQUIRES DELTA**，无任何现有 Authority 被修改。

**6. 9 份 Candidate 未来各自保留什么 Reference 价值？**
- **详细 Examples / CASE 验证**（C1–C7、B1–B6 等）：Authority 不收，留 Candidate/Review 作可演化参考。
- **Delta 推理史**（A1/A2/A3、B1、C1/C2 的取舍理由）：未来回看「为何如此设计」的唯一来源。
- **具体字段 Composition / 平台调查笔记**（如各平台 scheduling 能力核实）：实现层参考，不下放 Authority。
- **阈值校准实验 / `possible_cause` 事实规则校准**：⑨ 升格前的演进记录。
- **跨业务适用性分析**（每项「是否 RD/客服/销售也成立」）：未来判断是否升 Shared 的依据。
- **结论**：Authority = 短、稳定、难反悔的核心；Candidate/Review = 详细、可演化的活参考。两者长期并存。

---

*本文件为 Authority Consolidation Review，未 Frozen。最终 Frozen 文档按 §6 结构在批准后续建。*
