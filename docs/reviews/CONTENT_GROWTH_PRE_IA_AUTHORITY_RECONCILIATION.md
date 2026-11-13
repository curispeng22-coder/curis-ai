# CURIS CONTENT GROWTH
## PRE-IA AUTHORITY RECONCILIATION

Authority Class: REVIEW  
Status: Review  
Disposition: STOP FOR CEO REVIEW  
Date: 2026-08-24  
Scope: Content Growth IA 前的产品身份与 Authority 对账；只读，不修改 Current Authority、IA、UI、Figma、Runtime、Schema、DB 或代码。

## Executive conclusion

当前不能直接进入 IA。Content Growth 的专业工作方式研究已经很完整，但其产品身份尚有三处未闭合：

1. `Curis_Content_Growth_Domain_Authority.md` 仍用 `Office / Workspace` 并列，并把 Office 作为领域身份；Current Product Blueprint 已把 Workspace 定为唯一用户产品身份，Office 只保留为空间隐喻。
2. `XHS` 同时出现在两种语义中：平台 Channel，以及一个名为「AI 科技」的 Workspace 实例简称。若不区分，IA 会把平台、账号和 Workspace 混成同一层。
3. Content Growth Research 把 Main 写成「经营驾驶舱 / CEO Operating Result」，而当前 Shared/Main Authority 定义 Main 为“当前选中的 Professional Surface + Shared Work Area”。两者可以组合，但研究尚未获得 Current Authority 级别的默认入口授权。

因此本轮结论为：

**AUTHORITY BLOCKER STILL OPEN**

## Source and authority reading

| Source | Status / class | This audit consumes |
|---|---|---|
| `docs/00_Context/PRODUCT_DOCUMENT_POINTER.md` | Frozen / Truth Router | Product → Master Map → UI Blueprint 的 Current 路线；Professional Workspace 只在 Verified / Candidate / Unverified 轴上表达 |
| `docs/01_Product/Curis_Product_Blueprint.html` | Current / Frozen | `Company → Department → Business → Workspace`；Workspace 是完整专业环境；Office 只作隐喻；Main 为 selected Professional Surface + relevant Shared Work Area |
| `docs/01_Product/Curis_Product_Master_Map.md` | Current / Frozen | Business 必须归属 Department；Workspace 是 Business 下独立经营环境；Surface 不拥有 Runtime truth |
| `docs/01_Product/Curis_Product_UI_Blueprint.html` | Current / Frozen | UI 消费 Workspace / Surface / Main 的共享语义，不把 Domain 研究直接升级为 UI Authority |
| `docs/03_Design/Curis_Company_OS_Shared_Authority.md` | Frozen / Shared Authority | Employee 服务 Workspace；组织、服务、Capability 三轴分离；不授权 Office = Workspace |
| `docs/03_Design/Curis_Content_Growth_Domain_Authority.md` | Frozen / Domain Authority | Content Growth 的 Channel / Channel Account / Publication 不变量；同时保留了未与 Current Product Truth 对齐的 Office 术语 |
| `docs/03_Design/Curis_XHS_Workspace_Instance_Spec_v1.md` and `Curis_XHS_Workspace_UI_Authority_Map.md` | Instance authority reconciled / Candidate boundaries | `内容增长部 / 小红书运营 / AI 科技` 是 Workspace 实例候选；具体菜单和最终迁移仍未冻结 |
| `docs/Content_Growth_Professional_Workspace_Research/*` | Research / Expert Recommendation | Content Growth Professional Workspace、Channel、Main 驾驶舱、8 态与 4 桶的研究候选 |
| `CONTENT_GROWTH_PRE_IA_CONTRACT_CLOSURE.md` | Research / Red-Team closure | 研究层标记的“Content Growth=Workspace、XHS/Douyin=Channel、Main=驾驶舱”；不能覆盖 Current Authority |

## A. Current Truth

### A.1 Product identity terms

| Term | Current meaning | Source |
|---|---|---|
| **Business** | Company 下、Department 下的 canonical 业务身份；负责业务级方向、聚合与 Workspace Directory / Portfolio。长期 Business 必须归属 Department。 | Product Blueprint §公司与组织；Master Map Business field contract |
| **Workspace** | Business 下的独立经营单元和完整专业经营环境；不是 Page。包含 Shared Workspace Shell、Workspace-local Domain Navigation、Professional Surface、Shared Team Operating 与 Shared Employee Work Area。 | Product Blueprint §Business × Workspace；Master Map Workspace contract |
| **Office** | 不是 Current Product 的 canonical 一级对象。普通用户产品语言中仅保留为空间隐喻；它不是 Workspace 的正式别名。 | Product Blueprint §Business × Workspace；§产品语言 |
| **Professional Workspace** | Product Form，用于稳定专业经营问题的完整 Workspace 形态；Professional 不自动等于 Verified。 | Product Blueprint §Workspace Strategy |
| **Surface** | Workspace 内围绕一类稳定专业问题组织对象、动作、工具和经营 Truth 的人可见专业工作面；只声明 WHAT / Responsibility requirement，不拥有 Employee、Work、Result 或 Runtime。 | Product Blueprint §Professional Workspace；Shared Authority / Shell Contract |
| **Main** | Shared Shell 中始终存在的主工作区：当前 selected Professional Surface + relevant Shared Work Area；Employee Workstation 属于 Work Area，不等于整个 Main。 | Product Blueprint §Workspace 内职责；`Curis_Workspace_Shell_Contract_And_Shared_Patterns.md` §0.1 / §1.1 |

### A.2 Content Growth / Channel boundary

在 Content Growth Domain Authority 内，`Channel` 与 `Channel Account` 已有冻结的分层：平台事实是 Channel，账号经营事实是 Channel Account，Publication 按账号记录真实回执。XHS / Douyin 作为平台 Channel 与 `CHANNEL_NE_ACCOUNT` 一致；这不把它们变成全局 Core Domain enum，也不授权用平台名命名 Workspace 身份。

Content Growth 作为一个 Professional Workspace 形态与 Current Product 的通用 Workspace 模型相容，但“Content Growth = 当前已验证的 Professional Workspace”尚未在 Current Product Authority 中单独冻结；现有实例文档仍标为 Candidate / 迁移待独立 Gate。

## B. Accepted Candidate

以下是研究层可以继续供 IA 消费、但不能当作 Current Product Truth 的候选：

1. **Content Growth = Professional Workspace**：研究将跨渠道内容增长、研究、内容运营、增长评估、反馈与 Channel 适配组织成一个专业 Workspace；这是合理的 Domain Candidate，不是新增产品层级。
2. **XHS / Douyin = Channel**：Content Growth Research 与 Domain Authority 的平台事实模型一致。平台是 Channel，具体账号是 Channel Account，平台模块与 Connector 是能力边界。
3. **Operating Result / 经营驾驶舱**：作为 Content Growth 的一个默认候选 Professional Surface / projection，负责把 Result、Decision、Work、Publication 等现有对象压缩成 CEO 可读结果；不新造 Dashboard Truth 或聚合 Runtime。
4. **8 Operating States**：研究中用于区分 QUIET、RESULT、WATCH、DECISION、IN_PROGRESS、READY、ACTION_REQUIRED、ALERT 的行为模型；目前只能作为 Internal Research Model / accepted research candidate。
5. **4 Cognitive Buckets**：将 8 态投影为 NEEDS_ME_NOW、KNOW_ABOUT、RUNNING、QUIET 的 CEO 认知投影模型；目前只能作为 Projection Model / accepted research candidate。

## C. Conflict

### C.1 `Office / Workspace` 并列造成身份冲突

`Curis_Content_Growth_Domain_Authority.md` §0.1、§1.1、§2 仍写 `Company → Department → Business → Office / Workspace`，并以 Office 承载 Domain identity。该文件虽为 Frozen Domain Authority，但其 Office 术语没有得到 Current Product Blueprint 的等式授权；更高层 Product Truth 已明确 Workspace 为 canonical product identity、Office 仅为隐喻。

这不是可通过“Office = Workspace”兼容的差异：

- Workspace 是当前用户可进入、配置、工作和回看的身份；
- Office 在该 Domain 文件中还承担旧的 `company_id`、`OfficeAccountBinding`、账号池和经营单元语义；
- 直接建立等式会把产品语义与实现/domain identity 混为一层。

**当前裁定：不建立 `Office = Workspace`。Content Growth IA 必须消费 Workspace 作为 canonical identity；Office 只能被标为历史/实现迁移术语，直到 CEO 单独批准 Domain Authority 修正。**

### C.2 `XHS` 的双重命名

- Domain Authority / Research：XHS、Douyin 是 Channel。
- XHS Instance Authority：`内容增长部 / 小红书运营 / AI 科技` 是一个 Workspace 实例候选，文件中常以“XHS Workspace”简称它。

这两种说法可以共存，前提是 `XHS` 作为实例简称不再被读成平台身份；否则会产生 Channel → Workspace 的隐式等式。抖音 Instance 目前也没有被批准为 UI Authority。

### C.3 Main：selected Surface 与驾驶舱研究的层级差

当前 Main 不是全局 CEO Dashboard，也不是固定的 Content Growth 驾驶舱；它是当前 selected Professional Surface + Shared Work Area。Content Growth Research 的“经营驾驶舱”则是一个 Domain 默认入口候选，并且研究闭合文档进一步写成“Professional Surface 仅下钻层”。这超出了当前 Main Contract 的默认语义。

二者**不是逻辑上不可组合**：可以把“CEO Operating Result”表达为 Content Growth 内一个默认选中的 Professional Surface / projection，仍由 Main 承载；这样不需要重新定义 Main。可是，在 CEO 明确接受前，不能把该 Domain 候选写成 Current Rule，也不能把 Professional Surface 从 Main 降为全局下钻层。

## D. Deprecated

以下旧语义已被 Current Product Truth 或最新研究明确降级，不得作为 IA 当前规则：

- `Office` 作为普通用户一级导航、Business 的平级入口或 Workspace 的正式别名。
- “小红书运营办公室” / “研发办公室”作为并列 Office 产品入口。
- 把 XHS 或 Douyin 平台直接当作 Workspace、Tab 或独立 Business。
- 把 XHS 旧的 Calendar-Dominant 默认入口当作 Workspace 全局默认；最新 Instance Authority 已把 Calendar 收窄为 Content Operating 内的 Object View，经营概览仍只是 default candidate。
- 把研究中的 8 态 / 4 桶写成 Runtime State Schema、全局导航、固定 Page Contract 或新的 Truth / Result primitive。

历史文档和旧实现中的 `Office`、`office_id`、`OfficeAccountBinding` 不因本审计被删除或自动迁移；它们只能作为历史/实现 provenance 读取，不能覆盖 Current Product identity。

## E. Five-way disposition matrix

| Item | CURRENT TRUTH | ACCEPTED CANDIDATE | CONFLICT | DEPRECATED | CEO DECISION REQUIRED |
|---|---|---|---|---|---|
| Business | Company → Department → Business；canonical persisted business identity | — | — | Business 直接挂 Company | 否 |
| Workspace | Business 下独立专业经营环境 | Content Growth Workspace 形态 | Domain Authority 仍写 Office / Workspace | Office 作为用户产品别名 | 是：是否清理 Domain Authority 的 Office 术语 |
| Office | 无 canonical user-product equality | 可作为历史/domain implementation label | Domain Authority 仍让其承载身份与 binding | 普通用户 Office 入口 | 是 |
| Professional Workspace | Product Form；不自动等于 Verified | Content Growth Professional Workspace | Content Growth 具体 assurance / migration 未冻结 | Calendar-Dominant Workspace default | 是：是否接受 Content Growth 为当前 Domain candidate |
| Surface | Workspace 内专业工作面；Main 可选中它 | Operating Result / 经营驾驶舱作为默认 Surface | Research 将 Surface 降为 Main 下钻层 | XHS 六 Surface 的旧结构 | 是：Content Growth default Surface 取哪种表达 |
| Main | selected Professional Surface + Shared Work Area | CEO Operating Result 作为某个 selected Surface / projection | Research 写成固定驾驶舱且 Surface 仅下钻 | 全局 CEO Dashboard / 固定 Domain cockpit | 是：仅确认 Domain scoped default，不改 Main 全局语义 |
| XHS / Douyin | Domain 内平台 Channel；账号另为 Channel Account | Content Growth 多渠道 Workspace 中的 Channel modules | “XHS Workspace”简称可能与 Channel 混淆；Douyin Instance 未批准 | 平台=Workspace / Tab | 是：是否统一实例命名以避免双重语义 |
| 8 States | 无 Current Runtime Schema 授权 | Internal Research Model | 研究称“系统合同”但未进入 Current Authority | 作为固定 UI 状态/Runtime enum | 否，除非未来 Product Delta 要消费 |
| 4 Buckets | 无 Current Product Authority | CEO Projection Model | 研究层认知压缩，不是产品对象 | 作为导航或独立页面 | 否，除非未来 IA Review 要消费 |

## F. Direct answers to requested questions

### A. Current Authority 中六个词的准确语义

见 §A.1：Business 是 canonical 业务身份；Workspace 是独立经营环境；Office 不是当前正式产品身份；Professional Workspace 是 Workspace 的产品形态；Surface 是 Workspace 专业工作面；Main 是 selected Surface + Shared Work Area。

### B. `Office = Workspace` 是否已授权？

**没有。禁止建立等式。** Content Growth 应消费 Workspace canonical identity。Office 当前只能作为 Domain/实现历史标签，不能继续主导用户 IA。`OfficeAccountBinding` 等旧对象的迁移必须另行形成 Runtime / Schema Delta，本轮不猜测映射。

### C. Content Growth 作为 Professional Workspace 是否一致？

**模型上相容，权威上仍是 Accepted Candidate。** Product Blueprint 接受 Professional / Generic Workspace 形态；Content Growth Research 和 XHS Instance 文档证明了专业 Workspace 的候选结构，但没有把某个 Content Growth 实例升级为 Current Verified Professional Workspace。

### D. XHS / Douyin 作为 Channel 是否一致？

**在 Content Growth Domain Authority 内一致。** `CHANNEL_NE_ACCOUNT`、Channel Account 与 per-account Publication 真相已冻结。它们不因此成为全局业务类型，也不意味着 XHS/Douyin 是 Workspace identity。XHS Workspace 实例简称需与平台 Channel 明确分开；Douyin UI Instance 仍未批准。

### E. Main 的两种语义是否冲突？

不是不可组合，而是**当前规则与 Domain 研究默认值尚未对齐**。最小兼容表达是：

> `Main = selected Professional Surface + Shared Work Area`；对 Content Growth 而言，`CEO Operating Result` 可以成为一个默认选中的 Professional Surface / projection。

这不重新定义 Main，也不创建第二套 Dashboard / Truth。但要把它写成 Current Rule，仍需 CEO 选择是否接受该 Domain-scoped default；研究中的“Professional Surface 仅下钻层”不能直接覆盖 Shared Main Contract。

### F. 8 Operating States / 4 Cognitive Buckets 属于哪一层？

- **8 Operating States：Internal Research Model**，可作为后续行为投影候选；不是 Product Authority，也不是 Runtime Schema。
- **4 Cognitive Buckets：Projection Model**，用于压缩 CEO 第一眼体验；不是 Product Authority、导航或页面对象。

两者当前都属于 Research / Accepted Candidate，不得因 Red-Team closure 的“RESOLVED”字样直接升级为 Current Truth。

## G. CEO Decision Required（最多三个）

1. 是否确认：**Workspace 是 Content Growth 唯一 canonical user/product identity；Office 在 Domain Authority 中降为历史/实现迁移术语，不再与 Workspace 并列**？
2. 是否确认：**Content Growth 是一个 Professional Workspace candidate；XHS / Douyin 只作为其 Channel（平台）与 Channel Account 语义，不把平台名当 Workspace identity**？
3. 是否确认：**Content Growth 的 CEO Operating Result 可作为 Main 中默认选中的 Professional Surface / projection**，同时保持全局 `Main = selected Professional Surface + Shared Work Area` 不变？

在三个问题获得明确决定前，不进入 IA，不修改任何 Authority。8 态 / 4 桶继续作为研究材料保留，暂不要求 CEO 现在把它们升级为 Product Truth。

## STOP STATE

CONTENT_GROWTH_PRE_IA_AUTHORITY_RECONCILIATION
— CURRENT TRUTH / CANDIDATE / CONFLICT / DEPRECATED SEPARATED
— OFFICE ≠ WORKSPACE NOT AUTHORIZED
— CHANNEL BOUNDARY EXPLICIT
— MAIN CONFLICT NARROWED TO DOMAIN DEFAULT
— 8 STATES / 4 BUCKETS NOT PROMOTED
— STOP FOR CEO REVIEW

**AUTHORITY BLOCKER STILL OPEN**
