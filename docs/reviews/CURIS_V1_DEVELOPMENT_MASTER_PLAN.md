# CURIS V1 DEVELOPMENT MASTER PLAN

Status: Review  
Authority Class: REVIEW / PLAN  
Date: 2026-08-26  
Source: `CURIS_V1_APP_READINESS_AUDIT.md`  
Disposition: Proposed shortest path to a usable V1; does not modify Product Authority

## 1. Objective

将现有已验收 Runtime 与专业切片装配成一个普通用户可以真实使用、关闭并继续使用的 Curis V1。原则是复用已有底座，不新增第二套 Company、Workspace、Employee、Task、Decision、Result 或 Workflow 系统。

## 2. V1 Acceptance Gate

V1 只有在同一 fresh packaged Desktop、同一 isolated app-data 中证明以下链路后才可接受：

`Local CEO → verified model → Company/Assistant → canonical Business → General Workspace → Employee Work → Result/Evidence → Decision/Recovery → restart → same history`

并至少有一个专业 Workspace（RD）完成创建入口到真实执行结果的全链。

## 3. Delivery Order

### P0 — First Usable Company

Goal: 第一次打开后不再停在基础设施或空白 CEO Desk。

Reuse:
- FoundingRun / CompanyProposal
- canonical Business Spine atomic create
- CEO Assistant
- generic Workspace Package renderer
- current model catalog / Health / Keychain boundary

Deliver:
1. 普通语言 First Run，只采集最小经营意图和首个可验证结果。
2. 已有信息不重复询问；模型未连接可浏览/保存草稿，真实执行前阻断。
3. CEO 确认后原子创建 Company、Assistant、canonical Business、First General Workspace。
4. 成功返回真实对象与入口，不只 toast。
5. CEO Desk 展示第一项业务、Workspace、下一动作；无业务时提供唯一创建入口。
6. 安全 Secret 后端在 packaged Desktop 跨重启可用；不把明文写 SQLite/log/API。

Acceptance:
- cancel/reject 不产生 Business/Workspace。
- failure injection 不留下半创建对象。
- refresh/restart 恢复 Proposal 或已创建对象。
- active DB 不受测试影响。

### P1 — General Business Operating Loop

Goal: 用户不依赖专业模板也能经营第一项业务。

Reuse:
- InstalledWorkspaceRuntime / WorkspacePaneShell
- Team Operating / Responsibility Routing
- SharedEmployeeWorkArea
- ResultStore / Evidence / Handoff / Decision P7
- bounded Autonomous Operating

Deliver:
1. General Workspace 首页：目标、团队、当前工作、待决定、结果、下一步。
2. Goal 生成最小 Work；Employee/Responsibility 使用 canonical objects。
3. 用户表达问题与期望结果；技术执行参数进入高级详情。
4. Employee Conversation 只展示白话状态与 Result/Decision references。
5. Result/Evidence、failure/wait/UNKNOWN、handoff、CEO decision、next cycle 可回访。
6. restart 后 holder/executor/session truth 不漂移。

Acceptance:
- 至少一个真实 provider-backed Work；没有 live provider 时允许 Codex/Ollama 已证明路径，不得 mock。
- 一个真实 failure/recovery。
- 同一 Work/Result/Decision restart persistence。

### P2 — First Professional Workspace: RD

Goal: 将最成熟的专业 Workspace 变成 V1 的首个专业结果闭环。

Reuse:
- accepted RD professional shell and workstation
- real Codex execution
- async submit/observe
- Artifact Review / Handoff / P7
- Computer Access P0 truth

Deliver:
1. 从 canonical Business/Workspace 创建入口选择 RD。
2. 用户只填写研发目标和期望结果。
3. 真实 Employee → Codex → file change → tests → Artifact/Evidence。
4. review/handoff/decision 在产品层可回访。
5. 结果回到 CEO Desk，形成下一周期。

Acceptance:
- fresh packaged Desktop full RD journey。
- real file/test evidence。
- failure, duplicate protection, restart。
- XHS no-regression。

### P3 — Content Growth + Release Closure

Goal: 实现当前 authority 下的 Content Growth 内部专业经营面，并完成可分发 V1 门禁。

Deliver:
1. 只实现已批准 IA 的 Professional Surfaces，不复制 legacy XHS page 作为当前产品。
2. Research → Content → Evaluation 的内部真实 Work/Result/Evidence。
3. Channel 状态按 evidence matrix 显示 UNKNOWN/CONDITIONAL/UNAVAILABLE。
4. 无 Connector 时允许手动、未验证输入；不得生成假 publish/analytics。
5. macOS signing/notarization、安装/升级策略、backup/restore 最小闭环。

Acceptance:
- Content Growth internal loop 可用，外部能力边界诚实。
- signed/notarized release candidate 或明确 distribution blocker。
- backup/restore 与 update failure recovery 有实际证据。

## 4. Parallelization Without Divergence

可并行：

- Stream A: First Run / canonical Business UI wiring。
- Stream B: packaged Secret persistence / model setup continuity。
- Stream C: General Workspace product assembly。
- Stream D: packaged whole-app E2E and release infrastructure。

必须串行：

- `frontend/app/onboarding/page.js`、canonical creation API contract、shared Workspace entry 等 mixed integration seams。
- Product Authority 变更。
- active schema migration。

## 5. Hard Boundaries

- 不建立新 Company/Business/Workspace/Employee/Task/Decision/Result system。
- 不建立通用 DAG / Workflow Engine。
- 不把 Provider catalog 扩展当主线。
- 不把 mock、deterministic local provider 或 manual receipt 冒充真实外部能力。
- 不因 Content Growth 推迟 General Workspace 和 RD 首个可用闭环。
- 不修改 active SQLite；测试统一使用 repository-external isolated SQLite。

## 6. Completion Evidence Per Phase

每阶段必须同时有：

1. focused backend/frontend tests；
2. isolated SQLite；
3. Browser vertical proof；
4. fresh Packaged Desktop proof；
5. failure/recovery；
6. stop/restart/reopen；
7. active DB fingerprints unchanged；
8. explicit unsupported/not-proven list。

## 7. Recommended First Issue

`V1-P0-001 — FIRST RUN TO CANONICAL GENERAL WORKSPACE`

Bounded goal:

`FoundingRun → CEO-confirmed Proposal → canonical Business + First General Workspace atomic create → CEO Desk/Workspace entry → restart read`

Explicit exclusions:

- no new Provider catalog;
- no Content Growth/RD implementation;
- no new workflow/runtime primitive;
- no active DB migration;
- no visual redesign beyond current authority;
- no fake team/execution/result.

This is the shortest task that converts existing foundations into a product path.
