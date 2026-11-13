# CURIS AUTONOMOUS BUSINESS OPERATION — CODEX INDEPENDENT RESEARCH

Authority Class: RESEARCH
Status: Review
Disposition: CODEX INDEPENDENT TRACK COMPLETE — READY FOR CEO REVIEW
Date: 2026-08-20
Scope: System feasibility × Runtime reuse × durable operating loop; research only

## 0. Executive conclusion

### 0.1 Feasibility verdict

Curis 不需要、也不应再造一套 Agent Runtime、Workflow Runtime、Task Runtime 或 Execution
Engine。当前已接受的 Workspace-scoped Team Operating 底座已经能完成一轮内的真实链路：

```text
immutable Operating Definition
→ scoped Responsibility Assignment
→ canonical AI Employee
→ Capability Binding
→ existing Provider Task / Orchestrator / Session
→ verified callback
→ Result Contract
→ Responsibility Router
→ next Employee / Consult / Review / Return / Handoff / Decision / Wait
```

缺口位于这条链的上方和两端，而不在执行中间：

```text
CEO Intent / current Goal / current Strategy
→ create or wake one bounded Operating Cycle
→ [reuse existing Team Operating execution]
→ collect Results as Signals
→ evidence-bound Review
→ durable Next-cycle Decision
→ create/wake exactly one next Cycle, or wait/pause/stop
```

因此推荐模型是：

> **Operating Lifecycle = Company OS Control Plane** 之中的一个薄控制层。
> 它只拥有 Cycle 边界、durable wake/claim、Situation Snapshot、Review、Next-cycle Decision
> 与下一 Cycle 的幂等创建；实际工作继续由 Work、Assignment、Responsibility Router、Provider
> Execution 和 Result/Evidence 完成。

这在不假设模型突然变聪明的前提下可实现，因为系统把 AI 限定在三个有证据、有边界的判断点：

1. 基于当前 Goal 与可引用事实提出本轮 Plan；
2. 基于 Result/Evidence 形成带不确定性的 Interpretation / Learning candidate；
3. 在确定性规则允许的动作集合中建议或选择 Next-cycle Decision。

Scope、权限、预算、唯一责任、Result Contract、幂等、版本、触发去重、Decision Gate、暂停和停止
仍由确定性 Runtime 控制，不能交给模型自由发挥。

### 0.2 Current delivery truth

- **现在已有**：Workspace-scoped Responsibility Routing、Real Employee execution、Result Contract、
  immutable Operating Definition、reference-first Context、restart/cancel/loop guard、Handoff、Decision、
  Result recovery，以及既有 `CYCLE` / Evidence / Acceptance / transition log 等持久化底座。
- **现在部分具备**：Domain-specific RD Cycle、XHS/Content flow、TaskGraph trigger/scheduler、进程内 event
  bus、append-only evolution event、wake/session claim 模式；它们没有组成一个跨周期 Company OS loop。
- **现在缺失**：一个被正式接受的 durable Cycle Controller、Next-cycle Decision 合同、原子 next-cycle
  创建、跨重启 due-cycle scanner、Evidence→Signal→Learning 质量门、Cycle Context Contract，以及两个
  Domain 对同一生命周期的正式接入证据。
- **当前硬边界**：Business-scope Provider Execution 未实现；External live provider quality/cost 未验证；
  full RD/XHS migration 与 cross-layer automatic Leader escalation 未实现。

### 0.3 V1 boundary

V1 应先交付 **Workspace-scoped Autonomous Operating Loop**。Business 在 V1 中聚合 Workspace
Goal/Result/Signal 并承载 Business Goal/Strategy 约束，但不能宣称 Business-scoped AI Leader 已经通过
真实 Provider 执行；该能力需先完成现有 identity-scope extension。这样两个案例仍使用同一个
Operating Lifecycle，只是 Domain adapter 和当前可执行 Scope 不同。

---

## 1. Research boundary and evidence method

### 1.1 Authority consumed

本研究按 Truth Router 分层读取：

- Product Truth：`PRODUCT_DOCUMENT_POINTER.md` 指向的 Current Product Blueprint、Master Map、UI
  Blueprint 中与 Company / Department / Business / Workspace、Goal / Result / Review / Learning、Team
  Operating 和 Next Operating Cycle 相关的 Current 合同；
- Implementation Truth：`CURRENT_STATE.md`、正式 Responsibility Routing / Real Employee Issues、Accepted
  Reviews、当前 Runtime source 与 focused tests；
- Research input：Team Operating Engine research / contract，仅用于复用已选定的责任路由模型，不把
  Research 候选写成当前实现；
- External primary sources：durable execution、long-running agent harness、context engineering、ReAct、
  Reflexion、AutoGen、human callback gate、AI risk measurement 与 specification gaming。

### 1.2 Independence statement

本轮没有读取 WorkBuddy 对“Autonomous Business Operation / Operating Lifecycle”同题研究结论，也没有
读取 `.workbuddy/output/` 或 WorkBuddy 同题产物。工作树中的 WorkBuddy memory 仅在 `git status` 中被
看见文件名，未作为研究内容读取。结论未提前与另一专项对齐。

### 1.3 Evidence labels used below

- **EXISTING**：Current code/runtime 存在，且有正式 Accepted / current evidence 支持；
- **REUSABLE**：现有能力可以直接承担 V1 职责，不应复制；
- **PARTIAL**：代码或局部 Domain 机制存在，但缺当前整合、正式 acceptance 或目标 Scope；
- **MISSING**：目标机制没有当前可运行证据，必须新增或正式接入。

---

## 2. Existing substrate audit

| Area | Verdict | Current evidence | V1 decision |
| --- | --- | --- | --- |
| Company | EXISTING / REUSABLE | Tenant / Company scope 是 Runtime Foundation、Employee identity、Result 与 Workspace 的现有隔离边界 | 继续作为最高安全与审计范围；不新增 Company registry |
| Department | PARTIAL | 真实 Department 可解析，`DEPARTMENT` scoped Assignment 可登记 | 不作为 V1 自动执行 Scope；跨 Workspace→Business→Department Leader chain 仍缺 authority/runtime closure |
| Business | PARTIAL | `business_directions` 可支持 Business-scoped Assignment/Workflow/Router，且可无 Workspace 运行控制面 | Provider Execution 仍不支持 Business scope；V1 只做 Business aggregation/constraint，不宣称真实 Business AI execution |
| Workspace | EXISTING / REUSABLE | Workspace-scoped Team Operating、AI Employee、Capability、Result、restart、cancel 已 Accepted | V1 唯一首发执行 Scope |
| Leader / Responsibility Assignment | EXISTING at current scope / PARTIAL cross-layer | `Employee × Role × Scope`、唯一 current-scope Leader resolution、zero/multiple fail-closed 已实现 | 复用；不得以“Leader agent type”建立第二套身份。跨层升级保持显式 Decision Gate |
| Work / Cycle | EXISTING / REUSABLE | `CYCLE` 是持久化 Runtime entity；Responsibility Router 把 routing truth 写回同一 Work/Cycle | 继续使用同一 `CYCLE`；每轮一条新 Cycle，不建立 forever Task |
| Task / Execution | EXISTING / REUSABLE | ResultStore Task、Orchestrator、Provider session、Task execution control、Pipeline/legacy executors 均存在 | Lifecycle Controller 只 dispatch，不执行工具、不拥有 Task state |
| Result / Evidence | EXISTING / REUSABLE | Result refs、Artifact、Evidence、callback provenance、Result Contract、Acceptance 与 scoped read 已存在 | 作为 Signal 的唯一事实入口；模型摘要不能替代 Result/Evidence |
| Decision | EXISTING / REUSABLE | `DECISION_PACKET` 支持持久等待、apply、resume；重复请求可复用 | 高风险/权限/资源/不可逆/跨 Scope 决策继续复用；普通低风险 next-cycle 决策写入 Cycle review/event |
| Need / Problem | PARTIAL | Router 支持枚举 signal、problem 字段、Need responsibility/Leader/Decision 路由 | 缺 canonical typed Signal/Need lineage；V1 作为 Review 中的 typed signal，不新增 Need Center/table |
| Team Operating Engine | EXISTING / REUSABLE at Workspace | Accepted control plane 支持 Default Flow、Consult、Review、Return、Handoff、Wait、Decision、Result recovery | 作为唯一 team execution/routing substrate |
| Responsibility Router | EXISTING / REUSABLE | pinned version、Holder/Executor 分离、atomic transfer、duplicate-safe collaboration 已实现 | 不扩成自然语言万能 Router；只接收受控 action/signal |
| Real Employee Execution Loop | EXISTING at Workspace / MISSING at Business | Workspace local deterministic provider 已穿过真实 Task/Session/callback path；外部 live provider 未验证 | V1 先接 Workspace；Business 与 external live provider 分别建 gate |
| Context isolation | EXISTING / REUSABLE | Tenant/Company/Workspace scope validation；wrong-scope reads fail closed；Assignment context 分离 | Cycle Context 也必须带 scope/version/ref validation |
| Reference-first context | EXISTING / REUSABLE | Router context 上限 32 refs、compact context 1000 chars；accepted E2E 为 0 hydrated bodies、0 copied Conversation | 扩展为 typed Cycle Context，不复制历史 bodies |
| Immutable Operating Definition | EXISTING / REUSABLE | Workflow publish 产生 immutable snapshot；Work pin vN，新 Work 用 vN+1 | Goal/Strategy/Plan 也按 snapshot/ref pin；运行中不静默替换 |
| Result recovery | EXISTING within Work / PARTIAL cross-cycle | Result/Artifact/Evidence refs 回到同一 Work；restart 后保持；Domain cycle 可 review/close | 缺 Result→Review→Next-cycle 原子 closure |
| Restart / cancel / loop guard | EXISTING within Work | execution claim、duplicate callback conflict check、cancel、max provider executions、max returns 已 Accepted | 跨 Cycle 仍需 due scan、lease expiry、deterministic next-cycle key |
| Trigger / Scheduler | PARTIAL | TaskGraph scheduler 有 scheduled/event/condition trigger，但为进程内 thread + graph；EventBus 是非持久化进程内；`next_check_at` 与 append-only events 存在 | 不直接把它宣称为 durable Business scheduler；复用 trigger vocabulary 和 scan pattern，新增持久 claim/scan integration |
| Wake / session recovery | PARTIAL | `agent_wakeup_requests` 有幂等 key、atomic claim、TTL、checkpoint/recovery，但未证明是当前 Operating Lifecycle authority | 可复用 claim pattern或经独立 Issue 复用 store；不得直接把 Agent session 当 Operating Cycle |
| Workspace Engineering | EXISTING substrate / PARTIAL domain adoption | Declarative Package、schema-stable lifecycle、transactional migration 已有 accepted substrate | 可承载未来 Domain adapter/version；V1 不依赖 arbitrary plugin，不顺带完成 RD/XHS migration |
| CURRENT_STATE | EXISTING authority | 顶部 2026-08-20 reconciliation 已明确 accepted Workspace core 与四项 remaining boundary | 本研究不得覆盖这些边界 |

### 2.1 What the audit changes

旧的“最后一个 Workflow 节点完成就停止”问题已经不能再表述为“Curis 没有责任路由”。当前真实断点
已前移为：

```text
one Work can execute and route durably
BUT
one completed/reviewed Cycle does not durably and idempotently decide/wake the next Cycle
```

同样，仓库里存在 scheduler、event bus、wake request，不等于已经有 Company Operating Loop：

- TaskGraph scheduler 随 Graph 完成或 escalation 停止，且活动循环在进程内；
- EventBus 明确不负责跨进程持久分发；
- WakeRequest 是 Agent/Task session substrate，没有被 Operating Cycle authority 消费；
- existing RD Cycle closure 的 `CONTINUE / ADJUST / PAUSE` 只写当前 Cycle 决定，不自动创建下一 Cycle；
- Team Operating `/execute` 是一次请求内最多 16 次 Employee execution 的 bounded loop，不是跨日/跨周期
  wake mechanism。

---

## 3. Is Operating Lifecycle a new Runtime?

### 3.1 Decision

**不是。** Operating Lifecycle 是 Company OS Control Plane 的一部分，位于现有 Runtime 之上：

```text
┌─────────────────────────────────────────────────────────────┐
│ Company OS Operating Lifecycle Controller                  │
│ cycle boundary · trigger claim · snapshot · review         │
│ next-cycle decision · wait/pause/stop · audit              │
└──────────────────────────────┬──────────────────────────────┘
                               │ dispatch / refs / decisions
┌──────────────────────────────▼──────────────────────────────┐
│ Existing Team Operating Control Plane                      │
│ Work · Assignment · Holder · Router · Handoff · Decision   │
└──────────────────────────────┬──────────────────────────────┘
                               │ execute
┌──────────────────────────────▼──────────────────────────────┐
│ Existing Execution Substrates                              │
│ ResultStore Task · Orchestrator · Provider · Pipeline      │
│ Domain executor · Task control · Result/Evidence           │
└─────────────────────────────────────────────────────────────┘
```

### 3.2 Minimal new control responsibilities

只新增六项职责；任何更多能力必须由证据证明需要：

1. **Trigger intake and claim**：扫描 `nextCheckAt` 或消费 accepted Result signal；用稳定
   `triggerKey` 原子 claim，过期可回收；
2. **Single active Cycle invariant**：一个 Operating Scope / series 最多一个 active Cycle；
3. **Situation Snapshot**：在 Cycle start 固定 Goal/Strategy/Definition version 和当前事实 refs；
4. **Plan release**：把 Plan 转成现有 Work/Assignment 输入；Controller 不创建执行语义；
5. **Review and Next-cycle Decision**：验证 Evidence sufficiency 后，只能输出规定的六种 action；
6. **Atomic continuation**：记录本轮决定，并幂等地创建/安排一个 next Cycle，或进入 wait/pause/stop。

### 3.3 Explicit non-responsibilities

Controller 不得：

- 调用工具或直接执行 Provider；
- 维护第二套 Task/Result/Evidence/Employee/Role/Capability registry；
- 把 Conversation history 当 durable state；
- 解释任意自然语言成为权限或 Scope；
- 用 `while(true)` 常驻一个 Agent context；
- 把“模型认为完成”直接写成 Goal achieved；
- 把 schedule/event/threshold 全做成 V1 generic automation platform。

### 3.4 The one necessary Runtime delta

当前 `CYCLE` state machine 偏向旧 RD CEO-acceptance path：正常 Review 需要经过 CEO acceptance，且
`CLOSED/FAILED` 为 terminal。V1 需要对**同一个既有 Cycle primitive**做向后兼容扩展，而不是新增
`OPERATING_CYCLE_V2`：

- accepted Results 或 scheduled review 可由 SYSTEM 将 `RUNNING → REVIEWING`；
- low-risk、policy-authorized Review 可记录 Next-cycle Decision 后 `REVIEWING → CLOSED`；
- high-risk / authority missing 继续 `REVIEWING → WAITING_CEO` 并复用 Decision Packet；
- `WAIT` 关闭本 Cycle，但把 Scope control state 置为 `WAITING + nextCheckAt/event condition`；
- `PAUSE` / `STOP` 作用于 Scope 的 operating control state，不用一个永不结束的 Cycle 假装长期经营。

这是现有 state/transition 的最小增量，预计不需要新业务表；是否可仅使用
`runtime_entities.data_json + runtime_transition_log + evolution_events.idempotency_key` 必须在正式 Issue
的并发/索引 preflight 中验证。Research 不提前承诺 Schema 一定零变更。

---

## 4. Minimal canonical state

### 4.1 State ownership rule

长期经营不等于把所有名词都建表。V1 只有三种持久化形态：

1. **Existing first-class entity**：继续使用现有 Company/Business/Workspace/CYCLE/Assignment/Result/
   Evidence/Decision/Handoff；
2. **Versioned scope/cycle record**：会改变执行与审计结论的 Goal/Strategy/Plan/Snapshot/Review，作为现有
   scope 或 Cycle 的 versioned data/ref；
3. **Derived projection**：可以从权威事实重算且不参与决策幂等的摘要/状态，不单独持久化。

### 4.2 Canonical state matrix

| Concept | Persist? | Owner | Version/lifecycle | Existing relation | Crash recovery / duplicate / audit | V1 form |
| --- | --- | --- | --- | --- | --- | --- |
| Operating Responsibility | Yes, already | scoped Responsibility Assignment; current Holder on Cycle | Assignment revision; Cycle pins immutable snapshot | Employee × Role × Scope; Holder≠Executor | restart from pinned Assignment; zero/multiple fail closed; Handoff log | **REFERENCE**, no new object |
| Intent | Yes | CEO owns Company/Business Intent; Workspace consumes scoped intent | immutable revisions; only explicit Decision changes current ref | existing `intentRef`, Business/Workspace Truth | Cycle pins `intentRef`; duplicate update keyed by Decision; provenance required | scope field/ref, no Intent table in V1 |
| Goal | Yes | CEO/Business Leader/Workspace Leader according to scope authority | current Goal version; Cycle snapshots it; achieved/superseded/stopped explicit | existing Goal product truth and Cycle goal/outcome fields | restart reads pinned Goal version; goal change requires decision id | versioned scope record or referenced Artifact |
| Strategy | Yes if it constrains decisions | Leader at same scope; CEO for protected changes | immutable Strategy version; active ref changes only after approved Adjustment | Workspace/Business Strategy product truth; no accepted generic Runtime object | Cycle pins version; change has evidence refs, hypothesis, expected signal, review window | compact versioned JSON/ref, no table by default |
| Situation Snapshot | Yes | Lifecycle Controller, system-authored | immutable per Cycle | refs Company/Workspace Truth, Signals, last Decision/Learning | deterministic snapshot digest; same trigger returns same snapshot | Cycle child data/ref, bodies excluded |
| Operating Plan | Yes | current Leader Assignment | draft may change; released version immutable; superseded on replan | becomes Work/Assignment inputs; does not replace TaskGraph | stable `planVersion` + work idempotency keys; plan diff audited | Cycle data/ref with bounded steps and Work refs |
| Operating Cycle | Yes, already | current scoped Leader Assignment | one bounded generation; terminal closes; next Cycle is a new entity | existing `CYCLE` + responsibility routing | deterministic next-cycle id; one active invariant; restart scan/claim | **REUSE CYCLE** |
| Result | Yes, already | producing Assignment; acceptance owner distinct where required | immutable result/provenance; correction is new version/ref | existing Task/Artifact/Evidence/Outcome/Result refs | duplicate callback must match; wrong provenance/type rejected | **REUSE** |
| Signal | Sometimes | system derives; source owner remains Result/Evidence producer | formula/window/version required; recomputable unless used in decision | derived from Results, Evidence, external receipt, cost/usage | if decision-used, persist value+formula+window+source refs; otherwise projection | derived projection; material signals embedded in Review |
| Interpretation | Candidate only | reviewer/Leader, never source of truth | may be revised until Review closes | consumes Signals | no strategy change from unaccepted interpretation | Review field, not standalone object |
| Review | Yes | scoped Leader; independent reviewer for protected metrics | one current Review per Cycle; append-only amendments after close | Result/Evidence/Signal → decision | stable review key; evidence coverage and uncertainty audited | Cycle review record; no Review table by default |
| Learning | Only accepted learning | scoped Leader; CEO for Company-level policy | append-only accepted statement with valid-from/to and confidence | Review output; referenced by future Context | duplicate by review+learning key; contradiction creates new learning, not overwrite | compact record inside Review / referenced Artifact |
| Next-cycle Decision | Yes | Leader if within policy; CEO/authorized owner otherwise | immutable action + reason + policy/evidence refs | low-risk Cycle event; high-risk existing Decision Packet | deterministic decision key; application idempotent; rejected alternative reasons retained | Cycle decision + transition event; Decision Packet only when gated |
| Operating control state | Yes | existing Business/Workspace scope | `ACTIVE / WAITING / WAITING_DECISION / PAUSED / STOPPED`; current cycle ref and next check | coordinates bounded Cycles | atomic compare-and-set; restart scanner resumes due scopes | fields on existing scope projection/data, not new entity by default |

### 4.3 Why Learning is not a memory dump

只有同时满足以下条件的内容才成为 durable Learning：

- 指向可验证 Evidence/Result/Signal refs；
- 明确适用 Scope、时间窗口、样本量与已知限制；
- 能说明它改变或保留了哪个 Strategy/Plan assumption；
- 由有权 Reviewer 接受；
- 与旧 Learning 冲突时形成新版本/反证，不静默改写历史。

模型的自我评价、Conversation 总结、一次成功/失败的感想都只是 Interpretation candidate。

---

## 5. Durable Operating Cycle

### 5.1 Executable model

```text
TRIGGER CLAIMED
  │  stable triggerKey; lease; scope not paused/stopped
  ▼
CYCLE START
  │  create exactly one bounded CYCLE; pin Goal/Strategy/Operating Definition
  ▼
SITUATION SNAPSHOT
  │  current truth refs + freshness/unknown + previous decision/accepted learning
  ▼
PLAN
  │  bounded deliverables, result contracts, budget, review condition
  ▼
WORK GENERATION
  │  deterministic work keys; reuse existing Work/Assignment objects
  ▼
EXISTING TEAM OPERATING RUNTIME
  │  Router → real Employee execution → Results/Evidence; bounded execution/return
  ▼
RESULT INTAKE
  │  validate scope, producer, result type, provenance, freshness, duplicate key
  ▼
REVIEW
  │  Evidence → Signal → Interpretation → accepted Learning candidate
  ▼
NEXT-CYCLE DECISION
  ├─ CONTINUE ── create/schedule exactly one next Cycle, same Strategy version
  ├─ ADJUST ──── create approved Strategy/Plan version, then one next Cycle
  ├─ WAIT ────── no Cycle now; persist nextCheckAt/event condition
  ├─ ESCALATE ── reuse Decision Packet; wait durably; same scope/cycle lineage
  ├─ PAUSE ───── explicit resume required; no automatic wake
  └─ STOP ────── terminal operating scope; preserve all history/results
```

### 5.2 State invariants

1. One Scope/operating series has at most one active Cycle.
2. One Cycle pins one Goal version, Strategy version and Operating Definition version.
3. A trigger is an invitation to review/start, not authorization to bypass scope, permission, budget or Decision Gate.
4. Work is generated with deterministic keys `(cycleRef, planVersion, responsibilityKey, ordinal)`.
5. Accepted Result callbacks are idempotent; conflicting duplicates fail closed.
6. Review cannot start until required Results are terminal or the review trigger explicitly records missing/late data.
7. Every Next-cycle Decision closes or suspends the current boundary before another Cycle can become active.
8. `CONTINUE` is a decision, not an implicit `while(true)`.
9. `ADJUST` must name the changed assumption, evidence, expected effect and next review window.
10. `WAIT`, `PAUSE`, and `STOP` are different durable states and cannot be inferred from silence.

### 5.3 Restart-safe execution

On startup or periodic scan:

1. find scopes with `ACTIVE/WAITING` whose `nextCheckAt <= now`, accepted Result wake, or pending manual resume;
2. atomically claim using `(scopeRef, triggerKey)` and a lease/owner/expiry;
3. if an active Cycle exists, resume from its persisted phase instead of creating a new one;
4. if the prior Cycle has an applied Next-cycle Decision, derive the deterministic next Cycle id from the prior
   Cycle + Decision key and create-or-read it;
5. inspect existing Work/execution claims before dispatch; never infer failure only from missing process memory;
6. expire abandoned claims and make them reclaimable; do not repeat accepted Results or external side effects.

The current Workspace-scoped executor already covers within-Work claim/callback duplication. The missing acceptance
must prove the same semantics at the Cycle boundary.

### 5.4 Observability

Every Cycle must expose a read projection, not a new control console:

- current Scope, Cycle, phase/status, Holder, Executor;
- pinned Goal/Strategy/Operating Definition versions;
- trigger kind/key/time and claim owner/expiry;
- Plan/result/evidence/signal/review/decision refs;
- execution/return/adjustment counts, budget usage and next check;
- why the system continued, adjusted, waited, escalated, paused or stopped;
- current blocker and exact recovery action.

---

## 6. V1 trigger model

### 6.1 Minimum combination

V1 只实现三类入口：

| Trigger | Why required | V1 behavior |
| --- | --- | --- |
| Result-driven | 有 accepted Result 时不应等到下个 cron 才 review | Result intake records a stable trigger key and wakes/reviews the current Cycle; duplicate Result produces no duplicate review |
| Scheduled review | 没有 Result、外部数据迟到、员工卡住时仍必须被重新观察 | per-scope `nextCheckAt`; due scan uses durable claim; schedule is a fallback and review cadence, not forever Agent loop |
| Leader / CEO initiated | 新 Goal、显式 resume、紧急调整和人工 Decision 必须可立即进入同一机制 | same trigger intake/claim path; authority checked before Cycle/decision mutation |

### 6.2 Deferred triggers

- **Generic event-driven**：V1 不做任意 EventBus→Cycle rules。Result-driven 已覆盖最重要业务事件；
  权限失效、预算耗尽等硬事件直接 fail-closed/WAIT/ESCALATE，不需要通用规则引擎。
- **Threshold-driven**：V1 的 threshold 只在 Review 内把 Signals 分类为 normal/deviation/insufficient，
  不直接启动执行。只有当至少两个 Domain 证明同一低延迟需求且 false-positive 成本可控时，再提升为
  wake trigger。

这三类最小组合保证：正常结果立即继续、无新数据也会按时复查、CEO/Leader 可以随时介入；业务不会
因为一次 Workflow 完成而停机，也不会为了“自动”而引入完整 automation platform。

---

## 7. Review and Learning truth

### 7.1 Required evidence chain

```text
Evidence / Result
  └─ source, scope, producer, timestamp, verification, freshness, external receipt
       ↓ deterministic transform
Signal
  └─ metric/formula, window, baseline, sample size, comparability, uncertainty
       ↓ model + rules, explicitly uncertain
Interpretation
  └─ hypothesis, alternatives, confounders, missing evidence
       ↓ authorized Review
Learning
  └─ accepted/declined, confidence, applicability, expiry, evidence refs
       ↓ controlled change
Strategy / Plan change
  └─ version, expected effect, guardrails, review window, rollback/stop condition
```

Skipping any link makes `ADJUST` illegal. The allowed fallback is `CONTINUE`, `WAIT`, or `ESCALATE` with the
uncertainty recorded.

### 7.2 Evidence sufficiency contract

Each Goal/Strategy version must carry an Evaluation Contract:

- outcome metric and allowed proxy metrics;
- source authority and independent verification requirement;
- observation window and freshness;
- minimum sample size / minimum independent windows;
- baseline/comparison and comparability rules;
- materiality threshold and known confounders;
- maximum adjustment frequency/cooldown;
- risk/irreversibility conditions requiring CEO Decision;
- budget, permission and external commitment limits.

If this contract is absent, V1 may execute an already approved Plan and report Results, but may not autonomously
change Strategy.

### 7.3 Anti-overfitting and anti-drift rules

- One observation can trigger a **safety/operational fix** when the failure is deterministic and severe; it cannot
  alone prove a business strategy.
- Strategy adjustment normally requires the Evaluation Contract's sample/window threshold. A reasonable safe
  default when a Domain has not calibrated its own rule is two independent observation windows plus no material
  contradictory signal; otherwise `WAIT` or `ESCALATE`.
- Change one main hypothesis at a time where causal learning matters; concurrent changes must be recorded as
  non-attributable.
- Enforce cooldown/minimum review window before reversing a Strategy version, except security, permission,
  compliance, budget or severe external failure.
- Keep leading proxy, delivered output and external outcome separate. “发布 10 篇”不能自己证明“账号增长”。
- The producing Employee/model cannot be the sole acceptor of its own Result for protected decisions.
- Preserve negative/unknown/late evidence; do not let a summary omit it.
- Record rejected alternatives and why they were rejected, so a future model cannot rewrite the rationale.

### 7.4 Reward hacking controls

Google DeepMind documents specification gaming as satisfying the literal objective while missing the intended
outcome. Curis V1 therefore requires:

- paired outcome + guardrail metrics, never one optimization number;
- source/receipt verification outside the producing model where practical;
- no model write access to raw external metrics or verification status;
- budget/cost/quality/complaint/rollback signals alongside growth/velocity;
- anomaly and missing-data review before success classification;
- periodic independent Review for long-running strategies;
- CEO Gate for changing the Goal, success contract, guardrail or source authority itself.

### 7.5 What Reflexion/ReAct do and do not prove

[ReAct](https://arxiv.org/abs/2210.03629) supports interleaving reasoning with actions so a model can update a plan
and handle exceptions within a task. [Reflexion](https://arxiv.org/abs/2303.11366) shows that verbal reflection over
feedback can improve later trials through episodic memory. Neither establishes that an AI's self-summary is a
business truth, that repeated reflection converges, or that it may rewrite goals and evaluation rules. Curis should
reuse the useful mechanism—small plan updates and compact accepted learning—while keeping evidence acceptance and
strategy authority outside the model.

---

## 8. Cycle Context Contract

### 8.1 Default payload

Every Leader/Employee execution receives an Assignment-scoped view of one typed Cycle Context:

```text
CycleContext {
  scopeRef + cycleRef + pinned versions,
  currentGoal {summary, successContractRef},
  currentStrategy {summary, versionRef, constraints, evaluationContractRef},
  currentPlan {versionRef, current deliverable, resultContractRef},
  relevantLearning[] {summary, applicability, confidence, evidenceRefs},
  currentSignals[] {value/classification, window, freshness, sourceRefs},
  referencedResults[] {resultRef, type, status, producer, acceptedAt},
  currentDecisions[] {decisionRef/action, authority, constraints},
  retrievalHints[]
}
```

The context contains refs and bounded summaries. Evidence bodies, full Results, historical Cycle bodies and full
Conversation are hydrated only when the current Input Contract names them.

### 8.2 Hard exclusions

- complete historical Conversation;
- all historical Cycles;
- Evidence bodies by default;
- all Employee contexts or sessions;
- raw provider traces/tool output;
- stale strategy/plan versions not referenced by the current Cycle;
- every past Learning regardless of current applicability.

### 8.3 Budget and growth estimate

Recommended default budget per leader review/planning call:

| Segment | Target tokens |
| --- | ---: |
| Goal + success contract summary | 150–300 |
| Strategy summary + constraints + evaluation contract | 300–700 |
| Current Plan / responsibility input | 300–800 |
| Relevant accepted Learning (top 3–5) | 300–800 |
| Current Signals + uncertainty | 300–900 |
| Result/Decision reference metadata | 200–500 |
| Scope/version/retrieval instructions | 200–500 |
| **Default total** | **1,750–4,500** |

Hard target: p95 Cycle Context below 6,000 tokens; emergency on-demand hydration is a separate traceable retrieval,
not silently added to the persistent prompt.

Growth properties:

- prompt/context growth per Cycle is **O(1)** because refs, relevant Learning and Signals are capped and selected;
- durable metadata grows **O(number of Cycles)** and remains queryable outside the model;
- at 100 Cycles, a 1–3 KB compact Review/Learning record per Cycle is roughly 100–300 KB plus refs/indexes, while
  the next model call still receives roughly 1,750–4,500 tokens;
- copying a 2,500-token prior summary into every next Cycle would reach roughly 250,000 carried tokens by Cycle 100
  and is explicitly prohibited.

Current accepted Router evidence (3,411 context chars / 3,535 bytes / 22 refs / 0 hydrated bodies in one content
Work) proves reference-first feasibility, not this full Cycle Context budget. V1 acceptance must measure actual token
count, retrieval count, stale/missing refs and context-selection recall across at least 100 synthetic/replayed Cycles.

Anthropic's long-running agent work reports that compaction alone does not prevent premature completion or lost work;
structured artifacts are needed across sessions. Its context engineering guidance likewise treats context as finite
and recommends external structured notes plus the smallest high-signal token set. Curis maps that principle to
durable Goal/Plan/Review refs, not an ever-growing chat.

---

## 9. Failure model and recovery

| Failure | Durable system state | Automatic action | Human/next recovery | Duplicate/data rule |
| --- | --- | --- | --- | --- |
| Provider failure before Task | Cycle `RUNNING/WAITING`, execution claim `FAILED`; no accepted Result | bounded retry only if policy allows; otherwise WAIT | reconnect/switch approved capability or escalate | same execution key; no duplicate Task if prior Task exists |
| Provider failure during Task | Task failed/paused; Holder preserved; Executor cleared after reconciliation | existing cancel/failure path; do not route on provider success alone | retry/resume after capability health | conflicting callback rejected; late callback cannot revive cancelled execution |
| Employee capability missing | Work/Cycle WAITING; no fabricated Executor/Result | resolve another approved binding only if same Assignment policy permits | staffing/capability Decision | capability resolver cannot change Holder |
| Result Contract failure | execution record rejected/failed; Cycle remains active or waiting | Return if bounded explicit contract exists; else Review/WAIT | fix producer/output contract through authorized version | wrong type/provenance never advances |
| Leader crash | claim lease expires; Cycle phase and refs persist | another worker reclaims trigger and resumes phase | none unless repeated crash threshold | stable trigger/cycle/work keys suppress duplicate effects |
| Runtime restart | no in-memory loop assumed | startup due-scan + active claim reconciliation | operator only for inconsistent/unknown external execution | resume current Cycle; never create replacement to hide state |
| Data arrives late | Review records missing/late; WAIT with nextCheckAt | Result trigger reopens/continues review only if Cycle policy allows | Leader decides whether late data changes next Cycle | source event/result id de-duplicates; preserve original review and amendment |
| Duplicate callback | existing accepted truth returned if identical | no new Result/route/Cycle | investigate only on mismatch | mismatch fail closed and audit |
| CEO does not reply | `WAITING_DECISION`, Decision Packet pending, no next Cycle beyond safe policy | reminder/escalation cadence only; no unauthorized default | CEO/authorized delegate responds, or explicit expiry policy | one Decision Packet per decision key |
| Consecutive strategy failure | failed-window counter and contradictory Learning refs persist | after configured limit: no further ADJUST; ESCALATE/PAUSE | CEO revises Goal/strategy/team/budget or stops | counter based on accepted reviews, not model claims |
| No new data | scheduled Review records `INSUFFICIENT_DATA` | WAIT; optionally run approved data-collection Work, bounded | fix connector/measurement or change cadence | absence is a signal, not success or failure |
| Goal completed | Review proves success contract and guardrails | STOP current operating series or open a separately authorized new Goal | CEO/Leader confirms protected completion if policy requires | no implicit new Goal; terminal decision immutable |
| Permission revoked/expired | active execution cancelled/blocked; scope WAITING/ESCALATED | fail closed immediately despite pinned config | re-authorize or change approved plan | live revocation overrides pinned version |
| Budget/resource exhausted | no new Work; current cancellable work stopped safely; evidence preserved | WAIT/ESCALATE/PAUSE per policy | add budget/capacity, reduce scope, or STOP | usage source is external/audited; model cannot edit budget |
| Trigger storm | one claimed trigger; other equivalent triggers coalesced | process highest-priority reason in one Review | none unless conflicting authority | `triggerKey` + scope claim; retain contributing signal refs |
| Review/evaluator unavailable | Results persist; Review WAITING | bounded retry or alternate approved reviewer | Leader/CEO gate | producer cannot self-accept protected result by fallback |
| Strategy/Definition changed mid-cycle | running Cycle keeps pinned versions; live revocation still applies | new version affects next Cycle only | explicit migration Decision if truly required | no silent mutation; impact/diff event required |

Failure recovery follows the same principle as AWS Step Functions callback tasks: a workflow can wait durably for an
external/human callback and then continue, rather than terminate or spawn an unrelated flow. Curis already has
Decision Packet semantics suitable for this role; it does not need AWS Step Functions itself.

---

## 10. Two domains, one lifecycle

### 10.1 Case A — AI tech Xiaohongshu account growth

**Scope:** one XHS operating Workspace under a Business. Current external publishing/analytics boundaries remain
truthful; missing connectors force WAIT instead of fabricated growth.

| Lifecycle phase | Domain content |
| --- | --- |
| Goal | e.g. grow qualified follower/lead outcome under cost, complaint, brand and platform constraints |
| Situation Snapshot | account/platform connection health; last posts and accepted publication receipts; verified analytics freshness; content inventory; budget; relevant learnings |
| Plan | bounded hypothesis for one review window: topics, research, copy, visual, review, publish slots, measurement plan |
| Work Generation | existing content responsibilities and Result Contracts; publishing only if connector/permission effective |
| Team Operating | topic→research→copy→visual→publish default; Consult/Review/Return/Handoff as current Router supports |
| Result Intake | content package, publication receipt, verified platform metrics, cost/quality/complaint data; missing analytics is `INSUFFICIENT_DATA` |
| Review | compare outcome/proxy/guardrails to baseline/window; separate content quality from account growth |
| Next Decision | CONTINUE successful hypothesis; ADJUST one variable; WAIT for data/platform; ESCALATE risk/brand/budget; PAUSE revoked channel; STOP achieved/abandoned Goal |

Example truth boundary: “ready-to-publish package accepted” may complete a Responsibility but cannot prove post
publication growth. Without verified publication receipt and analytics, the Cycle may close with `WAIT`, not
`CONTINUE because growth succeeded`.

### 10.2 Case B — continuous Curis product development

**Scope:** one RD Workspace for Curis product. The same lifecycle is used; engineering artifacts replace content and
platform metrics.

| Lifecycle phase | Domain content |
| --- | --- |
| Goal | one product/business outcome with acceptance contract, not “keep coding forever” |
| Situation Snapshot | current Product/Implementation authority refs, active Issue/review, repository/Runtime truth, defects, user evidence, budget/capability/permission |
| Plan | bounded Issue set, allowed files, deliverables, tests and Runtime/Desktop evidence gates |
| Work Generation | existing RD Work/Task/Responsibility Assignments; Product→Architecture→Development→QA only as default responsibility flow |
| Team Operating | Consult Product/Architecture without Holder transfer; Developer↔QA Return/Handoff; Decision Packet for high-risk/authority choices |
| Result Intake | exact source diff, tests, Artifact/Evidence/Review, Browser/Desktop/DB evidence proportional to claim |
| Review | compare acceptance contract, regressions, product truth, runtime evidence, delivery risk; code completion is not product outcome |
| Next Decision | CONTINUE next accepted increment; ADJUST design/plan/team; WAIT external dependency; ESCALATE authority/product decision; PAUSE release; STOP goal accepted/cancelled |

Current limitation: full RD Domain migration to Team Operating and Business-scope Provider Execution are not accepted.
V1 must either integrate RD as a Workspace-scoped bounded Issue with fresh acceptance, or remain simulation/replay
evidence. It cannot cite the XHS content E2E as proof that RD autonomous execution is already delivered.

### 10.3 Same-model proof

Both Domains use identical control objects and actions:

```text
GoalVersion + StrategyVersion + Cycle + SituationSnapshot + PlanVersion
+ existing Work/Assignment/Result/Evidence
+ Review + NextCycleDecision
```

Only Domain adapters differ in:

- Result types and external sources;
- Evaluation Contract and review window;
- Domain responsibilities/default flow;
- irreversible/high-risk thresholds;
- allowed execution connectors.

No second lifecycle is required. If a Domain needs a unique lifecycle engine rather than a Result/Signal/Evaluation
adapter, the model has failed and that Domain must not be admitted to V1.

---

## 11. External research synthesis

| Primary source | Mechanism used | What Curis must not infer |
| --- | --- | --- |
| [Temporal documentation](https://docs.temporal.io/) | long-running work resumes from durable history after process/infrastructure failure | does not imply Curis must adopt Temporal; current SQLite substrate may be sufficient if acceptance proves equivalent local guarantees |
| [Microsoft Durable Task — Eternal orchestrations](https://learn.microsoft.com/en-us/azure/durable-task/common/durable-task-eternal-orchestrations) | infinite history grows without bound; `continue-as-new` keeps identity while starting a new generation | Curis should not implement an in-process forever loop; bounded new Cycle generations are the native equivalent |
| [AWS Step Functions callback pattern](https://docs.aws.amazon.com/step-functions/latest/dg/connect-to-resource.html) | durable wait for human/external callback, timeout and resume | do not terminate/recreate the business operation when CEO input is pending |
| [Anthropic — Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) | long work needs incremental sessions and clear durable handoff artifacts; compaction alone loses state or causes premature completion | do not rely on one long chat/context or model memory |
| [Anthropic — Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) | context is finite; structured external notes, compaction and just-in-time retrieval keep high-signal context | do not carry all historical results/cycles because the context window is large |
| [ReAct paper](https://arxiv.org/abs/2210.03629) | interleaved reasoning/action supports plan updates and exception handling | does not provide durability, authority, idempotency or business evaluation |
| [Reflexion paper](https://arxiv.org/abs/2303.11366) | feedback-conditioned verbal reflection can improve later trials via episodic memory | self-reflection is not verified Learning and must not set its own reward/evaluation contract |
| [AutoGen paper](https://arxiv.org/abs/2308.08155) | multiple specialized agents, humans and tools can follow programmable interaction patterns | multi-agent conversation is not responsibility truth; Curis should keep one Holder and use existing Assignment/Router |
| [NIST AI RMF Core](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/) | continuous governance, documented human oversight, uncertainty-aware measurement, independent review and monitoring | not every cycle requires CEO approval, but risk/authority policy and review responsibility must be explicit |
| [Google DeepMind — Specification gaming](https://deepmind.google/blog/specification-gaming-the-flip-side-of-ai-ingenuity/) | agents can optimize literal proxy rewards while missing intended outcomes | do not let the producer define, edit and judge the same success metric |

OODA、PDCA 与 Build–Measure–Learn 都支持“周期性观察/判断/行动/复盘”的业务直觉，但它们不是 Runtime
specification。Curis V1 adopts the bounded-cycle shape, then adds what those management loops leave unspecified:
durable identity, version pinning, exact ownership, Result/Evidence provenance, idempotency, wait/cancel/restart and
human authority gates.

---

## 12. Autonomous Operating V1

### 12.1 V1 capability statement

> 在一个已配置并授权的 Workspace 中，Workspace Leader 能基于持久 Goal/Strategy 与 scheduled/result/
> manual trigger，启动一个有界 Operating Cycle；生成受控 Plan 和现有 Team Operating Work；真实 AI
> Employees 通过现有 Provider execution 产出可验证 Results；Leader 依据 Evaluation Contract 做 Review，
> 并持久选择 CONTINUE / ADJUST / WAIT / ESCALATE / PAUSE / STOP；系统在重启、重复触发和重复 callback
> 下只继续或创建一次 next Cycle。

### 12.1.1 How much already exists

按 V1 必需的十个机制块计算，而不是按代码量或虚假进度百分比：

- **6 个可直接复用**：scope/identity、Assignment/Router、Employee execution、Result/Evidence、durable
  Cycle/Decision/Handoff primitives、immutable definition/reference-first context；
- **1 个部分可复用**：scheduler/event/wake/claim patterns，但还不是 accepted durable Operating trigger；
- **3 个 closure-critical 缺口**：Evidence-bound Review/Learning contract、atomic Next-cycle continuation、两个
  Domain 对同一 Lifecycle 的正式 integration/acceptance。

所以底层执行与持久化的大部分已存在，但 Autonomous Operating V1 不能写成“60% 已交付”：三个缺口
恰好决定系统会不会在一轮后停止、会不会重复执行，以及会不会从噪声中学错。

### 12.2 Minimum implementation deltas

1. **Extend existing Cycle contract**：兼容新增 SYSTEM review path、Next-cycle Decision、predecessor/
   successor refs、pinned Goal/Strategy/Plan versions；不新增 Cycle table。
2. **Operating scope control fields**：activeCycleRef、operatingStatus、nextCheckAt、lastDecisionRef、
   trigger/claim metadata；优先落在既有 Workspace/Business projection/data。
3. **Durable trigger scanner/claim**：result-driven + scheduled + manual；复用现有 idempotency/claim patterns，
   不复用进程内 EventBus 作为事实队列。
4. **Cycle Context assembler**：typed, reference-first, summary-first, retrieve-on-demand；budget/metrics mandatory。
5. **Review/Evaluation Contract validator**：Evidence sufficiency、source/freshness/window/sample/uncertainty、
   adjustment cooldown 和 Decision threshold。
6. **Atomic continuation**：decision application + deterministic next Cycle create/read in one transaction boundary。
7. **Two Domain adapters**：XHS growth and RD provide Result types, Signals, Evaluation Contracts and risk gates only；
   they do not own lifecycle engines。
8. **Acceptance harness**：isolated SQLite, restart between every major phase, duplicate/late callbacks, cancel, no
   data, CEO silence, budget/permission loss, 100+ replayed Cycles and current active DB fingerprint safety。

### 12.3 Explicitly not in V1

- Business-scope Provider Execution before identity-scope authority/acceptance;
- arbitrary event/threshold rule builder;
- autonomous Goal creation or Goal/success metric rewrite;
- free-form self-modifying workflows, skills or prompts;
- cross-layer automatic Workspace→Business→Department→CEO Leader routing;
- external publication/payment/deployment without existing permission and receipt contracts;
- global Learning/Memory/Review Center or new analytics truth;
- Temporal/Airflow/Celery/Kafka adoption without proven local substrate failure;
- all RD/XHS/TTK migration, Marketplace, arbitrary Workspace extension or full Evolvable closure。

### 12.4 Development difficulty

| Slice | Difficulty | Why |
| --- | --- | --- |
| Cycle/scope state + deterministic continuation | Medium | primitives exist; concurrency and compatibility tests are the real work |
| Durable scanner/claim/restart | Medium | claim/idempotency patterns exist; must prove process crash and lease recovery |
| Cycle Context assembler | Medium | existing reference-first base exists; relevance and stale/missing-ref metrics need acceptance |
| Review/Evaluation quality gate | High | Domain-specific signal semantics, uncertainty and authority cannot be solved by generic prompting |
| XHS Domain adapter | High | real publishing/analytics connection and receipts remain external dependency |
| RD Domain adapter | High | full migration and provider/scope acceptance remain incomplete |
| 100+ cycle reliability/observability evidence | High | long-run duplicates, history growth, drift and failure injection dominate risk |

Rough order of magnitude for one experienced backend/runtime engineer with domain review support: core controller and
replay harness is several weeks, not several days; each real Domain integration is a separate bounded delivery. This
is not a commitment because live connector/provider readiness is not currently verified.

### 12.5 Largest technical risk

The largest risk is **not durable scheduling**. SQLite, deterministic IDs, conditional updates, existing CYCLE/Work,
Decision and execution claims can implement a local durable controller.

The largest risk is **decision truth**:

- whether external Results are real, fresh and comparable;
- whether Signal definitions match the CEO's intended outcome;
- whether Review has enough evidence to distinguish noise from strategy failure;
- whether the same AI that produced the work can game or rationalize the evaluation;
- whether a Strategy adjustment remains within authority, budget and irreversible-risk limits.

If Curis cannot enforce the Evaluation Contract and independent evidence path, it can automate activity but cannot
truthfully claim autonomous business operation.

### 12.6 Go / no-go gates

V1 may enter implementation only after a formal Issue freezes:

1. first executable Scope = Workspace;
2. exact current Goal/Strategy storage authority and version rules;
3. Cycle state transition delta without breaking accepted RD/Team Operating paths;
4. trigger claim/idempotency transaction design and whether current schema/indexes suffice;
5. Evaluation Contracts for both Domain cases;
6. XHS external-data fallback and RD migration boundary;
7. risk/permission/budget/CEO Decision policy;
8. isolated DB, restart, Browser/Desktop and 100-cycle evidence contract.

No implementation should begin by adding tables for Intent/Goal/Strategy/Plan/Review/Learning. First prove which
fields/refs cannot live safely on existing scope/Cycle/Result/Evidence records.

---

## 13. Final answer to the core question

Curis 可以在当前模型能力下长期经营，但“长期”必须由 durable software guarantees 提供，而不是由一个
永不停止的 AI 对话提供：

```text
AI chooses within bounded contracts.
Runtime owns truth, scope, identity, versions, claims and stop conditions.
Evidence constrains Learning.
Every Cycle ends.
The operating series continues only through an explicit, durable, idempotent decision.
```

The minimal product/runtime move is one **Operating Lifecycle Controller** over the accepted Workspace-scoped Team
Operating core. It reuses Work, Assignment, Router, Provider Execution, Result, Evidence, Decision and CYCLE. It adds
only cross-cycle trigger/claim, snapshot, review truth, next-cycle decision and atomic continuation.

This is system-feasible. It is not yet delivered. Workspace V1 is the honest first gate; Business-scope autonomous
provider execution, external live quality/cost, complete RD/XHS migration and cross-layer Leader escalation remain
explicit follow-on boundaries.

---

CODEX AUTONOMOUS OPERATION RESEARCH<br>
— INDEPENDENT TRACK COMPLETE<br>
— SYSTEM FEASIBILITY DEFINED<br>
— RUNTIME REUSE DEFINED<br>
— DURABLE CYCLE DEFINED<br>
— FAILURE / TOKEN BOUNDARY DEFINED<br>
— V1 PROPOSED<br>
— STOP
