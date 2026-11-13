# Canonical Workspace Structure V1 Proposal

Status: Review  
Authority Class: REVIEW  
Baseline: `78cacbd0857cc36c9f3fe0e4b11346489993b728`  
Updated: 2026-09-24  
Disposition: AUDIT / PROPOSAL — NON-AUTHORITATIVE; CEO review required.

## Design rule

Reuse the existing product/implementation roots. Add no new first-level product, research, review, screenshot or task directories. Reuse the existing `artifacts/` root and propose one controlled `artifacts/tasks/` subdirectory for temporary task work. Creating that subdirectory still requires CEO approval. This structure is a proposal and does not authorize moves or new Authority.

```text
/
  AGENTS.md  README.md  repo configs
  docs/
    00_Context/ 01_Product/ 02_Architecture/ 03_Design/ 04_Development/
    05_Workspace_Engineering/ 07_Decisions/ 08_Change_Log/ 99_Archive/
    research/ reviews/ standards/ contracts/ (existing governed subtrees)
  issues/
  frontend/  backend/ desktop/ deploy/
  data/                         # runtime/user data, protected
  artifacts/
    tasks/<TASK-ID>/            # one temporary workspace per authorized task
  .agents/                      # repository agent config/skills only
  .worktrees/<TASK-ID>/         # managed code worktrees only
```

## Canonical directory contract

| Directory | Purpose | Allowed content | Forbidden content | Who can write | Lifecycle | Class |
|---|---|---|---|---|---|---|
| `/` | repository entry and build configuration | AGENTS, README, Git/config/build manifests, verified app entrypoints | Research, review, candidate, task output, HTML exploration, screenshots, audit, evidence, backlog copies | Repo owner / task agent only for exact Issue-allowed root files | long-lived; exact allowlist | Current / mixed config |
| `docs/00_Context/` | current route, implementation state and supporting indexes | Pointer, CURRENT_STATE, inventories, status rules | second Blueprint or duplicate current state | Product/System owner, bounded task with explicit file grant | current; references updated under the applicable rule | Current / Frozen |
| `docs/01_Product/` | sole product definitions | Product Blueprint, Master Map, UI Blueprint and routed product context | Candidate, research dumps, screenshot batches | Product owner only; explicit CEO decision for product truth changes | current; superseded contract is Deprecated/Archive through reviewed path | Current / Frozen |
| `docs/02_Architecture/`, `03_Design/`, `04_Development/`, `05_Workspace_Engineering/`, `07_Decisions/` | durable architecture/design/development/engineering/decision standards | governed contract docs, ADRs and accepted standards | active scratch/revisions, unreviewed alternatives | domain owner by exact Issue; Decision owner for Frozen ADR | durable; review then promote/supersede | Frozen / Review |
| `docs/research/` | durable research reports and provenance | scoped Research with evidence, source, date, owner, disposition | active screenshot/temp batches without task id; current truth | research owner within authorized task | keep cited findings; reject/archive per review | Research |
| `docs/reviews/` | review, acceptance, closure and decision evidence | formal Issue Reviews, CEO decisions, acceptance/evidence index | active multi-version design scratch; undocumented `TODO` treated as backlog | reviewer/owner of scoped Issue | permanent evidence if decision/acceptance; status/disposition explicit | Review / Evidence |
| `docs/99_Archive/` | traceable historical files | superseded docs with reference map and Deprecated status | current inputs, unreviewed dumps or runtime data | documentation owner after reference and consumer check | durable historical record | Historical |
| `issues/` | only active/closed executable task contracts | bounded Issue with task id, scope, Allowed Files/Directories, gates | free-form product facts, parallel backlog, unapproved work | Issue owner/triage; code task requires formal approval | Proposed → scoped → active → closed/cancelled | Backlog / Task |
| `frontend/`, `backend/`, `desktop/`, `deploy/` | implementation and deployment source | files named by approved Issue | research/doc/screenshot dumps; generated arbitrary output | engineering owner within Allowed Files | source-controlled; tests/evidence in authorized locations | Implementation |
| `data/` | persistent project/runtime data | canonical DB and authorized fixtures/backups | scratch reports and unclassified DB files | data/runtime owner only | protected; explicit backup/retention/restore policy | Protected data |
| `artifacts/tasks/<TASK-ID>/` | temporary workspace for all task/Agent intermediates | one task manifest, drafts, candidate HTML, screenshots, logs and test evidence allowed by task envelope | product authority claims; cross-task shared backlogs; secrets; unlisted directories | Task Lead + named agents only inside exact assigned path | must close with PROMOTE / ARCHIVE / DELETE; default expires 30 days after accepted/cancelled task, unless formal evidence is promoted or deletion is blocked | Temporary |
| `.agents/` | repo-owned agent config, skills and policies | reviewed skills/prompt references required by project | per-task outputs, screenshots, private user data | tool/repo owner by explicit Issue | durable config, versioned/reviewed | Configuration |
| `.worktrees/<TASK-ID>/` | managed isolated source checkout | Git worktree content under branch/Issue scope | duplicate canonical truth or untracked task artifacts that should use Task Workspace | developer/automation with exact task id; deletion separately authorized | close/hand back; never remove while dirty/active | Temporary checkout |
| dependency/build/cache dirs | reproducible generated state | tool-managed dependencies and build outputs | product docs, canonical evidence | package/build tooling | retain per tool/ignore rules; clean only exact safe targets | Generated |

Existing `reviews/`, `prototypes/`, `.design/`, `previews/` and business-named exploration roots are legacy locations: no new writes; keep current evidence until a separately authorized Part 2/3 reference and disposition review. This proposal does not move them.

## Chosen Task Workspace pattern

`artifacts/tasks/<TASK-ID>/` — flat at task root. The task output manifest lists paths and roles; no agent may invent a sibling `*_EXPLORATION`, `*_FINAL_NEW`, `*_TEST` or `_shots-rN` folder. A Task Lead assigns distinct filenames/paths to parallel agents. Product-source edits still occur only in Issue-allowed canonical source paths, not in the temporary workspace.

## Canonical structure verdict

Keep code and Product Authority where they already are. Establish one task artifact destination and a root allowlist first. Migration/cleanup of legacy directory families is a later gated task after Part 2 lineage review.
