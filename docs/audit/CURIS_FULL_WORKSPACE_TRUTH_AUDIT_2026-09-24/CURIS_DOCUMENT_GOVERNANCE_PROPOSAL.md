# Document Governance Proposal

Status: Review  
Authority Class: REVIEW  
Baseline: `78cacbd0857cc36c9f3fe0e4b11346489993b728`  
Updated: 2026-09-24  
Disposition: AUDIT / PROPOSAL — NON-AUTHORITATIVE; CEO review required.

## Proposed single vocabulary and classes

Limit new work to **six classes**. This set does not redefine existing Authority and remains a Review proposal.

| Class | Purpose | Allowed directory | Naming rule | Required metadata | Who creates | Who modifies | Who promotes | Retention | Archive/delete |
|---|---|---|---|---|---|---|---|---|---|
| Authority | Current Product/Architecture/Design/Development truth | Existing docs/01_Product, docs/02_Architecture, docs/03_Design, docs/04_Development, docs/05_Workspace_Engineering | Named module + Curis_* canonical title; no Final/Master suffix-as-authority | Title, Status, Authority Class, Owner, Updated, Source/Baseline; change requires Target Authority / Supersedes | Product/system owner; Agent only by exact Issue | Same owner; frozen text only by scoped authority change | CEO/product authority for Product; designated domain owner for other authority | Indefinite while current; then superseded historical retention | Deprecate + exact reference map to docs/99_Archive; never silent delete |
| Decision / ADR | Recorded durable decision and rationale | docs/07_Decisions/ (or existing decisions index until reconciliation) | ADR-NNNN-short-title.md | Status, Authority Class, Owner, Decision Date, Scope, Source, Disposition, Supersedes | Decision owner or CEO gate | Owner; change by new superseding decision, not silent rewrite | Named Decision owner / CEO when product authority | Indefinite | Archive with replacement link and preserve provenance |
| Issue / Backlog item | Authorized bounded work and active queue | issues/ for executable Issue; canonical backlogs in docs/reviews/ per Pointer | Issue id + bounded topic; one canonical backlog item id | Task ID, Owner, Scope, Non-Goals, Allowed Files, Allowed Directories, outputs, acceptance, verification, gate, Status | Triage/owner; new Active item only by backlog promotion | Issue owner within scope; product decisions not by implementer | Backlog owner for queue; CEO/product owner for scope/promotion | Keep closed issue/evidence; active item until disposition | Close as DONE/CANCELLED/SUPERSEDED and link canonical item |
| Research / Candidate / Proposal | Nonbinding evidence or a proposed change | docs/research/ for durable research; artifacts/tasks/<id>/ while active | topic + date + source; Candidate never named Current/Final | Status=Review/Draft; Authority Class=RESEARCH; task/scope/source/date; Owner; target decision/next gate; disposition | Task Lead with explicit scope | Author while task active | CEO/Product/Domain owner promotes; author cannot self-promote | Research with reusable evidence kept; raw intermediate expires with task | Accepted evidence linked into review; rejected/superseded remains historical or is removed per approved disposition |
| Review / Closure / Acceptance Evidence | Outcome, test/provenance, gate and unresolved risks | docs/reviews/<issue-or-decision>/ (existing flat canonical docs/reviews accepted) | Issue ID / decision + evidence type + date | Status, Authority Class=REVIEW/EVIDENCE, Owner, Source, Verdict, Disposition, Scope, Evidence, Next Action, Target Authority, Next Gate | Reviewer/Task Lead | Author may correct evidence within scope; acceptance statement only reviewer owns | Named reviewer; product decisions by CEO | Permanent when evidence supports accepted decision/release; otherwise task TTL | Retain if cited by authority/issue; archive under controlled path if superseded |
| Task Artifact / Visual / Temporary Evidence | Unpromoted drafts, captures, logs, scratch files | artifacts/tasks/<TASK-ID>/ | `<task-id>__<agent>__<type>__<seq>.<ext>`; manifest is required | Task ID, creator/agent, relative path, purpose, created time, sensitivity, intended retention, final disposition | Assigned Agent only in its path | Assigned Agent while active | No promotion by filename; Review owner requests; authority owner accepts | 30 days after task terminal by default; exact evidence may be promoted or retention extended | PROMOTE / ARCHIVE / DELETE at close; no silent carryover |

## CURIS Document Metadata Contract

**Required on all governed documents:** `Title`, `Status`, `Authority Class`, `Owner`, `Updated`, `Scope`, `Source`, `Task/Issue ID` (or `none` for a durable Authority), `Disposition`, and `Next Action` / `Next Gate` when not terminal.

**Required when applicable:** `Target Authority` for a candidate/review; `Supersedes` and `Superseded By` for replacement; `Baseline` (branch + full SHA) for implementation evidence; `Verdict` and linked evidence for Review/Acceptance; `Created By` and `Retention Until` for task artifacts; `Module` for domain documents. `Source` must point to concrete paths/evidence; no unbounded “from previous context.”

| Field | Required / optional | Allowed values / meaning | Promotion effect |
|---|---|---|---|
| `Status` | Required | Exactly `Draft`, `Review`, `Frozen`, `Deprecated` per `DOCUMENT_STATUS_RULES.md`; no `Approved`, `Final`, `Latest`, `Done-ish`, `Accepted maybe`, `Current Candidate` | Status describes maturity; never grants authority alone |
| `Authority Class` | Required | Existing set: `CURRENT`, `FROZEN`, `RESEARCH`, `REVIEW`, `HISTORY`, `EVIDENCE`; use exactly one primary class, no free text variants | Classification only; class name is not promotion |
| `Disposition` | Required on Review/Proposal and at task close | Proposed controlled set: `OPEN`, `ACCEPTED`, `REJECTED`, `RECONCILED`, `SUPERSEDED`, `RECORDED`, `CANCELLED`, `ARCHIVED`, `DELETE_APPROVED` | Records explicit decision; `ACCEPTED` alone does not edit Authority |
| `Owner` | Required | named accountable role/person | Routes review and maintenance |
| `Source` | Required | exact file/evidence paths, revision/date, external reference as applicable | Provenance only |
| `Target Authority` | Conditional | one canonical path + section, or `none` | Names the only allowed promotion target |
| `Next Action` / `Next Gate` | Conditional | concrete action/owner and explicit gate | No implicit dispatch |
| `Updated` | Required | ISO date | Freshness only |
| `Supersedes` / `Superseded By` | Conditional | exact old/new paths | Removes old file from default input only after accepted relation is recorded |
| `Scope` | Required | task/module/business and explicit non-goals | Scope constraint only |

`Status: Frozen` is reserved for explicitly accepted durable standards/decisions; `Disposition: ACCEPTED` is evidence of review outcome, not a fifth status. The current AGENTS instruction that important accepted Reviews record Verdict / Disposition / Owner / Next Action / Target Authority / Next Gate remains the stricter gate.

## Document lifecycle

```text
Create in Task Workspace (Status Draft / Review)
  → Active Work under Task ID + Allowed Directories
  → Review (Verdict + Disposition + evidence)
  → Promote to one named canonical class/destination, Reject, or Reconcile
  → Current / Frozen only by authority owner and required CEO gate
  → Supersede with exact replacement link
  → Archive durable provenance OR Delete transient artifact at close
```

- Research completed: keep the report in `docs/research/` only if it has traceable sources and a continuing decision use; otherwise close/delete raw workspace artifacts.
- Candidate accepted: convert only accepted findings into the existing target Authority; record source and disposition; candidate file stays evidence, no longer default input.
- Review completed: accepted evidence remains in `docs/reviews/`; rejected review stays only if it records a material decision, otherwise task artifact may expire.
- Closure and Decision Evidence: retain when needed to prove why a Frozen Authority changed or a release was accepted. Never delete the only evidence of a decision.
- Superseded docs: record `Superseded By`; set Deprecated; archive only after reference check.
- Exploration/HTML: active version only in Task Workspace; accepted interaction evidence is linked from Review, never Product Authority. Close with exact PROMOTE / ARCHIVE / DELETE.
- Screenshot: retain only screenshots cited by review/acceptance, with task/route/state/date; other captures expire after 30 days from terminal task. No screenshot directory per Agent.
- Temporary/log/test outputs: remove at task close or expire after 30 days; preserve failures only when they explain a gate or unblock reproduction. Sensitive data is never kept as generic evidence.

## Authority Promotion

Research → Candidate → Review → Accepted/Reconciled Evidence → Current Authority → Frozen. Promotion requires a named Owner, target path/section, explicit disposition, evidence, and applicable decision gate. Product changes require Product Definition and CEO decision; an implementation agent cannot promote its own candidate. `FINAL`, `MASTER`, `CURRENT`, `FROZEN`, timestamps and directory names never confer Authority. On promotion, the target Pointer/Index and `Superseded By` relation are updated only under an authorized Issue; the old candidate exits the default read path.

## Backlog governance

| Lane | Canonical entry | Owner / rule |
|---|---|---|
| Product truth | Blueprint + V1 Product Freeze, not a task backlog | Product owner; no Research TODO directly becomes product scope |
| Final UI / Frontend acceptance | `docs/reviews/CURIS_V1_FINAL_UI_ACCEPTANCE_BACKLOG.md` | UI/product owner; only scoped acceptance items become Issues |
| Implementation / Runtime | `docs/reviews/CURIS_V1_EXECUTION_BACKLOG.md` | Main Development; one canonical item per Issue, split only by owner |
| Capability validation | `docs/reviews/CURIS_V1_RUNTIME_CAPABILITY_VALIDATION_BACKLOG.md` | Runtime/capability owner; separate from Product Freeze |
| Release | release blockers reconciled through `CURIS_V1_PRODUCT_COMPLETION_RECONCILIATION.md` + Execution Backlog and the current release review | Release owner; release stays blocked without explicit authorization |
| Post-V1 | no Active queue until Product Owner accepts a scoped item | CEO/product owner; label `POST-V1`; no implementation dispatch |

A `TODO`, `Gap` or `Next Step` in Research/Review is not Active Work. Promotion requires deduplication against these entries, one canonical owner/path, exact acceptance evidence and an Issue. Duplicates stay in their source with a link to the canonical item; closure records `DONE`, `SUPERSEDED`, `CANCELLED` or `BLOCKED` plus evidence and replacement.
