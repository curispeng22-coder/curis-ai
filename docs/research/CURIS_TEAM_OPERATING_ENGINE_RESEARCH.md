# CURIS TEAM OPERATING ENGINE — CORE ENGINE DESIGN RESEARCH

Authority Class: RESEARCH
Status: Review
Disposition: READY FOR CEO REVIEW
Date: 2026-08-19
Scope: Product × Runtime architecture research only; no implementation authority

## 1. Executive conclusion

Curis 首版不应把现有 Sequential Workflow、DAG Pipeline 或 Domain Handoff 统一成另一套
“万能 Workflow Engine”。唯一推荐模型是：

> **Work-centered Responsibility Routing Control Plane**
> 以一个持续 Work / Goal 为中心，读取组织中的 Role、Responsibility、Employee Binding 与
> scoped Responsibility Assignment；根据 Result / Problem / Need 决定保持当前责任、Consult、
> Review、Handoff、Return、Escalate、Decision 或完成本轮，并把真实执行委托给现有执行底座。

中文产品名推荐为 **团队运转**；普通编辑区使用 **默认流程**。`Workflow`、DAG、状态机、Router、
Retry Edge 继续作为内部实现或高级审计语言，不成为 CEO 的主要产品概念。

这个模型不是第五套 Runtime：

- WorkspaceRuntime / shared Runtime foundation 保存 Work、责任状态、Handoff、Decision、Result refs；
- Responsibility Router 只做路由决定，不执行 Provider 工作；
- Orchestrator / Pipeline / Domain executor 继续完成任务；
- Employee Execution Identity Bridge 保证责任 Employee 与真实执行身份一致；
- Capability Resolver 选择“怎么做”，不能决定“谁对结果负责”；
- Result Store / Evidence 保持结果与依据的权威来源。

## 2. Truth boundary and research method

### 2.1 Product Truth consumed

- `docs/00_Context/PRODUCT_DOCUMENT_POINTER.md`
- `docs/01_Product/Curis_Product_Blueprint.html`
- `docs/01_Product/Curis_Product_Master_Map.md`
- `docs/01_Product/Curis_Product_UI_Blueprint.html`
- `docs/00_Context/CURRENT_STATE.md`
- `docs/reviews/BUSINESS_WORK_SURFACE_PAGE_CONTRACT.md`（Review Candidate，不覆盖 Frozen Product Truth）

当前产品语义明确：Leader 是 system-defined Responsibility Role；Assignment 的最小语义是
`Employee × Role × Scope`；Workflow 属于 Workspace，只表达 Role、Responsibility、Assigned
Employee、Input、Output 与 Handoff；Result 回到 Workspace Truth / Workspace Leader，再进入
Continue / Adjust / Escalate / Wait / Next Operating Cycle。以上是 Product Truth 或待 CEO Review
的 Product Delta，不等于已实现。

### 2.2 Current implementation evidence consumed

- `docs/reviews/CURIS_WORKFLOW_RUNTIME_IMPLEMENTATION_AUDIT.md`
- 该 Audit 引用的 Current Code、Issue、Accepted Review 与 focused evidence
- `docs/00_Context/CURRENT_STATE.md`

本研究不重新运行 Runtime、测试或数据库，也不把进行中的 Responsibility Routing 开发当作既成
事实。Current Implementation 结论保持为：多个执行机制并存；尚无统一 scoped Responsibility
Assignment + Default Flow + Result/Problem/Need Router。

### 2.3 Historical evidence consumed

- `docs/pmo/workflow.md`
- `docs/team-v2/WORKFLOW.md`
- `docs/team-v2/TEAM_ROLES.md`
- `docs/team-v2/CONTEXT_RULES.md`
- `docs/team-v2/LEGACY_RULES_AUDIT.md`

这些文件仅证明历史运行经验，不是 Current Product 或 Runtime Authority。

### 2.4 External principles consumed

| Source | Principle used | Curis boundary |
| --- | --- | --- |
| [Anthropic: Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) | 固定路径适合可预测工作；动态 Agent 适合需要反馈和调整的工作；从最简单可组合模式开始 | Default Flow 可以提供正常路径，但动态责任判断不应被固定 Workflow 锁死 |
| [Temporal documentation](https://docs.temporal.io/) | 长运行工作需要持久状态，并能在故障后从原位置恢复 | Work / Handoff / Gate / Cycle 必须 durable；不要求引入 Temporal 产品 |
| [Temporal Worker Versioning](https://github.com/temporalio/documentation/blob/main/docs/production-deployment/worker-deployments/worker-versioning.mdx) | 运行实例应绑定兼容版本，部署新版本不能静默改变旧实例 | Work pin Operating Definition version；修改只默认影响 New Work |
| [Microsoft Orleans documentation](https://learn.microsoft.com/en-us/dotnet/orleans/) | 有身份的对象封装状态与行为，持久化、事件与版本可独立管理 | Work 是单一责任状态边界；借鉴 ownership isolation，不引入 Actor 框架 |
| [AWS Step Functions human approval](https://docs.aws.amazon.com/step-functions/latest/dg/tutorial-human-approval.html) | 人工判断可以是可恢复的 wait/callback gate，而不是终止或另起流程 | Decision Gate 持久等待，Decision 后继续同一个 Work / Cycle |
| [OMG BPMN 2.0 specification](https://www.omg.org/spec/BPMN/2.0/About-BPMN/) | 标准流程图中的 sequence/default/conditional flow 都有严格执行语义 | Curis 的 Default Flow 必须自定义为责任默认关系，不能借用箭头却不定义语义 |
| [AutoGen paper](https://arxiv.org/abs/2308.08155) | 多 Agent 可通过可编程交互组合人、工具与 Agent | 证明交互拓扑可灵活；不证明 Curis 应暴露任意 Agent Graph |

外部资料只支持运行原理，不覆盖 Curis Current Truth，也不构成选型建议。

## 3. Current implementation starting point

### 3.1 Five mechanisms are not one Runtime

| Mechanism | Current truth | Why it is not the target engine |
| --- | --- | --- |
| WorkflowRuntime | `sequential software_rnd`；按第一个 pending Step 强制推进；失败则 Run 失败 | Arrow 是 mandatory order，不是 Default Responsibility Relationship |
| Orchestrator | 一个 Task 内按 List 顺序运行 Tool Steps，可等待输入或人工接管 | 没有 Role / Responsibility Assignment；Handoff 是同 Task control state |
| TaskGraph + PipelineRuntime | DAG readiness、retry、switch capability、replan、CEO escalation | 是执行计划/依赖子系统，不读取 Workspace Responsibility Assignment |
| RD Workspace | Holder / Executor 分离、Artifact Review、持久 Handoff、P7 Decision、Result/Evidence refs | 接近目标，但路由仍是 RD Domain command / explicit target |
| XHS Workspace | Creator 完成后向预配置 Reviewer 做自动 Handoff | 是 domain-coded fixed target，不是通用动态 Assignment resolution |

### 3.2 Useful proven invariants

- Holder 与 Current Executor 必须分开；Provider callback 不能自行夺取责任。
- Handoff 只有 ACK 后才改变 Holder；Send 时原 Holder 仍负责。
- Review / Consult 可产生另一个 Employee execution，但不必改变原 Holder。
- Decision Packet 是等待判断并恢复原 Work 的 Gate，不是 Handoff。
- RD/XHS Handoff 使用 reference-first，避免复制完整 Conversation / Artifact。
- 一个 Task 可以包含多个 execution Step；Handoff 本身不必创建新 Task。
- Capability retry / switch / replan 与组织责任路由是两层问题。

### 3.3 Current gaps that this model must close

1. Canonical scoped Responsibility Assignment 的读取与运行引用；
2. Default Responsibility Handoff Relationship 的严格表示；
3. Result / Problem / Need → Responsibility resolution → Assignment / Leader 的 Router；
4. Assignment-scoped Conversation / Context Package；
5. Result 回收与受控 Next Operating Cycle；
6. Operating Definition version pinning 与显式 running-work migration。

## 4. Historical five-seat lessons

### 4.1 Retain

- 一个目标保持单一主执行链，普通问题在当前 Holder 内解决；
- 只有责任边界变化才 Handoff；
- 质量 Review 独立，但不自动夺取业务责任；
- 安全、不可逆、高影响或 Scope 冲突才升级 Gate；
- Handoff 传最小摘要和 refs，不复制完整历史；
- Issue / Work、Review、Evidence 和最终 Result 可审计；
- 新接收者只恢复完成责任所需的最小 Context。

### 4.2 Reject

- 固定席位链不等于真实业务责任链；
- 每一个小问题都跨席位，会增加等待、上下文恢复与 Token；
- 每次 Handoff 都拆 Issue，会把连续 Work 切碎；
- 同一目标被多个 Agent 重复全量恢复，既贵又产生不同 Truth snapshot；
- 预设所有研发都必须 Product → Architecture → Development → QA，不能覆盖真实协作。

### 4.3 Generalized lesson

历史真正证明的不是“五席”，而是：

> **Single continuous Work + explicit responsibility + cheap consultation + acknowledged transfer +
> milestone review + exceptional escalation.**

## 5. Candidate models assessed

| Candidate | Strength | Failure for Curis | Decision |
| --- | --- | --- | --- |
| Strict sequential workflow | 简单、可预测 | 无法跳过、回退、Consult、动态找责任；最后节点后停机 | Reject as team engine |
| User-authored arbitrary DAG | 可表达复杂依赖 | 把 Router / Condition / Retry / Loop 暴露给 CEO；箭头同时混入依赖与责任 | Reject as product model |
| General state machine | 状态与 transition 严格 | 单独使用不能回答谁负责、Consult 是否转责、Context 如何传 | Internal technique only |
| Agent graph / group chat | 动态协作 | 容易把每个角色变成新 Session，并复制全部群聊上下文 | Reject as ownership model |
| Event-driven orchestration | 支持外部事件和异步等待 | 事件本身不能定义责任与结果契约 | Reuse internally |
| Responsibility routing | 直接回答 Holder、Assignment、Consult、Handoff、Leader | 需要 durable state 与 existing executor integration | **Selected** |

选定模型不是“只做 Router”。它是 **Responsibility Routing + Durable Work State + Existing
Execution Substrates** 的最小组合。

## 6. Core Runtime Model

```text
Goal / Work
  ├─ pinned Operating Definition Version
  ├─ current Operating Cycle
  ├─ current Responsibility Assignment / Holder
  ├─ Current Executor (optional, never implies ownership)
  ├─ Context Package refs
  ├─ Result / Problem / Need / Evidence events
  └─ Routing Decision
       ├─ STAY_AND_CONTINUE
       ├─ CONSULT
       ├─ REVIEW
       ├─ HANDOFF
       ├─ RETURN_OR_REVISION
       ├─ ESCALATE
       ├─ WAIT_DECISION
       ├─ COMPLETE_CYCLE
       └─ WAIT

Routing Decision
  -> existing Domain executor / Orchestrator / Pipeline
  -> existing Capability Resolver
  -> existing Employee Execution Identity Bridge
  -> existing Result / Evidence / Handoff / Decision records
```

责任路由控制层只拥有“谁负责下一结果、是否转责、为何转责、需要什么上下文”。它不重新实现
Tool calling、DAG execution、Provider Session、Capability fallback、Result storage 或 Workspace
Domain lifecycle。

## 7. Minimum Runtime primitives

### 7.1 First-class durable objects

| Primitive | Minimum contract | Ownership |
| --- | --- | --- |
| Work | `workId`, goal, scope, success/stop contract, status, pinned definition version, current cycle | Team Operating Engine |
| Operating Definition Version | immutable Role/Responsibility refs, default relations, Input/Output contracts, policies | Workspace Truth; versioned |
| Operating Cycle | cycle objective, input refs, current assignment, opened/closed times, terminal Result refs, continuation decision | Child of Work |
| Responsibility Assignment | `Employee × Role × Scope`, active interval, authority, source | Organization Truth; engine references, does not duplicate |
| Result | typed outcome, producer assignment, scope, status, refs, evidence, contract validation | Existing Result Store / Domain truth |
| Handoff | source/target assignment, reason, responsibility/result contract, refs, lifecycle, ACK provenance | Reuse shared Runtime Handoff |
| Decision Gate | owner/authority, question, options, evidence refs, deadline, status, applied decision | Reuse Decision Packet |
| Context Package | immutable manifest of required truth/result/artifact/evidence refs plus bounded summary and source versions | Work/Assignment scoped |
| Evidence | source, producer, time, integrity/provenance, ref | Existing Evidence model |

### 7.2 Referenced organization definitions, not engine-owned duplicates

- Role
- Responsibility Definition
- Employee
- Workspace / Business / Department / Company Scope
- Leader Assignment
- Employee Capability Binding

The engine resolves and records references to these authorities. It must not copy them into a second organization
registry.

### 7.3 State or relationship, not a new top-level object

| Concept | Representation |
| --- | --- |
| Current Holder / Owner | Work/Cycle field referencing active Responsibility Assignment |
| Current Executor | optional execution field; clears when execution ends; never changes Holder by implication |
| Default Flow | versioned directed relationship between Responsibility Definitions with priority and applicability |
| Return / Revision | typed Routing Decision; uses Handoff lifecycle only when accountability transfers |
| Leader | system-defined Responsibility Role resolved through scoped Assignment |
| Problem / Need | typed signal/event attached to Work/Cycle/Result; durable when it affects routing |
| Routing Decision | append-only event with input refs, selected action, reason, rule/version and alternatives rejected |
| Consult / Collaboration | normally a Work-scoped interaction/event; promote to durable record when async, cross-Employee, externally consequential or needed as evidence |
| Review | typed collaboration/request; Reviewer executes independently while original Holder remains unless explicit transfer occurs |

## 8. Responsibility Assignment semantics

1. Responsibility belongs to a Role within a Scope; Employee identity alone is insufficient.
2. A Work/Cycle has exactly one accountable Current Holder Assignment at a time, except before initial routing or
   while a completed cycle is waiting for continuation.
3. Current Executor may be none or one verified execution identity; executor never implies accountability.
4. Capability Resolver selects a valid execution path for the selected Employee; it cannot select a different
   accountable Employee without a Routing Decision.
5. If zero or multiple valid Assignments resolve where exactly one is required, fail closed and route to the lowest
   valid Leader / Decision Gate. Do not pick “first enabled employee”.
6. Assignment changes are explicit, versioned/audited and effective at a defined boundary; they do not silently mutate
   an active Holder.

## 9. Default Flow — strict Runtime semantics

`A → B` means:

> When A produces an accepted Output matching its Result Contract, and no stronger explicit route, Return,
> unresolved Need, Wait condition, Decision Gate or Domain policy applies, B is the default next
> **Responsibility Definition** to resolve within the same Workspace and Operating Definition Version.

It does **not** mean:

- B is a mandatory execution dependency;
- B must always run;
- A immediately loses responsibility when it emits a Result;
- B is a fixed Employee identity;
- a new Task or Provider Session must be created;
- the UI arrow is an arbitrary executable graph edge.

### 9.1 When B is used

- A's accepted Result satisfies the transition input contract for B;
- B's responsibility is still required for the current cycle;
- one valid active B Assignment resolves;
- no explicit Return / exception / Decision / wait rule has higher priority.

### 9.2 When B can be skipped

- B's required Result is already valid and fresh for this Work/Cycle;
- the current Result makes B unnecessary under an approved Domain policy;
- an explicit CEO/Leader instruction selects another valid responsibility within authority;
- B has no valid Assignment and an allowed alternate responsibility exists;
- the cycle can close without B under its Result Contract.

Every skip is a durable Routing Decision with reason; “Router felt like it” is invalid.

### 9.3 When work returns to A

- B rejects A's Result against a declared Output/Review contract;
- the required correction belongs to A's responsibility;
- Return includes the failed criteria, evidence refs and expected revised Result.

If A must again own the next Result, Return uses the acknowledged Handoff protocol back to A. If B remains
accountable and only needs clarification, it is Consult, not Return/Handoff.

### 9.4 When work goes to C

- Result / Problem / Need matches C's responsibility more specifically than B;
- an approved Domain policy or explicit Leader instruction selects C;
- B is unavailable and C is an authorized alternate Assignment;
- B Consults C while B remains Holder, if C only supplies advice or a sub-result.

### 9.5 When Leader enters

- no unique valid Assignment resolves;
- the matter crosses Workspace scope or exceeds current authority;
- Goal / Rule / staffing / priority must change;
- risk, compliance, irreversibility or external commitment reaches a Decision threshold;
- repeated Return/retry reaches the bounded escalation policy;
- Result requires Continue / Adjust / Escalate / Wait / Next Cycle judgment.

Leader is resolved by Scope, not drawn as a mandatory node.

## 10. Dynamic routing algorithm

Router precedence is deterministic even when an Agent helps classify the signal:

1. Validate Work, Scope, pinned version, signal provenance and current Holder.
2. Apply explicit accepted Decision / Return target / legally binding Domain rule.
3. Default to `STAY_AND_CONTINUE`; owner change is never the default response to a question.
4. If only information, opinion, review or bounded sub-result is missing, choose `CONSULT` or `REVIEW`.
5. If accountability for the next contracted Result belongs elsewhere, resolve that Responsibility Assignment and
   create `HANDOFF`.
6. If no unique legal Assignment resolves, follow the lowest valid Leader chain.
7. If authority/risk threshold is exceeded, create `WAIT_DECISION` and pause only the affected Work boundary.
8. If the cycle Result Contract is satisfied, `COMPLETE_CYCLE`; then separately decide continuation.
9. Persist selected action, reason, rule/version, input refs and rejected alternatives.

Model output may propose classification and candidates. Deterministic guards own Scope, authority, active Assignment,
tenant/company/workspace isolation, Result contract, Handoff transition and Decision application.

## 11. Consult / Collaboration vs Responsibility Handoff

| Question | Consult / Collaboration | Responsibility Handoff |
| --- | --- | --- |
| Who remains accountable? | Current Holder | Source until ACK; target after ACK |
| Why used? | Need information, critique, review, specialist sub-result or coordination | Next contracted Result belongs to another Responsibility |
| Does Owner change? | No | Yes, only after valid ACK |
| Context | Small question packet + relevant refs | Full minimum Context Package for new responsibility |
| New Task required? | Only if consultant performs real independent execution | Not by Handoff itself; target execution creates/reuses Task when work begins |
| Result | Consult response / Review evidence feeds current Holder | Target becomes accountable for next Result Contract |
| Failure | Holder continues, retries, changes consultant or escalates | Handoff remains unaccepted; source retains responsibility |

### Developer asks Product Manager

```text
Developer Holder
  -> Consult(Product Manager, requirement question, refs)
  -> Product response
  -> Developer continues same Work/Assignment context
```

No Product Handoff and no Developer return Handoff occur.

### QA returns a defect to Developer

If QA's responsibility is to decide release readiness and Developer must own the revised build, this is a typed
`RETURN_OR_REVISION` that transfers responsibility back only after ACK. If QA merely asks for an explanation while
remaining responsible for the verdict, it is Consult.

## 12. Handoff lifecycle

```text
PROPOSED -> SENT -> ACKNOWLEDGED -> TRANSFERRED
                    |
                    +-> REJECTED / RETURNED / EXPIRED
```

- Source Holder remains accountable through `SENT`.
- ACK must prove the target Assignment, target Employee identity, Work/Scope/version and Context Package are valid.
- Holder changes exactly once at `TRANSFERRED`; Current Executor remains none until verified execution begins.
- Reject/expire preserves source Holder and records the reason.
- Transfer never occurs from a Provider callback alone.
- Handoff never silently rewrites Operating Definition or creates a parallel Work.

RD's existing `CREATED -> SENT -> ACKNOWLEDGED` behavior is the preferred reuse baseline; naming can adapt without
creating a second Handoff system.

## 13. Review and Return

- Review is an independent judgment against declared criteria.
- Reviewer can have a real Task/Execution and Result/Evidence while original Holder remains unchanged.
- `APPROVE` returns a review Result to the Holder or allows the Router to use Default Flow.
- `REQUEST_REVISION` identifies failed criteria and target responsibility.
- Responsibility changes only if the revised Result belongs to another Assignment and the typed Return completes
  Handoff.
- Repeated revision is bounded by policy; exhaustion routes to Leader rather than an infinite loop.

## 14. Leader escalation and Decision Gate

Scope-aware chain:

```text
Employee / Role Assignment
  -> Workspace Leader Assignment
  -> Business Leader Assignment
  -> Department Leader Assignment
  -> CEO Decision Gate
```

Rules:

- resolve the lowest Scope with authority to decide;
- do not visit every level mechanically;
- skip a level only when no valid Assignment exists, authority requires a higher Scope, or policy explicitly permits;
- Leader is not a Workflow node or Employee type;
- a Decision Gate persists question, options, evidence, owner, deadline and resume action;
- while waiting, unrelated Work may continue; the gated Work preserves Holder and context;
- applying a Decision resumes the same Work/Cycle unless the Decision explicitly closes or replaces it.

## 15. Result semantics

A Result is not “Step completed”. Minimum contract:

- Work/Cycle and producing Assignment;
- Output type/schema and declared success criteria;
- status: accepted, rejected, partial, failed, unknown or awaiting external truth;
- Artifact/Evidence/External Receipt refs;
- provenance, time, version and confidence/unknown boundary;
- Problem/Need discovered;
- recommended next responsibility, treated as proposal rather than authority;
- consumer acceptance or rejection when required.

Only accepted Result satisfaction can complete a responsibility or cycle. Internal execution success cannot be
silently promoted to business success.

## 16. Context and Token strategy

### 16.1 One Work, scoped views

Keep one durable Work Context across the goal. Each Assignment sees a scoped projection rather than a copied full
history:

```text
Company/Business/Workspace Truth refs
+ pinned Operating Definition
+ current Cycle objective/state
+ current Responsibility contract
+ latest accepted Result refs
+ open Problem/Need/Decision/Handoff refs
+ only required Artifact/Evidence content
+ bounded routing summary
```

### 16.2 Reference-first rules

- Handoff and Consult contain refs plus a bounded summary, not full Conversation copies.
- Hydrate full Artifact only when the target responsibility's Input Contract requires it.
- Preserve source/version/hash so a receiver can distinguish current, stale and superseded inputs.
- Assignment-scoped Conversation reads the same Work refs but isolates unrelated Role/Scope history.
- Reuse a Provider Session when identity, Assignment, authority and task continuity remain valid; otherwise create a
  new verified Session with the same Work refs.
- Context cache is optional optimization; correctness comes from durable refs, not hidden model memory.

### 16.3 First-class cost metrics

For every Routing Decision record:

- context tokens/bytes assembled;
- number of refs and number/bytes of hydrated bodies;
- copied-history ratio;
- new Provider Task/Session: yes/no;
- resume latency;
- Consult vs Handoff count;
- Handoff acceptance latency;
- stale/missing ref count;
- Result/Evidence reuse count.

The target is not “zero handoffs”; it is the fewest responsibility transfers consistent with real accountability.

## 17. Version strategy

1. Operating Definition versions are immutable.
2. Work A pins version v3 when it starts; all Routing Decisions record v3.
3. CEO saves changes as v4; New Work defaults to v4.
4. Existing Work never silently changes Role/Responsibility relations, Input/Output contracts or default routes.
5. `Apply to running work` is explicit and requires impact preview, compatible state mapping, valid Assignments,
   Context validation and a migration event.
6. If migration cannot prove a unique safe mapping, keep v3 or stop at Leader Decision; never guess.
7. Employee availability and revoked authority are live safety facts. A pinned definition cannot force use of an
   invalid Employee; Router pauses, resolves an authorized replacement or escalates.
8. Replacing an Employee does not rewrite history. Active Holder changes only through explicit transfer/migration.

V1 UI needs only version label, “changes apply to new work”, running-work count and an explicit advanced action for
applying changes. It does not need a general migration designer.

## 18. Continuous Operating Loop

```text
Goal / Work
  -> Operating Cycle
  -> responsibility execution / collaboration / handoff
  -> accepted Cycle Result
  -> write Workspace Operating Truth
  -> Workspace Leader / policy evaluates continuation
       -> CONTINUE: open next Cycle in same Work
       -> ADJUST: create approved Definition/Rule/Staffing change, then next Cycle
       -> ESCALATE: Leader/CEO Decision Gate
       -> WAIT: preserve Work, do not create tasks
       -> COMPLETE_WORK: terminal Result and closure
```

### Task Completion vs Operating Continuation

- Task Completion: one concrete execution ended; it may produce a partial Result and does not determine Work closure.
- Responsibility Completion: current Assignment delivered an accepted contracted Result.
- Cycle Completion: Cycle Result Contract is satisfied and Result is written to Workspace Truth.
- Operating Continuation: a separate bounded decision opens another Cycle because the Goal/policy says more work is
  due.
- Work Completion: Goal/stop contract is satisfied, canceled or explicitly closed.

No automatic next task is created merely because a Task or Cycle ended. Continuation requires an explicit policy,
schedule, external event, new input or Leader decision and must respect budgets/stopping conditions.

## 19. Domain validation

### 19.1 Case A — content growth

Default Flow: `选题 → 调研 → 文案 → 视觉 → 发布`

| Scenario | Routing outcome |
| --- | --- |
| 正常自动推进 | accepted Result uses next Default Responsibility; each transfer completes Handoff |
| 视觉退回文案 | typed Return with failed criteria/evidence; 文案 ACK 后成为 Holder；修订后再到视觉 |
| 调研找 Leader 判断 | if only direction clarification: Consult Workspace Leader, 调研 remains Holder; if strategy/authority changes: Decision Gate |
| 发布出现合规问题 | stay with 发布 for local fix; Consult compliance specialist; escalate only when authority/risk threshold is crossed |
| Result 回 Leader | Cycle Result writes Workspace Truth; Workspace Leader selects continue/adjust/escalate/wait |
| 下一轮继续 | new Cycle in same Work only when policy/schedule/Leader decision authorizes it |

The linear summary remains useful, but none of these exceptions require CEO to author branches.

### 19.2 Case B — R&D

Default Flow: `产品 → 架构 → 开发 → 测试 → 发布`

| Scenario | Routing outcome |
| --- | --- |
| 开发问产品需求 | Consult Product; Developer Holder unchanged |
| 开发问架构约束 | Consult Architect; Developer Holder unchanged |
| 测试发现缺陷 | Return/Revision to Developer with criteria/evidence; transfer only on ACK |
| 开发修复后再测试 | accepted revised build follows Default/explicit Return target to QA |
| 重大架构变化 | Gate at lowest Leader with authority; CEO only if scope/risk requires |
| 小修复/重试 | stay in current Assignment and reuse Pipeline retry/capability switch; no new Handoff |

The Default Flow exists, but actual collaboration is not a fixed assembly line.

## 20. UI projection contract

### 20.1 Product terminology

- Page/section: **团队运转**
- Linear editor subsection: **默认流程**
- User explanation: “正常情况下，工作会按这个责任顺序流转；团队会根据结果、问题和需要调整。”
- Internal/audit term: Workflow Definition / Responsibility Routing

This recommendation is a Contract Candidate only. It does not rename Current Product Authority in this research
turn.

### 20.2 Main page and editor

V1 keeps a simple linear summary with light exception affordances:

```text
[选题] -> [调研] -> [文案] -> [视觉] -> [发布]    编辑默认流程
```

Node detail may edit Role, Responsibility, Employee Binding, Input and Output. Reorder changes only default priority/
sequence. Return/Review can be shown as compact relation badges or in the detail drawer. Do not show Runtime state on
the Definition surface.

No advanced Graph View is needed in V1. Add an advanced read-only diagnostic view only when support/evidence shows
that operators cannot explain actual Routing Decisions from the linear summary + event history. It must remain a
diagnostic projection, not a CEO-authored arbitrary DAG.

### 20.3 UI action -> Runtime meaning

| UI action | Runtime contract |
| --- | --- |
| 新增岗位 | create/reference Role + Responsibility Definition in a new Operating Definition version; does not invent Employee or mark executable |
| 删除岗位 | remove from new version only; block if it is sole required Leader/route or active Work lacks safe migration |
| 修改职责 | new Definition version changes responsibility matching/result contract; running Work remains pinned |
| 更换 Employee | revise scoped Assignment effective at explicit boundary; current Holder transfers/migrates, never silently swaps |
| Add node | add Responsibility Definition/reference and default relation in new version |
| Delete node | remove future default relation; preview affected running Work and gaps |
| Drag reorder | change default relation priority/order only; not mandatory runtime dependency |
| Connect | create a bounded Default/Return/Review relationship with named semantics; no generic executable edge |
| 修改 Input | update Context Assembly selector/required refs and validation contract in new version |
| 修改 Output | update Result Contract/schema/acceptance criteria in new version |
| Return | create typed Return/Revision relationship; runtime transfer occurs only when invoked and ACKed |
| Review / Retry | Review keeps Holder by default; Retry stays with current Assignment unless contract names another owner |
| 保存 | create immutable version; New Work uses it; running Work unchanged by default |

Any editable field that Router/Context/Result validation cannot consume must not appear as a functional control.

## 21. Current Runtime reuse matrix

| Current component | Mark | Decision and reason |
| --- | --- | --- |
| WorkflowRuntime | LEGACY | Mandatory sequential semantics conflict with Default Flow. Keep only as a compatibility executor while consumers migrate; never make it the Team Engine authority. |
| Orchestrator | REUSE | Reuse for sequential Tool Steps inside one Task/Assignment. Do not give it organization ownership. |
| TaskGraph | DO NOT MERGE | Keep DAG dependencies isolated inside execution planning; dependency edge must not become Responsibility edge. |
| PipelineRuntime | ADAPT | Reuse retry/switch/replan; emit typed Problem/Need/escalation Results to Router instead of owning Leader routing. |
| WorkspaceRuntime | REUSE | Preferred durable home for Work/Cycle/Holder/Handoff/Decision/Result refs; extend the shared foundation instead of creating a parallel service. |
| RD Handoff | REUSE | Proven ACK-before-transfer, Holder/Executor separation and reference-first provenance are the baseline. |
| XHS Handoff | ADAPT | Keep atomic domain transition and fail-closed behavior; replace fixed concrete `nextResponsibilityEmployeeRef` as the only routing model with versioned Responsibility resolution. |
| Decision Packet | REUSE | Already models durable wait, CEO choice and continuation; generalize owner to lowest authorized Leader without duplicating packet types. |
| Result Store | REUSE | Continue as canonical result location; add/consume Responsibility/Cycle refs rather than a second Result store. |
| Employee Execution Identity Bridge | REUSE | Preserve canonical Employee/Task/Capability/Session/callback provenance across all routed execution. |
| Capability Resolver | REUSE | Select execution capability after responsibility resolves; must not silently choose responsibility owner. |

### Retirement boundary

WorkflowRuntime becomes **CANDIDATE FOR RETIREMENT** as a public Team Operating authority only after all active
consumers are migrated and compatibility evidence exists. This research does not authorize retirement or code change.

## 22. Review criteria for the in-progress Responsibility Routing work

The later implementation Review should require:

1. It extends/reuses shared WorkspaceRuntime rather than adding another top-level Runtime or Result/Handoff store.
2. Assignment resolution consumes authoritative `Employee × Role × Scope` truth and fails closed on zero/multiple.
3. Holder and Executor remain separate; no callback or capability choice changes Holder.
4. Consult/Review preserve Holder; Handoff transfers only after ACK.
5. Default Flow is a hint with defined precedence, not mandatory sequence or arbitrary DAG.
6. Result/Problem/Need produces an auditable Routing Decision.
7. RD/XHS proven Handoff, Decision, Evidence and identity provenance are reused.
8. Work pins a Definition version; running Work never silently changes route.
9. Context is reference-first and Assignment-scoped; token/session metrics are observable.
10. Task completion does not automatically imply Cycle or Work completion/continuation.
11. Both content-growth and R&D cases pass normal, Return, Consult, Leader, Decision and recovery paths.
12. Failure/restart evidence proves no duplicate transfer, no lost Holder and no cross-scope routing.

## 23. NOT THIS

- strict sequential-only
- user-authored arbitrary DAG
- every interaction = Handoff
- every Handoff = new Issue
- every Role = new full context
- Leader as mandatory Workflow Node
- Capability Resolver choosing business accountability
- Provider callback changing Holder
- silent running-work migration
- infinite automatic task creation
- a fifth parallel Runtime

## 24. Recommendation and next gate

**Verdict:** SELECT `Work-centered Responsibility Routing Control Plane` as the single CURIS TEAM OPERATING ENGINE
model.
**Disposition:** READY FOR CEO REVIEW.
**Owner:** CEO / Product Authority owner.
**Next Action:** Review the companion Contract Candidate against the bounded Responsibility Routing implementation;
do not modify Product Authority or Runtime from this Research alone.
**Target Authority:** If accepted, update the applicable Product/Runtime Contract through a separate authorized
documentation decision.
**Next Gate:** CEO accepts/revises/rejects the Contract Candidate, then a formal Issue may authorize implementation or
Review deltas.

## 25. Stop state

CURIS TEAM OPERATING ENGINE
— RESEARCH COMPLETE
— CURRENT RUNTIMES COMPARED
— HISTORICAL FIVE-SEAT LESSONS INCORPORATED
— RESPONSIBILITY ROUTING MODEL SELECTED
— DEFAULT FLOW SEMANTICS DEFINED
— CONSULT / HANDOFF BOUNDARY DEFINED
— CONTEXT STRATEGY DEFINED
— UI PROJECTION DEFINED
— CONTRACT CANDIDATE READY
— STOP FOR CEO REVIEW
