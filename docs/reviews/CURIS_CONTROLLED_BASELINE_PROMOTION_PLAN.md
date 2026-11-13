# CURIS CONTROLLED BASELINE PROMOTION PLAN

> **Authority Class:** REVIEW / PLAN
>
> **Status:** Review
>
> **Date:** 2026-09-13
>
> **Source:** `docs/reviews/RECENT_UNREGISTERED_ACCEPTED_TRUTH.md` + current Git/diff/reference inspection
>
> **Disposition:** READY FOR CEO / CHATGPT REVIEW — NO STAGE / COMMIT / PUSH AUTHORIZED

## 0. Decision summary

Curis 不需要第二个 Manifest 或 Development Pointer。应把现有 `AGENTS.md → PRODUCT_DOCUMENT_POINTER.md → CURRENT_STATE.md` 路线固化为 Git 可恢复基线。

当前文件不能直接批量提交：Pointer 的可解析本地引用中有 86 个目标仍 untracked；CURRENT_STATE、Pointer、Product Blueprint、Product Context、Company OS Shared Authority 与 Change Log 都包含跨多个时期的大型 mixed diff。安全方案是先提交被入口消费的 Current leaf authorities，再提交 Professional Business，再提交最小 Accepted Implementation Evidence，最后提交经过 hunk review 的入口与登记文件。

### Minimum target

- **32 个 live files**。
- **2 个旧 canonical path deletion/rename operations**：旧 versioned Master Map 与 UI Blueprint 路径和新 canonical 文件必须在同一 commit 中处理。
- **4 个 baseline commits**。
- Research 如以后需要保存，只能作为独立第 5 个 Research commit；不计入 Product Truth baseline。

这 32 个文件是“Product + Development 当前路线可恢复”的最小闭包，不是全部 Accepted 历史，也不包含截图、数据库、构建产物或所有底层测试证据。

---

## 1. Current Git truth

| Item | Current fact |
|---|---|
| Branch | `main` |
| HEAD | `bb72916daba3ae9555914d03bdb7fcea9953ab9c` |
| HEAD time | `2026-09-04T17:29:49+08:00` |
| Staged | 0 |
| Modified | 129 |
| Deleted | 2 |
| Untracked (`-uall`), before creating this required plan | 1,426 |
| Total status paths (`-uall`), before creating this required plan | 1,557 |
| Untracked / total after creating this required plan | 1,427 / 1,558；唯一增量是本计划文件 |

上一轮报告的 623 untracked / 754 total 使用目录折叠的普通 status 口径；本轮按要求使用 `-uall` 展开目录内每个文件。两者不是状态反转。

硬规则：禁止 `git add .`、`git add -A`、目录级 bulk add。未来每次 stage 都必须使用本计划列出的精确路径，并在独立临时 index 或等价可审查方式中验证。

---

## 2. Inclusion semantics

| Include | Meaning |
|---|---|
| YES | 当前内容职责单一，建议进入指定 baseline commit；执行前仍需 diff/read check |
| REVIEW | 属于 minimum target，但当前存在 mixed diff、pending disposition 或 stale clause；先完成指定人工 review/窄修，再纳入 |
| NO | 不属于 Minimum Recoverable Product Truth Baseline；保留在 working tree，必要时另行 Research/Evidence commit |

“REVIEW”不是建议丢弃；表示**禁止原样 whole-file stage**。

---

## 3. File classification table

### Commit A — Canonical Product Structure + Frozen Shared Authority

这个 commit 必须原子提交。Product Blueprint/UI Blueprint/Shared Authority/Structure Baseline 彼此引用，拆开会产生中间 checkout 的 missing authority。

| File | Git State | Authority | Why Needed | Target Commit | Include? | Risk |
|---|---|---|---|---|---|---|
| `docs/01_Product/Curis_Product_Blueprint.html` | modified | Current Product Authority / Frozen | 唯一 Product Blueprint | A | REVIEW | 691-line diff；含历史与 Current 修订；提交前需 Current stale/implementation wording scan |
| `docs/01_Product/Curis_Product_Master_Map_v2.0.md` | deleted | Old canonical path | 与新 canonical path 构成治理上的 rename/replacement | A | YES | 必须与新文件同 commit；不可单独提交删除 |
| `docs/01_Product/Curis_Product_Master_Map.md` | untracked | CURRENT / PRODUCT STRUCTURE AUTHORITY / Frozen | 当前 canonical Master Map v3.2 | A | REVIEW | 相对 HEAD 旧文件为 209 additions / 2072 deletions；Git 可能显示 delete+add；需确认 Current 段无旧 account/workspace 语义冲突 |
| `docs/01_Product/Curis_Product_UI_Blueprint_v1.0.html` | deleted | Old canonical path | 与新 canonical path 构成治理上的 rename/replacement | A | YES | 必须与新文件同 commit；不可形成第二份 Current UI Blueprint |
| `docs/01_Product/Curis_Product_UI_Blueprint.html` | untracked | CURRENT / FROZEN / FINAL ACCEPTED | 当前唯一 UI Blueprint | A | REVIEW | 相对 HEAD 旧文件为 327 additions / 1490 deletions；仍含 Knowledge/Meeting implementation-pending 等可能被 CURRENT_STATE supersede 的文字 |
| `docs/01_Product/Curis_Product_Context.md` | modified | Product module entry | AGENTS Module Routing 和 Pointer 的产品语境入口 | A | REVIEW | 129-line mixed diff；需确认只保留 Current Product Context，不把 Runtime checkpoint写成 Product Truth |
| `docs/01_Product/CURIS_PRODUCT_STRUCTURE_BASELINE_PRE_DESIGN_RESEARCH.md` | untracked | CURRENT / PRODUCT STRUCTURE AUTHORITY / Frozen | 设计研究前唯一结构集中基线 | A | REVIEW | Disposition 仍为 pending CEO/ChatGPT review；正式 promotion 前必须先固化本次 CEO disposition，不得猜测 Accepted |
| `docs/reviews/CURIS_CORE_PRODUCT_AUTHORITY_REPAIR.md` | untracked | CURRENT / ACCEPTED CEO scoped amendment | Product Blueprint、Master Map、UI Blueprint、Shared Authority 的直接修订依据 | A | YES | 不是第二 Product Truth；必须保持 scoped amendment 身份 |
| `docs/03_Design/Curis_Company_OS_Shared_Authority.md` | modified | Frozen Shared Authority | Company / organization / responsibility shared truth | A | REVIEW | 242-line mixed diff；需确认旧 Office/optional Department/implementation状态只作 provenance |
| `docs/03_Design/Curis_Workspace_Shell_Contract_And_Shared_Patterns.md` | untracked | Frozen Shared Authority | Four-Pane、Employee、Conversation、Composer、UI-state independence 的唯一 shared truth | A | YES | 文件较长但职责单一；须以 current top/Frozen deltas为准，不拆 shared contract |
| `docs/03_Design/CURIS_VISUAL_STANDARD_V1.md` | untracked | FROZEN / DESIGN | 当前 Visual Language：Direction D / Iris `#806BE5` | A | YES | Product Composition 未冻结；不可把此文件扩大成页面布局 authority |

Commit A 统计：**9 live files + 2 old-path deletion operations**。

### Rename adjudication

- Master Map：**canonical rename + substantial in-place product upgrade**，不是独立第二文件。
- UI Blueprint：**canonical rename + substantial in-place UI authority upgrade**，不是独立第二文件。
- 执行时应同时 stage 旧路径 deletion 与新路径 content，让最终 tree 只有无版本号 canonical path。
- 即使 Git 因相似度不足显示 delete/add，Change Log 和 commit message 也必须登记其治理语义为 rename/replacement，而非新建第二份 Current。

### Commit B — Professional Business Authorities

Commit B 依赖 A，不能先于 A。它只固化当前合法 domain/instance truth，不带旧 XHS/Office prototype。

| File | Git State | Authority | Why Needed | Target Commit | Include? | Risk |
|---|---|---|---|---|---|---|
| `docs/03_Design/Curis_Content_Growth_Domain_Authority.md` | modified | Frozen Domain Authority | Content Growth、Channel、Channel Account、Workspace identity 当前真源 | B | REVIEW | 51-line diff；必须确认 Office 仅 provenance、Content Growth 仍为 Candidate |
| `docs/reviews/CONTENT_GROWTH_CEO_AUTHORITY_DECISION_RECONCILIATION.md` | untracked | Review / CEO decision reconciliation | 解释 Office退出、Main projection、Channel边界的 supersession | B | YES | 不能升级为独立 Product Authority |
| `docs/03_Design/Curis_Content_Growth_Operating_Strategy_UX_Translation.md` | untracked | Accepted UX Translation | Domain Authority 到 UX 的必要 translation | B | YES | 只能消费 Shared/Domain Authority；8 states/4 buckets 不得升格 |
| `docs/03_Design/Curis_RD_Workspace_Instance_Spec_v1.md` | untracked | RD INSTANCE APPROVED | 当前 RD domain/instance anatomy | B | REVIEW | 含已被 Frozen Shell supersede 的 default expand/collapse 与旧 Compact Composer；原样提交会误导新 Agent |
| `docs/03_Design/Curis_RD_Design_Phase_Closeout_2026-08-15.md` | untracked | Accepted design closeout / evidence | 证明 RD instance disposition 与责任语义来源 | B | YES | 只作 closeout，不覆盖 Frozen Shell 或 Current Runtime |

Commit B 统计：**5 live files**。

#### RD pre-promotion rule

在未来 stage 前，必须二选一并由 CEO/Authority Owner确认：

1. 在 RD Instance Spec 顶部加入一条窄幅 supersession note，明确所有 shared UI rules 以 Frozen Shell 为准；或
2. 对冲突段做 hunk cleanup，仅保留 RD domain/object anatomy。

不能只在 commit message 解释；新 Agent 打开文件本身就必须看到 supersession。不得因此重新设计 RD。

### Commit C — Minimum Accepted Implementation Evidence

Commit C 依赖 A；涉及 Professional Workspace 的引用同时依赖 B。这里只保留 CURRENT_STATE 顶部重要 claims 的最短可追溯链。截图、SQLite、构建产物和所有底层专项证据不进入此 commit。

| File | Git State | Authority | Why Needed | Target Commit | Include? | Risk |
|---|---|---|---|---|---|---|
| `docs/reviews/CURIS_CANONICAL_EXECUTION_SCOPE_RECONCILIATION_REVIEW.md` | untracked | Review / Current Implementation Evidence | 四层 canonical execution scope 顶部 Current claim | C | YES | Accepted Candidate，不得写成全部四层自主经营已验收 |
| `issues/CURIS-CANONICAL-EXECUTION-SCOPE-RECONCILIATION-001.md` | untracked | Current Implementation Issue | Scope review 的授权、范围、Allowed truth 与证据入口 | C | YES | 保留 pending final review wording |
| `docs/reviews/CURIS_PHASE_B_CORE_PRODUCT_RECONCILIATION_REVIEW.md` | untracked | Review / Current Implementation Evidence | built-in organization、Business activation、Four-Pane、Assistant 的当前集成证据 | C | YES | Accepted Candidate；不等于 release |
| `issues/CURIS-PHASE-B-P0-CORE-PRODUCT-RECONCILIATION-001.md` | untracked | Implementation Issue | Phase B 实施范围和证据归属 | C | YES | 不恢复下方 historical gate为Current |
| `docs/reviews/CURIS_V1_PRODUCT_COMPLETION_RECONCILIATION.md` | untracked | Current Implementation Evidence / reconciliation | 将多项 scoped acceptance 汇总为当前完成边界 | C | REVIEW | 含多代 checkpoint；提交前检查顶部 current section与historical标记 |
| `docs/reviews/CURIS_V1_EXECUTION_BACKLOG.md` | untracked | Current structure/implementation queue | 当前 Next Gate 与未完成边界 | C | REVIEW | 含历史队列；只能保留清晰 Current-first 阅读顺序 |
| `docs/reviews/CURIS_V1_MEETING_ROOM_PRODUCTIZATION_REVIEW.md` | untracked | Current Implementation Registration | Meeting core 当前实现边界 | C | YES | Implementation complete ≠ final real-world multi-cycle acceptance |
| `docs/reviews/CURIS_V1_MEETING_AUTONOMOUS_DISCUSSION_REVIEW.md` | untracked | Review / Accepted Candidate | Meeting autonomy、自然multi-cycle证据边界 | C | YES | 不得夸大为真实外部长期经营已验收 |
| `docs/reviews/CURIS_V1_KNOWLEDGE_LIBRARY_IMPLEMENTATION_ACCEPTANCE.md` | untracked | Frozen Current Implementation Truth | Knowledge current accepted claim | C | YES | Unsupported formats/search/ACL保持 gap |
| `docs/reviews/CURIS_V1_TALENT_CAPABILITY_IMPLEMENTATION_ACCEPTANCE.md` | untracked | Frozen Current Implementation Truth | Talent/Employee/Skill/Avatar current accepted claim | C | YES | Connector未授权与外部Talent仍不冒充可用 |
| `docs/reviews/CURIS_V1_OPERATING_INTELLIGENCE_IMPLEMENTATION_ACCEPTANCE.md` | untracked | Frozen Current Implementation Truth | canonical analytical projection current claim | C | YES | 外部Outcome与自动报告保持 gap |
| `docs/reviews/CURIS_V1_ORGANIZATION_CENTER_IMPLEMENTATION_ACCEPTANCE.md` | untracked | Frozen Current Implementation Truth | canonical organization projection current claim | C | YES | Vacancy/Risk不能推断 |
| `docs/reviews/CURIS_V1_WHOLE_APP_LIVE_AI_ACCEPTANCE_REGISTRATION.md` | untracked | Frozen Implementation Acceptance Record | current whole-app live AI vertical | C | YES | 只覆盖已证明vertical与recorded P1 |
| `docs/reviews/CURIS_V1_CLOUD_AI_CONTINUITY_ACCEPTANCE.md` | untracked | Frozen Implementation Acceptance Record | Keychain/cloud/restart current claim | C | YES | DeepSeek证明architecture链，不等于所有Provider verified |

Commit C 统计：**14 live files**。

### Commit D — Entry, Current State and Governance Registration

Commit D 必须最后提交。这样任何 checkout 到 D 时，Pointer 和 CURRENT_STATE 的 Current route 已有 A–C 的目标文件。

| File | Git State | Authority | Why Needed | Target Commit | Include? | Risk |
|---|---|---|---|---|---|---|
| `AGENTS.md` | modified | Frozen repository governance | 新 Agent 的第一行为入口 | D | YES | 只保留治理与 retrieval，不得重新塞入 current facts |
| `docs/00_Context/PRODUCT_DOCUMENT_POINTER.md` | modified | Current Product/Development router | 唯一文档入口 | D | REVIEW | 474-line diff；当前指向 86 个 untracked targets；必须区分 Current route 与 historical/reference index，不能 whole-file blind stage |
| `docs/00_Context/CURRENT_STATE.md` | modified | Implementation Truth | 新开发会话的实现入口 | D | REVIEW | 631-line diff；Current + historical checkpoint混合；只允许 Current-first并明确supersession |
| `docs/08_Change_Log/CHANGE_LOG.md` | modified | Change History | 登记 canonical rename、Authority、evidence与entry promotion | D | REVIEW | 243-line diff；只纳入与A–D对应的已有变更记录，不夹带未验收Research/Prototype disposition |

Commit D 统计：**4 live files**。

### Total

| Group | Live files | Deletion/rename path operations |
|---|---:|---:|
| A — Product + Shared | 9 | 2 |
| B — Professional Business | 5 | 0 |
| C — Minimum Implementation Evidence | 14 | 0 |
| D — Entry / Current State / Change Log | 4 | 0 |
| **Total** | **32** | **2** |

---

## 4. Evidence not in minimum baseline

### USEFUL — separate Evidence commit later

以下有价值，但不影响最小 Product/Development route 成立：

| File / set | Classification | Why not required now |
|---|---|---|
| `docs/reviews/CURIS_V1_GLOBAL_UI_SEVEN_AREA_FINAL_ACCEPTANCE.md` + matching Issue | USEFUL | 已被 2026-09-09 Phase B/current structure收窄为 historical scoped checkpoint |
| General Workspace Lifecycle Issue/Review | USEFUL | Whole-App + Phase B + Product Completion 已提供当前最小链；详细 lifecycle证据可另存 |
| Conversation Attention Issue/Review | USEFUL | 同上；不是 Product Authority |
| App Entry、CEO Desk、Organization、Insights、Knowledge、Meeting 的 UI Acceptance docs | USEFUL | UI Blueprint已登记Current设计基线；详细视觉验收不影响结构基线恢复 |
| RD implementation Issue/Review | USEFUL | 本 baseline只需 RD instance truth + closeout；Current Runtime按CURRENT_STATE读取 |
| Content Growth Channel Capability / Autonomy audits | USEFUL | Capability/guardrail专项证据，不是Domain Product Authority |
| `CURIS_V1_CURRENT_UI_FOUNDATION.md` | USEFUL | 当前 UI structure已由UI Blueprint + Shell + Visual Standard承载 |
| Three-document consistency / recovery / historical audit reports | USEFUL | 解释形成过程，不是运行Current route的必要文件 |

这些文件若要保存，应按 Evidence ownership 分批，不得与 Commit A/B 混合。

### DEFER / NO — not Product Truth baseline

| File / directory | Include? | Reason |
|---|---|---|
| `docs/research/system_competitive_research/` | NO | Research / Evidence；其中仍有旧六区和视觉权威混用 |
| `docs/prototypes/full-product-html/` | NO | READY FOR REVIEW Prototype；包含fixture、模拟状态和stale输入 |
| Pixel Reference / Page Reference Blueprint | NO | Research reference，不是 Product Authority |
| Zcode inventories | NO | competitor/self inventory，不是 Curis Current Truth |
| Prototype screenshots | NO | Design evidence；不构成 authority或runtime evidence |
| `docs/reviews/RECENT_UNREGISTERED_ACCEPTED_TRUTH.md` | NO | 本次 audit evidence；可单独 governance commit，但不属于baseline nucleus |
| `docs/reviews/CURIS_CONTROLLED_BASELINE_PROMOTION_PLAN.md` | NO | Promotion plan；CEO接受后可单独保存，不得与被规划的baseline混为一体 |
| `docs/reviews/CURIS_CORE_PRODUCT_TRUTH_LEDGER.md` | NO | Review / CEO Review Required；不是入口 |
| `docs/04_Development/CURIS_MASTER_DEVELOPMENT_STATE_2026-09-03.md` | NO | 旧时间点Draft snapshot，已由CURRENT_STATE和后续review覆盖 |
| `PROJECT_HANDOFF.md` / `frontend/docs/FRONTEND_HANDOFF.md` | NO | Deprecated或旧专项handoff |

---

## 5. HUNK REVIEW REQUIRED

### 5.1 Modified mixed files

以下文件禁止 whole-file blind stage：

1. `docs/00_Context/PRODUCT_DOCUMENT_POINTER.md`
   - Current顶部、历史checkpoint、长索引和86个untracked引用混在同文件。
   - 只保留一个Current-first route；非baseline文件必须明确为Research/History/Deferred，不能作为必读链接。
   - Promotion gate：Current route的本地引用在临时 checkout 中全部存在。

2. `docs/00_Context/CURRENT_STATE.md`
   - 631行新增、多个日期checkpoint和已supersede状态混合。
   - 必须确认顶部Current结论覆盖旧blocker；不能让“implementation pending/partial”在无历史标签下重新成为Current。

3. `docs/08_Change_Log/CHANGE_LOG.md`
   - 只纳入已经发生且属于A–D的记录。
   - Research complete、Prototype ready或计划本身不能写成Accepted Product Truth。

4. `docs/01_Product/Curis_Product_Blueprint.html`
   - 大型重构diff必须按Current sections复核。
   - Product Truth可描述产品能力；implementation状态一律路由CURRENT_STATE。

5. `docs/01_Product/Curis_Product_Context.md`
   - Product语义与旧Bootstrap/Assistant/Workspace Studio路径混合修改，需要逐hunk确认。

6. `docs/03_Design/Curis_Company_OS_Shared_Authority.md`
   - 旧Office、长期Workspace、Department/Business关系与新增组织语义混合。

7. `docs/03_Design/Curis_Content_Growth_Domain_Authority.md`
   - 确认只把Office留作provenance，且不将Channel/Account写成Workspace。

### 5.2 Untracked current files requiring content review

untracked 不代表可以 whole-file直接添加：

- `CURIS_PRODUCT_STRUCTURE_BASELINE_PRE_DESIGN_RESEARCH.md`：pending CEO/ChatGPT disposition。
- `Curis_Product_Master_Map.md`：顶部supersession与正文旧account/workspace例句需一致。
- `Curis_Product_UI_Blueprint.html`：旧implementation-pending段须明确由CURRENT_STATE supersede。
- `Curis_RD_Workspace_Instance_Spec_v1.md`：必须先处理Frozen Shell supersession。
- `CURIS_V1_PRODUCT_COMPLETION_RECONCILIATION.md` / `CURIS_V1_EXECUTION_BACKLOG.md`：Current-first与historical边界检查。

---

## 6. STALE_INPUT_HANDLING_PLAN

本阶段不执行下列修正。

| Stale input | Current location | Planned handling | Delete? |
|---|---|---|---|
| 旧六区 | `CURIS_CURRENT_UI_AUDIT.md` D代描述 | 文件Header/段落标 `HISTORICAL IMPLEMENTATION OBSERVATION — CURRENT NAVIGATION IS SEVEN AREAS` | NO |
| `#32f08c` 旧视觉真源 | `CURIS_UI_EVIDENCE_CATALOG.md`、prototype tokens | 改为 `LEGACY IMPLEMENTATION TOKEN`；指向 `CURIS_VISUAL_STANDARD_V1.md`；保留实际代码债务事实 | NO |
| 重新打开 Iris 决策 | HTML Prototype Review §5 | 加 `SUPERSEDED — #806BE5 FROZEN`; 只保留prototype质量review | NO |
| 旧 RD shared UI rules | RD Instance Spec | 顶部supersession note或窄幅删除冲突shared clauses；明确Shell优先 | NO |
| 旧 Compact Composer | RD Instance Spec / copied prototype | 指向Frozen Composer slots；RD只保留domain-specific extension | NO |
| 旧 XHS / Office fixture | `PROFESSIONAL_BUSINESS_EXISTING_TRUTH.md` | 标 `HISTORICAL DESIGN FIXTURE`; identity改由Content Growth Domain Authority路由 | NO |
| Employee `done` | prototype `js/components.js` | 在Prototype后续cleanup中改为Work/Result状态；Employee投影只用三态 | NO |
| 旧 RD reliability状态 | `PROFESSIONAL_BUSINESS_EXISTING_TRUTH.md` | 标 `HISTORICAL / SUPERSEDED BY CURRENT_STATE ACCEPTED/CLOSED` | NO |
| 旧 versioned Master/UI filenames | tracked old paths | 与canonical新路径同commit记录rename/replacement；最终tree只保留canonical文件名 | Path replaced, content not deleted |

Archive只适用于完整历史资产且引用扫描通过的后续治理任务。本计划不建议为了“干净”移动或删除仍有provenance价值的文件。

---

## 7. Commit plan and dependencies

```text
A  Canonical Product Structure + Frozen Shared Authority
   ↓
B  Professional Business Authorities
   ↓
C  Minimum Accepted Implementation Evidence
   ↓
D  AGENTS + Pointer + CURRENT_STATE + Change Log
```

### Commit A

Suggested message: `docs(authority): establish canonical product and shared baseline`

Gate:

- 9 live files + 2 rename/deletion operations only。
- canonical HTML parse passes。
- Master/UI old path引用扫描完成。
- Product/Shared stale scan通过。

### Commit B

Suggested message: `docs(domain): register current content growth and rd authorities`

Gate:

- Commit A exists。
- RD supersession visible inside RD file itself。
- no Office/XHS identity resurrection。
- no fixed domain workflow promoted into Core。

### Commit C

Suggested message: `docs(evidence): preserve minimum current implementation traceability`

Gate:

- Commits A/B exist。
- 14 exact evidence files only。
- Every verdict preserves Accepted vs Accepted Candidate vs remaining gap。
- no DB/build/screenshots/generated artifacts。

### Commit D

Suggested message: `docs(governance): point agents to recoverable current truth`

Gate:

- A–C checkout contains every Current required target。
- Pointer Current route has zero missing targets。
- CURRENT_STATE headline claims map to included acceptance records。
- historical/deferred links cannot appear as mandatory Current input。
- `git diff --check` and clean-clone link check pass。

### Optional Commit E — Research

Not part of this baseline. Only after separate CEO disposition and stale-input cleanup:

`docs(research): preserve competitive research inputs`

它不得与 A–D squash，也不得改变 Pointer Current route 或视觉/产品 Authority。

---

## 8. Execution procedure for a future authorized phase

本节是计划，不是当前授权。

1. 记录当前 branch、HEAD、full `git status -uall` 和保护DB指纹；不读secret。
2. 使用临时 index / exact path list 构造 Commit A candidate；绝不修改真实index直到明确授权。
3. 对所有 REVIEW 文件完成逐hunk/逐section核对；发现Authority冲突立即STOP。
4. 从candidate tree执行HTML parse、Markdown/local-link scan、旧canonical path scan、stale-term scan与`git diff --check`。
5. A通过后依次构造B、C、D；每一步都以父commit的临时checkout检查。
6. D完成后从最终candidate commit创建新的clean checkout，严格执行：
   `AGENTS.md → PRODUCT_DOCUMENT_POINTER.md → Product/Shared` 与
   `AGENTS.md → PRODUCT_DOCUMENT_POINTER.md → CURRENT_STATE.md → Accepted Evidence`。
7. 只有上述闭包通过，才可请求真正stage/commit授权；push另走独立Gate。

---

## 9. Required answers

### A. Minimum Recoverable Product Truth Baseline 一共有多少文件？

**32个live files，加2个旧canonical path的rename/deletion operations。**

其中：Product + Shared 9、Professional Business 5、Implementation Evidence 14、Entry/Governance 4。

### B. 分成几个commit最安全？

**4个baseline commits。** Research如保留是独立可选第5个，不属于baseline。

### C. 哪些文件必须先人工hunk review？

必须人工review：Pointer、CURRENT_STATE、CHANGE_LOG、Product Blueprint、Product Context、Company OS Shared Authority、Content Growth Domain Authority；另对untracked的Structure Baseline、Master Map、UI Blueprint、RD Instance Spec、Product Completion、Execution Backlog做完整内容review。RD Spec和Pointer是硬Stop Gate。

### D. 哪些untracked Accepted/Frozen文件其实不应该进入当前baseline？

详细UI acceptance、General/Conversation/Global Seven-area旧scoped evidence、RD implementation长证据、Content Growth capability/autonomy audits、三文档历史审计、Current UI Foundation、Research、Prototype、screenshots都不进入minimum baseline。它们可保留为USEFUL/DEFER并以后按Evidence/Research独立提交。

### E. 哪些旧文件需要supersession标记，但不应删除？

近期Research中的六区与旧绿色视觉权威、RD Instance的旧展开规则/Compact Composer、Prototype的旧XHS/Office fixture与Employee done、旧RD reliability文字，均应加supersession/historical标记并保留provenance。旧versioned Master/UI是canonical rename path，内容由新路径继承，不属于删除历史文档。

### F. 完成这些commit后，clean checkout能否可靠恢复Current Curis Truth？

**可以，但必须满足两个条件：**

1. 所有REVIEW项先完成窄幅content/hunk review，尤其RD Spec、Pointer、CURRENT_STATE；
2. 最终clean checkout的Current link closure为0 missing，且D最后提交。

如果原样whole-file提交当前Pointer/CURRENT_STATE，或跳过A–C先提交D，答案仍然是**不能**。

---

## 10. Stop state

- No files staged。
- No commit created。
- No push performed。
- No reset / restore / clean / rename / delete performed。
- No Product Authority / Pointer / CURRENT_STATE modified。

**CURIS CONTROLLED BASELINE PROMOTION PLAN — READY FOR CEO / CHATGPT REVIEW**
