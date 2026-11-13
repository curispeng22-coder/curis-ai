# CURIS RECENT PRODUCT TRUTH & DEVELOPMENT BASELINE CHECK

> **Authority Class:** REVIEW / EVIDENCE
>
> **Status:** Review
>
> **Date:** 2026-09-13
>
> **Scope:** 只读增量审计；不修改 Product Authority、实现、Prototype 或 Figma
>
> **Disposition:** STOP FOR CEO / CHATGPT REVIEW

## 0. Executive verdict

Curis **已经存在产品与开发工作的统一治理入口**，无需创建第二份 Manifest 或 `CURIS_DEVELOPMENT_BASELINE_POINTER.md`。

- Repository 行为入口：`/Users/yy/Documents/Curis AI Workspace/AGENTS.md`
- 唯一产品/开发文档入口：`/Users/yy/Documents/Curis AI Workspace/docs/00_Context/PRODUCT_DOCUMENT_POINTER.md`
- Implementation Truth 入口：`/Users/yy/Documents/Curis AI Workspace/docs/00_Context/CURRENT_STATE.md`
- 当前产品结构基线：`/Users/yy/Documents/Curis AI Workspace/docs/01_Product/CURIS_PRODUCT_STRUCTURE_BASELINE_PRE_DESIGN_RESEARCH.md`

这个机制在**当前 dirty working tree 的内容层面仍然有效**，但尚未形成 Git 可恢复基线：当前 `main` 的 HEAD 停在 2026-09-04，而 2026-09-10 的结构基线、canonical Master Map / UI Blueprint、Frozen Shell、Visual Standard 与大量 Accepted Review 仍为 untracked 或 unstaged。新 Agent 在这台机器的当前目录中能够找到新 Truth；从 clean checkout、另一台机器或只看 Git history 时会回到旧入口/旧文件名，存在实质误读风险。

本次没有发现 2026-09-10 结构基线之后新增且已经 CEO Accepted / Frozen、却完全没有登记的 Product Truth。9 月 12 日新增内容均为 `RESEARCH / EVIDENCE` 或 `READY FOR CEO / CHATGPT REVIEW`，不得登记为 Current Authority。

---

## 1. Existing entry-point candidates

| 当前主入口候选 | 实际职责 | Authority / Status | 更新时间或边界 | 是否仍有效 |
|---|---|---|---|---|
| `AGENTS.md` | 所有 Agent 的最小仓库规则；规定按任务类型读取 Pointer 或 CURRENT_STATE | Repository governance；`Status: Frozen` | 文件 mtime 2026-08-18；当前有 unstaged 修改 | **有效，但不是 Product Truth 本体** |
| `docs/00_Context/PRODUCT_DOCUMENT_POINTER.md` | Current Product Truth、Frozen Authority、Implementation evidence 与专项入口的统一 router | `CURRENT / PRODUCT STRUCTURE AUTHORITY`；顶部 `Status: Frozen` | 顶部 Current 条目 2026-09-10；unstaged modified | **唯一推荐文档入口** |
| `docs/00_Context/CURRENT_STATE.md` | 当前实现、Accepted evidence、Product → Implementation Gap | `CURRENT / IMPLEMENTATION EVIDENCE`，并含结构登记 | 顶部 Current 条目 2026-09-10；unstaged modified | **有效；仅用于 Implementation Truth** |
| `docs/01_Product/CURIS_PRODUCT_STRUCTURE_BASELINE_PRE_DESIGN_RESEARCH.md` | 设计研究前的集中产品结构基线；约束 Design Research / Final UI Master / Frontend Reconciliation | `CURRENT / PRODUCT STRUCTURE AUTHORITY`；`Status: Frozen`；`RECORDED / PENDING CEO–CHATGPT PRODUCT STRUCTURE REVIEW` | Effective 2026-09-10；untracked | **有效的当前结构边界，但仍待 CEO/ChatGPT Review，且不可由 clean checkout 恢复** |
| `docs/reviews/CURIS_CORE_PRODUCT_TRUTH_LEDGER.md` | 产品真相盘点/修复证据 | REVIEW / EVIDENCE；CEO Review Required | 2026-09-09；untracked | **不是入口** |
| `docs/04_Development/CURIS_MASTER_DEVELOPMENT_STATE_2026-09-03.md` | 2026-09-03 的实现快照 | EVIDENCE / CURRENT snapshot；`Status: Draft` | 快照时 HEAD `c797db840` | **历史开发快照，不是当前入口** |
| `docs/reviews/CURIS_CODEX_MASTER_DEVELOPMENT_RECOVERY_2026-09-05.md` | 主开发恢复事故、Git 与 Meeting 边界证据 | REVIEW / EVIDENCE | 已识别当前 HEAD `bb72916d…` | **专门恢复记录，不是入口** |
| `PROJECT_HANDOFF.md` | 2026-07 临时团队交接 | `Status: Deprecated` | 2026-07-08 | **失效；不得作为新会话入口** |
| `frontend/docs/FRONTEND_HANDOFF.md` | 2026-08-05 前端专项交接 | 历史专项 handoff | 2026-08-05 | **不是仓库级入口** |

### Entry-point decision

新 Agent / Codex / Zcode 的最短合法读取顺序是：

1. `AGENTS.md`：先确定任务类型和停止条件。
2. `docs/00_Context/PRODUCT_DOCUMENT_POINTER.md`：作为唯一文档路由入口。
3. 产品任务按 Pointer 进入 Product Blueprint → Master Map → UI Blueprint → applicable Frozen Authority；开发任务转入 `CURRENT_STATE.md` → active Issue / Approved Design → Accepted Review → Code / Runtime / Evidence。

不存在需要新建的并列 Development Pointer。当前问题不是“没有入口”，而是“入口及其所指向的 Current 文件没有进入可恢复 Git baseline”。

---

## 2. Incremental audit boundary

### 2.1 Git-recoverable boundary

- Branch: `main`
- HEAD: `bb72916daba3ae9555914d03bdb7fcea9953ab9c`
- Commit time: `2026-09-04T17:29:49+08:00`
- Commit: `fix(meeting): 门控后 speaker/leader 调用复检全局 budget，闭合硬约束 #5/#6`

这是最后一个可由 Git 直接恢复的边界，但它早于当前 Product Structure consolidation。

### 2.2 Current working-tree product boundary

- Boundary: `CURIS_PRODUCT_STRUCTURE_BASELINE_PRE_DESIGN_RESEARCH.md`
- Effective: 2026-09-10
- Authority: `CURRENT / PRODUCT STRUCTURE AUTHORITY`
- Status: Frozen
- Disposition: `RECORDED / PENDING CEO–CHATGPT PRODUCT STRUCTURE REVIEW`

本次增量审计以该 2026-09-10 内容边界为起点，只检查其后的 9 月 12 日 system competitive research 与 full-product HTML prototype，同时检查这些内容引用的 Product / Professional Workspace 输入。该边界是工作树中的 Current 结构记录，不是 clean committed baseline。

---

## 3. Git state and recoverability

审计时只读核验结果：

| 项目 | 当前事实 |
|---|---|
| Branch | `main` |
| HEAD | `bb72916daba3ae9555914d03bdb7fcea9953ab9c` |
| Staged | 0 |
| Working-tree entries | 754 |
| Modified | 129 |
| Deleted | 2 |
| Untracked | 623 |
| Untracked docs with acceptance/freeze markers | 74（文本标记扫描；表示风险集合，不等于逐份重新验收） |

关键 canonical 文件状态：

| 文件 | Git 状态 | 风险 |
|---|---|---|
| `docs/00_Context/PRODUCT_DOCUMENT_POINTER.md` | modified, unstaged | Current router 只存在于本机 working tree 的新内容 |
| `docs/00_Context/CURRENT_STATE.md` | modified, unstaged | 最新 Implementation Truth 不可从 HEAD 恢复 |
| `docs/01_Product/Curis_Product_Blueprint.html` | modified, unstaged | Current Product Blueprint 与 HEAD 不一致 |
| `docs/01_Product/Curis_Product_Master_Map_v2.0.md` | deleted, unstaged | 旧 tracked canonical 名仍存在于 HEAD |
| `docs/01_Product/Curis_Product_Master_Map.md` | untracked | 新 canonical Current 文件不在 HEAD |
| `docs/01_Product/Curis_Product_UI_Blueprint_v1.0.html` | deleted, unstaged | 旧 tracked canonical 名仍存在于 HEAD |
| `docs/01_Product/Curis_Product_UI_Blueprint.html` | untracked | 新 canonical Current 文件不在 HEAD |
| `docs/01_Product/CURIS_PRODUCT_STRUCTURE_BASELINE_PRE_DESIGN_RESEARCH.md` | untracked | 当前结构基线不在 HEAD |
| `docs/03_Design/Curis_Workspace_Shell_Contract_And_Shared_Patterns.md` | untracked | Frozen Shell 不在 HEAD |
| `docs/03_Design/CURIS_VISUAL_STANDARD_V1.md` | untracked | Current Visual Language 不在 HEAD |
| `docs/03_Design/Curis_Content_Growth_Domain_Authority.md` | modified, unstaged | 最新 Content Growth identity reconciliation 不在 HEAD |

### Git conclusion

**存在“已经 Frozen / Accepted / Current，但没有 commit，导致新 Agent 在 clean checkout 中搜索不到或误读旧版本”的情况。** 这不是新的 Product Authority 冲突，而是 baseline promotion / provenance 风险。解决它需要以后由正式集成 Owner 在完整 ownership、Allowed Files、diff、测试和 commit gate 下收口；本审计不 add、commit 或改写文件。

---

## 4. Recent accepted truth not safely registered

| 内容 | 当前文件 | 确认证据 | Git 状态 | 当前入口是否登记 | 应登记到哪里 |
|---|---|---|---|---|---|
| Pre-Design-Research Product Structure Baseline | `docs/01_Product/CURIS_PRODUCT_STRUCTURE_BASELINE_PRE_DESIGN_RESEARCH.md` | `CURRENT / PRODUCT STRUCTURE AUTHORITY`、`Status: Frozen`、2026-09-10；仍写明 pending CEO/ChatGPT review | untracked | **已登记**：Pointer / CURRENT_STATE 顶部 | 不新建入口；待 CEO Review 后由受控 Git baseline closure 固化 disposition 与 provenance |
| Canonical Master Map / UI Blueprint 文件名治理 | `docs/01_Product/Curis_Product_Master_Map.md`；`docs/01_Product/Curis_Product_UI_Blueprint.html` | Current 文档正文与 Pointer 已采用 canonical path；旧 versioned path 已退出 working tree | 新文件 untracked；旧 tracked 文件 deleted | **已登记** | 继续由现有 Pointer 管理；需要受控 rename/promotion commit，不能只留 working-tree rename |
| Frozen Shell / Current Visual Standard | `docs/03_Design/Curis_Workspace_Shell_Contract_And_Shared_Patterns.md`；`docs/03_Design/CURIS_VISUAL_STANDARD_V1.md` | Shell `Status: Frozen`；Visual Standard `CEO SELECTED D — CURRENT VISUAL LANGUAGE`、Iris `#806BE5` | untracked | **已登记**：Pointer #45 / required authorities | 现有 Pointer 足够；需要 Git baseline closure，不需要新 registry |
| 当前 scoped Implementation Acceptances | Pointer / CURRENT_STATE 所列 Whole-App、Organization、Operating Intelligence、Talent、Knowledge、Meeting、Phase B 等 Acceptance / Review | 各自 Accepted/Closure 文档与 Pointer registration | 多份 untracked；扫描到 74 份 untracked doc 含 acceptance/freeze markers | **大部分已登记** | Implementation Truth 继续进入 CURRENT_STATE + Accepted Review；P0 是 clean-baseline promotion，不是再建清单 |
| RD Professional Workspace Instance | `docs/03_Design/Curis_RD_Workspace_Instance_Spec_v1.md`；`Curis_RD_Design_Phase_Closeout_2026-08-15.md` | `RD INSTANCE APPROVED` / design closeout | Instance Spec untracked | **CURRENT_STATE 有登记；Pointer 没有清晰的 RD canonical sub-authority 条目** | 未来只补到现有 Pointer 的 Professional Workspace / RD 路由；但必须先处理下述 stale shared-rule 冲突，不能原样升级为独立 Current shared authority |
| 2026-09-12 Competitive Research / HTML Prototype | `docs/research/system_competitive_research/`；`docs/prototypes/full-product-html/` | Research 文件为 COMPLETE/Draft；Prototype 为 `READY FOR CEO / CHATGPT REVIEW` | untracked | 不应登记为 Current Product Truth | 保持 Research / Evidence；CEO 接受后才产生明确 Disposition，不得提前写 Pointer Current 区 |

### P0 finding

本表没有发现“9 月 10 日之后已经 CEO ACCEPTED、但 Pointer 完全漏掉”的新 Product Truth。P0 是：**已登记的 Current/Frozen/Accepted truth 本身没有形成 clean committed baseline**。因此“入口正确”与“任何新环境都能可靠读取”目前不能同时成立。

---

## 5. Recent stale / mixed truth reintroduced into Zcode research and HTML

这里只登记 2026-09-10 边界后重新进入工作流的旧语义，不重审全部 Archive。

| 最近文件 | 重新带入的旧资料或冲突 | 分类 | 对下游的约束 |
|---|---|---|---|
| `docs/research/system_competitive_research/CURIS_CURRENT_UI_AUDIT.md:187-190` | 将 D 代描述为“六区导航”，并称其为 Final UI Master 重启“最可信输入池”；又把 `#32f08c` 与 `#806BE5` 写成 accent 裁决仍悬而未决 | **STALE CURRENT LANGUAGE** | 七区已 Frozen；D 代只能是 historical/structural evidence；Visual Standard 已裁决 Iris `#806BE5`，不能由 Research 重开 |
| `docs/research/system_competitive_research/CURIS_UI_EVIDENCE_CATALOG.md:82-89` | 把实际 frontend `globals.css` 的旧 green token 称为“视觉真源/FROZEN”，把 `#806BE5` 称为“残留旧品牌色” | **PRODUCT TRUTH ≠ IMPLEMENTATION TRUTH 混用** | 可以记录代码仍用旧 token，但 Current visual authority 必须是 `CURIS_VISUAL_STANDARD_V1.md`；旧 green 是 implementation migration debt |
| `docs/prototypes/full-product-html/CURIS_FULL_PRODUCT_HTML_PROTOTYPE_REVIEW.md:48-52` | 已承认 Visual Standard Frozen，却再次要求 CEO 在 `#806BE5` 与重启视觉方向之间裁决 | **UNAUTHORIZED REOPEN** | Prototype 可以待视觉质量 Review，但不能重开 Frozen brand accent；若有新视觉方向必须另走 Product/Design Delta |
| `docs/prototypes/full-product-html/CURIS_FULL_PRODUCT_HTML_PROTOTYPE_REVIEW.md:44-46,71-79` | 使用“人才市场结构”作为说明文字，同时实际一级区已为“人才与能力” | **MINOR STALE LABEL** | Market/Discover 只能是“人才与能力”内部 Surface，不得成为正式一级名称 |
| `docs/prototypes/full-product-html/js/components.js:41-46` | Employee helper 将 `done` 映射为“已完成” Employee UI Status | **FROZEN SHELL CONFLICT** | Shared Employee UI Status 只能是 `空闲 / 工作中·desc / 阻塞·cause`；“已完成”属于 Work/Result/Responsibility |
| `docs/prototypes/full-product-html/css/tokens.css:27-32` + `css/curis.css:7-16` | 复制的旧 token 文件仍含 `#32f08c`，再由 `curis.css` override 为 `#806BE5` | **MIXED PROVENANCE / DEAD-CONFLICT RISK** | 当前 rendered prototype 倾向消费 Iris override，但 Design input 不能把旧 tokens 文件独立当 Frozen authority |
| `docs/prototypes/full-product-html/css/shell.css` | 含旧 `52px topbar` 结构，但 `index.html` 当前未加载该文件 | **UNUSED STALE ASSET** | 不是当前渲染冲突；仍不应被下一轮 Zcode/HTML 复制为 active Shell authority |
| `docs/prototypes/full-product-html/PROFESSIONAL_BUSINESS_EXISTING_TRUTH.md:127-128,152-167` | 名为 Existing Truth，却混入旧 “小红书运营母业务 / AI科技 Workspace”、固定串行 team-flow fixture，以及已关闭的 RD reliability `REVIEW REQUIRED` 说法 | **CURRENT + HISTORICAL FIXTURE MIXED** | 后续 Prototype 应从 Domain Authority / Current reconciliation 取 identity，从 Accepted Runtime Review 取 implementation state；fixture 必须标为 fixture，不能伪装 current business identity 或 mandatory workflow |
| `docs/03_Design/Curis_RD_Workspace_Instance_Spec_v1.md:26-28,144-148,290-295` | RD Approved Instance 仍包含 Runtime state → 默认展开/收起，以及旧 `＋ / Mode / Model / Send` Composer；与后来 Frozen Shell 的 UI-state independence 和完整 Composer slots 冲突 | **LOWER AUTHORITY STALE RULES** | 读取 RD 时必须先读 Frozen Shell；这些 shared clauses 视为被 Shell supersede，只保留 RD domain/object anatomy。当前不应把该文件单独交给 Zcode 当完整 UI authority |
| `docs/prototypes/full-product-html/README.md` / models prototype | 以“13 家厂商 + 输 Key 即用”作普通产品展示，容易把 registry presence 扩大成全 Provider verified | **CAPABILITY TRUTH OVERCLAIM RISK** | 已验证 E2E 证明 provider architecture + DeepSeek 链，不证明所有 Provider 均可用；每个 Provider 仍按 credential / health / discovery / eligibility 显示真实状态 |

### Prototype contamination verdict

- **结构主干没有被完全污染**：当前 HTML 的实际一级导航是七区；UI label 使用“内容增长工作空间”；Four-Pane、pane-local header、floating Assistant 与 `Channel ≠ Workspace` 主语义大体正确。
- **输入包仍存在新旧混合**：Research 把旧实现 token/旧 prototype 状态误称视觉权威；RD Instance 把后来已 supersede 的 shared UI 规则继续带进 Prototype；Employee status 和模型能力文案存在当前冲突。
- 因此 `docs/prototypes/full-product-html/` 当前只能保持 `RESEARCH / EVIDENCE — READY FOR REVIEW`，不能成为 Final UI Master 或 Frontend development baseline。

---

## 6. Professional Business canonical reading route

### 6.1 Content Growth

按以下顺序读取：

1. `docs/01_Product/CURIS_PRODUCT_STRUCTURE_BASELINE_PRE_DESIGN_RESEARCH.md` — Current structure boundary。
2. `docs/03_Design/Curis_Company_OS_Shared_Authority.md` — Company/Organization/shared truth。
3. `docs/03_Design/Curis_Workspace_Shell_Contract_And_Shared_Patterns.md` — current shared spatial/UI contract。
4. `docs/03_Design/Curis_Content_Growth_Domain_Authority.md` — Frozen domain authority；Content Growth = Professional Workspace Candidate；Channel / Channel Account 不是 Workspace。
5. `docs/reviews/CONTENT_GROWTH_CEO_AUTHORITY_DECISION_RECONCILIATION.md` — Office/Workspace/Main/Channel 的最新 CEO reconciliation record。
6. `docs/03_Design/Curis_Content_Growth_Operating_Strategy_UX_Translation.md` — `APPROVED WITH 5 DELTAS` 的 domain UX translation；只能消费上列 Authority。
7. `docs/reviews/CONTENT_GROWTH_CHANNEL_CAPABILITY_EVIDENCE_AUDIT.md` 与 `CONTENT_GROWTH_AUTONOMY_GUARDRAIL_CALIBRATION_AUDIT.md` — Capability / autonomy 真实边界，不是页面 authority。

不得作为 Current identity 使用：

- “XHS Workspace / 小红书运营办公室 / Office = Workspace”；
- 旧平台名作为 Workspace identity；
- 8 Operating States / 4 Cognitive Buckets 作为 Runtime Schema 或 fixed UI；
- 历史 XHS HTML、D 代 fixture 或 Research proposal 覆盖 Frozen Domain Authority。

### 6.2 RD

按以下顺序读取：

1. `docs/01_Product/CURIS_PRODUCT_STRUCTURE_BASELINE_PRE_DESIGN_RESEARCH.md`。
2. `docs/03_Design/Curis_Company_OS_Shared_Authority.md`。
3. `docs/03_Design/Curis_Workspace_Shell_Contract_And_Shared_Patterns.md`。
4. `docs/03_Design/Curis_RD_Workspace_Instance_Spec_v1.md` — RD instance/domain anatomy，`RD INSTANCE APPROVED`。
5. `docs/03_Design/Curis_RD_Design_Phase_Closeout_2026-08-15.md` — design closeout evidence。
6. `issues/RD-WORKSPACE-INSTANCE-001.md` 与 `reviews/RD-WORKSPACE-INSTANCE-001_review.md` — scoped implementation/acceptance evidence；具体 Current Runtime 状态仍回到 CURRENT_STATE 和后续 Accepted Reviews。

必须附带 supersession 说明：

- RD Instance Spec 中 Runtime State → default expand/collapse 已被 Frozen Shell 2026-08-18 cleanup supersede。
- RD Instance Spec 中旧 Compact Composer slots 已被 Frozen Shared Composer contract supersede。
- `Curis_Design_System_Delta_RD_Workspace.md` 的旧六区/旧视觉规则不是 Current shared authority。
- 旧 RD high-fidelity HTML/Figma 是 instance/design evidence，不是当前 Final Visual Authority。
- RD 是 Professional Workspace example / approved instance，不是 Curis Core 固定业务类型，也不授权固定行业 workflow。

### Professional Workspace conclusion

- Content Growth：当前合法身份是 **Professional Workspace Candidate**，并有 Frozen Domain Authority；不是 Verified Professional Workspace。
- RD：存在 **RD INSTANCE APPROVED** 的 instance contract 和 accepted scoped implementation evidence，但该 instance contract 的 shared UI clauses 部分已被更高层 Frozen Shell supersede。Pointer 应在未来治理修补时给出显式 RD 路由与 supersession note，而不是把旧 spec 原样当完整 Current UI authority。

---

## 7. Current development baseline map

### A. Product 开发开始前第一入口

`/Users/yy/Documents/Curis AI Workspace/docs/00_Context/PRODUCT_DOCUMENT_POINTER.md`

仓库行为上先读 `AGENTS.md`，但 Product/Development 文档的唯一推荐入口是 Pointer。

### B. Product Structure Authority

- `docs/01_Product/Curis_Product_Blueprint.html`
- `docs/01_Product/Curis_Product_Master_Map.md`
- `docs/01_Product/Curis_Product_UI_Blueprint.html`
- 集中边界：`docs/01_Product/CURIS_PRODUCT_STRUCTURE_BASELINE_PRE_DESIGN_RESEARCH.md`

Baseline 是设计研究前的结构 router，不替代前三份 Current Product Truth。

### C. Company OS / Organization Authority

- `docs/03_Design/Curis_Company_OS_Shared_Authority.md`
- `docs/03_Design/Curis_Workspace_Shell_Contract_And_Shared_Patterns.md`
- Current 结构关系仍由 Product Blueprint / Master Map 解释；Shared Authority 不反向创造产品层级。

### D. Professional Workspace Authority

- Shared entry: Product Blueprint → Structure Baseline → Company OS Shared Authority → Frozen Shell。
- Content Growth: `docs/03_Design/Curis_Content_Growth_Domain_Authority.md` + current CEO reconciliation + UX translation + capability/autonomy audits。
- RD: `docs/03_Design/Curis_RD_Workspace_Instance_Spec_v1.md` + design closeout + scoped Issue/Accepted Review；所有 shared UI 冲突以 Frozen Shell 为准。

### E. UI / Design current baseline

- Structure: `docs/01_Product/Curis_Product_UI_Blueprint.html`
- Shell: `docs/03_Design/Curis_Workspace_Shell_Contract_And_Shared_Patterns.md`
- Visual language: `docs/03_Design/CURIS_VISUAL_STANDARD_V1.md`（Direction D / Iris `#806BE5`）
- Product Structure Baseline 明确：19 张 Figma 只作 Structural / IA Reference；Final UI Master paused；Final Visual Authority not approved。
- 2026-09-12 Research 与 full-product HTML 均不是 Current UI Authority。

### F. Runtime / current implementation

`docs/00_Context/CURRENT_STATE.md`，再按 active Issue / Approved Design → Accepted Review → Code / Runtime / Test / Browser / Desktop / Database evidence 读取。

旧 `CURIS_MASTER_DEVELOPMENT_STATE_2026-09-03.md` 与 handoff/recovery 文档只能作为时间点证据，不能覆盖 CURRENT_STATE。

### G. Research

`docs/research/`、Exploration、Prototype、Review Candidate 只作为 Reference / Reasoning / Evidence。`COMPLETE`、`READY FOR REVIEW` 或文件更新较新都不产生 Product Authority；只有明确 CEO decision + Product Consumption 才能进入 Current Truth。

---

## 8. Five required answers

### 1. 以前是否已经存在 Product Truth / Development 主入口？在哪里？

是。仓库规则入口是 `AGENTS.md`；唯一 Product/Development 文档入口是 `docs/00_Context/PRODUCT_DOCUMENT_POINTER.md`；Implementation Truth 由它和 AGENTS 路由到 `docs/00_Context/CURRENT_STATE.md`。

### 2. 它现在是否仍然正确？

**内容路由正确，Git 可恢复性不合格。** 当前 working tree 中 Pointer 正确指向 canonical Product Truth、Frozen Authority、结构基线和 Implementation Truth；但它本身及多份目标文件未 stage/commit，clean checkout 会看到旧版本或根本看不到 canonical 新文件。

### 3. 最近有哪些 Accepted/Frozen 成果没有登记进去或没有提交？

- 9 月 10 日后没有发现新 Accepted/Frozen Product Truth 漏登记；9 月 12 日新增均是 Research 或 Prototype review candidate。
- 已登记但未提交的关键成果包括结构基线、canonical Master Map/UI Blueprint、Frozen Shell、Visual Standard、Content Growth reconciliation 以及多份 scoped Accepted implementation reviews。
- RD Instance 已在 CURRENT_STATE 出现，但 Pointer 缺少明确 canonical RD sub-authority 路由，并且原 spec 存在已被 Frozen Shell supersede 的 shared UI rules，不能未经说明直接提供给新 Agent。

### 4. 最近哪些旧资料重新污染了 Zcode / HTML？

旧六区、旧 green token 作为视觉权威、重新打开已 Frozen 的 Iris accent、Employee“已完成”状态、RD Runtime-state 驱动展开/收起、旧 Compact Composer、旧 XHS/Office fixture 与已经关闭的 RD reliability 状态，均在近期 Research/Prototype 输入或输出中出现。实际 HTML 的七区/Four-Pane/Content Growth 主身份大体正确，但输入包不是纯 Current Truth。

### 5. 从今天开始，Codex/Zcode 开发 Curis 应该首先读取哪一个开发主基线？

先读 `AGENTS.md`，随后**唯一第一文档入口**是：

`/Users/yy/Documents/Curis AI Workspace/docs/00_Context/PRODUCT_DOCUMENT_POINTER.md`

开发任务再进入：

`/Users/yy/Documents/Curis AI Workspace/docs/00_Context/CURRENT_STATE.md`

不得以 `PROJECT_HANDOFF.md`、旧 frontend handoff、单份 Research、HTML Prototype、旧 Figma、旧 RD/XHS spec 或文件 mtime 代替这条路线。

---

## 9. Review disposition

- **现有治理机制：足够，不新增 Manifest / Development Pointer。**
- **当前入口：内容有效。**
- **Clean Git baseline：不存在。**
- **Recent post-boundary accepted truth gap：未发现。**
- **Recent stale/mixed input：已定位，尚未修复。**
- **Required next decision:** CEO 决定是否授权独立的 controlled baseline promotion / stale-input cleanup；该动作必须保留 ownership、Allowed Files、历史 provenance 与 no-bulk-add 纪律。

**STOP FOR CEO / CHATGPT REVIEW**
