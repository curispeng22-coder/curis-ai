# Agent Execution Loop

## Purpose

The Agent Execution Loop defines how an AI agent repeatedly acts inside Curis Workspace without drifting from gates, context boundaries, or role authority.

## Loop

```text
Observe
  -> Classify
  -> Authorize
  -> Bound Context
  -> Act
  -> Verify
  -> Reflect
  -> Report
```

For first-run bootstrap execution, use the smaller loop in `mvp-execution-loop.md`.

## Step Rules

### Observe

Read the minimum state required:

- `AGENTS.md`
- Current Sprint review file
- `system-state-machine.md`
- `sprint-gate-system.md`
- Target source-of-truth document

### Classify

Classify the request by:

- Phase
- Scope class
- Owner role
- Gate impact
- Risk level

### Authorize

Check:

- Is the task allowed by the current gate?
- Does the acting role have authority?
- Is a blocker present?
- Is business code requested before Sprint 1?

If authorization fails, stop and report the blocking gate.

### Bound Context

Apply the context tiers in `context-boundary-system.md`.

Do not load broad context unless target files or governing rules are unclear.

### Act

Make the smallest reviewable change inside the allowed file boundary.

Do not combine unrelated governance, planning, and implementation tasks.

### Verify

Run the strongest practical verification:

- Plugin validation when plugin metadata or skill docs change
- Skill validation when skill docs change
- Targeted text search for forbidden placeholders or gate contradictions
- Git status review for changed files

### Report

面向 CEO、用户或上级 AI 员工的汇报统一使用 `ceo-reporting-standard.md`：

```text
结论：发生了什么。
原因：为什么。
建议：下一步怎么做。
```

内部可以保留完整证据；最终汇报默认使用中文白话，不堆技术术语、Contract 或 Issue 内容。

### Reflect

Check whether:

- The output satisfies the requested artifacts.
- The state machine needs an update.
- Sprint gates remain closed or require status changes.
- Feedback should be routed into another runtime slice.

### Report

Report only:

- Changed files
- Verification evidence
- Current runtime state
- Gate status

## Stop Conditions

Stop immediately when:

- The task enters business implementation before Sprint 1.
- A blocker authority stops work.
- Verification contradicts completion.
- The user explicitly pauses or redirects the task.
