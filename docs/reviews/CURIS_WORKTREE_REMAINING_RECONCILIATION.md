# Curis Worktree Remaining Reconciliation

Status: Review

Date: 2026-08-16

Branch: `main`

HEAD at audit: `42db50cde54bc735d709bd603fe4d98d7f8233c8`

Scope: G2 unstage、剩余工作树收口判断、docs-only 精确 staging 与风险盘点。

## 0. 执行边界

本轮没有：

- commit；
- push；
- delete、move、reset、clean；
- 修改 `.gitignore`；
- 修改 Shared Runtime 架构或任何业务源码；
- 修改 CURRENT_STATE、Pointer、Change Log 或旧 Issue / Review 状态。

本轮唯一允许的工作树变更是：

1. 将此前 G2 的五个 staged path 安全移出 index；
2. 对状态明确、canonical、docs-only 的 Frozen / Approved Candidate 文档做精确 staging；
3. 生成本审计报告。

## 1. Executive result

### G2

G2 五个文件已安全 unstage。unstage 前后工作树文件 hash 保持不变，当前均为 working-tree untracked：

| Path | Current hash | Current state |
|---|---|---|
| `backend/tests/test_xhs_calendar_note_runtime.py` | `958ea828dfd9e9c0f419d689a9959960664ecbbd` | untracked, unstaged |
| `frontend/app/ceo-office/workspace/xhs/page.js` | `314161a8f72893966371af814ddbf4eea84e182d` | untracked, unstaged |
| `frontend/components/xhs/XhsWorkspacePhaseOne.js` | `54aecb7d0bdd20fdf7b6ee6e6dd3b98f0fe76b9c` | untracked, unstaged |
| `issues/XHS-WORKSPACE-INSTANCE-001.md` | `f8245773160ce72baba1196bb93a41444a495439` | untracked, unstaged |
| `reviews/XHS-WORKSPACE-INSTANCE-001_review.md` | `b8520cee807c6603daf66b8cfeb293b692642486` | untracked, unstaged |

G2 现阶段标记为：

> **ACCEPTED IMPLEMENTATION / COMMIT BLOCKED BY SHARED RUNTIME STRUCTURE**

这表示 XHS 内部 vertical slice 的实现与验收记录保留，但当前不能把它伪装成一个没有 Shared Runtime 混合依赖的独立源码提交。该接受结论仍不包含真实外部发布或外部 Analytics 接通。

### Remaining worktree

当前工作树快照：

- 69 个 tracked worktree modifications；
- 290 个 untracked paths；
- 10 个 docs-only paths 当前 staged；
- tracked diff 约 7,376 additions / 3,608 deletions；
- 当前 staged diff 约 2,262 additions，全部位于 `docs/`。

这不是一个适合整体提交的工作树。源码、Runtime、产品文档、验收记录、数据库、构建产物和本机记忆文件仍然混在同一 snapshot 中。

## 2. Current staged docs-only scope

以下 10 个文件是本轮唯一保留在 index 中的内容：

### 2.1 Frozen Authority group — `COMMITTABLE NOW`

1. `docs/07_Decisions/ADR-0046-local-agent-computer-access-authority.md`
2. `docs/03_Design/Curis_Company_OS_Shared_Authority.md`
3. `docs/03_Design/Curis_Content_Growth_Domain_Authority.md`

共同特征：明确 `Status: Frozen`，canonical，属于产品 / 架构权威文档，不包含业务源码或运行时数据库。它们不宣称新的 Runtime 实现，也不覆盖当前 G2 / RD 的源码边界。

### 2.2 Workspace Engineering methodology group — `DOCS-ONLY COMMITTABLE`

4. `docs/05_Workspace_Engineering/Curis_Workspace_Engineering_Methodology.md`
5. `docs/05_Workspace_Engineering/Curis_Workspace_Engineering_Lifecycle.md`
6. `docs/05_Workspace_Engineering/Curis_Workspace_Engineering_Gates_and_Acceptance.md`
7. `docs/05_Workspace_Engineering/Curis_Workspace_Engineering_Expert_Handoff_Protocol.md`
8. `docs/05_Workspace_Engineering/Curis_Workspace_Engineering_Content_Growth_Case_Study.md`
9. `docs/05_Workspace_Engineering/Curis_RD_Methodology_Gap_Review.md`

共同状态为 `Review / WORKSPACE ENGINEERING METHODOLOGY APPROVED CANDIDATE`。这些文件是方法论、生命周期、门禁、交接和案例复盘，不是 Dynamic Workspace Package Runtime 的实现证明。

### 2.3 Workspace Engineering technical direction — `DOCS-ONLY COMMITTABLE`

10. `docs/02_Architecture/WORKSPACE_PACKAGE_TECHNICAL_PROPOSAL.md`

该文件是 `Review / WORKSPACE ENGINEERING TECHNICAL DIRECTION APPROVED CANDIDATE`，属于技术方向记录，不是已实现的 Package Runtime。

### 2.4 Staged validation

已执行并通过：

- staged path audit：全部 10 个 path 均在 `docs/`；
- selected-path audit：无 selected-set 之外的 path；
- `git diff --cached --check`：**PASS**；
- staged 内容未发现具体 credential / private key / secret 值；文档中出现的 `token`、`secret`、`API key` 等是规范术语或边界描述，不是凭据；
- 未运行 backend / frontend tests，因为本轮没有 staged code change；
- 未启动数据库、Desktop、外部 Agent 或任何运行时服务。

这 10 个文件仍未 commit。若通过 Review，建议按上面两个语义组拆成最多两个 docs-only commits；本轮不执行拆分提交或 commit。

## 3. Remaining implementation reconciliation

| Group | Current fact | Classification | Reason / next action |
|---|---|---|---|
| G2 XHS accepted scope | XHS page/component/test 与 Issue/Review 存在；`workspace.py`、foundation router、`runtimeApi.js`、shared UI test 与其他 initiative 交叉 | **ACCEPTED IMPLEMENTATION / COMMIT BLOCKED BY SHARED RUNTIME STRUCTURE** | 保持五文件 unstaged；另建 bounded shared-boundary task 后才重新精确拆分源码 |
| G3 RD Phase 0/1 accepted scope | Issue/Review 记录 Phase 0/1 accepted，但 RD 执行链使用 `main.py`、Runtime Workspace、foundation/router、frontend Runtime/RD seams；这些文件同时承载其他 wave | **BLOCKED BY MIXED SOURCE** | 不重构、不 whole-file stage；等待明确 ownership / index-only split |
| RD long-running execution reliability | Issue/Review 中记录 implemented/closed facts，但与 Phase 2A、design fidelity 和 `REVIEW REQUIRED` 共存；实现位于 mixed Runtime / orchestration seams | **BLOCKED BY MIXED SOURCE / HOLD** | 当前没有可独立证明“long-running only”的 canonical closure record；不把合并记录当成干净独立提交 |
| G7 Frozen Authority docs | ADR-0046、Company OS Shared Authority、Content Growth Domain Authority 均明确 Frozen | **COMMITTABLE NOW** | 已精确 staged，等待 Review；不涉及源码 |
| Content Growth Frozen authority | `Curis_Content_Growth_Domain_Authority.md` 明确 Frozen | **COMMITTABLE NOW** | 已纳入 G7 Frozen Authority group |
| Content Growth product / UX explorations | Product Model Closure、Operating Model、UX / IA / First Run / Terminology / Composition 等为 Review、Recommendation、Exploration 或 Candidate | **HOLD** | 不能因为“已完成设计讨论”升级为 Frozen 或实现；保持 unstaged |
| Workspace Engineering methodology set | 六份方法论文档均 Review / Approved Candidate | **DOCS-ONLY COMMITTABLE** | 已精确 staged；只提交方法论事实，不声称 Runtime 已实现 |
| Workspace Package Technical Proposal | Review / Technical Direction Approved Candidate | **DOCS-ONLY COMMITTABLE** | 已精确 staged；与实现计划分开 |
| Workspace Engineering P0 Definition | Review / P0 Defined；Implementation State `NOT STARTED / REVIEW REQUIRED` | **HOLD** | 定义已形成，但尚未成为实施授权或完成证明；本轮不 stage |
| Workspace Engineering runtime/extensibility audit | Review / read-only implementation audit，基于 dirty snapshot | **HOLD** | 它描述当前混合工作树事实，不适合与 Approved Candidate 方法论一起当成完成提交 |
| Workspace Engineering P0 Implementation Plan | Review / Draft / Not Started | **HOLD** | 计划不是实现，不加入当前 docs-only queue |
| G1 Agent Computer Access | 已在 HEAD `42db50cde` 完成正式 commit | **ALREADY COMMITTED** | 不重新 stage、不修改 |
| Other accepted / frozen Issue / Review records | 分散于新 untracked `issues/`、`reviews/` 和历史记录；多数与实现、Review Required 或旧阶段混合 | **HOLD / OWNER REVIEW** | 需逐条按 Issue Allowed Files、Review status、canonical pointer 重新确认，不批量 stage |

## 4. Why the code groups cannot close without Runtime refactor

本轮确认的共同 mixed seams 包括：

- `backend/app/main.py`：Agent / provider / RD / Runtime / other initiative changes overlap；
- `backend/app/runtime/models.py`、`registry.py`、`states.py`、`store.py`：Shared Runtime foundation 与 domain-specific additions overlap；
- `backend/app/runtime/foundation.py`、`workspace.py`：untracked implementation contains shared-looking and domain-specific behavior together；
- `backend/app/api/runtime_foundation_router.py`：XHS、RD 及其他 Runtime routes overlap；
- `frontend/lib/runtimeApi.js`：RD、XHS、Runtime foundation and other endpoint blocks overlap；
- `frontend/components/runtime/`、`WorkspacePaneShell.js`、`RuntimeProvider.js`、`RuntimeStates.js` 与 `frontend/tests/runtimeWorkspaceUi.test.mjs`：shared UI / Runtime assumptions are shared by XHS and RD;
- RD / XHS page and component paths are independently identifiable, but their runtime contract is not currently independently staged without splitting shared source hunks.

结论：当前真正阻塞的是 source ownership / mixed hunk，而不是“缺少一个 staging 命令”。为了提交 G2 或 G3 去抽取 Shared Runtime 会改变本轮授权边界，因此本轮没有做。

## 5. Generated / local / sensitive-risk reconciliation

### 5.1 Future `.gitignore` candidates — report only

以下路径看起来属于生成物、本机缓存、运行时状态或测试副产物，建议后续由独立 repository hygiene task 评估后加入 `.gitignore`；本轮没有修改 `.gitignore`：

- `.cache/`、`.next/`、`frontend/.cache/`、`.workbuddy/output/`；
- `artifacts/`、`previews/`、`delivery/`；
- `desktop/target/`、`desktop/node_modules/`、其他 Desktop build output；
- `.runtime/`、`__pycache__/`、`*.pyc`、`.DS_Store`；
- SQLite `*-wal` / `*-shm`，以及明确属于本机运行的 `backend/*.sqlite`、`backend/data/`、`data/issue_pipeline.sqlite-*`；
- 临时截图、preview、packaged-app evidence 目录（若不属于正式验收归档）。

`.gitignore` 当前本身是 modified，必须由 owner review 后再处理，不能把本轮 staging 当作清理授权。

### 5.2 Delete candidates — no deletion performed

以下是候选，不是已批准删除目标：

- 根目录形如 `<app.database.Database object at 0x...>` 的异常命名 SQLite 文件；
- `curis-ui-prototype.bak/`；
- `data/curis.sqlite.bak-20260806`；
- 过期 build/cache/preview/evidence 目录；
- 重复的旧根目录产品文档或迁移来源。

在删除前必须确认：是否被 Review / evidence 引用、是否是唯一可复现数据、是否仍被本机工具使用、是否应先归档。当前不删除、不移动、不覆盖。

### 5.3 Evidence review required

需要单独 evidence review 的对象：

- `desktop/` packaged app / target output；
- `artifacts/`、`previews/`、`delivery/` 和 `docs/reviews/**` 下的截图、报告、验证输出；
- `backend/curis.sqlite`、`backend/curis_dev.db`、`backend/data/`、`data/curis.sqlite.bak-20260806`；
- `data/issue_pipeline.sqlite-wal`、`data/issue_pipeline.sqlite-shm`；
- 根目录异常命名的 Database object 文件；
- `.workbuddy/output/` 和本机记忆文件。

这些文件可能包含活动数据库、个人路径、测试数据或验收证据。发现风险只记录，不在本轮提交或删除。

### 5.4 Owner review required

以下 tracked / untracked 内容不能由本轮自动归类为正式成果：

- `AGENTS.md`、`.gitignore`；
- `docs/00_Context/CURRENT_STATE.md`、`PRODUCT_DOCUMENT_POINTER.md`、`CHANGE_LOG.md` 及 Blueprint 的当前修改；
- Talent Market、AI Capability、Strategy Meeting、Content Growth product wave、frontend product wave；
- 根目录 `Curis_Page_Map_v1.0.md`、`Curis_Product_Master_Map_v2.0.md` 等待迁移来源；
- 旧 Review、Research、Prototype、audit JSON / HTML 与新正式文档之间的关系。

## 6. Minimal Commit Queue

目标是快速收敛，而不是为了制造漂亮的历史边界重构产品。

### Queue 1 — Frozen Authority docs

建议名称：

`docs: record frozen company and content authorities`

包含当前 staged 的 3 个 Frozen Authority 文件。无需源码验证；提交前重复 `git diff --cached --check` 与 path audit 即可。

### Queue 2 — Workspace Engineering docs-only

建议名称：

`docs: record workspace engineering approved candidate method`

包含当前 staged 的 6 份 methodology / case / gap docs 与 1 份 technical proposal。提交时必须保持文案中的 `APPROVED CANDIDATE`、`NOT IMPLEMENTED`、`NOT STARTED` 事实，不将候选方向写成完成实现。

### Queue 3 — G2 XHS code

当前：**ACCEPTED IMPLEMENTATION / COMMIT BLOCKED BY SHARED RUNTIME STRUCTURE**。

前置：建立明确的 Shared Runtime ownership / bounded extraction 或完成受控 index-only hunk split。不得 whole-file stage `workspace.py`、foundation router、`runtimeApi.js` 或 shared UI test。

### Queue 4 — G3 RD and long-running reliability code

当前：**BLOCKED BY MIXED SOURCE**。

前置：为 RD execution 与 long-running reliability 形成独立 allowed-file boundary；不能把 `main.py`、Runtime foundation、router、provider 或 shared frontend seams 的其他 initiative hunk 带入。

### Queue 5 — remaining product / evidence / hygiene

当前：**HOLD / OWNER REVIEW**。

先完成 canonical pointer、Current State、Change Log、evidence retention、database provenance 和 `.gitignore` 决策，再处理其余 Issue / Review / Research / prototype / generated files。

## 7. Blocking risks

当前阻塞后续源码提交的主要风险：

1. Shared Runtime mixed ownership 仍未解决；
2. G2 / G3 Issue 与 Review 记录包含不同 phase 的状态，不能把单一 `ACCEPTED` 词语当作整个文件或整个工作树已收口；
3. Current State / Pointer / Change Log / Blueprint 有 tracked modifications，产品事实与本轮新增 docs 的一致性尚未由 owner 收口；
4. 工作树存在 active SQLite、WAL / SHM、packaged output、cache 和 evidence，可能包含本机路径或测试数据；
5. untracked docs 很多，不能按文件名或目录名批量判断为正式成果；
6. 本轮没有验证未 staged code 的全量测试，因此不能把工作树整体称为可提交或可发布。

## 8. Final audit conclusion

### A. 当前工作树包含什么

它同时包含：G1 已提交成果、G2 XHS accepted slice、G3 RD accepted / review-required slice、Shared Runtime 混合源码、产品与架构文档、Workspace Engineering 方法论、Content Growth 设计材料、Issue / Review / evidence、数据库和大量本机生成物。

### B. 哪些可以安全提交

- 本轮精确 staged 的 3 份 Frozen Authority docs；
- 本轮精确 staged 的 7 份 Workspace Engineering docs-only candidate / technical direction docs；
- G1 已经在 HEAD 中，不需要再次处理。

### C. 哪些需要进一步确认

- G2 / G3 implementation code；
- RD long-running reliability 的独立 closure 记录；
- P0 definition / implementation plan；
- Content Growth 非-Frozen product docs；
- 其他 Issue / Review / audit / evidence 文件；
- Current State、Pointer、Change Log、Blueprint 与根目录迁移来源。

### D. 推荐 Commit 顺序

1. Review 后提交 Frozen Authority docs；
2. Review 后提交 Workspace Engineering docs-only group；
3. 另行处理 G2 mixed-source boundary；
4. 另行处理 G3 / long-running reliability mixed-source boundary；
5. 最后处理 evidence retention、database provenance、`.gitignore` 和 delete candidates。

### E. 应排除 / 清理什么

当前应排除 generated/local、active database、WAL / SHM、cache、build、preview、packaged output、异常命名 DB 文件和未确认的旧迁移来源。清理必须另开授权，不在本轮执行。

### F. 是否存在阻塞提交的风险

存在。Frozen Authority 与 Workspace Engineering docs-only groups 本身没有发现阻塞，且 staged check 已通过；G2、G3、RD long-running reliability 的源码提交仍被 mixed Shared Runtime structure 阻塞。工作树整体仍不可作为单一 commit 提交。

## 9. Stop condition

**REMAINING WORKTREE RECONCILIATION COMPLETE**

**NO COMMIT CREATED**

**NO PUSH PERFORMED**

**NO FILE DELETED OR MOVED**

**NO SHARED RUNTIME REFACTOR PERFORMED**

**G2 UNSTAGED WITH WORKING-TREE CONTENT PRESERVED**

**DOCS-ONLY CANDIDATES STAGED FOR REVIEW ONLY**

