# CURIS WORKTREE AUDIT & CLEANUP

Status: Review  
Date: 2026-08-16  
Scope: first-round read-only repository governance audit  
Branch: `main`  
HEAD: `adb52210a` (`docs: centralize product document bootstrap rules`)  
Document authority: `/Users/yy/Documents/Curis AI Workspace/docs/`

## 0. Boundary and conclusion

本轮只做了审计、分类、提交分组、风险报告和验证计划。

本轮没有执行：

- `git add`
- `git commit`
- `git push`
- 删除文件
- `git reset --hard`
- `git clean -fd`
- 大规模修改 `.gitignore`
- 业务功能修改

当前工作树不是一条单独功能分支的待提交状态，而是至少包含以下几类同时叠加的内容：

1. 已有正式实现的补丁。
2. 仍处于 Review Required 的实现切片。
3. 已批准或已 Frozen 的产品、架构和设计文档。
4. 新增 Issue、Review、Evidence 和测试。
5. Desktop / Next / Rust / Python 的本机 build、cache、数据库和运行时产物。
6. 旧 Worktree、Prototype、迁移来源和无法自动判断归属的文件。

因此，当前状态不允许执行 `git add .`，也不允许形成一个“总收口 Commit”。必须先按 Issue / Review 边界拆分，并先处理混合修改和生成物隔离问题。

## 1. 审计快照

### 1.1 Git 状态

| 项目 | 结果 |
|---|---:|
| 分支 | `main` |
| 实际 HEAD | `adb52210a` |
| AGENTS 记录的产品基线 | `main @ c0e1855f446a55aa3a384006cfcfed987713033` |
| `git status --short` modified 条目 | 72 |
| `git status --short` untracked 条目 | 293 |
| `git status --short` 条目合计 | 365 |
| `git ls-files --others --exclude-standard` 实际未跟踪文件数 | 23,548 |
| 其中 `desktop/target/` 文件数 | 22,627 |

`git status` 将整个未跟踪目录折叠成一行，所以“293 个 untracked 条目”并不等于 293 个文件。实际未跟踪文件数量主要被 `desktop/target/` 放大。

### 1.2 Modified 条目按顶层目录

| 顶层 | 条目数 | 初步判断 |
|---|---:|---|
| `backend/` | 23 | Runtime、能力、Agent、数据库、执行桥和 API 混合修改 |
| `frontend/` | 19 | CEO 工作台、共享壳层、组织、决策、Workspace 和 onboarding 混合修改 |
| `docs/` | 25 | 权威文档、Blueprint、Current State、Change Log、旧计划混合修改 |
| `AGENTS.md` | 1 | 仓库治理规则修改，需单独确认 |
| `.gitignore` | 1 | 只新增 `desktop/.runtime/` 规则，未覆盖全部生成物 |
| `.workbuddy/` | 2 | 本机记忆/工作痕迹，不应进入产品提交 |
| `data/` | 1 | 样例发布包文档修改，归属待确认 |

### 1.3 Untracked 条目按来源

重要的未跟踪来源包括：

- `backend/`：36 个 status 条目，包含 Agent Adapter、Runtime foundation、XHS/RD 测试、Talent Market / Agent conversion 支撑。
- `frontend/`：21 个 status 条目，包含 Runtime Provider、Workspace Pane、RD、XHS、Workspace 路由和 Talent Market。
- `docs/`：151 个 status 条目，包含 Workspace Engineering、Content Growth、Company OS Authority、ADR-0046、Issues/Reviews 对应文档和大量候选材料。
- `issues/`：27 个正式 Issue 条目。
- `reviews/`：12 个正式 Review 条目。
- `desktop/`：一个被 `git status` 折叠的未跟踪目录，除源码外还包含约 4.7 GB 的 `target/`。
- `artifacts/`、`previews/`、`delivery/`、`curis-ui-prototype/`：证据、预览、迁移来源或 Prototype，需要逐类处理。
- 根目录的 `Curis_Product_Master_Map_v2.0.md`、`Curis_Page_Map_v1.0.md`、Talent Market 文档等：与 canonical `docs/` 文档重复的迁移来源，不应直接当作当前产品真相提交。
- 根目录多个形如 `"<app.database.Database object at ...>"` 的条目：高度疑似异常生成路径，尚未删除，归属未确认。

## 2. 近期主要工作分类

### 2.1 XHS Workspace

状态：`XHS IMPLEMENTATION ACCEPTED`，范围是 Phase 0–6 的第一条 XHS Workspace vertical slice。

Review 记录显示：

- XHS Workspace、Calendar Note、Handoff、Decision Packet、CEO 选择和重启恢复已有正式验收记录。
- 后端 focused test 为 14 passed；前端 Runtime Workspace UI test 为 7 passed。
- 当前 XHS 发布仍是等待真实 `PLATFORM_API` receipt；没有真实平台发布和分析连接器，不能把“已验收”解释为外部平台闭环已完成。
- Issue 明确排除 TerraShell / TerraSidebar、RD / TTK、共享 Runtime 之外的扩张。

主要文件范围：

- `frontend/components/xhs/XhsWorkspacePhaseOne.js`
- `frontend/app/ceo-office/workspace/xhs/page.js`
- `backend/app/runtime/workspace.py`
- `backend/app/api/runtime_foundation_router.py`
- `backend/tests/test_xhs_calendar_note_runtime.py`
- `frontend/lib/runtimeApi.js`
- `frontend/tests/runtimeWorkspaceUi.test.mjs`
- `issues/XHS-WORKSPACE-INSTANCE-001.md`
- `reviews/XHS-WORKSPACE-INSTANCE-001_review.md`

提交判断：XHS 已验收部分可以成为独立提交组，但共享 Runtime、`runtimeApi.js` 和 `WorkspacePaneShell` 需要先做逐块拆分；不能把整个 `frontend/` 或整个 Runtime 目录作为 XHS 提交。

### 2.2 RD Workspace / Phase 2A

状态不是完整接受，而是：

`PHASE 0/1 ACCEPTED · PHASE 2A DESIGN FIDELITY PASS · LONG-RUNNING EXECUTION RELIABILITY IMPLEMENTED · REVIEW REQUIRED`。

Review 事实：

- Phase 0/1 的真实代码执行、Evidence、Artifact 和失败路径已通过边界验收。
- Phase 2A 有真实 Composer、Workspace Pane、Utility / Diff / test result 视图和 focused UI 验证。
- Long-running reliability 已实现，但仍有 packaged Desktop 等边界：长任务超过 Gateway 等待窗时，调用方可能先收到 503，而后台仍继续完成并持久化。
- Artifact Review、正式 Handoff、P7 CEO Decision、Phase 2B 尚未完成。
- Review 明确禁止把后续阶段写成全部已完成。

主要文件范围：

- `backend/app/main.py`
- `backend/app/agent_adapter.py`
- `backend/app/runtime/workspace.py`
- `backend/app/api/runtime_foundation_router.py`
- `backend/app/runtime/execution_adapter.py`
- `backend/tests/test_rd_workspace_real_execution.py`
- `frontend/components/rd/RdRealExecutionComposer.js`
- `frontend/components/rd/RdWorkspacePhaseTwo.js`
- `frontend/components/runtime/WorkspaceRuntimeView.js`
- `frontend/components/workspace/WorkspacePaneShell.js`
- `frontend/app/ceo-office/workspace/software/page.js`
- `frontend/tests/rdWorkspaceExecution.test.mjs`
- `frontend/tests/runtimeWorkspaceUi.test.mjs`
- `issues/RD-WORKSPACE-INSTANCE-001.md`
- `reviews/RD-WORKSPACE-INSTANCE-001_review.md`

提交判断：Phase 0/1 可单独形成正式提交；Phase 2A 和 long-running reliability 只能以 Review Required / candidate 提交，不能伪装为 RD 全量收口。`backend/app/main.py` 和共享 Runtime 文件存在跨组混改，暂不安全。

### 2.3 Agent Computer Access

状态：`AGENT COMPUTER ACCESS RUNTIME P0 IMPLEMENTED / ACCEPTED`。

Review 记录显示：

- requested / configured / effective / verification / limitation 的状态分层已实现。
- isolated SQLite restart read-back 和 focused regression 通过，记录为 36 passed。
- 不包含 Full Computer Access，不包含 UI 扩张，不包含 XHS/RD/TTK 业务扩张。

主要文件范围：

- `backend/app/agent_adapter.py`
- `backend/app/main.py`
- `backend/app/tool_executor.py`
- `backend/app/orchestrator.py`
- `backend/app/result_store.py`
- `backend/tests/test_agent_adapter.py`
- `backend/tests/test_agent_computer_access_runtime_p0.py`
- `issues/AGENT-COMPUTER-ACCESS-RUNTIME-P0-001.md`
- `reviews/AGENT-COMPUTER-ACCESS-RUNTIME-P0-001_review.md`

提交判断：业务边界清楚，但 `main.py`、`orchestrator.py`、`result_store.py` 与 RD / Shared Runtime 同时被修改。必须用 hunk 级拆分或先建立临时分支，再提交接受范围；不能按整文件提交。

### 2.4 Content Growth

状态：文档和设计为主，包含 Frozen Authority 与 Review / Research 两种状态，不等于内容业务代码已完成。

已识别的正式 Authority：

- `docs/03_Design/Curis_Company_OS_Shared_Authority.md`：`Status: Frozen`。
- `docs/03_Design/Curis_Content_Growth_Domain_Authority.md`：`Status: Frozen`。

候选 / 研究 / 设计材料包括：

- `docs/03_Design/Curis_Content_Growth_*`
- `docs/Content_Growth_Research/`
- Company OS Authority Consolidation Review
- Content Growth Authority Consolidation Review
- First Run、Home、Strategy、Employee、Evolution、Workspace Composition 等 wireframe / interaction 文档。

提交判断：Frozen Authority 文档是正式产品资产，应该优先从根目录重复文件中区分出来并独立提交；其余研究、Candidate、Wireframe、Consolidation Review 需按文档状态另组，不能混成“Content Growth 已完成”。

### 2.5 Workspace Engineering Methodology / Technical Audit / P0

状态：`Review` / `APPROVED CANDIDATE`，不是 Frozen 实现，也不是已交付 Dynamic Workspace Package Runtime。

事实：

- Methodology、Lifecycle、Gates and Acceptance 是方法论候选。
- Runtime and Extensibility Audit 明确区分了当前已存在的固定 Workspace 与未实现的动态 Package Runtime。
- Technical Proposal 是技术方向候选。
- P0 Definition 的 Implementation State 是 `NOT STARTED / REVIEW REQUIRED`。
- P0 Implementation Plan 是 `DRAFT / NOT STARTED`。

提交判断：这些文件可以作为独立的 Review 文档组；不能和实现代码一起提交并宣称 P0 已实现。P0 的依赖顺序必须保留：先确认 Definition / Issue，再实施，再通过 Business Runtime Simulation。

### 2.6 Shared Runtime / Shell

当前既有：

- `backend/app/runtime/models.py`
- `backend/app/runtime/registry.py`
- `backend/app/runtime/states.py`
- `backend/app/runtime/store.py`
- `backend/app/runtime/foundation.py`
- `backend/app/runtime/simulation.py`
- `backend/app/runtime/workspace.py`
- `backend/app/runtime/execution_adapter.py`
- `backend/app/api/runtime_foundation_router.py`
- `frontend/components/runtime/*`
- `frontend/lib/runtimeApi.js`
- `frontend/components/workspace/WorkspacePaneShell.js`

这些文件同时被 XHS、RD、CEO 工作台和 Shared Runtime 使用。它们是当前最明显的共享依赖层，也是拆分风险最高的层。当前不能把“某一业务已通过验收”扩展为“共享 Runtime 已经完全收口”。

## 3. 当前变更类型清单

### A. 已实现并已验收的正式代码

可识别的边界验收成果：

1. Agent Computer Access Runtime P0。
2. XHS Workspace first vertical slice，明确仅到已记录的 XHS scope。
3. RD Phase 0/1 real execution slice。
4. 既有部分 Shared Runtime foundation，在对应 Review 记录的范围内。

注意：这些成果仍有大量源码未跟踪，且部分核心文件与其他工作混改，所以“功能 Review 已接受”不等于“当前工作树可直接按该功能提交”。

### B. 已实现但仍处 Review 的代码

- RD Phase 2A design fidelity。
- RD long-running execution reliability。
- Runtime Foundation / Workspace shared expansion。
- Talent Market / Agent conversion / external candidate discovery。
- AI capability registry / multi-protocol model gateway / local provider handling。
- CEO 工作台的 Company OS / staffing / capability supply / simulation / approval UI 改造。

这些不能按“正式验收代码”处理。

### C. 已批准 / Frozen 的正式文档

- `docs/03_Design/Curis_Company_OS_Shared_Authority.md`
- `docs/03_Design/Curis_Content_Growth_Domain_Authority.md`
- `docs/07_Decisions/ADR-0046-local-agent-computer-access-authority.md`
- `docs/00_Context/CURRENT_STATE.md`
- `docs/00_Context/PRODUCT_DOCUMENT_POINTER.md`
- 其他已在 Pointer / Current State 注册的 Frozen 产品、架构和治理文档。

其中不少文件当前只在工作树里存在，或有未提交修改；因此 committed HEAD 不能重现当前文档真相。

### D. Review / Candidate / Research 文档

- Master Map v2.0：`REVIEW REQUIRED`。
- Page Map v1.0：`REVIEW REQUIRED`。
- Blueprint v5.1：`Review`。
- Workspace Engineering Methodology / Technical Proposal / P0：`Review`。
- Content Growth wireframe、interaction、research、consolidation review。
- Talent Market Product Map / Integration Contract / Resource Audit 的 Review 部分。

### E. 新增 Issue / Review / Evidence

正式但未跟踪的根目录：

- `issues/`
- `reviews/`

这些不能因为未跟踪就当作临时文件。它们被 Pointer、Issue 或 Review 相互引用，属于重要正式记录候选；但应随对应实现组提交，或建立明确的 governance-only commit。

### F. 测试代码

主要新增 / 未跟踪测试：

- `backend/tests/test_agent_adapter.py`
- `backend/tests/test_agent_computer_access_runtime_p0.py`
- `backend/tests/test_rd_workspace_real_execution.py`
- `backend/tests/test_xhs_calendar_note_runtime.py`
- `frontend/tests/rdWorkspaceExecution.test.mjs`
- `frontend/tests/runtimeApi.test.mjs`
- `frontend/tests/runtimeFirstArrival.test.mjs`
- `frontend/tests/runtimeMaterialization.test.mjs`
- `frontend/tests/runtimeProvider.test.mjs`
- `frontend/tests/runtimeWorkspaceUi.test.mjs`

测试必须随其所属实现组绑定，不能单独提交后被解释为实现已验收。

### G. 临时数据库 / 运行时数据

发现：

- `backend/curis.sqlite`
- `backend/curis_dev.db`
- `backend/data/`
- `data/curis.sqlite.bak-20260806`
- `data/issue_pipeline.sqlite-shm`
- `data/issue_pipeline.sqlite-wal`

这些文件可能包含活动状态、租户数据、Issue 状态、模型引用或本机运行痕迹。不得提交，不得删除，先保留并在后续清理任务中按数据库保留 / 备份策略处理。

### H. Build / cache / log / screenshot / evidence 产物

发现：

- `desktop/target/`：约 4.7 GB，约 22,627 个未跟踪文件。
- `desktop/node_modules/`：约 29 MB。
- `desktop/.runtime/`：约 742 MB；已被当前 `.gitignore` 忽略。
- `frontend/.next/`：约 718 MB；已被当前 `.gitignore` 忽略。
- `.cache/`：约 836 KB。
- `artifacts/`：约 192 MB。
- `previews/`、`.workbuddy/output/`、Prototype `.audit/`、截图和 packaged app。

这些不是提交候选。当前只报告，不清理。

### I. 本机环境与配置

- `.workbuddy/memory/`、`.workbuddy/output/` 属于本机工作痕迹。
- `desktop/` 源码本身当前没有已跟踪文件，但目录同时包含正式 Tauri 源码、生成 schema、图标和巨大 build 产物；必须拆分源文件与产物后再决定。
- `deploy/new-api/.env` 由 `.gitignore` 保护；本轮没有读取或输出其内容。
- `AGENTS.md` 有未提交修改，应由仓库 owner 单独确认，不与业务代码混提交。

### J. 无法判断来源 / 疑似误生成

- 根目录 16 个左右形如 `"<app.database.Database object at ...>"` 的文件路径。
- 根目录重复的 Master Map / Page Map / Talent Market / Rethink 文件。
- `delivery/`、`curis-ui-prototype.bak/`、部分 `previews/`。
- `build_rd_pages.py`、`rebuild_rd_default.py`、`reproduce_rd_baseline_v1.py` 与当前正式实现的关系尚未由 Issue / Review 证明。

这些文件保留，暂不删除或提交。

## 4. 混合修改与冲突地图

### 4.1 高风险共享代码文件

| 文件 | 观察到的混合来源 | 处理结论 |
|---|---|---|
| `backend/app/main.py` | dotenv、Agent Adapter、Talent Market、AI Capability、Strategy Meeting、Runtime Foundation、RD execution | 最高风险；必须 hunk 拆分，不能整文件提交 |
| `backend/app/database.py` | Runtime schema、Capability ownership、Strategy Meeting、已有数据库迁移 | 需要数据库迁移边界和活动 DB 风险确认 |
| `backend/app/result_store.py` | Agent Computer Access、RD Artifact / Evidence、Runtime 结果 | 需要按调用链拆分 |
| `backend/app/orchestrator.py` | Computer Access 传播、既有执行编排 | 只允许提交已验收 P0 hunk |
| `backend/app/tool_executor.py` | Computer Access snapshot / existing tools | 只允许提交 P0 hunk |
| `backend/app/runtime/workspace.py` | XHS、RD、Shared Workspace | 需按 Issue 逐块核对 |
| `backend/app/api/runtime_foundation_router.py` | XHS、RD、Runtime Foundation | 不能作为单一业务提交 |
| `frontend/lib/runtimeApi.js` | XHS、RD、共享 Runtime UI | 先确认公共接口，再拆分 |
| `frontend/components/workspace/WorkspacePaneShell.js` | RD Phase 2A、XHS / Shared Workspace shell | RD 不应独占整个文件 |
| `frontend/components/runtime/WorkspaceRuntimeView.js` | RD Phase 0/1、共享 Runtime | 需要保留共享回归边界 |
| `frontend/components/terra/*` | CEO / 普通用户产品 IA 与共享 Shell | XHS Issue 明确排除，不能随 XHS 提交 |
| `frontend/app/ceo-office/page.js` | CEO 工作台重做、Runtime simulation、staffing、capability supply | 大面积产品层修改，单独 Review |

### 4.2 高风险权威文档

| 文件 | 风险 |
|---|---|
| `docs/00_Context/CURRENT_STATE.md` | 当前事实与交付边界，必须与实际代码 / Review 一致 |
| `docs/00_Context/PRODUCT_DOCUMENT_POINTER.md` | 当前文档真相入口；现有 Pointer 已指向若干未跟踪文件 |
| `docs/08_Change_Log/CHANGE_LOG.md` | 记录 Frozen 变化；不能和普通草稿一起无审查提交 |
| `docs/01_Product/Curis_Product_Blueprint.html` | Blueprint 是目标状态，不得覆盖 Current State 的 delivered fact |
| `docs/01_Product/Curis_Product_Context.md` | Frozen 产品边界，需检查是否把 Review 实现写成已交付 |
| `AGENTS.md` | 仓库级治理规则；不属于业务 feature commit |

## 5. 文档与事实一致性检查

已确认的主要一致性风险：

1. AGENTS 记录的基线是 `c0e1855f`，实际 HEAD 是 `adb52210a`；后续提交已改变文档和产品方向，但基线记录仍需 owner 确认是否应更新。
2. Pointer / Current State 已指向 XHS、RD、Computer Access、Talent Market、Workspace Engineering 等新记录，但不少对应 Issue / Review / Authority 文件仍未跟踪；从 committed HEAD 无法重现当前文档图谱。
3. RD Review 同时包含 Accepted、Implemented 和 Review Required，必须保留阶段级状态，不能压成“RD 已完成”。
4. Workspace Engineering 文档明确 Dynamic Workspace Package Runtime 尚未实现；后续任何提交都不能把 P0 Definition / Technical Proposal 当作代码交付。
5. Master Map / Page Map 是 `REVIEW REQUIRED`，Blueprint 是 `Review`；它们定义目标形状，不可替代 Current State 的已交付事实。
6. XHS 已接受的含义是 Curis 内部 Workspace vertical slice 已验收，不包含真实外部平台发布 / 分析连接器。
7. Talent Market 与 AI Capability Integration 仍有 Review / Candidate 记录，不能与已接受 Agent Computer Access P0 混成同一完成状态。
8. 旧 `docs/plan/`、`docs/curis-takeover/` 和根目录重复文档可能仍被新文档引用，但当前不能仅凭文件名决定它们应提交、归档还是保留为迁移来源。

## 6. 仓库卫生与安全风险

### 6.1 `.gitignore` 现状

当前 `.gitignore` 的工作树修改只增加：

```text
desktop/.runtime/
```

它没有覆盖：

- `desktop/target/`
- `desktop/node_modules/`
- 根目录 `.next/`
- 根目录 `.cache/`
- `data/*.sqlite.bak-*`
- `data/*-wal` / `data/*-shm`
- `backend/curis.sqlite` / `backend/curis_dev.db`
- 根目录异常 `Database object` 路径

本轮不扩展 `.gitignore`。后续如果要加规则，应单独形成 repository hygiene commit，并先确认这些路径中是否存在需要保留的正式证据或发布包。

### 6.2 Credentials / token / secret 扫描

本轮做了排除 build、数据库、cache 后的文件名和内容模式扫描：

- 未发现可直接确认的私钥内容。
- 命中主要是代码中的密钥读取、测试占位值、`.env.example` 和安全策略代码。
- `deploy/new-api/.env` 未读取；数据库和 packaged `target` 内容没有作为提交候选。
- 该扫描不能证明所有敏感数据不存在；尤其不能把活动 SQLite、WAL/SHM、Desktop packaged runtime 或日志当成安全文本文件。

结论：存在“可能包含本机数据 / 活动数据 / 配置引用”的提交风险，当前不能安全整体提交。

### 6.3 Prototype / Mock / Fixture 风险

- `curis-ui-prototype/` 与 `curis-ui-prototype.bak/` 是设计 / Prototype 来源，不能当作生产 UI 实现。
- `data/sample_publish_package.md` 是样例材料，需确认是否为文档 fixture。
- `delivery/`、`previews/`、`artifacts/` 可能是验收证据，但不能直接当作产品源文件。
- Frontend 中的静态空态、演示文本或测试数据必须与真实 API / Runtime 证据区分；本轮没有把页面存在等同于能力完成。

## 7. 建议的逻辑 Commit 分组

以下是未来提交方案，不是本轮执行结果。

### Group 0 — 证据快照与卫生隔离（不提交业务代码）

- 建议名称：`chore(repo): isolate generated artifacts and local state`
- 包含：未来经确认的 `.gitignore` 规则、明确的构建产物排除说明；不包含删除动作。
- 当前状态：未开始。
- 安全性：当前不安全；先判断 root 异常文件、数据库备份、Evidence 目录和 packaged app 是否需保留。
- 依赖：无，但应先于大规模 stage。

### Group 1 — Agent Computer Access Runtime P0

- 建议名称：`feat(runtime): accept computer access truth for local agents`
- 包含：P0 Issue / Review、`agent_adapter.py`、`test_agent_adapter.py`、`test_agent_computer_access_runtime_p0.py`，以及 `main.py` / `tool_executor.py` / `orchestrator.py` / `result_store.py` 中经过 hunk 级确认的 P0 片段。
- 当前状态：Review 已正式接受。
- 安全性：逻辑上可提交；当前文件层面不安全，因共享文件混改。
- 依赖：基础 Agent / ResultStore 既有行为。

### Group 2 — XHS Workspace accepted slice

- 建议名称：`feat(workspace): accept XHS workspace vertical slice`
- 包含：XHS Issue / Review、XHS 页面与组件、XHS focused tests、其专属 Runtime hunk、必要的 shared API hunk。
- 当前状态：`XHS IMPLEMENTATION ACCEPTED`。
- 安全性：在排除真实外部发布 / 分析承诺并拆出共享文件后可提交。
- 依赖：Shared Runtime foundation 和 Agent / capability 状态的既有契约。

### Group 3 — RD Phase 0/1 accepted slice

- 建议名称：`feat(workspace): accept RD phase 0 and phase 1 execution slice`
- 包含：Phase 0/1 的明确代码、Issue / Review、测试和对应 Evidence 引用。
- 当前状态：Phase 0/1 accepted。
- 安全性：可提交，但必须排除 Phase 2A / long-running 未收口 hunk。
- 依赖：Group 1 的 Agent Computer Access truth；共享 Runtime 不应被回退。

### Group 4 — RD Phase 2A / long-running reliability candidate

- 建议名称：`feat(workspace): add RD phase 2A execution reliability candidate`
- 包含：Phase 2A UI、worker / long-running execution、相关测试、Review Required 记录。
- 当前状态：Implemented / Review Required。
- 安全性：不能标记为正式验收；必须独立提交，便于回退与复审。
- 依赖：Group 3、Group 1 和 Shared Runtime。

### Group 5 — Shared Runtime / Workspace foundation

- 建议名称：`feat(runtime): consolidate workspace runtime foundation`
- 包含：`backend/app/runtime/*`、runtime foundation router、Runtime Provider / State / API、Workspace Pane 中确认属于共享内核的 hunk。
- 当前状态：部分已有验证，整体边界仍混合。
- 安全性：当前不安全；需要先有文件级 ownership matrix 和回归基线。
- 依赖：既有 Company OS / Workspace contract；被 XHS / RD 依赖。

### Group 6 — AI Capability / Talent Market Review candidate

- 建议名称：`feat(capability): add capability and talent market review candidate`
- 包含：AI capability registry、multi-protocol gateway、Agent conversion、Talent Market 页面 / tests / docs、对应 Review。
- 当前状态：Review / Candidate；不宣称外部资源已可用。
- 安全性：不安全，尤其 `backend/app/main.py`、数据库迁移、Talent Market UI 混入多项能力。
- 依赖：Company Capability contract、Credential / Agent boundary、Group 1 的状态真相。

### Group 7 — Frozen product / architecture / design authority docs

- 建议名称：`docs(authority): register frozen product and workspace authorities`
- 包含：已确认 Frozen 的 Authority / ADR，以及与其直接配套的正式 Review 记录；不包含根目录重复来源。
- 当前状态：部分 Frozen，部分 Review。
- 安全性：文档可独立提交，但必须先做引用扫描和状态核对。
- 依赖：Pointer / Current State / Change Log 的一致性。

### Group 8 — Product rebaseline / candidate docs

- 建议名称：`docs(product): record ordinary-user product rebaseline candidates`
- 包含：Master Map v2.0、Page Map v1.0、Blueprint / Product Context 的对应变更、Talent Market / Content Growth candidate docs。
- 当前状态：Review Required / Review。
- 安全性：需 CEO review 后提交；不能与 Frozen authority 混淆。
- 依赖：Group 7 的上位边界。

### Group 9 — Workspace Engineering methodology / P0 planning

- 建议名称：`docs(workspace): add workspace engineering review package`
- 包含：Methodology、Lifecycle、Gates、Technical Audit、Technical Proposal、P0 Definition / Plan。
- 当前状态：Review / Approved Candidate / Not Started。
- 安全性：文档组可提交；不得包含或暗示 Dynamic Package Runtime 已实现。
- 依赖：XHS accepted、RD Phase 0/1 accepted、Computer Access truth，但不是实现依赖。

### Group 10 — Issues / Reviews / Evidence registration

- 建议名称：`docs(review): register implementation issues and acceptance records`
- 包含：与已选定实现组一一对应的 Issue、Review、Evidence 索引。
- 当前状态：正式记录候选，部分 Accepted，部分 Review Required。
- 安全性：应随实现或紧随实现提交；不能单独把 Review 文档当作代码验收。
- 依赖：实际代码 diff 和测试结果。

## 8. 推荐提交顺序

1. 先建立只读 manifest 和文件 ownership matrix；本轮报告已经提供第一版分类，但还不能替代逐文件确认。
2. 先确认并隔离生成物、活动 DB、WAL/SHM、Prototype 和本机记忆；不删除。
3. 提交或确认 Group 7 的 Frozen authority 文档，使文档引用可重现。
4. 提交 Group 1 Agent Computer Access P0 的精确 hunk。
5. 提交 Group 2 XHS accepted slice。
6. 提交 Group 3 RD Phase 0/1 accepted slice。
7. 单独提交 Group 5 Shared Runtime foundation，或在实际依赖需要时先拆出其最小公共部分。
8. 提交 Group 4 RD Phase 2A / long-running candidate，并保留 Review Required。
9. 提交 Group 8、Group 9 的产品 / Workspace Engineering Review 文档。
10. 最后处理 Group 6 Talent Market / AI Capability candidate 和 Group 10 Review registration。
11. Repository hygiene 规则另行提交；不与业务代码混合。

如果 ownership matrix 证明 Group 5 是 Group 2 / 3 的必要公共基础，则 Group 5 的最小稳定部分应提前；但不应把全部 Runtime 目录作为一个“大公共提交”。

## 9. 最小验证计划

本轮只制定计划，没有运行完整产品验收。

### 9.1 Stage 前

- 保存 `git status --short --branch`、`git diff --stat` 和完整未跟踪 manifest。
- `git diff --check`。
- 对每个组逐文件核对 Issue 的 Allowed Files / Explicit Excludes。
- 对 `main.py`、`database.py`、`result_store.py`、`runtime/workspace.py`、`runtimeApi.js` 做 hunk ownership 检查。
- 对 `.env`、private key、token、数据库、WAL/SHM、packaged runtime 做敏感数据复查。
- 检查 Pointer、Current State、Change Log、Issue、Review 的状态和相互引用。
- 明确哪些根目录文件只是迁移来源，哪些 `docs/` 文件是 canonical truth。

### 9.2 Group 1

按现有 Review 的最小集合运行：

```text
backend/.venv/bin/python -m pytest -q \
  backend/tests/test_agent_adapter.py \
  backend/tests/test_agent_computer_access_runtime_p0.py \
  backend/tests/test_ai_capability_registry.py \
  backend/tests/test_codex_agent_backend.py \
  backend/tests/test_runtime_bridge_private_model.py
```

预期基准：Review 记录为 36 passed。不得使用活动数据库替代 isolated SQLite。

### 9.3 Group 2

```text
backend/.venv/bin/python -m pytest \
  backend/tests/test_xhs_calendar_note_runtime.py \
  backend/tests/test_runtime_workspace_foundation.py -q

node --test frontend/tests/runtimeWorkspaceUi.test.mjs
```

预期基准：14 backend passed、7 frontend passed；并确认没有把外部平台 publishing / analytics 写成已接通。

### 9.4 Group 3 / Group 4

- 运行 RD Review 对应的 isolated real-execution、failure-path、artifact / evidence focused tests。
- 对 Phase 2A 运行 `rdWorkspaceExecution.test.mjs` 与 `runtimeWorkspaceUi.test.mjs`。
- 对 long-running reliability 单独确认 worker、polling、timeout、persisted completion 和 packaged Desktop 503 边界。
- 不因为整理提交而重复完整产品验收；只验证拆分没有破坏已接受 Phase 0/1 和 XHS。

### 9.5 Group 5

- Runtime foundation focused backend tests。
- Runtime provider / materialization / first arrival / API / UI focused tests。
- Schema migration test 使用临时 SQLite；不接触活动 `data/curis.sqlite`。
- `git diff --check` 和前端 syntax / eslint focused check。

### 9.6 文档组

- `git diff --check`。
- 状态头、绝对路径引用、Pointer 注册和 Change Log 关系检查。
- 检查文档是否把 Blueprint target 写成 delivered fact。
- 文档组不需要为仓库整理重新跑完整 frontend / backend 验收。

### 9.7 每个未来 Commit 后

- `git diff --cached --check`。
- 只核对该 Commit 的 staged path 与本组清单一致。
- 运行该组最小 focused tests。
- 检查没有数据库、WAL/SHM、`.env`、private key、node_modules、target、`.next` 或 `.workbuddy` 进入 staged 区。

## 10. 最终回答

### A. 当前工作树到底包含什么

它包含 XHS 已接受 slice、RD Phase 0/1 已接受 slice、Agent Computer Access P0 已接受 slice、RD Phase 2A / long-running Review Required 实现、Shared Runtime / Workspace foundation、Talent Market / AI Capability candidate、产品重定基线文档、Workspace Engineering 方法论和 P0 规划，以及大量正式 Issue / Review / Evidence、Prototype、数据库、Desktop build 和本机缓存。

它不是一个可整体提交的变更集。

### B. 哪些可以安全提交

逻辑上最接近可安全提交的是：

- Agent Computer Access P0 的精确边界。
- XHS accepted slice 的精确边界。
- RD Phase 0/1 accepted slice 的精确边界。
- 已确认 Frozen 的 Authority / ADR 文档。

但当前文件状态仍有共享文件混改，所以“逻辑上可提交”不等于“现在可以直接 stage”。

### C. 哪些需要进一步确认

- `main.py`、`database.py`、`result_store.py`、Runtime workspace / router、`runtimeApi.js` 的 hunk ownership。
- RD Phase 2A 和 long-running reliability 的最终 Review 状态。
- Shared Runtime 是否已形成独立可回归边界。
- 根目录重复产品文档与 canonical `docs/` 的迁移关系。
- `desktop/` 中正式源码、证据包和 4.7 GB build 产物的边界。
- `AGENTS.md` 的治理修改是否应保留。
- 根目录异常 `Database object` 文件和活动数据库备份的来源及保留策略。

### D. 推荐 Commit 顺序

先隔离本机产物和 DB 风险，再按 Frozen authority → Agent Computer Access P0 → XHS accepted → RD Phase 0/1 → Shared Runtime → RD Review Required → 产品 / Workspace Engineering docs → Talent Market / AI Capability candidate → Review registration 的顺序推进。每组都必须按真实 diff 拆分，不能按目录盲加。

### E. 哪些应该排除 / 清理

后续清理候选：

- `desktop/target/`
- `desktop/node_modules/`
- `desktop/.runtime/`
- `frontend/.next/`
- `.cache/`
- `.workbuddy/` 本机输出与记忆
- 活动 SQLite、backup、WAL/SHM
- Prototype `.audit/`、预览和临时 artifacts
- 根目录重复迁移来源（先归档 / 注册，后续再决定是否清理）
- 根目录异常 `Database object` 文件

本轮不删除、不移动、不扩大 `.gitignore`。

### F. 是否存在阻塞提交的风险

存在，且至少有四项实质阻塞：

1. 共享核心文件跨多个 Issue 混改，无法安全按整文件提交。
2. 23,548 个实际未跟踪文件中绝大多数是 Desktop build / runtime 产物，存在误提交和敏感数据扩散风险。
3. 权威文档、Issue、Review 有相当部分只存在工作树，committed HEAD 不能重现当前文档真相。
4. AGENTS 记录的基线与实际 HEAD 不一致，且当前工作树包含 Review Required 实现，不能直接宣称干净基线。

因此本轮结论为：

> **CURIS WORKTREE AUDIT REVIEW REQUIRED**  
> **NO FILES STAGED**  
> **NO COMMITS CREATED**  
> **NO PUSH PERFORMED**

## 11. 本轮文档登记

- 已写入绝对路径：`/Users/yy/Documents/Curis AI Workspace/docs/reviews/CURIS_WORKTREE_CLEANUP_AUDIT.md`
- Status：`Review`
- 来源：当前仓库 `main` 工作树的 `git status`、`git diff --stat`、关键 `git diff`、`git ls-files --others --exclude-standard`、Issue / Review、`CURRENT_STATE`、`PRODUCT_DOCUMENT_POINTER`、`CHANGE_LOG`、敏感数据模式扫描和生成物盘点。
- Pointer / `CURRENT_STATE` / `CHANGE_LOG`：本轮未修改；原因是用户要求第一轮只做 Audit / Classification / Commit Plan / Risk Report / Validation Plan。审查通过后再决定是否注册或追加变更记录。
- 未解决下一步：由 owner 审阅本报告，确认文件 ownership、是否保留异常 / 迁移来源、以及是否授权进入分组 staging 计划。
