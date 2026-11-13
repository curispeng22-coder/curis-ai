# ADR-0016 Gate Submission Package — 总控决策席 决策请求

- Date: 2026-07-07
- Submitted by: 系统交付席（架构评审结论执行）
- Source gate: `issues/044_execution_substance_phase_gate.md`（Proposed, pending）
- Source ADR: `docs/decisions/ADR-0016-execution-substance-initiative.md`（Proposed）
- Target approval: **总控决策席**
- Status: Approved by 总控决策席 (option a) on 2026-07-07 — ADR-0016 gate approved; Sprint 3 Role Context block lifted for Sub-decision A (see ADR-0018).

---

## 1. 背景与定位

- 本包是 `issues/044` 的正式决策请求，附 `docs/decisions/ADR-0016`。
- 上游已定：`reviews/037_redesign_v2_architecture_review_decision.md` 结论为——**v2 架构文档归档为未来蓝图、不替换唯一事实源（SoT）；下一执行动作 = 把 ADR-0016 提总控决策席做 gate 批准，按 Role wiring → Event log → Sandbox 三个小 gate 走**。本包即该动作。
- `issues/044` 已定义边界，但**遗漏了 D1 与已批准 Sprint 3 边界的正面冲突**。本包补上该关键决策点，供总控决策席 conscious 裁决。

## 2. 决策请求（一句话）

请求总控决策席：**批准 ADR-0016 的 gate**，并**显式裁决 D1（runtime role 接入 prompt）与 Sprint 3 Role Context 边界的冲突**，随后按三个小 gate 顺序推进三切片。

## 3. ADR-0016 三切片摘要

| 切片 | 内容 | 性质 | 风险 |
|------|------|------|------|
| **D1 Runtime Role Wiring** | 把 `backend/app/role_context.py` 按显式 profile-id 接入 `prompt_builder.py` / `employee.py` step 路由；role context 仅加 prompt/context 指引 | 行为变更（受约束） | 中（撞 Sprint 3 边界，见 §4） |
| **D2 Governor Sandbox** | 在 throwaway 副本上 apply+rollback 一个 Stability-first 提案，捕获证据；零写入权威 repo/SQLite；生产变更仍需人工批准 | 加性执行基底 | 高价值 / 高谨慎 |
| **D3 Append-Only Event Log** | 新增不可变 `evolution_events` 表（带 correlation id）；mutable 表可保留供查询 | 加性 schema | 低（无行为变更直至读端点使用） |

## 4. ⚠️ 关键决策点：D1 vs Sprint 3 Role Context 边界冲突

**冲突双方**
- ADR-0016 D1：把 `role_context` **接入 `prompt_builder.py` / `employee.py` step 路由**（runtime prompt 集成）。
- `knowledge/003_Architecture.md` **Sprint 3 Role Context Runtime Reference Boundary**（line 112–121）：明确写 **"Runtime prompt integration remains blocked"**；且 `role_context.py` 当前仅只读 helper，**未接 prompt 执行、API、持久化、路由**。
- `issues/044` line 55 隐含允许 "role-context guidance" 接入，与 Sprint 3 边界**直接矛盾**。

**风险**：若不显式裁决，D1 实现会**静默违反已批准边界**，破坏 gate 纪律（这正是 037 判定的「0.3 需单独解禁 gate」）。

**选项**
- **(a) 批准 D1 并显式解禁 Sprint 3 边界**：仅限 ADR-0016 Sub-decision A 约束——显式 profile-id、仅加 prompt/context 指引、**不选工具 / 不路由 / 不改任务状态 / 不触发演进**、缺失或无效 profile-id 时行为不变。解禁须记录为对 Sprint 3 边界的 **consciously superseded**（新 ADR 或边界修订），不得静默。
- **(b) 暂缓 D1，保留 Sprint 3 边界**：本期只走 D3 + D2；D1 留待独立 gate。
- **(c) 否决 D1**：从本倡议移除 runtime role 接入。

**建议：(a)**。D1 是 ADR-0016 最低风险、最高价值首切片；解禁范围已被严格约束，且须留痕，不构成失控自演进。

## 5. 推荐执行顺序与每片验证

**顺序（若选 a）**：D1（须先完成 Sprint 3 解禁留痕）→ D3 → D2
**顺序（若选 b）**：D3 → D2，D1 另立 gate

**每片验证（来自 ADR-0016 §Verification）**
- D1：断言 `role_context` 被 `prompt_builder` / `employee` import；缺失/无效 profile-id 输出不变。
- D3：断言 `evolution_events` **仅 insert**（无 UPDATE/DELETE 路径）且带 correlation id。
- D2：断言 sandbox **仅写 throwaway 路径**；dry run 下零写入 repo/SQLite。
- 通用 guard：`git diff --name-only HEAD -- backend frontend` + `rg`  forbidden-scope 关键词（Employee CRUD / multi-agent / company organization / ROI / business module / external channel / dashboard / automatic code self-modification）。

## 6. Trade-off（命名放弃项）

- **放弃**：v0.1「纯文档 / 无生产变更」纯度，换取三个未来最大阻断（runtime role / Governor 执行 / 演进审计）从 deferred 转为 demonstrable。
- **保留**：Stability > Optimization > Evolution 策略、生产变更人工批准、不解除自动改码禁令、现有执行行为（除三窄变更）、中文操作台、Task API `{ content }`、Project Memory 事实源归属。

## 7. Forbidden Scope（沿用 ADR-0016 + 044）

后端/前端行为变更（三切片外）、新功能、复杂 UI/dashboard、API 语义变更（加性读/事件端点除外）、丢弃/变更现有表、向量库/embeddings、外部记忆服务、agent/Employee 记忆、task-role 关联、task 证据挂载、多 Agent 协调/路由、新执行行为、自动演进行为变更 / 自动改码、ROI/经济、业务模块、Employee CRUD/扩展、公司组织/部门、agent 抽象层、未来层实现。

## 8. Required Preservation（沿用 044）

AI Task Executor MVP v0.1 本地/demo 发布、Tool System v1.8 loop、Stability > Optimization > Evolution、中文操作台、Task API `{ content }`、现有 API 语义（加性端点除外）、现有执行行为（三窄变更除外）、Evolution Governor 决策策略、人工批准 gate、Project Memory 事实源归属、Role Profiles / Role Context / release 记录与标签语义。

## 9. 关联与依赖

- `reviews/037_redesign_v2_architecture_review_decision.md` — v2 评审结论（蓝图不替 SoT；本 gate 为下一执行动作）
- `docs/decisions/ADR-0016-execution-substance-initiative.md` — 源决策（Proposed）
- `issues/044_execution_substance_phase_gate.md` — 边界 gate（Proposed, pending）
- `issues/045_runtime_role_wiring_first_slice.md` / `046_evolution_governor_sandbox_first_slice.md` / `047_append_only_evolution_log_first_slice.md` — 三 first-slice issue，gate 批准后可开
- `docs/decisions/ADR-0017-multitenant-department-catalog.md` — 多租户部门（未来 gate，不在此包）

## 10. Compact Handoff Payload（给总控决策席）

- **Issue**: `issues/048_adr0016_gate_submission_package.md`（+ `044` + `ADR-0016`）
- **Objective**: 批准 ADR-0016 gate；裁决 D1 / Sprint 3 边界冲突；按小 gate 推进三切片
- **关键决策**: D1 解禁 Sprint 3 边界（建议 a，须留痕） / 或暂缓（b）
- **Preserve**: 见 §8 ｜ **Allow**: 仅三切片边界定义 + 事实源更新 ｜ **Forbid**: 见 §7
- **Next Seat**: 批准后 → 系统交付席 定义每片边界 → 质量运行席 验证 → 产品规划席 接受 → 开 `045/046/047`

## Handoff

**Handoff: APPROVED (decision recorded) — next seat 系统交付席 defines per-slice boundaries.**

总控决策席 于 2026-07-07 选中选项 (a)：批准 ADR-0016 gate；显式解禁 Sprint 3 Role Context 边界，D1 接 prompt 留痕（ADR-0018）；顺序 D1→D3→D2。Supersede 记录见 ADR-0018；D1 边界见 ADR-0019。Payload 见 §10。本包与 `issues/044` 一并提交：044 定义边界，本包补充关键决策点（D1 / Sprint 3 冲突）与裁决请求，二者不可拆分审批。
