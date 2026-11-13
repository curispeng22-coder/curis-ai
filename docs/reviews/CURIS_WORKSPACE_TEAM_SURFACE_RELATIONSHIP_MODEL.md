# CURIS WORKSPACE — TEAM × SURFACE RELATIONSHIP MODEL

**Authority Class:** RESEARCH

**Status:** Review

**Disposition:** CEO REVIEW REQUIRED

**Date:** 2026-08-21

**Authority Effect:** NONE

## 1. Canonical relationship

```text
Workspace → Operating Team → Leader → Responsibilities → Employees

Professional Surfaces
→ Responsibility Requirements
→ Work / Result / Evidence Projections
```

```text
Workspace
├─ carries → Workspace Goal / Strategy / Operating Series
├─ is accountable through → one Operating Team boundary
│  ├─ led by → Workspace Leader / Operating Owner Assignment
│  ├─ defines → Responsibilities
│  ├─ requires → Responsibility Requirements (WHAT)
│  ├─ resolves through → Organization Routing (WHO)
│  ├─ binds → Workspace-scoped Assignments
│  └─ executes through → Employees + Capabilities (HOW)
└─ presents through → Professional Surfaces
   ├─ originate/consume → Responsibility Requirements
   ├─ project → Work / Holder / Executor
   ├─ project → Result / Evidence / Evaluation / Decision
   └─ project → responsibility-relevant Employee presence
```

## 2. Identity separations

```text
Surface ≠ Team ≠ Employee ≠ Responsibility ≠ Cycle
```

| Concept | Meaning | Owns / carries | Must not become |
|---|---|---|---|
| Workspace | Independent operating unit and professional environment | Goal, strategy, scope, team responsibility boundary | A page or tab |
| Operating Team | Leader + members + responsibility coverage for the Workspace | Ongoing professional accountability | One team per Surface |
| Professional Surface | Domain work projection and action origin | Navigation, objects, scoped projections | Runtime, team, owner, executor |
| Employee | Canonical Organization identity | Stable identity, role/specialty; scoped service via Assignment | Surface-specific copy |
| Responsibility | Accountable WHAT at a scope | Requirement/Assignment/Holder relation | Screen, Employee, capability |
| Assignment | Responsibility binding at scope | Eligibility/service and accountable Holder relation | Permanent full-context ownership |
| Work | Durable unit of accountable work | Holder, optional Executor, refs, state | A UI panel |
| Handoff | ACK-governed accountability transfer | Source/target Assignments and provenance | Navigation event |
| Result/Evidence | Canonical output and proof | Workspace truth refs | Surface-local copy |
| Cycle | Bounded operating period | Work/Result/Evidence/Evaluation/Decision lineage | Surface session |

## 3. Responsibility bridge

```text
Professional Surface
  → declares requirement: WHAT
  → Organization Routing resolves Assignment: WHO
  → Employee uses Capability: HOW
  → existing Work executes
  → Result / Evidence return to Workspace truth
  → one or more Surfaces project the refs
```

Rules:

- Requirement never names an Employee.
- Surface never resolves WHO.
- Employee identity is never duplicated per Surface or Workspace.
- A Responsibility may be relevant to several Surfaces.
- An Employee may hold several scoped Responsibilities and appear on several Surfaces.
- A Work/Result/Evidence identity may have several projections.
- Projection relevance does not create ownership or permission.

## 4. Leader and routing

```text
Workspace Leader
├─ continuously owns business coherence
│  ├─ goal / strategy execution
│  ├─ responsibility coverage and collaboration
│  ├─ material result / exception judgment
│  └─ CEO communication
└─ does not route every ordinary task
   └─ Organization Router resolves ordinary WHO
```

Leader is an ordinary Employee holding a scoped leadership Assignment, not a separate Employee type or a Surface owner.

## 5. Cross-Surface operating flow

```text
Surface A action/object
→ Requirement A
→ Work A / Holder A
→ Result + Evidence
→ projection into Surface B
→ Requirement B
→ same Work continues OR distinct linked Work begins
→ Handoff only if accountability changes
→ Leader Review / Cycle decision
```

Surface switching has no Runtime meaning. Closing Surface A cannot pause Work A. The same Cycle may span several Surfaces and several Work items.

## 6. Presence and Workstation

```text
Surface projection
├─ no relevance → no Employee presence
├─ assigned responsibility → lightweight presence
├─ active Work → Holder presence
├─ verified execution → Current Executor presence
├─ consult/review → collaboration presence
└─ explicit Employee entry → shared Employee Detail / Workstation
```

There is one shared Workstation. It receives Employee + Assignment + Workspace + Work/Cycle + object/Result/Evidence refs and an optional source/return Surface context.

## 7. Package and Runtime boundary

Package may declare:

- Domain Navigation and Surfaces;
- responsibility requirements by semantic type;
- object/Work/Result/Evidence projection rules;
- bounded presence policy.

Package must not declare:

- Surface-owned Employees or Teams;
- Employee IDs as responsibility requirements;
- Surface lifecycle/runtime states;
- another Work, Handoff, Result, Evidence, or Cycle system.

**Research verdict:** the gap is Package declaration + UI projection + acceptance evidence. **No Surface Runtime is required.**
