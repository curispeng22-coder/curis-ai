# CURIS VISUAL BASELINE REAL PRODUCT IMPLEMENTATION REVIEW

Status: Review
Authority Class: REVIEW
Issue: `CURIS-VISUAL-BASELINE-REAL-PRODUCT-INTEGRATION-001`
Verdict: `PARTIAL — CLEAR REMAINING GAPS`

## Executive finding

Curis has a real accepted Workspace-scoped operating core and two substantial professional Workspace implementations. It does **not** yet have a coherent persisted and navigable `Company -> Department -> Business -> Workspace` product spine.

The main deficit is not visual polish. It is identity and integration truth: Business is not an authoritative Company/Department-scoped persisted object, Workspace accepts a free-form Business reference, and the local frontend path depends on untracked mixed-source files. Direct implementation therefore stopped at the documented Authority/Schema and ownership boundaries.

## Product-to-implementation matrix

| Product contract | Visual baseline | Frontend | API | Persistence | Runtime | E2E | Final |
|---|---|---|---|---|---|---|---|
| Company -> Department -> Business -> Workspace | ACCEPTED | PARTIAL | PARTIAL | NOT IMPLEMENTED | PARTIAL | FAIL | P0 |
| Department entity | ACCEPTED | legacy/partial | EXISTS | EXISTS | legacy/partial | NOT RUN | PARTIAL |
| Business requires Department | ACCEPTED | NOT IMPLEMENTED | NOT IMPLEMENTED | NOT IMPLEMENTED | NOT IMPLEMENTED | FAIL | P0 |
| Workspace requires valid Business | ACCEPTED | implied only | accepts free ref | unchecked text ref | no validation | FAIL | P0 |
| Business guarantees first Workspace | ACCEPTED | NOT IMPLEMENTED | no atomic API | no atomic transaction | NOT IMPLEMENTED | FAIL | P0 |
| Business Definition | ACCEPTED | Workspace-card list | no canonical read model | legacy direction only | PARTIAL | FAIL | P0/P1 |
| Business Operating Summary | ACCEPTED | NOT IMPLEMENTED | no projection | no canonical aggregate | source facts exist | FAIL | P1 |
| Business Workspace Directory | ACCEPTED | Workspace list masquerades as Business | Workspace collection exists | real Workspace rows | reusable | PARTIAL | P1 |
| Business Team | ACCEPTED | NOT IMPLEMENTED | no Business-scoped canonical team | ambiguous | Workspace team accepted | FAIL | P1 / authority-dependent |
| Workspace Parent Path | ACCEPTED | static/company-only crumb | no parent resolver | no valid relation | cannot derive | FAIL | P0 |
| Workspace H1 / identity | ACCEPTED | EXISTS | EXISTS | EXISTS | EXISTS | PASS | IMPLEMENTED |
| Workspace Leader as Assignment | ACCEPTED | PARTIAL | Team Operating supports Assignment | persisted in operating definition | accepted | PARTIAL | P1 |
| Workspace Goal | ACCEPTED | partial/domain-specific | blueprint/outcome refs | persisted in several forms | reusable facts | PARTIAL | P1 |
| Rules / configuration | ACCEPTED | partial | blueprint and package APIs | persisted | reusable | PARTIAL | P1 |
| Current Operating | ACCEPTED | domain-specific | no shared projection | derived facts available | Work/Result/Need real | PARTIAL | P1 |
| Conditional CEO Decision | ACCEPTED | XHS/RD real; absent when none | real packet APIs | persisted | accepted P7 | PASS in domains | IMPLEMENTED in XHS/RD |
| Generic work-centered surface | ACCEPTED | package object renderer, not target surface | package APIs | real package instance | partial | PARTIAL | P1 |
| XHS primary surface | ACCEPTED | real Calendar/Note surface | real XHS APIs | persisted | real responsibility/decision | PASS in focused regression | IMPLEMENTED |
| RD primary surface | ACCEPTED | real professional workstation | real RD APIs | persisted | real Codex/Artifact/Evidence | PASS in focused regression | IMPLEMENTED, local file untracked |
| Four-pane shell | ACCEPTED | EXISTS | N/A | local preference | N/A | frontend tests pass | IMPLEMENTED |
| Pane resize / maximize | ACCEPTED | pointer drag + maximize | N/A | local preference | N/A | prior accepted closure | IMPLEMENTED |
| Company-wide search | ACCEPTED | honest placeholder | NOT IMPLEMENTED | N/A | NOT IMPLEMENTED | FAIL | P1 |
| Team Operating editor | ACCEPTED | real in XHS only | real adapter | immutable versions | accepted | adapter tests pass | PARTIAL |
| Add/Delete/Reorder/Binding/Input/Output/Save | ACCEPTED | EXISTS in editor | EXISTS | EXISTS | accepted | PASS | IMPLEMENTED where mounted |
| Default Flow is not mandatory DAG | ACCEPTED | reorder-only presentation | correct adapter | versioned | accepted | PASS | IMPLEMENTED |
| Employee Work Area | ACCEPTED | shared component exists but not commonly mounted | projection exists | accepted employee truth | accepted loop | component tests pass | PARTIAL |
| Assignment-scoped workstation identity | ACCEPTED | custom XHS/RD projections | shared projection exists | persisted | canonical bridge accepted | PASS in Runtime | PARTIAL UI integration |
| Result Reference / Evidence utility | ACCEPTED | XHS/RD real | real APIs | persisted | accepted | PASS | IMPLEMENTED in domains |
| Department -> Business -> Workspace deep route | ACCEPTED | NOT IMPLEMENTED | no canonical resolver | missing relation | N/A | FAIL | P0 |
| Generic -> professional upgrade | ACCEPTED direction | installed package renderer exists | package lifecycle exists | version pin/migration journal partial | accepted bounded package lifecycle | no identity-preserving domain upgrade E2E | PARTIAL |

## Evidence by layer

### Organization hierarchy

- `department_instances` exists and is Company-scoped.
- `business_directions` contains `tenant_id` but no `company_id` or `department_id`.
- `workspaces` contains `company_id` and `business_id`, but `business_id` has no foreign key or Runtime existence check.
- Legacy Project, Department Instance, CEO Day Business Direction and Workspace paths coexist. They are not a single frozen hierarchy implementation.
- The current shared projection can attempt to resolve a Business Direction, but it truthfully returns unresolved when the free reference has no matching row.

### Business surface

- `/ceo-office/business` reads `runtime.snapshot.workspaces` and renders one card per Workspace.
- It has no Business Definition, aggregate operating truth or Business Team.
- Workspace cards enter real Workspace routes, but the page is a local untracked file and is not recoverable from clean HEAD.
- Single- and multi-Workspace rendering uses the same Workspace map, but without a real Business grouping key.

### Workspace shell and professional surfaces

- `WorkspacePaneShell` is a real reusable four-pane component with pane-local headers, pointer resizing, maximize and honest search placeholder.
- XHS consumes real Content Item, Note Version, Handoff, Decision and scheduling state.
- RD consumes real Project/Cycle, Codex execution, Artifact, Evidence, Result Reference and Computer Access truth.
- The accepted Team Operating editor and Runtime are real, but only XHS mounts the editor in the inspected current routes.
- `SharedEmployeeWorkArea` is reusable and backed by real projection semantics, but neither XHS nor RD currently mounts it as their shared employee work-area layer.

### Decision slot

- XHS derives Needs CEO only when the Note is `IN_REVIEW` and the same linked Decision Packet is `WAITING_CEO`; no packet means no decision component.
- RD uses the same persisted Decision Packet semantics.
- This is real domain integration, not a fixture. A Business/Generic shared Decision slot remains unmapped because the parent hierarchy is unresolved.

### Generic and package evolution

- Installed Workspace packages can dynamically render declared objects and actions through the accepted package Runtime.
- The current renderer is a constrained declarative object surface, not yet the Frozen generic Work-centered surface.
- Package lifecycle/versioning exists in accepted bounded form, but a proven upgrade from generic to XHS/RD while preserving identity, leader, goal, rules, operating definition and workstations is not present.

## Isolated API and persistence proof

Database: `/tmp/curis-visual-audit.HiOs6Q/audit.sqlite`

```text
ceo_day_direction 200
orphan_workspace_create 201
workspace_read 200 business-does-not-exist
restart_read 200 DRAFT
business_directions columns: no company_id, no department_id
department_instances rows: 0
workspaces rows: 1
workspace foreign keys: 0
integrity_check: ok
```

This is a failure proof for the Frozen hierarchy: the system persisted and recovered a Workspace whose `business_ref` did not exist. Persistence works; relational product truth does not.

## Requested E2E scenarios

### Scenario A — Single Workspace Business

Status: `PARTIAL`

- A real RD Workspace, Team Operating Work, Employee execution and Result can run.
- A truthful Department -> Business -> Workspace creation/navigation chain cannot be proven because Business ownership and parent routing are missing.

### Scenario B — Multi Workspace Business

Status: `PARTIAL`

- Multiple Workspaces can share the same free-form `business_id` and each can run scoped Team Operating.
- The Business Workspace Directory cannot be accepted because the Business record and grouping relation are not authoritative.

### Scenario C — Generic New Business

Status: `FAIL / P0`

- There is no atomic Department + Business + first Workspace + Leader creation path.
- Generic installed Workspace rendering exists, but it cannot cure the missing hierarchy transaction.

## Tests

Backend isolated regression:

```text
31 passed
```

Covered Team Operating real Employee E2E, Team adapter, Shared Workspace projection, Workspace Runtime foundation, XHS, RD real execution, package Company integration and backend DB safety.

Frontend selected regression:

```text
18 passed, 2 failed
```

Both failures are stale expectation drift in `frontend/tests/runtimeProvider.test.mjs`:

- old CEO Desk label expectation `能力引用` vs current `运行引用`;
- old persistent navigation list omits the current `人才市场` entry.

No product code was changed to satisfy stale tests.

## Safe direct-closeout decision

No implementation change was safe in this pass:

1. Fixing Business hierarchy requires a canonical identity/ownership and migration decision.
2. Atomic creation depends on that unresolved relation.
3. Routing depends on the same parent resolver.
4. Key frontend files are untracked mixed-source work; committing or rewriting them without ownership would violate the preserved baseline.

Accordingly, only the bounded Issue and Review were added. This is not deferral of a clear one-line fix; it is the required stop at explicit schema/reference and ownership boundaries.

## Active database safety

Both repository SQLite files remained unchanged after all tests and isolated evidence runs:

| Database | Size | mtime | SHA-256 | Integrity |
|---|---:|---:|---|---|
| `data/curis.sqlite` | 1,232,896 | 1786873339 | `2ea2506f90f764e834d47d8f6bae3cb41c22d457757e0e9216c0ae8c39a39ec6` | ok |
| `backend/data/curis.sqlite` | 1,277,952 | 1786783659 | `a9d96a9536a5bce3b3b30f912e86a37f61d28527a8eb2d35af7a5857d29414e4` | ok |

## Remaining gate

Owner: Product/Runtime Authority.

Required decision:

1. Freeze the canonical Business identity and its Company/Department relation.
2. State how legacy `business_directions`, Project and Office/Workspace records coexist or migrate.
3. Assign ownership/promote a clean frontend baseline for the untracked Business/Workspace/RD/XHS routes.

Only after these facts are frozen should implementation continue with the smallest existing-Runtime transaction and route adapter.

## Final answer

- Visual Baseline: Frozen and accepted.
- Real Workspace/Employee Runtime: implemented and accepted in its scoped domains.
- Real Company -> Department -> Business -> Workspace product spine: not implemented.
- Closed this pass: evidence reconciliation and precise bounded issue; no unsafe code gap was disguised as closed.
- Final state: `PARTIAL — CLEAR REMAINING GAPS`.

`Visual Baseline -> Real Product -> Accepted Runtime` is **not yet a closed chain**.
