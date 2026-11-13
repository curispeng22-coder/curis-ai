# Workflow

Status: Deprecated

## Goal

Keep AI collaboration low-token, role-bounded, and reviewable.

## Default Rule

Read only the minimum context needed for the current task.

Do not scan the whole repository unless the task explicitly requires repo-wide review.

Do not repeat role responsibilities, default read files, or standard forbidden scope in every handoff. Each Curis seat is expected to know its own boundary and the other seats' boundaries from `AGENTS.md`.

## Curis Seat Defaults

### 产品规划席

默认读取：

- `knowledge/000_Project_Brief.md`
- `knowledge/002_Product_Vision.md`
- `knowledge/CURRENT_CONTEXT.md`
- `PROJECT_STATUS.md`
- `TASKS.md`

负责产品目标、用户需求、Roadmap、Milestone、Sprint 目标、验收标准、Backlog 优先级和唯一事实源校准。

### 系统交付席

默认读取：

- `AGENTS.md`
- `knowledge/003_Architecture.md`
- `knowledge/CURRENT_CONTEXT.md`
- 当前 Issue 文件

负责系统架构、模块边界、Issue 技术设计、后端/前端实现、技术 Review 和已批准 Issue 的 Commit。

### 质量运行席

默认读取：

- `AGENTS.md`
- `PROJECT_STATUS.md`
- `knowledge/CURRENT_CONTEXT.md`
- 当前 Issue 文件

负责测试策略、验证命令、环境可靠性、完成证据和回归风险。

### 总控决策席

默认读取：

- `PROJECT_STATUS.md`
- `TASKS.md`
- `knowledge/CURRENT_CONTEXT.md`
- 相关 Issue 或 Review 文件

负责 Gate 决策、范围冲突裁决、Sprint 推进审批，以及长期愿景和当前 gate 的边界裁决。

### 安全边界席

默认读取：

- `AGENTS.md`
- `knowledge/005_Key_Decisions.md`
- 相关 Issue 或 Review 文件

负责数据处理、密钥、外部服务、隐私与安全阻塞项。

## Curis Operating Seats

- 总控决策席：direction, gate decisions, scope conflict, sprint advancement.
- 产品规划席：product scope, PRD, backlog, acceptance criteria, source-of-truth hygiene.
- 系统交付席：architecture boundaries, implementation, technical review, commits.
- 质量运行席：verification, commands, environment reliability, completion evidence.
- 安全边界席：secrets, external services, data handling, privacy, security blockers.

Standalone legacy roles are no longer active dispatch targets.

## Compact Handoff

Default handoff format:

```text
Issue:
Objective:
Special Constraints:
Next Seat:
```

Use this short format unless the task has unusual constraints or crosses a role boundary.

Rules:

- Do not restate normal role responsibilities.
- Do not restate default read lists.
- Do not paste long context from source documents.
- Link to the issue, review, or current context instead of summarizing it.
- Add reminders only for new risk, gate change, blocker, or permission boundary.

## Automatic Seat Routing

Curis seats route work by default after completing their part. The main thread should not continuously poll role threads.

Default route:

1. 产品规划席 -> 系统交付席
2. 系统交付席 -> 质量运行席
3. 质量运行席 -> 产品规划席
4. 产品规划席 -> main thread closeout to user

Exception route:

- Gate decision, sprint advancement, or scope conflict -> 总控决策席
- Secrets, external services, privacy, or data handling risk -> 安全边界席
- Product ambiguity found by another seat -> 产品规划席
- Architecture ambiguity found by quality review -> 系统交付席

Each seat must write `Next Seat` and update `knowledge/CURRENT_CONTEXT.md` before handoff.

The main thread only performs final acceptance closeout, user-facing summary, and escalation when a blocker needs the user.

Every final user-facing report must start with one sentence summarizing product progress: what Curis Workspace can do now.

Handoff execution rule:

- Writing `Next Seat` is not enough.
- The completing seat must attempt to send the compact handoff to the next seat when thread messaging is available.
- If direct sending succeeds, report `Handoff: sent to <seat>`.
- If direct sending is unavailable, report `Handoff: HANDOFF_REQUIRED` with target seat and compact handoff payload.
- Direct seat-to-seat messaging is preferred, but not assumed to be available in every thread.
- The main thread acts as workflow router only for `HANDOFF_REQUIRED`, final closeout, or user-level blocker.
- A work item is not complete until handoff status is `sent`, `final closeout`, or `HANDOFF_REQUIRED`.

Seat thread ids live in `docs/pmo/current-status.md` and should be read only when a seat needs to send a direct handoff.

## Issue Flow

1. 产品规划席定义产品意图和验收标准。
2. 总控决策席确认任务是否在当前 gate 内。
3. 系统交付席在需要时编写 Issue 技术设计并实现已批准 Issue。
4. 系统交付席用 compact handoff 交给质量运行席。
5. 质量运行席提供验证证据，并用 compact handoff 交回产品规划席。
6. 产品规划席验收或要求修订。
7. 产品规划席将完成证据交给 main thread，由 main thread 向用户收尾汇报。
8. 总控决策席只在 Sprint 关闭、推进或 gate 冲突时介入。
9. Update `knowledge/CURRENT_CONTEXT.md`.
10. If the sprint changed, update `PROJECT_STATUS.md` and `TASKS.md`.

## Final Report Shape

```text
Product Progress: Curis Workspace can now ...
Completed:
Verification:
Known Gap:
Next:
Handoff:
```
