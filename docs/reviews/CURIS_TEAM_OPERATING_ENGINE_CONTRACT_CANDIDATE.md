# CURIS TEAM OPERATING ENGINE — CONTRACT CANDIDATE

Authority Class: REVIEW
Status: Review
Disposition: READY FOR CEO REVIEW
Date: 2026-08-19
Source Research: `docs/research/CURIS_TEAM_OPERATING_ENGINE_RESEARCH.md`
Scope: Runtime/UI review contract only; no implementation authority

## 1. Decision

Curis Team Operating Engine is a **Work-centered Responsibility Routing Control Plane** over existing Runtime
substrates.

It owns durable Work responsibility state and routing decisions. It does not replace Orchestrator, PipelineRuntime,
Workspace Domain executors, Capability Resolver, Employee Execution Identity Bridge, Result Store, Evidence,
Handoff or Decision Packet.

```text
Goal / Work
  -> Current Responsibility Assignment / Holder
  -> Result / Problem / Need
  -> STAY | CONSULT | REVIEW | HANDOFF | RETURN | ESCALATE | DECIDE | COMPLETE CYCLE | WAIT
  -> existing executor
  -> Result + Evidence
  -> Workspace Truth / Leader
  -> Continue | Adjust | Escalate | Wait | Complete Work
```

## 2. Required primitives

### First-class durable

- Work
- immutable Operating Definition Version
- Operating Cycle
- authoritative Responsibility Assignment reference: `Employee × Role × Scope`
- Result
- Handoff
- Decision Gate / Decision Packet
- Context Package
- Evidence

### Fields, relationships or events

- Current Holder: Work/Cycle field referencing one active Assignment
- Current Executor: optional verified execution field; never implies ownership
- Default Flow: versioned responsibility relationship
- Problem / Need: typed routing signal
- Consult / Collaboration / Review: Work-scoped interaction; Holder unchanged by default
- Return / Revision: typed Routing Decision; uses Handoff only when accountability transfers
- Routing Decision: append-only reason/provenance event
- Leader: system-defined Responsibility Role resolved through scoped Assignment

Role, Responsibility, Employee, Scope and Capability Binding remain authoritative Organization/Employee Truth. The
Engine references them; it must not create a parallel registry.

## 3. Responsibility invariants

1. A running Work/Cycle has exactly one accountable Current Holder Assignment.
2. Employee identity alone cannot receive work; routing requires Role + Scope Assignment.
3. Zero or multiple valid Assignments fail closed; never select the first enabled Employee.
4. Holder and Executor are separate.
5. Capability Resolver chooses how the selected Employee executes, not who owns the result.
6. Provider callback cannot change Holder.
7. Assignment/history changes are explicit and auditable.

## 4. Default Flow contract

`A -> B` means:

> After A produces an accepted Result, B is the default next Responsibility to resolve when no stronger explicit
> Return, Decision, Wait, exception or Domain rule applies.

It is not a mandatory route, Task dependency, fixed Employee edge or automatic transfer.

- Skip B only with a recorded reason: already satisfied, not applicable, explicit authorized route, valid alternate,
  or cycle closure.
- Return to A when B rejects A's Result against declared criteria and A must own revision.
- Route to C when Result/Problem/Need matches C more specifically or C is an authorized alternate.
- Keep Current Holder when another Role only provides information, review or a bounded sub-result.
- Route to the lowest valid Leader when Assignment, authority, goal/rule/staffing, repeated failure, risk or
  continuation judgment cannot be resolved locally.

Every route records Work/Cycle, pinned version, signal/result refs, selected action, reason and rejected alternatives.

## 5. Consult vs Handoff

| Contract | Consult / Review | Handoff |
| --- | --- | --- |
| Purpose | information, critique, validation, specialist sub-result | another Responsibility owns the next Result |
| Holder | unchanged | source until ACK; target after ACK |
| Context | minimal question/review packet + refs | minimum responsibility Context Package + refs |
| Task/Session | only if real independent execution is needed | created/reused only when target execution begins |
| Failure | current Holder continues or escalates | source remains Holder |

Developer asking Product/Architect is Consult. QA returning a build to Developer is Return + acknowledged transfer
only when Developer must own the revised Result.

## 6. Handoff and Return

```text
PROPOSED -> SENT -> ACKNOWLEDGED -> TRANSFERRED
                    -> REJECTED / RETURNED / EXPIRED
```

- Source remains accountable through `SENT`.
- ACK validates target Assignment, Scope, Employee identity, Work/version and Context Package.
- Holder changes once at transfer; Executor remains none until verified work begins.
- Reject/expire preserves source Holder.
- Handoff itself does not create a new Issue, Work, Task or Provider Session.
- Review keeps original Holder unless a separate transfer is completed.
- Return includes failed criteria, Evidence refs and required revised Result; revision loops are bounded.

## 7. Dynamic routing precedence

1. Validate tenant/company/workspace Scope, Work, pinned version, signal provenance and Holder.
2. Apply accepted Decision, explicit Return target or binding Domain rule.
3. Default to `STAY_AND_CONTINUE`.
4. Use Consult/Review when accountability need not change.
5. Use Handoff when the next contracted Result belongs to another Responsibility.
6. Resolve the lowest authorized Leader when no unique legal Assignment exists.
7. Create Decision Gate for authority/risk/irreversibility thresholds.
8. Complete Cycle only after accepted Result Contract satisfaction.
9. Decide continuation separately; never auto-create infinite tasks.

Agent/model classification may propose a route. Deterministic guards own Scope, authority, Assignment uniqueness,
Result contract, Handoff transition and Decision application.

## 8. Leader / Decision contract

```text
Role Assignment
  -> Workspace Leader
  -> Business Leader
  -> Department Leader
  -> CEO Decision Gate
```

- Use the lowest Scope with authority; do not mechanically traverse all levels.
- Leader is not an Employee type or mandatory Workflow node.
- Decision Gate persists question, options, evidence, owner, deadline and resume action.
- Decision resumes the same Work/Cycle unless it explicitly closes or replaces it.

## 9. Result contract

Result must include Work/Cycle, producing Assignment, output/result contract, status, provenance, version, Artifact /
Evidence / External Receipt refs, discovered Problem/Need and acceptance/rejection where required.

Execution success is not automatically business success. Only accepted Result satisfaction can complete a
responsibility or cycle.

## 10. Context and cost contract

- One durable Work Context; Assignment-scoped views.
- Handoff/Consult are reference-first with bounded summaries.
- Hydrate only bodies required by the target Input Contract.
- Preserve source/version/hash and stale/unknown state.
- Reuse Provider Session only when identity, Assignment, authority and continuity remain valid.
- Record context tokens/bytes, hydrated refs/bodies, copied-history ratio, new Task/Session, resume latency,
  Consult/Handoff count, acceptance latency and stale/missing refs.

## 11. Version contract

- Operating Definition versions are immutable.
- Work pins the version active at start.
- Saving creates a new version used by New Work.
- Running Work never silently changes route, Role/Responsibility, Input or Output contract.
- Applying a new version to running Work requires impact preview, compatible mapping, valid Assignments, context
  validation and a durable migration event.
- Live revocation/invalid authority overrides pinned configuration and fails closed.

## 12. Operating loop contract

- Task Completion: one execution ended.
- Responsibility Completion: current Assignment produced an accepted Result.
- Cycle Completion: Cycle Result is accepted and written to Workspace Truth.
- Operating Continuation: explicit policy/schedule/event/input/Leader decision opens the next Cycle.
- Work Completion: goal/stop contract is satisfied, canceled or explicitly closed.

Result returns to Workspace Truth and Workspace Leader for `Continue / Adjust / Escalate / Wait / Complete`.
Completing a Task or Workflow node never automatically proves Work completion or authorizes another Task.

## 13. UI projection

### User language

- Main section: `团队运转`
- Editor: `默认流程`
- Explanation: `正常情况下，工作会按这个责任顺序流转；团队会根据结果、问题和需要调整。`
- `Workflow / Router / State Machine / DAG` remain internal or advanced audit language.

### V1 surface

Keep a simple linear summary and inline editor. Node detail may edit Role, Responsibility, Employee Binding, Input,
Output, Review and Return. Do not expose Runtime state in the Definition editor. Do not ship an arbitrary Graph View.

Add a read-only advanced diagnostic projection only after evidence shows linear summary + Routing Decision history is
insufficient for support.

### UI action mapping

| UI action | Required Runtime meaning |
| --- | --- |
| Add/Delete/Reorder | new immutable version; changes default responsibility relations only |
| Modify Responsibility | new version changes routing/result match; running Work remains pinned |
| Replace Employee | scoped Assignment revision at explicit boundary; active Holder never silently swaps |
| Modify Input | Context Assembly required refs/validation contract |
| Modify Output | Result schema/criteria/acceptance contract |
| Return | typed Return/Revision relation; transfer only when invoked and ACKed |
| Save | New Work uses new version; running Work unchanged by default |

No editable control may exist unless Router, Context Assembly or Result validation consumes it.

## 14. Reuse decision

| Component | Decision |
| --- | --- |
| WorkflowRuntime | LEGACY; compatibility executor only, never Team Engine authority |
| Orchestrator | REUSE inside one Task/Assignment |
| TaskGraph | DO NOT MERGE with responsibility relationships |
| PipelineRuntime | ADAPT retry/switch/replan to emit typed routing signals |
| WorkspaceRuntime | REUSE as durable control-plane home |
| RD Handoff | REUSE ACK-before-transfer/reference-first baseline |
| XHS Handoff | ADAPT fixed target to versioned Responsibility resolution |
| Decision Packet | REUSE and resolve lowest authorized Leader |
| Result Store | REUSE; no second Result store |
| Employee Execution Identity Bridge | REUSE unchanged trust boundary |
| Capability Resolver | REUSE after responsibility resolves |

WorkflowRuntime is only a future retirement candidate after consumer migration and compatibility evidence; this
contract does not authorize retirement.

## 15. Domain acceptance cases

### Content growth

- normal: 选题 -> 调研 -> 文案 -> 视觉 -> 发布 by default relations;
- 视觉 requests revision from 文案 with criteria/evidence;
- 调研 Consults Leader without transfer when only judgment input is needed;
- 发布 compliance problem stays local/Consults specialist or escalates by risk;
- Cycle Result returns to Workspace Leader;
- next Cycle opens only by explicit continuation policy/decision.

### R&D

- Developer Consults Product/Architect without changing Holder;
- QA Return transfers to Developer only for revised-build ownership;
- small retry stays with current Assignment and reuses Pipeline behavior;
- major architecture change routes to lowest authorized Leader/Decision Gate;
- Default Flow exists but does not lock work into Product -> Architecture -> Development -> QA -> Release.

## 16. Implementation review hard gates

Reject the implementation if any is true:

- creates a fifth Runtime, Handoff store, Result store or organization registry;
- uses first-enabled Employee instead of unique scoped Assignment;
- treats Consult/Review as Handoff;
- changes Holder before ACK or from Provider callback;
- treats Default Flow as mandatory sequence or arbitrary DAG;
- lets Capability Resolver select accountability;
- silently changes running Work after definition/employee edits;
- copies full context for every Role by default;
- equates Task completion with Cycle/Work completion;
- auto-creates unbounded next tasks;
- lacks restart, duplicate-transfer, zero/multiple Assignment, stale ref, cross-scope and Decision-resume evidence.

## 17. NOT THIS

- strict sequential-only
- user-authored arbitrary DAG
- every interaction = Handoff
- every Handoff = new Issue
- every Role = new full context
- Leader as mandatory Workflow Node
- fifth parallel Runtime

## 18. Review disposition

**Verdict:** RECOMMEND `Work-centered Responsibility Routing Control Plane`.
**Disposition:** READY FOR CEO REVIEW.
**Owner:** CEO / Product Authority owner.
**Next Action:** Review this contract against Product Truth and the bounded Responsibility Routing implementation.
**Target Authority:** Applicable Product/Runtime Contract only after explicit acceptance.
**Next Gate:** ACCEPT / REVISE / REJECT; no Runtime, Schema, UI or code change is authorized by this candidate.
