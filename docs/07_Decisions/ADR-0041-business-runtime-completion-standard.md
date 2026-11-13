# ADR-0041: Business Runtime Completion Standard

Status: Frozen

Baseline: `main @ c0e1855f`

Updated: 2026-07-31

Module: Product Definition / Development Acceptance

## Decision

Curis features are accepted by complete business operation, not by the
existence of pages, buttons, interactions or APIs.

Every Company OS primary module and every Workspace type must define a
Business Runtime containing:

1. Business Lifecycle
2. State Machine
3. Business Runtime stages
4. Input
5. Output
6. Owner
7. Next Stage
8. Feedback and exception path
9. Closure and archive condition
10. Business Runtime Simulation

The Business Runtime Blueprint is a core chapter of the single Current Product
Blueprint. It is not an appendix.

## Completion Rule

The following are implementation evidence, but none is a completion standard:

- page rendered
- button clickable
- interaction available
- API returned success
- unit test passed
- local component state changed

A feature is complete only when one realistic business scenario runs through
the entire lifecycle using the real runtime, persistence, identity and
cross-module handoffs, and produces durable business outputs.

A controlled test scenario may be used, but mocked UI state, fake transitions
or manually edited database rows cannot replace the real runtime.

## Runtime Stage Contract

Every runtime stage must specify:

| Field | Requirement |
| --- | --- |
| Stage | Stable business stage name |
| Page / Surface | Where the responsible actor works |
| Entry State | Required persisted state before entry |
| Owner | Human, AI or system role accountable for the stage |
| Participants | Who may contribute or observe |
| Input | Required facts, resources and prior outputs |
| Runtime Action | Business work performed, not UI gestures |
| Output | Durable artifact, decision, state or handoff |
| Exit Condition | Verifiable condition that ends the stage |
| Next Stage | Valid transitions, including exception paths |
| Feedback | How downstream execution updates the originating business object |
| Audit | Actor, time, reason, state transition and evidence |

## State Machine Rule

- State is a persisted business fact, not a label inferred from a page.
- Every transition declares actor, precondition, command, output and audit
  evidence.
- Terminal states are explicit.
- Rejection, retry, cancellation, delay, timeout and failure paths cannot be
  omitted where they are possible in the real business.
- Cross-module handoffs carry correlation identifiers and cannot depend on
  copied text alone.

## Business Runtime Simulation

Acceptance must record:

1. Initial business trigger and starting state
2. Real participating roles
3. Input provenance
4. Every state transition
5. Durable output from each decisive stage
6. Cross-module handoffs
7. At least one relevant failure, rejection or retry path
8. Downstream feedback to the originating module
9. Completion and archive evidence
10. Browser evidence for human stages and backend/data evidence for system
    stages

Meeting, Workspace and Business Engineering require full lifecycle simulation
before their feature family may be accepted.

## Consequences

- Product change order becomes:
  `Product Definition → Business Runtime Blueprint → UI Design → Code`.
- Product Blueprint 2.0 remains `Review` until all primary module Runtime
  Blueprints are complete and reviewed.
- Product Reset implementation remains
  `BLOCKED_PENDING_BUSINESS_RUNTIME_BLUEPRINT`.
- Issues must identify the Runtime stage and transition they implement.
- Reviews must reject page-only, button-only, API-only and partial-lifecycle
  evidence.

