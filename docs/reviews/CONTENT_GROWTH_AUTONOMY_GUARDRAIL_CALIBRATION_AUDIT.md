# CONTENT GROWTH — AUTONOMY GUARDRAIL & CALIBRATION AUDIT

Authority Class: EVIDENCE  
Status: Review  
Date: 2026-08-24  
Scope: CURRENT RUNTIME TRUTH ONLY  
Method: read-only source, accepted-test and formal-evidence inspection. No Provider call, test execution, Runtime/Schema/Policy/DB mutation, IA, Figma, commit or push.

## Executive conclusion

Curis has a real bounded autonomous operating control path. It can persist one active Cycle per Operating Series, release real Work to canonical Employees/Providers, require Result/Artifact/Evidence before close, obtain Acceptance and evidence-bound Evaluation, apply Leader/CEO authority, produce exactly one authorized successor for `CONTINUE`/bounded `ADJUST`, preserve `WAIT/PAUSE/STOP`, fail closed on Provider/capability errors, and recover persisted truth after restart.

It does **not** have a calibrated universal autonomy policy. In particular, current evidence does not establish a global autonomous-chain depth, Cycle token/cost budget, external-provider cost truth, universal retry count, research timeout, consecutive-failure escalation threshold, repeated-decision loop threshold, or automatic cost degradation. Existing numeric limits belong to specific adapters or legacy runtimes and must not be promoted into Content Growth product truth.

Current evidence-bound Learning is implemented and accepted, but it is deliberately non-self-modifying: it requires two distinct closed Cycles and explicit Leader/CEO acceptance, remains a scoped Artifact/reference, and cannot automatically rewrite Strategy, Goal, Envelope, Package, capability routing, prompt authority or code.

The Pre-IA blocker can close because the boundary is now unambiguous. IA may express current facts and honest unknowns; it must not invent precise autonomous thresholds or imply indefinite self-operation.

## Status vocabulary

- `IMPLEMENTED`: current Runtime plus accepted evidence proves the mechanism in its stated scope.
- `PARTIAL`: a bounded implementation exists, but it is not universal, fully wired or calibrated for Content Growth.
- `CANDIDATE`: research/product proposal only; not current Runtime truth.
- `UNKNOWN`: insufficient current evidence.
- `UNAVAILABLE`: current Runtime does not provide the mechanism in the audited path.

## 1. Current Runtime Guardrail Inventory

| Runtime area | Current guardrail truth | Evidence | Boundary |
|---|---|---|---|
| Autonomous Operating control | Persisted Operating Series, deterministic Trigger Claim, one-active-Cycle invariant, approved Strategy/Envelope pins, successor authority, WAIT/PAUSE/STOP and replay. | `backend/app/runtime/autonomous_operating.py:22-26,194-325,372-560,1058-1303`; accepted Phase 1–3B and Primary Two-Cycle reviews | Does not prove indefinite operation, Cycle 3+, global chain depth or calibrated budgets. |
| Canonical child Work | Distinct persisted child Work under one Cycle, Work-scoped Result/Evidence/Acceptance, sequential release and aggregate evaluation. | `backend/app/runtime/child_work.py`; `docs/reviews/CURIS_CANONICAL_CHILD_WORK_FOUNDATION_REVIEW.md`; `docs/reviews/CURIS_AUTONOMOUS_CROSS_SURFACE_MULTI_WORK_RUNTIME_PROOF_REVIEW.md:20-29,36-113` | Sequential multi-Work is proved; parallel/fan-out/fan-in/DAG is not implemented/proved. |
| Responsibility / Team Operating | Canonical Assignment/Employee, current executor, Provider Task/Session/callback, bounded result contract, Handoff/Consult/Return, cancellation and loop ceilings. | `backend/app/runtime/responsibility_routing.py`; `backend/app/api/team_operating_router.py`; `docs/reviews/CURIS_TEAM_OPERATING_REAL_EMPLOYEE_E2E_REVIEW.md:9-28,91-100` | Uses controlled deterministic Provider evidence; external live quality/cost is unverified. Limits are Work/adapter-specific, not universal policy. |
| Evidence / Acceptance / Evaluation | Cycle close requires real Result, Artifact and Provider evidence; Evaluation requires current verified Evidence and closed Acceptance. | `backend/app/runtime/autonomous_operating.py:711-1056`; accepted Phase 2/3A and Two-Cycle reviews | Does not calibrate business confidence from sample size or prove external outcome quality. |
| Decision / Relevant Gate | Next-cycle choices are `CONTINUE/ADJUST/WAIT/ESCALATE/PAUSE/STOP`; bounded ADJUST is checked against approved envelope; protected/out-of-envelope actions create CEO gate. Runtime Governance separately gates high-impact deploy/external send/delete/spend/permission actions. | `backend/app/runtime/autonomous_operating.py:1058-1275`; `backend/app/runtime_governance.py:98-108,127-153,195-259` | Generic high-impact classification is real, but no single Content Growth-specific “Relevant Gate” policy covers every possible action. |
| Execution claim / duplicate safety | Provider execution claims are idempotent; one active executor per Work; Trigger Claims and successor IDs are deterministic. | `backend/app/runtime/responsibility_routing.py:407-525`; `backend/app/agent_execution_kernel.py:1-25,255-334`; accepted Team/Two-Cycle evidence | Claim TTL values are configuration, not calibrated business safety thresholds. Kernel is default-off. |
| Cancellation / failure | Work can be cancelled; active Task cancellation is attempted; executor is cleared; technical Cycle failure persists partial refs and does not fabricate completion. | `backend/app/api/team_operating_router.py:460-477`; `backend/app/runtime/responsibility_routing.py:476-545`; `backend/app/runtime/autonomous_operating.py:1277-1303` | Ordinary Cycle failure does not automatically stop the Series or apply a consecutive-failure policy. |
| Capability truth | Assignment pins capability bindings; missing/disabled capability rejects materialization before Provider work in accepted proofs. | `backend/app/runtime/responsibility_routing.py:112-168`; Primary Two-Cycle failure matrix; Cross-domain proof | No automatic capability substitution or calibrated degradation policy is proved. |
| Usage / cost observations | Model Gateway and ResultStore can persist tokens, cost source and usage events when a Provider supplies valid metadata. | `backend/app/model_gateway.py:250-389`; `backend/app/result_store.py:658-733`; accepted R4 usage reviews | Controlled Team proof uses synthetic local usage metadata; external live provider cost remains unverified. |
| Budget enforcement | Runtime Governance has a token hard-limit gate. `BudgetGuard` can warn/hard-stop `RealRDExecutor` when explicitly enabled and usable token data exists. | `backend/app/runtime_governance_config.json`; `backend/app/budget_guard.py:55-82,172-244`; `backend/tests/test_budget_guard.py`; `backend/app/real_rd_executor.py:474-544,630-664` | `BudgetGuard` is default-off, RD-specific, blind when CLI usage is zero, and not a Cycle/Content Growth budget. |
| Timeout / lease | Model Gateway has a request timeout; execution claims have TTL/heartbeat/reaping configuration. | `backend/app/model_gateway.py:112-123,157-192`; `backend/app/agent_execution_kernel.py:45-68,197-228` | No accepted Research timeout, whole-Work deadline, whole-Cycle deadline or calibrated timeout policy. |
| Learning | Evidence-bound Candidate and distinct Accepted Learning Artifacts, scope/authority checks, conflict/supersede/invalidation, restart and domain isolation. | `backend/app/runtime/autonomous_operating.py:1311-1685`; `docs/reviews/CURIS_AUTONOMOUS_OPERATING_V1_EVIDENCE_BOUND_LEARNING_REVIEW.md:7-19,35-106` | No automatic Strategy/Goal/Package mutation, no Learning Engine and no confidence calibration. |

### Runtime separation warning

Curis also contains legacy/independent mechanisms such as `PipelineRuntime` retry/replan values, `RealRDExecutor` rounds and BudgetGuard, Task execution controls and model-gateway timeouts. Their existence does not make them Autonomous Operating or Content Growth policy. This audit counts them only as bounded partial mechanisms where the accepted path actually consumes them.

## 2. Guardrail Truth Matrix

| # | Guardrail | Status | Current implementation / accepted evidence | Proves | Does not prove |
|---:|---|---|---|---|---|
| 1 | Evidence requirement | `IMPLEMENTED` | Cycle close requires Result + Artifact + Provider evidence; Evaluation requires verified/current Evidence and closed Acceptance; Learning repeats those checks. | Success/continuation/Learning cannot be based on a bare employee summary. | Evidence quality outside the recorded source, external business truth or statistical sufficiency. |
| 2 | Confidence / UNKNOWN | `PARTIAL` | Evaluation supports `INSUFFICIENT`; Learning Candidate requires explicit confidence, conditions, limitations and revalidation criteria. | Unknown/insufficient evidence can block autonomous continuation; confidence is recorded rather than inferred as fact. | A calibrated confidence score, automatic `HIGH`, or evidence-count-to-confidence rule. |
| 3 | Relevant Gate | `PARTIAL` | Strategy Envelope gates protected/out-of-envelope ADJUST; Runtime Governance gates classified high-impact actions. | Protected strategy changes and common external/high-impact actions can fail closed or require authority. | Complete Content Growth action taxonomy or proof that every future Tool/Connector uses the same gate. |
| 4 | Human-in-the-loop | `IMPLEMENTED` | `DECISION_PACKET` can persist `WAITING_CEO`; CEO Acceptance and terminal PAUSE/STOP decisions are explicit and evidence-linked. | Runtime waits for real authority and resumes/applies from the same persisted object. | A response SLA, automatic timeout choice, or permission to auto-approve high-risk actions. |
| 5 | Strategy Envelope | `IMPLEMENTED` | Approved version/hash/provenance is pinned to Series/Cycle; allowed/protected change keys determine Leader authority versus CEO escalation. | Bounded ADJUST cannot silently cross protected authority. | Business correctness of the envelope contents or calibrated monetary/materiality boundaries. |
| 6 | Cost / Token cap | `PARTIAL` | Generic G4 token gate exists; opt-in RD BudgetGuard can hard-stop based on known tokens. | A bounded executor can stop when enabled and supplied trustworthy usage. | Default Content Growth enforcement, CLI token truth, external cost truth, Tool cost completeness or a universal safe cap. |
| 7 | Cycle budget | `UNAVAILABLE` | No canonical per-Cycle token/cost budget or aggregate enforcement was found in `AutonomousOperatingControl`. | — | Cycle total spend, remaining budget, or stop/degrade at a Cycle threshold. |
| 8 | Maximum autonomous chain depth | `UNAVAILABLE` | One active Cycle and exactly-one successor per applied Decision are enforced. No total successor-depth ceiling exists. | Concurrent/duplicate successor expansion is blocked. | A maximum number of Cycles/Works or indefinite-operation safety. |
| 9 | Retry limit | `PARTIAL` | Team path has bounded `maxReturns` and provider execution count; some legacy runtimes have their own retry/replan limits. | Specific revision/execution loops stop or wait at their local ceiling. | One universal `Retry ≤ 2`, Provider retry policy, or calibrated retry by action/risk. |
| 10 | Timeout | `PARTIAL` | Model Gateway request timeout and execution-claim TTL exist. | Individual transport/lease operations are bounded. | `Research Timeout = 30min`, Work deadline, Cycle deadline, or calibrated timeout by channel/action. |
| 11 | Loop detection | `PARTIAL` | Deterministic keys prevent duplicate Work/Task/successor; Team Work has execution and return ceilings. | Exact replay and bounded local revision loops do not multiply execution. | Semantic loop detection across repeated decisions/Cycles, recursive child-Work depth, or “same decision ×3 → STOP”. |
| 12 | Cancellation / STOP | `IMPLEMENTED` | Task/Work cancellation and Operating Series STOP are persisted; STOP creates no successor. | A user/authority can terminate bounded work/series without fabricating completion. | Guaranteed remote Provider termination for every adapter or rollback of already-completed external side effects. |
| 13 | WAIT / blocked state | `IMPLEMENTED` | Work `WAITING/WAITING_DECISION`, Series `WAITING` with `nextCheckAt`, capability gap and insufficient evidence states are persisted. | Waiting is a legal truth distinct from success/failure. | Automatic wake-up timing for every wait reason or calibrated expiry behavior. |
| 14 | Consecutive failure handling | `PARTIAL` | Provider/Work failure becomes waiting/failed; Cycle can become `FAILED`; partial truth remains. | Failures are not rewritten as completion and do not automatically create evidence/successor. | “Consecutive failures ≥3” detection, automatic Series pause or calibrated escalation threshold. |
| 15 | Leader escalation | `PARTIAL` | Responsibility Router supports `NEED_LEADER`; canonical Workspace Leader performs evidence-bound next-cycle review. | A real Leader identity and bounded authority path exist. | Universal cross-layer automatic escalation, response deadline or every Content Growth failure routed to Leader. |
| 16 | CEO escalation | `IMPLEMENTED` | Out-of-envelope ADJUST, explicit ESCALATE and protected PAUSE/STOP produce or require canonical CEO-gated Decision truth. | Protected decisions cannot be silently decided by an Employee/Leader. | Automatic CEO escalation for all unclassified future conditions or calibrated urgency. |
| 17 | Provider failure | `IMPLEMENTED` | Provider exception/timeout/malformed result leaves Work waiting or Cycle failed, keeps partial artifact truth and creates no fake Acceptance/Learning/successor. | Failure truth, callback identity and duplicate safety. | External provider availability/quality, universal retry or guaranteed remote cancellation. |
| 18 | Capability unavailable | `IMPLEMENTED` | Missing/disabled binding rejects Work materialization before Provider Task in accepted Primary/Cross-domain failure proofs. | No fake execution when required supply is absent. | Automatic replacement, performance equivalence or calibrated fallback choice. |
| 19 | Learning acceptance | `IMPLEMENTED` | Two distinct closed Cycles + completed Provider Results + verified Evidence + Acceptance + Evaluation + applied Decisions; separate Candidate/Accepted Artifacts and explicit Leader/CEO authority. | Learning is evidence-bound, scoped, replay-safe and non-self-modifying. | “≥3 observations”, automatic acceptance, automatic Strategy change, or confidence quality from sample count alone. |
| 20 | Restart / recovery safety | `IMPLEMENTED` | Series/Cycle/Claim/Work/Task/Result/Evidence/Decision/Learning persist; replay returns deterministic existing objects and does not treat duplicate calls as new work. | Accepted final truth and bounded control survive restart without duplication. | Proof that an external Agent is still alive merely because a persisted record says RUNNING; every adapter’s remote resume semantics. |

## 3. Cost Safety Truth

Cost safety is three separate capabilities and must remain separately represented.

### 3.1 Cost observability

| Question | Current truth | Status |
|---|---|---|
| Tokens used by one Work | Available only when the Provider/model adapter supplies valid usage; controlled Team proof used synthetic local metadata. | `PARTIAL` |
| Provider cost | ResultStore/Model Gateway can record provider-reported or estimated cost with a source label. External live-provider cost is explicitly unverified. | `PARTIAL` |
| Tool cost | Generic ResultStore execution cost fields exist, but no accepted Content Growth proof establishes complete Tool cost capture. | `PARTIAL` |
| Cycle total cost | No canonical Autonomous Cycle aggregate or accepted enforcement evidence. | `UNAVAILABLE` |
| Employee accumulated cost | Usage events can carry employee identity, but no accepted Autonomous/Content Growth cumulative cost truth was found. | `PARTIAL` observability, no enforcement |

### 3.2 Cost estimation

Model Gateway can calculate an estimate when usage and pricing metadata are usable and labels the cost source (`provider_reported`, `estimated`, or `unknown`). Existing R4 evidence correctly fails incomplete projections closed when cost/price metadata is absent or invalid. This is `PARTIAL`: it proves source-aware estimates for specific model paths, not universal or externally reconciled cost.

### 3.3 Cost enforcement

- Generic Runtime Governance can gate token spend against its configured hard limit.
- `BudgetGuard` can warn/hard-stop `RealRDExecutor` when explicitly enabled.
- Current `budget_guard_config.json` is `enabled=false`.
- The accepted test documents CLI usage blindness when adapters return `total_tokens=0`.
- Autonomous Operating does not own a Work/Cycle/Employee/company cost envelope.
- No current mechanism automatically downgrades model/tool quality or changes strategy when a cost threshold is reached.

Therefore IA must **not** claim “Curis automatically controls Cycle cost”, “automatically stops all Employees at budget”, or “automatically chooses a cheaper model”. It may show known usage with provenance and an honest `unknown/incomplete` state.

## 4. Autonomous Chain Safety

### 4.1 What can expand automatically

- A Team Operating call can execute a bounded sequence of responsibility assignments for one Work.
- Canonical child Work can be released sequentially under one Cycle.
- A legitimate Handoff transfers accountability between pinned responsibilities.
- An applied `CONTINUE` or in-envelope `ADJUST` Decision is the sole authority for exactly one successor Cycle.

### 4.2 Existing containment

1. One Operating Series has at most one active Cycle.
2. Trigger Claims, child Work and successor identities are deterministic/idempotent.
3. Work has one current executor and a persisted provider-execution ceiling.
4. Team request execution is bounded; returns/revisions have a local maximum.
5. Cycle close requires real Result/Artifact/Evidence and Acceptance.
6. Insufficient Evidence cannot `CONTINUE` or `ADJUST` autonomously.
7. `WAIT`, `ESCALATE`, `PAUSE` and `STOP` create no successor.
8. Capability/Provider/result-contract failures fail closed.

### 4.3 Remaining expansion risk

There is no global maximum number of child Works, no total successor-Cycle depth, no Series lifetime budget and no semantic detector for repeated equivalent decisions. A Leader could theoretically authorize another bounded `CONTINUE` after every completed/evaluated Cycle. That path is not “infinite automation already implemented”; each successor still requires accepted evidence/evaluation/Decision authority. But it also is not a proved indefinite-operation safety system.

Current accepted evidence proves two sequential Cycles and two sequential child Works, not parallel autonomous expansion. IA must not depict an unlimited self-growing chain, parallel scheduler, recursive research tree or automatic endless optimization.

## 5. Learning Truth

### Implemented

```text
at least two distinct CLOSED Cycles
→ completed Provider Results
→ CURRENT + VERIFIED Evidence
→ CLOSED Acceptance
→ Evaluation
→ APPLIED Decision
→ Learning Candidate Artifact
→ explicit Leader/CEO acceptance
→ separate Accepted Learning Artifact
```

Accepted evidence proves deterministic replay, concurrent duplicate safety, restart persistence, domain isolation, conflict rejection, explicit supersede and evidence-bound invalidation.

### Not implemented

- no automatic Learning from three observations;
- no automatic confidence calculation;
- no automatic Strategy/Goal/Envelope/Package/prompt/capability/code mutation;
- no Learning Engine, Memory replacement or Product/API/UI surface;
- no Cycle 3 produced by Learning;
- no proof that two Cycles are a statistically safe universal sample size.

The implementation prerequisite “at least two closed Cycles” is a provenance floor, not a calibrated claim that two observations imply `HIGH` confidence.

## 6. Contract vs Implementation vs Calibration

| Proposed rule / mechanism | Contract truth | Current implementation | Calibration truth |
|---|---|---|---|
| Evidence required before continuation/Learning | Required safety contract | `IMPLEMENTED` | Evidence freshness/source rules exist; business sufficiency still domain-specific. |
| UNKNOWN / insufficient evidence is legal | Required safety contract | `IMPLEMENTED/PARTIAL` through `INSUFFICIENT`, unverified/stale rejection and explicit unknown cost sources | No universal confidence scale. |
| Relevant Gate for high-impact/protected action | Required safety contract | `PARTIAL`: envelope + generic G1–G8 gates | Content Growth action taxonomy/materiality thresholds require future calibration. |
| `≥2 independent Evidence → HIGH` | Not established as current contract | Not implemented | `CANDIDATE — CALIBRATION REQUIRED`; evidence count alone cannot establish confidence. |
| `≥3 Observations → Learning` | Not current contract | Not implemented; current Learning requires two fully closed/evaluated Cycles and explicit acceptance | `CANDIDATE — CALIBRATION REQUIRED`. |
| `Retry ≤ 2` | Retry must be bounded where used | Only local `maxReturns` defaults to 2; other paths differ | No universal safe default; calibrate by action, side effect and failure class. |
| `Research Timeout = 30min` | Timeouts must exist at external/long-running boundaries | No Research-specific timeout | `UNKNOWN / CALIBRATION REQUIRED`. |
| `Consecutive failures ≥3 → escalation/stop` | Repeated failure needs bounded handling | No autonomous consecutive-failure counter/policy | `CANDIDATE — CALIBRATION REQUIRED`. |
| `Same decision repeated ≥3 → STOP` | Semantic loops must not run indefinitely | No semantic repeated-decision detector | `CANDIDATE — CALIBRATION REQUIRED`. |
| Work token cap | Resource use must be bounded where measurable | RD-only/default-off partial guard; not Team/Content Growth universal | `CALIBRATION REQUIRED`; unknown usage must remain unknown/fail-closed where policy requires. |
| Cycle token/cost cap | Material autonomous spending requires a bounded authority | Not implemented | `CALIBRATION REQUIRED` before product claim. |
| Progressive Investment L0–L4 | Research/product candidate, not Current Runtime contract | Not implemented as an investment runtime | `CANDIDATE`; UI disclosure L1–L4 is unrelated and must not be conflated. |
| One active Cycle | Current hard control contract | `IMPLEMENTED` atomically | No numeric calibration needed. |
| Exactly-one successor per applied Decision | Current hard control contract | `IMPLEMENTED` deterministically | No numeric calibration needed. |
| Learning does not self-modify authority | Current hard safety contract | `IMPLEMENTED` | No numeric calibration needed. |

## 7. IA-safe Assumptions

### IA may safely assume

- external/high-impact or protected strategy actions can require a real Gate;
- a canonical Employee/Leader/CEO authority can be shown distinctly;
- Work/Cycle can truthfully be running, waiting, failed, cancelled, paused or stopped;
- `WAITING_CEO` is a real persisted state, not a visual placeholder;
- unknown/insufficient/stale/unverified Evidence is legal and can block continuation;
- Result, Artifact, Evidence, Acceptance, Evaluation and Decision can be traced separately;
- Provider and capability failure can be shown without fabricating success;
- bounded Handoff/Return and sequential child Work exist;
- restart can restore persisted truth and deterministic replay without duplicating accepted work;
- Accepted Learning exists only after evidence-bound Candidate plus explicit authority;
- accepted Learning can be shown as scoped/reference-first and may later be invalidated/superseded without deleting history.

### IA must not assume

- automatic universal token or cost budget enforcement;
- accurate cost for every Provider/Tool/Employee/Cycle;
- automatic cheaper-model/tool selection;
- a universal retry count of 2;
- a 30-minute research timeout;
- “three failures” or “three repeated decisions” as a current stop rule;
- a fixed confidence score derived from evidence count;
- three observations automatically create Learning;
- unlimited, parallel or recursive autonomous Work/Cycle expansion;
- automatic Strategy modification from Learning;
- external Agent remains alive after restart solely because persisted state says running;
- Full autonomous operation without Leader/CEO/evidence boundaries.

IA may use qualitative language such as “受成本限制”, “需要更多证据”, “等待负责人/CEO决定”, “执行已停止”, “当前成本未知” and “能力不可用”. It must not show invented counters, deadlines, confidence percentages, cost totals or automatic optimization claims.

## 8. Remaining Runtime Gaps

These are implementation/calibration gaps, not permission to develop them in this audit:

1. canonical Work/Cycle/Series token and cost aggregation with provenance;
2. default-on or explicitly configured budget enforcement for the actual Team/Autonomous path;
3. unknown-usage policy for CLI/external Agents;
4. Tool cost completeness and external provider reconciliation;
5. maximum autonomous successor/child-Work depth or another approved bounded-operation policy;
6. semantic loop/repeated-decision detection;
7. consecutive-failure counter and escalation/stop policy;
8. risk/action-specific retry and timeout policies;
9. Content Growth-specific relevant-action classification and materiality thresholds;
10. calibrated confidence/evidence sufficiency rules;
11. calibrated Learning observation/sample requirements;
12. parallel multi-Work safety, if parallelism is later authorized;
13. remote Provider cancellation/resume truth per adapter;
14. Product/API/UI surfacing of Learning without exposing internal Runtime detail.

Each numeric value remains `CALIBRATION REQUIRED` until backed by domain evidence, failure cost, side-effect reversibility and operational observation. Existing defaults must not silently become universal policy.

## 9. Final Blocker Decision

**AUTONOMY GUARDRAIL BLOCKER RESOLVED**

This resolves the IA truth boundary, not all Runtime gaps:

- hard current mechanisms are identified;
- partial/local mechanisms are separated from universal policy;
- Research Candidates are not presented as implementation;
- precise thresholds without evidence remain `CALIBRATION REQUIRED` or `UNKNOWN`;
- IA can proceed without guessing by showing only actual state, authority, evidence, unknowns and qualitative limits;
- future numeric policy requires a separate Runtime Calibration gate.

Active databases were opened read-only only. At audit start:

- `data/curis.sqlite`: size `1232896`, mtime `1786873339`, SHA-256 `2ea2506f90f764e834d47d8f6bae3cb41c22d457757e0e9216c0ae8c39a39ec6`, `integrity_check=ok`.
- `backend/data/curis.sqlite`: size `1277952`, mtime `1786783659`, SHA-256 `a9d96a9536a5bce3b3b30f912e86a37f61d28527a8eb2d35af7a5857d29414e4`, `integrity_check=ok`.

No Runtime, Schema, DB, Policy, test, Provider, Research, Authority, IA or Figma artifact was modified.
