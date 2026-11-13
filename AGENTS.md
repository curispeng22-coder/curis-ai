# Curis Agent Instructions

Status: Frozen

本文件只规定 Agent 如何工作、如何找 Truth、如何报告结果；不复制 Curis 的当前产品或实现事实。

## 1. Minimal Retrieval Rule

先判断任务类型，只读取对应最小路径：

`PRODUCT_DOCUMENT_POINTER.md` 中只有 `Current Required Input` 是默认入口；其 Reference Ledger、Research、History 与 Deferred 清单仅在任务明确需要时读取。

### Product Truth

1. `docs/00_Context/PRODUCT_DOCUMENT_POINTER.md`
2. `docs/01_Product/Curis_Product_Blueprint.html`
3. `docs/01_Product/Curis_Product_Master_Map.md`
4. `docs/01_Product/Curis_Product_UI_Blueprint.html`
5. 适用的 `Status: Frozen` Authority

### Development / Implementation Truth

1. `docs/00_Context/CURRENT_STATE.md`
2. 当前正式 Issue / Allowed Files / Approved Design
3. 当前 Accepted Review
4. Code / Runtime / Test / Browser / Desktop / Database Evidence

### Research / Reasoning

读取被明确点名的 Research、Exploration、Review 或 Decision Evidence；它们解释为什么，不能覆盖 Current Authority。

### History / Archive

只在任务需要历史依据、迁移来源或决策 provenance 时读取 `docs/99_Archive/` 或被明确点名的历史文件。历史永远不是普通任务的 Current Authority。

不要默认通读历史文档、全部 Review 或全部代码。完成任务前，确认每个引用的 `Authority Class` 与 `Status / Disposition`。

## 2. Truth Governance

- Product Truth、Implementation Truth、Research Evidence、History / Archive 必须分开表达。
- Product Truth 的路线是：Pointer → Product Blueprint → Master Map → UI Blueprint → applicable Frozen Authority。
- Implementation Truth 的路线是：CURRENT_STATE → active Issue / Approved Design → Code / Runtime → Accepted Evidence。
- Research / History 只能提供背景、理由或证据，不能因搜索、RAG 或文件名优先而覆盖 Current。
- 发现 Current Authority 互相冲突时，立即 `STOP / REPORT AUTHORITY CONFLICT`，不得自行选择或创造第三种答案。
- Product 与 Implementation 不一致时，登记 `PRODUCT → IMPLEMENTATION GAP`；不得把目标产品冒充已交付，也不得用实现反向改写产品。
- CEO 接受的 Research / Review 必须有明确 `Disposition`；接受结果必须写明 `Verdict / Disposition / Owner / Next Action / Target Authority / Next Gate`。
- 重要文档使用轻量元数据：`Authority Class`（CURRENT / FROZEN / RESEARCH / REVIEW / HISTORY / EVIDENCE）与 `Status` / `Disposition`。

## 3. Repository And Scope Discipline

- 当前产品文档只写入 `/Users/yy/Documents/Curis AI Workspace/docs/`；worktree、临时目录和未登记文件不是产品真相。
- 不创建第二份 Current Blueprint、Master Map、Page Map、UI Blueprint 或平行产品架构。
- 不覆盖、重置、删除、checkout、stage、commit 或 push 用户已有改动，除非明确授权。
- 文档任务不得修改业务代码、Runtime、Schema、数据库、Prototype 或高保真 UI。
- 不泄露凭证、密钥、私有提示词、Cookie 或用户数据；不绕过 Tenant、Company、身份和数据隔离。
- 不将 Mock、静态页面、候选构建、局部测试或单个 API 结果当作完整产品能力。

## 4. Task / Issue / Review Discipline

- 任何业务代码变更必须先有正式 Issue，Issue 必须定义 Scope、Allowed Files、输入、输出和验收证据。
- 不在未获产品 Decision 时重设计产品；顺序固定为 Product Definition → Business Runtime Blueprint → UI Design → Code。
- 质量验收必须使用与任务匹配的真实证据；完整能力不能仅凭页面、按钮、API 200 或测试通过宣称完成。
- Review 必须记录实际证据、失败边界、Decision 和未完成项；未接受、阻塞、草稿不得写成完成。
- 已完成历史可搜索，但不会自动成为新任务上下文。

## 5. Documentation Discipline

- 文档只能使用 `Status: Draft`、`Review`、`Frozen`、`Deprecated`；详细状态规则见 `docs/00_Context/DOCUMENT_STATUS_RULES.md`。
- 创建或迁移文档时，回报绝对路径、Status、Authority Class、来源、Pointer/Index 更新和未解决下一步。
- 修改 Current Product Truth、Implementation Truth 或 Frozen Decision 时，同步更新相应 Pointer、CURRENT_STATE 和 `docs/08_Change_Log/CHANGE_LOG.md`。
- 移动、重命名或归档前先扫描引用；历史决策应归档，不应伪装成当前内容或直接删除。

## 6. Module Routing

- Product: `docs/01_Product/Curis_Product_Context.md`
- Architecture: `docs/02_Architecture/Curis_System_Architecture.md`
- Design: `docs/03_Design/Curis_Design_System.md`
- Development: `docs/04_Development/Curis_Development_Guide.md`
- 支撑索引：`docs/00_Context/DOCUMENT_INVENTORY.md`。索引只用于定位，不产生 Authority。

## 7. Current Product Documents

- Product Blueprint 是唯一 Product Authority。
- Master Map 只展开 Blueprint 的页面、字段、动作、入口和来源。
- UI Blueprint 只消费 Product Blueprint、Master Map 与适用 Frozen Authority，不得静默改变产品模型。
- `docs/00_Context/CURRENT_STATE.md` 记录 Implementation Truth 与 Product → Implementation Gap，不等同于产品目标。

## 8. Stop Conditions

遇到 Authority 冲突、缺少必要授权、缺少合法证据、Scope 不清或会产生第二套真相时，停止扩展，报告具体阻塞、责任 Owner、恢复入口和下一 Gate。

## 9. Agent Start, Task Scope, And Workspace

- Start each task from this file, then read `docs/00_Context/CURIS_CURRENT_ENTRYPOINT.md`; follow its links to the Pointer, Current State, governance, canonical backlogs, and active task. The entrypoint navigates only and is not Product Authority.
- Every multi-file or implementation task must have a Task ID and explicit `Allowed Files` and `Allowed Directories`. The user’s exact grant may define them. If scope is missing or a target is outside it, fail closed and ask for the missing scope before writing.
- `artifacts/tasks/<TASK-ID>/` is the approved temporary artifact area when the task needs one. Do not create it in advance. Do not create a new top-level directory or use an unlisted directory. A specific task may explicitly authorize an existing directory or exact new directory.
- Do not use the workspace root for reports, screenshots, prototypes, generated outputs, or temporary files unless the task explicitly names the exact root path.
- Product / Frozen Authority writes require explicit CEO or delegated Owner decision, an exact file grant, and synchronized provenance. A task issue, review, prototype, or agent output cannot promote itself.

## 10. Agent Start / End And Output Contract

- Start: record Task ID, objective, Allowed Files/Directories, required inputs, outputs, owner, and acceptance evidence. Read only the current routed inputs and task-scoped history needed for this work.
- Keep generated or temporary files under the granted Task Workspace. Do not move them into canonical docs until an Owner accepts their disposition.
- End: report changed paths, Authority Class / Status, evidence and checks, skipped items with reasons, unresolved risks, and the next Gate. Include a Task Output Manifest listing each output path and its disposition.
- Use only these dispositions for durable task outputs: `PROMOTE` after authorized acceptance into its canonical Authority/Backlog; `ARCHIVE` after an approved historical destination and index entry; `DELETE` only for an exact approved set after retention, source, evidence, Git, reference, and recovery checks; otherwise retain in the scoped task area or mark `REVIEW_REQUIRED`.
- Backlog promotion updates the existing canonical backlog and its links; never create a parallel backlog. Temporary cleanup is exact-path and owner-scoped; never sweep unrelated task output.
- Do not stage, commit, push, clean, reset, checkout, stash, or remove worktrees unless the task explicitly authorizes the exact operation and paths.
