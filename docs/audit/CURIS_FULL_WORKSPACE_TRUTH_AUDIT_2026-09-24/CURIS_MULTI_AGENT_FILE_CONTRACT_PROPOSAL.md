# Multi-Agent File Creation Contract Proposal

Status: Review  
Authority Class: REVIEW  
Baseline: `78cacbd0857cc36c9f3fe0e4b11346489993b728`  
Updated: 2026-09-24  
Disposition: AUDIT / PROPOSAL — NON-AUTHORITATIVE; CEO review required.

## Default: fail closed

No Agent writes until the Task Lead supplies the following task envelope. Missing field means **no filesystem write** and a return asking the Task Lead to fill it.

| Field | Required value | Default without grant |
|---|---|---|
| Task ID | Formal Issue ID / audit ID | Block |
| Owner and Task Lead | One accountable owner + coordinator | Block |
| Allowed Files | Exact existing paths or bounded creation glob | No existing files writable |
| Allowed Directories | Exact directories; `artifacts/tasks/<TASK-ID>/` for task artifacts | No directory creation |
| Task Workspace | One exact path | None; block artifact generation |
| Can Create File? | Yes/no + types + max scope | No |
| Can Create Directory? | No by default; exact named subpath if yes | No |
| Can Modify Authority? | Exact file(s) and decision/CEO grant | No |
| Can Modify Pointer? | Exact path and verified authority promotion | No |
| Can Modify Current State? | Exact path and implementation registration scope | No |
| Can Modify Backlog? | Canonical backlog item path + owner approval | No |
| Can Generate HTML / Screenshot? | Explicit yes/no; allowed path and evidence purpose | No |
| Can Generate Temporary Evidence? | Explicit types, storage, sensitivity, retention | No |
| Required outputs and acceptance | Reviewable files/evidence and done definition | Block |
| End disposition | PROMOTE / ARCHIVE / DELETE owner and gate | Block task closure |

## Write routing

- Product/code source: only exact Issue `Allowed Files` in canonical `docs/`, `frontend/`, `backend/`, `desktop/`, `deploy/` roots. Creating a new directory is a separate explicit grant.
- Research, review draft, HTML, screenshots, test logs, comparison assets and Agent intermediate outputs: `artifacts/tasks/<TASK-ID>/` only. No root writes and no per-Agent sibling task roots.
- Evidence promoted to durable Review: move/copy only under an explicit promotion grant after naming the review target and source provenance. Do not duplicate output across folders without a reason.
- Worktree is for source isolation only; it does not grant authority or permit new product-doc roots.
- Multi-Agent jobs: Task Lead assigns non-overlapping file lists and unique output names. Shared writes require one named owner; parallel edits to the same file fail closed.
- Secret, DB and user data: never copied into generic Task Workspace; use protected tool-owned storage and redacted references.

## Task Workspace layout

```text
artifacts/tasks/<TASK-ID>/
  TASK_OUTPUT_MANIFEST.md
  <task-id>__<agent>__<type>__<seq>.<ext>
```

No nested type/agent directory is needed by default. The manifest records every created/modified file, agent/source, purpose, evidence, candidate outputs, backlog references, promotion request and final disposition. An Issue may authorize a task-specific subdirectory when it reduces collisions; the grant names it exactly.

## Agent End-of-Task Contract

Before returning, each Agent (including subagents) reports:

1. Task ID and scope result.
2. Created files, modified files, and any file left outside its exact grant.
3. Temporary files and screenshots, with disposition and retention date.
4. Evidence (source/revision, commands/results or capture context).
5. Candidate outputs, proposed target Authority, and promotion requested (yes/no).
6. Backlog item changes with canonical backlog path and owner.
7. Cleanup candidates; no cleanup performed unless task explicitly authorized.
8. Remaining blocker / next gate / handoff owner.

Task Lead reconciles this return to `TASK_OUTPUT_MANIFEST.md`; missing outputs or dispositions keep the task open. Promotion requests never self-approve.

## Task close

`PROMOTE` only cited evidence or accepted truth to its authorized canonical class. `ARCHIVE` durable rejected/superseded provenance after reference review. `DELETE` only exact transient outputs after owner confirmation and integrity/data-risk check. If no safe disposition is known, leave it in Task Workspace, mark `REVIEW_REQUIRED`, set owner/date, and do not create another copy. Default transient TTL: 30 days after task terminal; protect evidence with explicit retention.
