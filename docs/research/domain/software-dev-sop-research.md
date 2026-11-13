# Curis Software Development SOP Research

Status: Phase-3.5 research conclusion

## Decision

Curis Phase-4 should use a minimal, sequential Software R&D SOP:

```text
Requirement Understanding
-> Task Breakdown
-> Architecture Design
-> Coding
-> Testing
-> Report
```

This borrows the role/action chain from MetaGPT and the review/test loop discipline from ChatDev, while avoiding a full multi-agent workflow engine.

## Evidence

- MetaGPT: one-line requirement becomes PRD, architecture, tasks, code, tests, and docs.
- ChatDev: virtual software company separates planning, coding, review, testing, and loop limits.
- Paperclip Companies: AgentSys Engineering separates discovery, planning, implementation, review, and shipping.
- CrewAI examples: tasks should define `description`, `expected_output`, and assigned agent.

## Curis R&D SOP v1

| Step | Owner | Output | Capabilities |
| --- | --- | --- | --- |
| Requirement Understanding | Product Manager | objective, user need, scope, non-goals, acceptance criteria | model |
| Task Breakdown | Tech Lead | ordered subtasks, dependencies, risk notes | model, tool |
| Architecture Design | Architect | module boundary, data/API contract, implementation guardrails | model, tool |
| Coding | Frontend Engineer / Backend Engineer | code changes inside approved boundary | model, tool |
| Testing | QA Engineer | command evidence, failing/passing status, known gaps | model, tool, connector |
| Report | Tech Lead + Product Manager | CEO-readable completion summary and next step | model |

## Phase-4 Implement

If approved by gate:

- store SOP as metadata or template records
- allow a task to be assigned to Software R&D department
- expose which employee owns each step
- preserve output summaries in a trace/read model
- keep current Task Execution path intact unless a separate runtime gate approves routing

## Phase-4 Reserve

- automatic step execution
- automatic code generation through employees
- multi-iteration review loops
- human approval nodes
- cross-department routing
- dynamic employee generation

## Step Contracts

Requirement Understanding:

- input: CEO task content
- output: concise product brief
- owner: Product Manager

Task Breakdown:

- input: product brief
- output: ordered work items
- owner: Tech Lead

Architecture Design:

- input: product brief and work items
- output: boundary plan
- owner: Architect

Coding:

- input: boundary plan and work items
- output: implementation evidence
- owner: Frontend/Backend Engineer

Testing:

- input: implementation evidence
- output: verification report
- owner: QA Engineer

Report:

- input: verification report and work summary
- output: CEO summary
- owner: Tech Lead/Product Manager

## Not Adopted

- MetaGPT full repo generation.
- ChatDev full YAML DAG runtime.
- Paperclip 24/7 autonomous heartbeats.
- CrewAI hierarchical manager process.
- AutoAgents dynamic role creation.

## Phase-4 Acceptance Direction

The first implementation should prove:

- R&D department template exists.
- six employee templates exist.
- SOP step ownership is visible or queryable.
- capability binding can be attached to employees.
- no current task execution regression occurs.
