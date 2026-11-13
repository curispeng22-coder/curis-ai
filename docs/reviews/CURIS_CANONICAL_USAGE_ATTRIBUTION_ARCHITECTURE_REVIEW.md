# CURIS CANONICAL USAGE ATTRIBUTION ARCHITECTURE REVIEW

Status: Review

Authority Class: REVIEW

Baseline: `main @ c797db840bad285d7e9f1962d06eac61aa28508b`

Updated: 2026-08-27

Module: Company OS / Usage Attribution / Provider Execution

Owner: Main Development / Runtime Integration

Disposition: PENDING CEO / ARCHITECTURE REVIEW

Supersedes: none

## 0. Review boundary and verdict

This is a read-only architecture review. It did not modify Runtime, schema, tests, APIs, active SQLite, Product Authority, or the stopped V1 Epic.

The current failure is a shared ownership-contract defect, not a General Workspace domain defect:

```text
General Workspace
→ canonical Cycle / Work / Responsibility / Employee / Capability
→ ResultStore Task
→ execute_model_gateway()
→ AIUsageService Project-required validation
→ "business model call attribution is incomplete"
→ Provider is not launched
```

Current Product Authority defines `Company → Department → Business → Workspace` as canonical ownership. `Project` remains a legitimate RD/legacy domain object, but is not a universal Company OS parent and must not be synthesized merely to authorize execution.

**Verdict: ARCHITECTURE CHANGE APPROVED CANDIDATE**

The minimum change is to extend the existing Task + `ai_usage_records` attribution contract so it accepts either a verified canonical Workspace lineage or the existing verified legacy Project lineage. It must remain one usage/audit system.

## 1. Current Project dependency map

### 1.1 Project is a real domain object in these paths

| Area | Current use | Classification | Required treatment |
|---|---|---|---|
| RD / Company Project Runtime | Project owns RD-oriented tasks, department relation and legacy project operating context | Legitimate domain object | Keep |
| Legacy Workflow Runtime | `workflow_instances` / runs may resolve and validate `project_id` and Department | Legitimate compatibility/domain context | Keep |
| Project task job route | Route and authorization are explicitly scoped by `{project_id}/tasks/{task_id}` | Legitimate legacy API | Keep |
| Project Knowledge / Context / Memory paths | Project scopes relevant domain material | Legitimate optional domain context | Keep; not a shared execution prerequisite |
| Existing RD Provider E2E | Task → Project → Department supplies accepted legacy attribution | Accepted compatibility path | Preserve as regression baseline |

### 1.2 Project is currently borrowed only to recover shared ownership

| Location | Current dependency | Why it is not a domain requirement |
|---|---|---|
| `backend/app/main.py::execute_model_gateway/execute_attempt` | Reads Task `project_id`, then Project `department_id` before every model/agent attempt | Provider execution needs trustworthy Company ownership, not an RD Project |
| `backend/app/ai_usage.py::AIUsageService._validate_lineage` | Requires Task, Project, Department and Employee; rejects missing Project | The ledger is using Project as a surrogate Company/Department resolver |
| `backend/app/database.py::ai_usage_records` | `project_id text not null`; no Company/Business/Workspace/Work/Execution fields | Schema encodes the old surrogate as mandatory |
| `backend/app/business_metrics.py` | Company cost is summed by joining usage Project IDs back to Company | Canonical Workspace usage would be omitted even if execution were allowed |
| `backend/app/task_execution_control.py` | Left joins Project to derive Department for timeline associations | Timeline lacks canonical Business/Workspace/Work attribution |
| `backend/app/orchestrator.py` | Reconstructs `RuntimeCapabilityContext` from Task company/project fields | Durable Task has no canonical Workspace/Work execution snapshot |

### 1.3 Compatibility surfaces that expose Project but do not require it

- `tasks.project_id` is already nullable.
- ResultStore Task/API payloads expose optional `project_id`.
- Workflow and task-job read models return Project attribution for legacy callers.
- Existing billing totals aggregate tenant usage without requiring Project.
- Existing usage APIs filter/group by Project and Department; those dimensions must remain available.

### 1.4 Incorrect shared precondition

The false invariant is:

```text
Project exists
→ therefore execution ownership is valid
```

The correct invariant is:

```text
one verified ownership lineage exists
→ therefore execution attribution is valid

canonical: Tenant / Company / Workspace / Business / Department / Work / Execution
legacy:    Tenant / Company / Project / Department / Task
```

No path may fall back to an arbitrary/default Project.

## 2. Why the current contract blocks General Workspace

General Workspace correctly creates no Project. Its durable facts already include:

- `company_id` and `workspace_id` on canonical Runtime entities;
- `business_id` on Workspace;
- Workspace → canonical Business → Department → Company constraints;
- canonical `WORK` under the Workspace;
- Responsibility Assignment and canonical Employee;
- active Capability Binding;
- Team Operating `work_ref` and `execution_key`;
- append-only `execution.identity_bound` provenance for the ResultStore Task.

The Team Operating bridge then creates a ResultStore Task containing Company, Employee and Capability, but it does not persist Workspace, Work or Execution attribution on that Task. The Orchestrator can therefore reconstruct only the old Task/Project-shaped context. `execute_model_gateway()` asks for Project and Department, and `AIUsageService` plus `ai_usage_records.project_id NOT NULL` enforce the same historical assumption.

This is why a valid General Workspace reaches the accepted execution bridge yet fails before Codex launch. Creating a Project would hide the contract defect and contradict Current Product Truth.

## 3. Canonical ownership model

### 3.1 Shared ownership lineage

For new canonical Workspace execution, the authoritative resolver is:

```text
tenant
└── company
    └── workspace
        └── canonical business
            └── department

workspace
└── canonical work
    ├── responsibility assignment
    ├── canonical employee identity / company employee bridge
    ├── capability binding
    └── execution / ResultStore task
```

The caller supplies stable source identities already owned by the Runtime: Company, Workspace, Work and Execution. The shared service resolves Business and Department from canonical persisted relations; it must not trust duplicated caller strings.

### 3.2 Attribution snapshot for each provider/model/tool attempt

The resulting immutable attribution must answer:

- Tenant
- Company
- Department
- Business and Workspace for canonical Workspace calls
- Work and Execution for canonical Workspace calls
- ResultStore Task
- Responsibility/assignment provenance
- canonical Employee / execution identity
- Capability and binding
- Provider/model/tool attempt
- optional Project or workflow context where a domain genuinely has it

The persisted usage row is an at-call-time accounting snapshot. Later Business/Department changes must not rewrite historical usage.

### 3.3 Fail-closed rules

Canonical execution is rejected before Provider launch when any of these are unresolved or inconsistent:

- Workspace is missing, cross-tenant/cross-Company, `UNRESOLVED`, or `QUARANTINED`;
- Workspace Business does not exist or does not resolve to the same Company/Department;
- Work does not belong to that Workspace/Company;
- ResultStore Task does not match the bound Employee/Capability/Work/Execution;
- Employee identity bridge or Capability Binding is missing/invalid;
- supplied Project conflicts with canonical ownership.

The resolver must never choose the first Project, a default Project, or a free-form parent reference.

## 4. Domain object versus ownership object

| Object | Shared ownership role | Domain role |
|---|---|---|
| Company | Required root | None |
| Department | Required canonical parent of Business | Organizational context |
| Business | Required canonical parent of Workspace | Sustainable business identity |
| Workspace | Required operating ownership scope | Professional workspace instance |
| Work / Execution | Required execution attribution | Domain-independent operating work |
| Project | Not universally required | Optional RD/legacy domain object |
| Topic / Research / Content | Not shared ownership parents | Future Workspace-domain context |

RD may validly use:

```text
Workspace → RD Project → Work
```

General Workspace may validly use:

```text
Workspace → Work
```

Content Growth may later use:

```text
Workspace → Research / Content → Work
```

Project, Topic, Research and Content must remain optional domain attribution. This review does not recommend adding speculative `topic_id`, `research_id`, or `content_id` columns.

## 5. Minimal schema, Runtime and API change

### 5.1 Reuse, do not create a second system

Reuse:

- existing `AIUsageService` and immutable `ai_usage_records` ledger;
- existing ResultStore Task;
- existing Orchestrator and Model Gateway;
- existing canonical Business/Workspace constraints and Parent Resolver;
- existing canonical Work / Responsibility Routing;
- existing Employee execution identity binding and callback provenance;
- existing Capability Registry and Binding.

Do not create `GeneralWorkspaceUsage`, `BusinessUsageV2`, `WorkspaceModelUsage`, a second cost ledger, or a new execution engine.

### 5.2 Durable Task attribution

Add only the canonical source references needed to reconstruct execution after restart:

- `workspace_id` (nullable for legacy tasks);
- `work_ref` (nullable for legacy tasks);
- `execution_ref` (nullable for legacy tasks; use the existing Team Operating execution identity rather than inventing another job identity).

Keep `company_id`, nullable `project_id`, Employee and Capability fields. Business and Department should be resolved from Workspace rather than duplicated on Task unless implementation evidence proves a restart ambiguity that cannot be resolved from the canonical relation.

### 5.3 Immutable usage ledger attribution

Extend the existing ledger with an immutable ownership snapshot:

- `company_id` — required for every new record;
- `business_id`, `workspace_id`, `work_ref`, `execution_ref` — required together for canonical Workspace records, nullable for historical/legacy Project records;
- `project_id` — retained but made nullable;
- existing `department_id`, Task, Employee, Capability, Provider/model, request, token/cost and execution fields — retained.

Use one row-level lineage constraint: a new record must have either a complete canonical Workspace lineage or a valid legacy Project lineage. Canonical records may additionally carry an optional legitimate Project.

Because SQLite cannot relax `project_id NOT NULL` additively, the ledger migration requires the repository's existing transactional table-rebuild pattern. It must preserve every row, index, unique idempotency key, and no-update/no-delete trigger. Historical `company_id` is backfilled only through the recorded Project lineage. If any historical row cannot resolve, migration stops; it must not invent ownership.

### 5.4 One shared resolver/validator

Move Project-versus-Workspace branching into the existing `AIUsageService` validation boundary. `main.py` must not independently reconstruct ownership.

The validator returns one normalized attribution snapshot:

- canonical Workspace mode when Task has `workspace_id`;
- legacy Project mode only for an existing legitimate Project task;
- rejection for missing, ambiguous or conflicting lineage.

This is a value/result inside the existing service, not a new attribution subsystem or registry.

### 5.5 Propagation

- Team Operating submit persists Workspace/Work/Execution refs on its ResultStore Task.
- Orchestrator reconstructs those refs from Task after restart.
- Model Gateway records the normalized snapshot for success and failure attempts.
- ResultStore's existing tool/task execution events carry the same canonical refs.
- Tool cost is not generalized in this change; existing tool/task events gain attribution only. No evidence currently supports a complete tool-cost ledger.

### 5.6 Read API and reports

- Preserve all existing Project/Department filters and response fields.
- Add canonical Company/Business/Workspace/Work/Execution filters or grouping only to the existing Usage API.
- Make `project_id` nullable in response projections.
- Change Company business metrics to aggregate direct ledger `company_id`, so canonical Workspace usage is not omitted.
- Add canonical refs to the existing task execution timeline without removing Project refs.
- Tenant billing totals remain on the same ledger and require no parallel implementation.

## 6. Backward compatibility

### 6.1 Historical rows

- Retain original Project and Department values.
- Backfill only Company via verified Project relation.
- Leave Business/Workspace/Work/Execution null; do not retroactively guess.
- Preserve immutability triggers and idempotency behavior.

### 6.2 Existing RD and legacy execution

- Existing Task → Project → Department validation remains a supported compatibility mode.
- Existing RD task/job/workflow routes keep their Project semantics.
- Existing reports and APIs continue to expose/filter Project.
- New canonical fields are additive to API payloads; old clients continue to work.
- Later RD migration may attach canonical Workspace attribution in addition to Project, but that is outside this closure.

### 6.3 Compatibility expiry

This change does not schedule Project removal. Removing legacy Project attribution requires a separate inventory and migration decision after all accepted RD/history consumers have canonical Workspace ownership.

## 7. RD regression risk

| Risk | Required control |
|---|---|
| Relaxing ledger `project_id NOT NULL` accidentally weakens validation | Service-level and row-level rule requires complete canonical or legacy lineage |
| Historical rows lose immutability/indexes during rebuild | Migration tests assert rows, SHA-equivalent values, triggers, indexes and idempotency keys |
| RD task is misclassified as canonical | Mode is selected from persisted Task Workspace attribution; no inferred/default Workspace |
| Existing Project usage filters break on null | Keep legacy filters and make response nullable-safe |
| Company cost omits canonical calls | Aggregate by direct immutable `company_id` |
| Employee Department equality blocks Company-level employee | Canonical path validates same Company plus scoped assignment/identity binding; it does not invent a Department affiliation requirement |
| Mixed-source `main.py` absorbs unrelated changes | Capture pre-change hash and patch only named gateway/team-submit functions; stop on hunk collision |

RD's accepted real Codex path is a mandatory no-regression suite, not a migration target for this issue.

## 8. Content Growth and future Workspace compatibility

The proposed contract is domain-neutral because it attributes execution to canonical Workspace/Work and keeps domain context optional.

It allows future Content Growth execution without requiring an RD Project and without adding Content Growth-specific usage tables. Research/Content objects remain linked through Work, Result, Evidence and domain Runtime. If a future reporting requirement needs first-class domain dimensions, it should be proven by that domain and added separately; it is not prebuilt here.

The same rule applies to Declarative/Generic Workspace Packages: installed Workspace + canonical Work is sufficient only when the Parent Resolver, Employee assignment and Capability Binding all verify. Package installation itself never authorizes Provider execution.

## 9. Required tests and evidence

### 9.1 Schema and migration

1. Fresh isolated SQLite creates the extended Task and immutable usage schema.
2. Upgrade fixture with existing Project usage preserves every value, index, idempotency key and immutability trigger.
3. Unresolvable historical Project ownership aborts migration without partial writes.
4. Canonical usage row accepts null Project only with complete verified canonical ownership.
5. Incomplete canonical and incomplete legacy rows fail closed.

### 9.2 Canonical General Workspace execution

6. General Workspace Cycle/Work creates one ResultStore Task with Workspace/Work/Execution refs and no Project.
7. Resolver proves Workspace → Business → Department → Company before Provider launch.
8. Successful and failed model attempts persist the same canonical ownership snapshot and real token/cost truth.
9. Restart reconstructs the same Task attribution; persistence does not bypass revalidation.
10. Replay/idempotency does not create duplicate usage or Provider attempts.

### 9.3 Security and isolation

11. Cross-tenant, cross-Company, wrong Business, wrong Work, quarantined/unresolved Workspace, invalid Employee identity and invalid Capability Binding are rejected before Provider launch.
12. A supplied Project conflicting with canonical Workspace ownership is rejected.
13. No fallback/default Project is created or selected.

### 9.4 Compatibility and reporting

14. Existing RD real Codex, Workflow, Project task-job and AI usage ledger regressions pass unchanged.
15. Existing Project/Department usage filters remain correct.
16. Company business metrics include both legacy Project and canonical Workspace usage exactly once.
17. Tenant billing totals remain unchanged for historical fixtures.
18. Task timeline and existing tool/task usage events expose canonical refs without inventing tool cost.
19. Backend DB safety guard proves all tests use repository-external isolated SQLite; both active databases remain byte-identical.

Real Provider evidence is required to close M2 execution acceptance after implementation. Deterministic/local adapters may verify contract behavior but must not be reported as live Provider quality or cost evidence.

## 10. Exact allowed implementation scope

This review does not authorize implementation. A bounded Issue must approve an exact manifest before edits.

### 10.1 Candidate source files

| Path | Exact reason |
|---|---|
| `backend/app/database.py` | Task additive refs; transactional ledger rebuild; constraints/indexes/triggers |
| `backend/app/ai_usage.py` | Single canonical/legacy resolver, validation, record/read filters |
| `backend/app/result_store.py` | Persist canonical Task refs and propagate existing usage event attribution |
| `backend/app/orchestrator.py` | Reconstruct canonical refs from durable Task |
| `backend/app/main.py` | Exact owned hunks only: model gateway attribution and `team_employee:auto` task creation |
| `backend/app/task_execution_control.py` | Canonical timeline associations, preserving Project |
| `backend/app/business_metrics.py` | Direct Company ledger aggregation |

`backend/app/employee_execution_identity.py`, `backend/app/runtime/general_workspace_delivery.py`, `backend/app/runtime/models.py`, `backend/app/api/team_operating_router.py`, legacy RD/Workflow modules and UI are reuse-only unless a focused test proves a named missing seam. Any expansion requires Issue amendment and ownership review.

### 10.2 Candidate tests

- new focused canonical usage attribution test;
- new fresh/upgrade/failure-atomic schema migration test;
- existing AI usage ledger and database migration tests;
- General Workspace operating and Team Operating real Employee E2E;
- Employee execution identity/callback trust;
- existing RD real Codex/model gateway/workflow/task-job regression;
- business metrics, billing, task timeline and backend DB safety regression.

### 10.3 Explicit exclusions

- no synthetic/default/free-form Project;
- no second Usage/Cost/Audit table or service;
- no General Workspace special-case ledger;
- no active SQLite migration or data repair;
- no guessed historical Business/Workspace mapping;
- no RD domain rewrite;
- no Content Growth object/schema work;
- no topic/research/content attribution columns;
- no UI change;
- no M3 credential/security work;
- no tool-cost system or cost-enforcement expansion;
- no Workflow/DAG/Execution engine;
- no Product Authority modification;
- no commit or push under this review.

## 11. Minimal implementation plan after approval

1. Establish bounded Issue, exact Allowed Files, mixed-source pre-change hashes and active-DB fingerprints.
2. Implement isolated, transactional Task/ledger migration with legacy-row proof first.
3. Extend the existing `AIUsageService` validator to return one canonical-or-legacy snapshot.
4. Propagate existing Workspace/Work/Execution refs through ResultStore Task → Orchestrator → Model Gateway and existing usage events.
5. Update only affected read/report projections.
6. Run the tests in §9 with isolated SQLite, then one real General Workspace Provider proof and the accepted RD no-regression chain.
7. Stop if migration cannot preserve historical rows, mixed-source ownership collides, or canonical Parent Resolver cannot verify ownership.

## 12. Final decision

The architecture is sufficiently determined by Current Product Authority and current Runtime truth. The change is a bounded correction to the one existing attribution ledger, not a new Runtime system.

**ARCHITECTURE CHANGE APPROVED CANDIDATE**

Implementation remains unauthorized until CEO/Architecture acceptance creates a bounded Issue with exact Allowed Files and migration evidence requirements.
