# RD-WORKSPACE-INSTANCE-001 Review

**Status:** PHASE 0/1 ACCEPTED · PHASE 2A DESIGN FIDELITY PASS · LONG-RUNNING EXECUTION RELIABILITY IMPLEMENTED · REVIEW REQUIRED  
**Date:** 2026-08-16  
**Issue:** `issues/RD-WORKSPACE-INSTANCE-001.md`

## Scope

Phase 0 / Phase 1 only: RD real Project/Cycle → Task → Codex → Artifact/Evidence/
Result Reference → restart/failure truth.

## Implemented vertical slice

```text
existing Project → Runtime Cycle (`rd_task:auto`) → Responsibility Holder
→ Company Employee + tenant-private Codex capability binding
→ existing Task / Orchestrator / CodexCliAdapter
→ declared-file diff + post-execution command
→ ResultStore Artifact + Runtime Evidence + Conversation Result Reference
```

- Cycle no longer needs a manually entered `workflow_run:<id>` for this bounded path.
- Object Owner, Responsibility Holder and Current Executor remain separate. The executor is
  populated only around the real Task call and is `none` after success, failure and restart.
- Initial assignment is not represented as Handoff. Artifact Review, Acceptance and Decision
  are intentionally absent from this Phase 0/1 slice.

## Changed files

- `backend/app/runtime/workspace.py`
- `backend/app/runtime/execution_adapter.py`
- `backend/app/api/runtime_foundation_router.py`
- `backend/app/main.py`
- `backend/app/agent_adapter.py`
- `backend/tests/test_agent_adapter.py`
- `backend/tests/test_rd_workspace_real_execution.py`
- `frontend/components/rd/RdRealExecutionComposer.js`
- `frontend/components/runtime/WorkspaceRuntimeView.js`
- `frontend/tests/rdWorkspaceExecution.test.mjs`
- `issues/RD-WORKSPACE-INSTANCE-001.md`
- `reviews/RD-WORKSPACE-INSTANCE-001_review.md`

No XHS/TTK source, Frozen Contract, Product Blueprint or active database was changed.

## Real Runtime evidence

Evidence root: `/tmp/curis-rd-real-oys_cvl4/`  
SQLite: `/tmp/curis-rd-real-oys_cvl4/rd-real.sqlite`  
Machine-readable manifest: `/tmp/curis-rd-real-oys_cvl4/evidence.json`

### Successful real Codex execution

- Workspace: `workspace-2f644031-4d5b-4ec9-8650-734160b3bdeb`
- Cycle: `cycle-2ca16f43-b625-4c46-80df-8e1a3129c1f1`
- Task: `667c7d6f-ce74-4f40-82e1-bd38d7954080` → `COMPLETED`
- Codex session: `01a0067c-6a29-79b1-b832-7d2e46fd447e`
- Code-change Artifact: `artifact-00c96e3e-728e-4ad9-9594-301599572553`
- Runtime Evidence: `evidence-ff114f7f-32f1-433e-a8fe-182bafb8caf0`
- Real file diff: `calc.py`, `return a - b` → `return a + b`
- Real command: `python3 -m unittest -q`, exit `0`
- Cycle execution status: `COMPLETED`; lifecycle remains `RUNNING` because later RD review/
  acceptance phases are explicitly out of scope.
- Conversation contains only a plain summary and Result References; diff/test detail remains
  in Artifact/Evidence.

### Truthful failure execution

- Workspace: `workspace-5c53d6a8-204b-4ec2-8ab1-9f34e5e3dbb5`
- Cycle: `cycle-60f1e2f7-7f4a-4987-9686-99743bcbfec5`
- Task: `74509aea-2740-480e-b913-ce9f771094be` → `FAILED`
- Codex session: `01a0067c-dc77-7ae0-b008-79fa164cf142`
- Code-change Artifact: `artifact-b2749197-053c-443a-bbb2-968630a36a7a`
- Runtime Evidence: `evidence-abfc07be-cadf-40d9-923f-24eea6a2ce03`
- The same real code diff was retained, but the declared verification command exited `7`.
- Cycle is `PAUSED`, execution is `FAILED`, Responsibility remains assigned, Current Executor
  is `none`; it was not converted to Completed and no CEO Decision was invented.

The initial run also exposed a real adapter failure before any Artifact: Codex refused a
non-Git isolated directory. The minimum root-cause fix adds Codex's native
`--skip-git-repo-check` to new sessions, matching the already truthful resume path. No sandbox
or approval state was widened.

## Computer Access truth

Both real sessions persist:

- requested intent: `AUTO_WITHIN_BOUNDARY`
- native mapping: `workspace-write`, command argument `APPLIED`
- configured state: `CONFIGURED`
- effective state: `UNKNOWN`
- verification state: `UNVERIFIED`

No Full Computer Access was requested or enabled. `CONFIGURED` is not projected as granted or
effective.

## Persistence evidence

A new App instance and TestClient reopened the same isolated SQLite after both executions.
The same Cycle, Responsibility, Company Employee/Capability binding, Task, Codex session,
Artifact, Evidence, Result Reference and final status were readable. Current Executor remained
`none` for both success and failure. Persistence did not imply that Codex was still running.

## Verification

- Backend focused + Computer Access + XHS no-regression: `16 passed`.
- Frontend RD/API/Workspace/XHS shared-view checks: `20 passed`.
- Python compile and JavaScript syntax checks: passed.
- `git diff --check` for all bounded files: passed.
- Test warnings are pre-existing FastAPI deprecations and Node module-type warnings; no test
  failed.

## Remaining RD phases

- Approved RD professional shell/high-fidelity work surface migration.
- Multi-Employee responsibility/executor projections.
- Artifact Review Request, distinct from Handoff.
- Genuine Handoff between employees.
- P7 CEO Decision where business judgment is required.
- Broader System Activity and packaged Desktop acceptance.

## Decision

`RD PHASE 0/1 PASS · REAL CODE EXECUTION VERIFIED`

## Phase 2A acceptance record

### Implemented professional Workspace

- `WorkspacePaneShell` remains the shared four-Pane shell. RD supplies its own pane labels,
  Context and Utility while XHS defaults stay unchanged.
- RD Main is a vertical Employee Workstation stack backed by real Runtime Cycles; no XHS
  Calendar/Note object or lifecycle was copied.
- Each station independently projects Object Owner, Responsibility Holder, Current Executor,
  Task and execution status. During the real Codex call the Runtime projected `RUNNING` and
  the actual executor; after completion and failure it projected `Current Executor = none`.
- Conversation contains only the plain result summary and a Result Reference. Context contains
  only the current Project/Cycle/Task, declared files and related Evidence.
- Utility reads the same Task's `code_change` Artifact and exposes Diff, test evidence and
  execution metadata including the Codex session and Computer Access snapshot.

### Fresh isolated Runtime evidence

Evidence root: `/tmp/curis-rd-real-oys_cvl4/`  
SQLite: `/tmp/curis-rd-real-oys_cvl4/rd-real.sqlite`  
SQLite SHA-256 after execution: `50c52ffda50e28b4bffa46e5b136625171ae50c947aa550057c4f7e385dd6d4c`  
SQLite integrity: `ok`

Successful Phase 2A execution:

- Company: `company-rd-phase2a-5a9a837b`
- Workspace: `workspace-6cd38a33-16d5-4eaf-a3c3-9b41aa5e0836`
- Project: `project-7b8a47c1-4b8c-4a54-ace3-5a304d1b2f93`
- Cycle: `cycle-862a743e-8dc4-40aa-82b0-2a31ad440ed6`
- Task: `0fb5bfa9-8213-4a82-84a4-3b5ae809e764` → `COMPLETED`
- Codex session: `01a0069e-0d0a-7b32-8aeb-87eac603ca8a`
- Code-change Artifact: `artifact-6a4d9ab8-c2cf-44c0-969f-348264213a17`
- Evidence: `evidence-2659f254-5bf8-4d53-8728-1fd0b6b2a165`
- Real diff: `calc.py`, `return a - b` → `return a + b`
- Real test: `python3 -m unittest -q`, exit `0`, one test `OK`
- Browser polling observed `1 项执行中`, Holder `Engineering AI` and Current Executor
  `Engineering AI` while Codex was running. The same station then became `执行完成`, retained
  its Holder, cleared Current Executor to `none`, and exposed the Result Reference.

Computer Access remained truthful:

- requested: `AUTO_WITHIN_BOUNDARY`
- native mapping: Codex new session, `workspace-write`, `APPLIED`
- configured: `CONFIGURED`
- effective: `UNKNOWN`
- verification: `UNVERIFIED`

Truthful failure projection:

- Workspace: `workspace-555bd032-b61e-495d-91c8-791c7d28796a`
- Cycle: `cycle-2199611d-ded1-48a6-98ce-b1c1aaa81088` → lifecycle `PAUSED`, execution `FAILED`
- Task: `4c26f773-86f2-458f-9949-ed753e2378da`
- Evidence: `evidence-0d025a17-f74f-416c-8e49-5cee80e03d9b`
- Browser displayed `执行失败`, retained the Responsibility Holder, cleared Current Executor
  to `none`, and did not offer an invented automatic retry or mark the Cycle Completed.

### Browser and persistence evidence

- Fresh Browser route rendered real Project/Cycle/Task, three Runtime-backed workstations,
  Context and Utility with no console error.
- Utility Diff showed the exact `calc.py` patch; Test showed the real command and exit `0`;
  Execution showed the same Task, Artifact, session and Computer Access truth.
- Context and Utility were open simultaneously with Main; shared Search and Utility Maximize
  remained available through the already accepted Shell implementation.
- Screenshot: `/tmp/rd-phase2a-final.jpg`; failure screenshot:
  `/tmp/rd-phase2a-failure.jpg`.
- The backend was stopped and recreated against the exact same SQLite. Browser reload recovered
  the same Project/Cycle/Task/status and still showed `0 项执行中`; persistence did not imply
  that Codex remained active.

### Verification

- Frontend RD/API/shared Workspace focused suite: `21 passed`.
- Backend RD real execution + Codex Adapter: `5 passed`.
- XHS accepted Runtime no-regression: `2 passed`.
- Browser console: no errors or warnings on the fresh acceptance page.

### Phase 2A changed files

- `backend/app/main.py` — the existing synchronous Codex execution is run in a worker thread
  so the same Runtime can truthfully expose `RUNNING` to concurrent reads; no execution model
  or new queue was introduced.
- `frontend/app/ceo-office/workspace/software/page.js`
- `frontend/components/rd/RdWorkspacePhaseTwo.js`
- `frontend/components/workspace/WorkspacePaneShell.js`
- `frontend/tests/rdWorkspaceExecution.test.mjs`
- `frontend/tests/runtimeWorkspaceUi.test.mjs`
- `issues/RD-WORKSPACE-INSTANCE-001.md`
- `reviews/RD-WORKSPACE-INSTANCE-001_review.md`

No XHS/TTK business source, Frozen Contract, Product Blueprint, active database, Handoff,
Artifact Review Request, CEO Decision or Phase 2B behavior was added.

## Phase 2A decision

`RD PHASE 2A PROFESSIONAL WORKSPACE REVIEW REQUIRED`

## Phase 2A design fidelity closure record

### Changed files

- `frontend/components/rd/RdWorkspacePhaseTwo.js`
- `frontend/components/rd/RdRealExecutionComposer.js`
- `frontend/tests/rdWorkspaceExecution.test.mjs`
- `issues/RD-WORKSPACE-INSTANCE-001.md`
- `reviews/RD-WORKSPACE-INSTANCE-001_review.md`

没有修改 backend Runtime、XHS/TTK、Frozen Contract、Product Blueprint 或活动数据库。

### Browser evidence

- Fresh Browser 使用 Phase 2A 同一隔离 Runtime/SQLite，默认 Main 不显示 Task/Cycle/
  Artifact/Evidence/Codex Session UUID 或 Computer Access 内部枚举。
- Context 默认显示项目背景、当前工作、相关文件、已有结果；内部 ID 仅在关闭的
  `查看技术引用` 中。
- Main 显示“研发员工 · 研发工程师”、当前工作、负责人、当前无人执行、白话结果与
  `查看代码变化与测试结果` Result Reference。
- Utility 默认显示真实 Diff；执行详情把 requested/configured/effective 事实翻译为
  “自动处理 / 已按允许范围配置 / 当前无法由服务方确认”，原枚举仅在关闭的技术详情。
- Composer 默认只显示研发项目、要解决的问题和期望结果；执行范围与验证方式位于关闭的
  `执行详情（通常无需修改）`。
- Browser screenshot: `/tmp/rd-phase2a-design-fidelity.jpg`。

### Packaged Desktop evidence

- Current source fresh build succeeded:
  `desktop/target/release/bundle/macos/Curis.app`，build manifest
  `2026-08-15T18:31:53Z`。
- Fresh isolated root: `/tmp/curis-rd-desktop-success.25XYqy/`；没有读取或写入
  `data/curis.sqlite`。
- Packaged Runtime 通过官方 API 建立 Company/Project/Employee/Workspace/Cycle，调用
  real Codex session 修改 `src/calc.py`，Task `COMPLETED`，真实测试
  `python3 -m unittest -q tests.test_calc` exit `0`，生成真实 code-change Artifact；
  Computer Access 仍为 requested `AUTO_WITHIN_BOUNDARY`、configured `CONFIGURED`、
  effective `UNKNOWN`、verification `UNVERIFIED`。
- Desktop 页面显示 1 名研发员工、1 项工作、0 项进行中、1 项已完成；展开后显示
  “当前无人执行”、白话结果、Result Reference，并可在 Context + Main + Utility 同时打开时
  读取真实 Diff。截图：`/tmp/rd-phase2a-design-fidelity-desktop-success.png`。
- stop/restart 后同一 Company/Workspace/Task/Artifact 仍可读取，Employee 恢复为可接手；
  SQLite SHA-256 `90da3b51ce9b988570d1093e67ca2d2fee5a8826698ab204b35cd848e5a490a0`，
  integrity `ok`。
- Frontend stderr 为空；页面和 Workspace/Task API 重启后均为 200。

### Fidelity comparison

| Result | Approved intent | Closure result |
|---|---|---|
| KEEP | 四 Pane、T1/T2/T3、Resizable、Search、Utility Maximize、Result Reference | 复用已验收 Shared Shell；本轮未重写 |
| MATCHED | Main 是 Employee Workstation / Work Conversation | 员工、当前责任、执行者、进展和结果成为默认主对象 |
| MATCHED | Context 是项目/当前工作/文件/结果 | UUID 收入折叠技术引用 |
| MATCHED | Utility 分层展示 Diff/Test/执行证据 | 用户结果、专业 Evidence、技术 metadata 三层 |
| MATCHED | Employee != Agent | Codex/provider/session 只在 Utility 技术层 |
| MATCHED | 真实 waiting/failed/idle/completed | UI 只消费 Runtime 状态；完成后 Current Executor 为 none |
| INTENTIONAL DELTA | Approved reference 使用具名员工 | Workspace Runtime 仍只有 `Engineering AI`；为避免编造，显示中性“研发员工 · 研发工程师” |
| INTENTIONAL DELTA | 常规启动不要求执行细节 | Project 尚无 Context Assembly 默认范围；文件范围/验证命令仍在 Advanced 中按需确认 |
| REMAINING DRIFT | Employee proper identity | 需后续真实 Employee identity/assignment 数据，不属于本 Closure |
| REMAINING DRIFT | Packaged 长耗时执行反馈 | real Codex 超过 Gateway 等待窗时调用方收到 503，backend 仍完成并持久化；本轮不改 Runtime/IPC |

### Verification

- Frontend focused/API/shared Workspace suite: `21 passed`。
- Backend RD real execution + Codex Adapter + XHS Runtime no-regression: `7 passed`。
- Current source packaged Desktop build: passed。
- JavaScript syntax and bounded `git diff --check`: passed。
- 现有 FastAPI deprecation 与 Node module-type warning 保持原样；没有新增测试失败。

### Review decision requested

`RD PHASE 2A DESIGN FIDELITY REVIEW REQUIRED`

## Long-running execution reliability closure record

### Implemented transport/runtime boundary

- `POST .../cycles/{cycle_id}/execute` 对 `rd_task:auto` 只负责把既有 Cycle/Responsibility/
  Execution Binding 原子推进到真实 `RUNNING`，随后 HTTP `202` 返回；不等待 Codex、测试、
  Artifact 或 Evidence。
- 后台继续复用既有 `RuntimeExecutionAdapter`、真实 Task/Orchestrator/Codex Adapter、
  ResultStore 与原成功/失败落库函数；没有新增 Job Queue、Workflow、DAG 或第二套执行对象。
- 当前真实 Task ref 在创建后写回同一 Cycle，Workspace Runtime 可以在 Codex 返回前观察
  Task、Responsibility Holder 与 Current Executor。
- 同一 Cycle 已是 `RUNNING` 时，重复提交直接返回同一 Cycle；数据库确认对应 Task 只有
  1 条 `executions` 记录。
- 真实测试命令移入 worker thread，长测试期间 Backend event loop 仍可响应 Runtime/Health
  读取。Frontend 对既有 Workspace Runtime 的 `RUNNING` 进行 800ms 轮询，不伪造流式状态。
- 启动时仅对无法证明外部 Agent 仍存活的遗留 `rd_task:auto / RUNNING` 执行 fail-closed
  reconciliation；已完成和已失败状态不被重写。

### Packaged Desktop long-running success evidence

Current-source package:

- App: `desktop/target/release/bundle/macos/Curis.app`
- Build manifest: `gitSha=adb52210aaa4b230560412e6b224b37622dad495`,
  `builtAt=2026-08-15T19:45:31Z`
- Isolated HOME/SQLite root: `/tmp/curis-rd-desktop-success.25XYqy/`
- SQLite: `/tmp/curis-rd-desktop-success.25XYqy/Library/Application Support/com.curis.desktop/data/curis.sqlite`
- Controlled project: `/tmp/curis-rd-desktop-success.25XYqy/rd-project`

Successful real execution:

- Workspace: `workspace-2cb533dc-f74d-4edb-b1ad-18047107263a`
- Cycle: `cycle-f1fc9f90-df8d-4952-a37f-1da837819ad2`
- Task: `872d1eac-8556-4c43-90af-7f1500a942b3` → `COMPLETED`
- Codex session: `01a006f7-f5a0-7053-b993-5c80332b0eaf`
- Code/result Artifacts: `artifact-225c885b-ee2d-4bda-8eb0-42089382d7ad`,
  `artifact-6d7dacd6-acff-4eb6-a9af-83166d6836ea`
- Evidence: `evidence-c9b22785-f258-41ad-85a3-733bb0e45c06`
- Real diff: `src/calc.py` 新增 `square(value)`；没有修改声明范围外文件。
- Real verification: `python3 -c 'import time; time.sleep(55); ...'`, exit `0`。

Submit/observe truth:

- start: HTTP `200`, `0.010569s`
- submit: HTTP `202`, `0.015752s`, body `RUNNING`
- immediate duplicate: HTTP `202`, `0.009963s`, same Cycle；没有第二个 active execution。
- 任务从 Task `created_at=19:48:25Z` 到最终 Artifact `created_at=19:51:16Z`，明确超过旧
  Gateway 等待窗；期间连续观察保持 `RUNNING`，Health 读取约 `0.0012–0.0024s`，没有 503。
- 完成后同一 Cycle 显示 `COMPLETED`，2 Artifacts、1 Evidence、Result References 可读，
  Current Executor 为 `none`。

### Truthful failure evidence

- Cycle: `cycle-3c10de20-767e-4cde-b3bf-4632cc8351e1`
- Task: `383a788a-da19-4c32-98a5-5a68ee579323` → `FAILED`
- Codex session: `01a006fd-4e95-7f32-932f-fa8de5670f11`
- Artifacts: `artifact-55b4573a-6d89-4400-86f3-c661013f3cae`,
  `artifact-67663cd5-159a-4d20-945d-e3126cc5ab92`
- Evidence: `evidence-912f9400-072e-4ee9-9d6a-6aac3687b198`
- Real Codex diff added `negate(value)`；声明验证命令真实 exit `7`。
- Cycle=`PAUSED`、Execution=`FAILED`、Current Executor=`none`；Conversation 明确保留代码
  与失败 Evidence，UI 不显示 Completed，也不自动重试。

### Browser/Desktop and restart evidence

- Browser route显示 4 项真实工作：3 项完成、1 项需要处理；失败项显示真实 Holder、
  `当前无人执行`、失败证据入口与“当前不会自动重试”。Browser console errors: `0`。
- Packaged Desktop 显示完成项 Result Reference，Utility 读取同一 `src/calc.py` Diff；失败项
  显示“需要处理”且 Current Executor 已清空。
- Desktop screenshots:
  `/tmp/rd-long-running-desktop-completed.jpeg`,
  `/tmp/rd-long-running-desktop-failed.jpeg`。
- Browser screenshot: `/tmp/rd-long-running-browser-failed.png`。
- 在两个执行均收口后停止并重启同一 `.app` / 同一隔离 SQLite：成功 Cycle 仍为
  `COMPLETED`，失败 Cycle 仍为 `PAUSED/FAILED`；两者各保留 2 Artifacts、1 Evidence，
  Current Executor 均为 `none`。SQLite integrity: `ok`。

### Computer Access truth

成功与失败 Session 均保持：

- requested: `AUTO_WITHIN_BOUNDARY`
- native mapping: Codex new session, `workspace-write`, `APPLIED`
- configured: `CONFIGURED`
- effective: `UNKNOWN`
- verification: `UNVERIFIED`

没有请求或启用 Full Computer Access；异步化没有把 configured 投影成 effective。

### Changed files

- `backend/app/api/runtime_foundation_router.py`
- `backend/app/runtime/workspace.py`
- `backend/app/main.py`
- `backend/tests/test_rd_workspace_real_execution.py`
- `frontend/components/rd/RdWorkspacePhaseTwo.js`
- `frontend/tests/rdWorkspaceExecution.test.mjs`
- `issues/RD-WORKSPACE-INSTANCE-001.md`
- `reviews/RD-WORKSPACE-INSTANCE-001_review.md`

没有修改 XHS/TTK 业务源、Frozen Contract、Product Blueprint 或活动数据库。

### Verification

- Backend RD/operating-cycle/Computer Access/XHS Runtime focused suite: `11 passed`。
- Frontend RD/shared Workspace focused suite: `3 passed`。
- Current-source packaged Desktop build: passed。
- Browser console errors: `0`；SQLite integrity: `ok`；bounded `git diff --check`: passed。
- 现有 FastAPI deprecation warnings 保持原样；没有测试失败。

### Remaining RD scope

Phase 2B Multi-Employee、Artifact Review Request、真实 Handoff 与后续 P7 仍未开始；本
Closure 不改变其顺序，也不进入 Computer Access P1/P2。

### Review decision requested

`RD LONG-RUNNING EXECUTION RELIABILITY REVIEW REQUIRED`
