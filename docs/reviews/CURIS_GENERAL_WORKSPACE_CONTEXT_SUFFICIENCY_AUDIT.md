# CURIS GENERAL WORKSPACE CONTEXT SUFFICIENCY AUDIT

Status: Review

Authority Class: REVIEW / EVIDENCE

Date: 2026-08-27

Scope: M2.5 read-only audit; no implementation, schema, test, Runtime or active-database change.

## 1. Real WAITING case

Evidence database: repository-external `/tmp/curis-canonical-usage-attribution.YtLWJY/live-codex/live.sqlite`.

The accepted M2 proof created one canonical General Workspace execution with no Project:

`Business → Workspace → Cycle → Work → Responsibility → Employee → Capability → ResultStore Task → real codex-cli`

Observed identities:

- Business: `客户反馈业务`, goal `形成一个可验证改进`.
- Workspace: `客户反馈办公室`, `GENERIC`, canonical relation `RESOLVED`.
- Cycle: `cycle-b95219dcea4f77078fdee9518deb45c5`.
- Work: `work-a32669c8a6ad0824b1474002f5549a55`.
- Employee: `小策 / 业务负责人`.
- Provider task: `3a50ab27-1fbe-4ef0-9c2f-b2db807741f8`.
- Provider: real installed `codex-cli 0.144.6`.

The Provider process completed successfully, so the ResultStore Task is `COMPLETED`. The returned business result was `REJECTED`; Responsibility Routing correctly cleared Current Executor and left the Work route `WAITING`. These are not contradictory states: transport/execution completed, while the requested business result was not accepted.

Provider reason, preserved in Task output and Artifact:

> 缺少具体业务问题、目标、输入事实或验收标准；当前上下文仅包含任务标识，无法在不伪造事实的情况下执行。

No fake business completion was produced.

## 2. Exact Provider input

The persisted Task content and Provider prompt contained:

```text
工作目标：work-a32669c8a6ad0824b1474002f5549a55
当前责任：推进当前业务问题并返回可验证结果
所需输入引用：[]
输出结果类型：general-business-result
上下文引用：["work-a32669c8a6ad0824b1474002f5549a55"]
补充说明：推进当前业务问题并返回可验证结果
```

The existing Context Package then repeated this Task content, added the capability `agent.general.local`, generic isolation constraints, and reported no relevant Memory or Knowledge.

The Provider did **not** receive:

- Business name or goal;
- Workspace name, purpose or state;
- Cycle contract `problem`;
- Cycle contract `expectedResult`;
- Cycle contract constraints;
- the actual source facts needed to summarize customer feedback;
- an acceptance criterion more precise than the generic result type.

## 3. Exact missing facts

The Provider's own output identifies four missing categories. Current persisted truth separates them as follows:

1. **Specific business problem** — already persisted in the Cycle contract; not propagated.
2. **Goal / expected result** — Business goal and Cycle `expectedResult` already persisted; not propagated.
3. **Input facts** — no customer-feedback source was supplied in the real case; genuinely missing.
4. **Acceptance standard** — `expectedResult` exists and should be propagated, but no separate formal acceptance criteria are captured by the General Work command.

The correct post-fix outcome for this exact Work may still be `WAITING`, because the customer-feedback facts genuinely do not exist. The improvement is that Curis can state the exact missing input and recovery path instead of presenting only a generic rejected result.

## 4. Context source map

| Context item | Current source | Current truth |
|---|---|---|
| Business identity/name | `canonical_businesses` | EXISTS + NOT PROPAGATED |
| Business goal | `canonical_businesses.goal` | EXISTS + NOT PROPAGATED |
| Business positioning | `canonical_businesses.positioning` | Schema exists; empty in real case; GENUINELY MISSING |
| Company identity/name | `companies` | EXISTS + NOT PROPAGATED |
| Workspace identity/name/state | `workspaces` | EXISTS + attribution propagated, semantic content NOT PROPAGATED |
| Workspace purpose/goal | M1 `blueprint_json.goal / intentSummary` when materialized through FirstRunDelivery | EXISTS IN ACCEPTED M1 PATH + NOT PROPAGATED; absent from this seeded proof Workspace |
| Work problem | parent Cycle `data.contract.problem` | EXISTS + NOT PROPAGATED |
| Expected result | parent Cycle `data.contract.expectedResult` | EXISTS + NOT PROPAGATED |
| Constraints | parent Cycle `data.contract.constraints` | EXISTS + NOT PROPAGATED |
| Input references | Cycle contract and Work `inputRefs` | EXISTS as refs + NOT PROPAGATED by Team prompt; empty in real case |
| Formal acceptance criteria | no GeneralWork input field; Work has only later `acceptanceRefs` | NOT CAPTURED |
| Why this Work exists | Work problem + Business goal | EXISTS + NOT PROPAGATED |
| Responsibility | persisted Assignment | EXISTS + PROPAGATED |
| Employee identity/name/role | Runtime Employee bridge and `employee_instances` | Identity used for trust/callback; user-readable identity NOT PROPAGATED to prompt |
| Capability | binding and RuntimeCapabilityContext | EXISTS + PROPAGATED |
| Computer Access truth | Provider/session evidence | EXISTS for applicable providers; not required by this business-only Work |
| Prior Result/Artifact/Evidence refs | Responsibility Routing | EXISTS WHEN AVAILABLE + refs selected; bodies NOT HYDRATED |
| Conversation history | not copied by this execution | NOT REQUIRED by default; correctly bounded |
| Relevant Memory | existing `ContextService` retrieval | Available but Project/Employee-oriented; none selected in real case |
| Relevant Knowledge | existing `ContextService` retrieval | Company/Department/Project-oriented; no Workspace/Business-scoped selection in this case |

## 5. Where context was lost

The primary loss is deterministic and occurs before ResultStore Task creation:

1. `GeneralWorkspaceDelivery.create_work()` persists `problem`, `expectedResult`, `constraints` and `references` in the parent Cycle contract (`backend/app/runtime/general_workspace_delivery.py:109-144`; `backend/app/runtime/child_work.py:246-315`).
2. The child Work stores its Cycle parent and input refs, but does not duplicate the Cycle contract. This is acceptable; the Cycle remains the source of truth.
3. `run_assignment()` reads only the Work body and formats `work.data.goal || work.data.outcomeRef || work_ref` (`backend/app/api/team_operating_router.py:200-227`). A canonical child Work has neither `goal` nor `outcomeRef`, so the UUID becomes the goal.
4. The same function takes required input refs from the Assignment `inputContract`, not from the Work/Cycle contract. The real Assignment has no required refs, so `[]` is sent.
5. `ResponsibilityRoutingRuntime.build_execution_context()` correctly produces a bounded reference-first package, but the caller supplies only the Work ref and a responsibility summary. It does not hydrate the parent Cycle contract or canonical Business/Workspace facts (`backend/app/runtime/responsibility_routing.py:376-405`).
6. `execute_runtime_business()` persists exactly the supplied prompt as Task content (`backend/app/main.py:4811-4901`).
7. `ContextService` builds a bounded package from that Task content. It cannot recover facts that were omitted before Task creation (`backend/app/context_service.py:36-99`).
8. `PromptBuilder` faithfully sends Task content plus the bounded package. The Provider therefore receives the UUID-centric prompt (`backend/app/prompt_builder.py:6-38`).

This is chiefly a **PROPAGATION GAP**, not a missing architecture or Provider failure.

## 6. Capture gaps

### First Run

The accepted headless M1 materialization contract can capture normalized `goal`, `positioning` and `intent_summary`; it persists goal/positioning in canonical Business and goal/intent summary in Workspace blueprint (`backend/app/runtime/first_run_delivery.py:15-28, 92-114`).

The current onboarding page, however, does not call `materialize-first-general-workspace`. It accepts a natural-language `intent`, creates only an opaque generated `intent_ref`, and then calls `materialize-company`; the text is not sent to Runtime (`frontend/app/onboarding/page.js:57-80, 108-129`; `frontend/lib/runtimeApi.js:261-274`). The page explicitly says the raw description is not persisted. Therefore:

- normalized First Run intent **can** be captured by the accepted backend path;
- the current onboarding adapter does **not** propagate the user's expressed text into that path;
- the original narrative is NOT CAPTURED; only an opaque ref is durable.

This is a bounded existing-path integration gap, not justification for CompanyProposalV2 or another context store.

### General Work

The General Work API captures problem, expected result, constraints and references. It does not separately capture:

- explicit acceptance criteria;
- the business reason beyond the problem text;
- ownership/meaning of each opaque reference.

For the first correction, `expected_result` can serve as the minimum result/acceptance statement. A new acceptance model is not required unless Product later needs criteria distinct from expected result.

## 7. Propagation gaps

- Cycle contract is not hydrated by Team Operating before Provider Task creation.
- Business and Workspace semantic facts are available through canonical persistence/parent resolution but absent from execution content.
- Work `inputRefs` are ignored; Assignment required refs are used instead.
- Employee name/role is retained for execution provenance but not included in the bounded business context.
- Existing result/artifact/evidence refs are collected, but no selected bodies are hydrated; this is honest reference-first behavior, although it limits tasks that require prior content.
- The Provider's structured `problem` is preserved in Task output/Artifact but not copied into the Work execution record; the Work surface can therefore expose only generic WAITING activity without resolving the exact missing fact cheaply.

## 8. Selection / scope gaps

- `ContextService` is bounded (`MAX_MEMORY=5`, `MAX_KNOWLEDGE=3`, prompt cap 12 KiB) and reusable.
- Memory selection is user/Project/Employee scoped. A General Workspace with no Project receives user/Employee candidates, not Workspace/Business memory.
- Knowledge selection supports Company/Department/Project. With no Project, current lookup does not derive Department from canonical Workspace; only company-global entries can naturally qualify.
- References are kept reference-first, but there is no shared resolver in this path that selects and hydrates only the refs required by the current Work.

These are real selection limits. They did not cause the observed omission of problem/expected result—the earlier Team prompt assembly did—but they matter for later source-backed General or Content Growth Work.

## 9. Genuine missing facts

For the real case, no customer feedback, source document, previous Result, Artifact, Evidence or Knowledge entry was supplied. Curis cannot summarize “current customer feedback” from a Work identifier alone.

Valid recovery sources are existing mechanisms:

- user/CEO supplies a source reference or manual input;
- an Employee performs bounded Research if authorized and capable;
- Capability Discovery supplies a missing connector/tool;
- a real Result/Artifact/Evidence ref from prior Work is attached;
- a CEO Decision is requested only when an actual business choice—not missing raw facts—requires CEO authority.

This fact gap must not be filled by prompt invention.

## 10. Existing reusable Context mechanisms

No new Context system is needed for the bounded correction:

- canonical Workspace parent resolver and Business read model;
- Cycle contract and Work parent relation;
- Work `inputRefs` and Responsibility Routing `truthRefs`;
- existing `ContextService` bounded package;
- existing PromptBuilder;
- ResultStore Task/Artifact and usage evidence;
- Result/Artifact/Evidence references already held by Responsibility Routing;
- existing Memory and Knowledge services where their current scope is applicable;
- existing WAITING route with Holder retained and Current Executor cleared.

The existing mechanisms already enforce reference-first context, bounded text and no copied conversation history.

## 11. Minimal correction

### Runtime propagation

1. In the existing Team Operating execution adapter, resolve the Work's parent Cycle and require a valid `GENERAL_WORK_CYCLE` contract.
2. Build one bounded Task content block from existing truth only:
   - Business/Workspace name and goal/purpose;
   - Cycle problem and expected result;
   - Cycle constraints;
   - Work input refs plus already-selected Result/Artifact/Evidence refs;
   - current Employee role/responsibility and output contract.
3. Keep refs reference-first. Do not hydrate arbitrary histories or all Workspace data.
4. Persist the Provider's structured rejection `problem` in the existing execution record so WAITING can explain missing facts and recovery without parsing the full Artifact.
5. If the required source ref/body is absent, retain WAITING and report the real missing fact. Do not convert it to success.

### First Run capture

Wire the existing First Run adapter to the already implemented `materialize-first-general-workspace` path so normalized goal, positioning and intent summary reach canonical Business/Workspace persistence. Do not add a second Proposal or Context object and do not persist secrets.

## 12. Required tests

1. General Work contract reaches Provider Task content: problem, expected result and constraints exactly once.
2. Canonical Business/Workspace identity and goal are included, with no Project requirement.
3. Work input refs are included; cross-tenant/company/work refs are rejected.
4. Context remains bounded; whole conversation/history is absent.
5. Existing result/artifact/evidence refs remain reference-first and duplicate-safe.
6. Real missing input produces `REJECTED → Work WAITING`, exact reason retained, Current Executor cleared, Holder retained.
7. Supplying the missing source and retrying the same Work uses the updated bounded context without a duplicate active execution.
8. Restart preserves the same Cycle contract, Task context evidence, WAITING reason and refs.
9. Existing RD prompt/file/test context remains unchanged.
10. Existing Team Operating, Handoff/P7, ContextService and canonical usage attribution regressions pass.
11. First Run accepted API path persists normalized goal/positioning/intent summary; current UI integration is separately verified when authorized.

## 13. Exact implementation scope candidate

### M2.5A — headless propagation and WAITING recovery truth

- `backend/app/api/team_operating_router.py`
- `backend/app/runtime/responsibility_routing.py` — existing execution record only; no new state/primitive
- `backend/tests/test_v1_general_operating_contract.py`
- `backend/tests/test_canonical_usage_attribution.py`
- existing Team Operating/RD tests as run-only regression

No database or schema file is required. If implementation proves otherwise, stop and amend the Issue.

### M2.5B — existing First Run capture wiring

This is an existing-adapter integration item and should be separately bounded because the current M2.5 Epic is UI-independent:

- `frontend/lib/runtimeApi.js`
- `frontend/app/onboarding/page.js`
- existing First Run frontend test file, if present; otherwise one focused test beside the current onboarding tests
- `backend/tests/test_v1_first_run_delivery.py` as run-only contract proof

The backend FirstRunDelivery and materialization API already persist the normalized fields; no new backend object or schema is justified by current evidence.

## 14. RD regression considerations

RD succeeds more often because its existing execution binding explicitly requires and injects:

- active Project scope;
- concrete instruction;
- bounded resource/file refs;
- allowed working directory;
- test command;
- expected file change and Artifact/Evidence production.

`backend/app/main.py:5151-5252` constructs this bounded, executable context before Codex launch. General Workspace should reuse the principle—specific Work intent, expected result, bounded refs and verification truth—not the RD Project model, filesystem fields or test-command contract.

The M2.5 correction must not alter the `rd_task:auto` branch, RD Project attribution, computer-access truth or Artifact Review semantics.

## 15. Content Growth compatibility

The same existing shared contract can support future Research, Content and Evaluation Work if each Domain persists its specific Work contract and passes only:

- canonical Business/Workspace goal;
- current Domain object ref;
- Work problem and expected result;
- bounded source/evidence/previous-result refs;
- current responsibility and capability boundary.

Content Growth still needs its own Domain objects and real source capabilities, but it does not need a second Prompt, Memory or Context system. Channel data that does not exist must remain missing/unknown rather than being synthesized.

## Final decision

**CONTEXT CAPTURE + PROPAGATION FIX REQUIRED**

Reason:

- the real M2 execution is primarily blocked by a bounded propagation defect: persisted Cycle and canonical Business/Workspace truth was omitted before Task creation;
- the current onboarding adapter also accepts a user intent that is not carried into the already implemented normalized First Run materialization path;
- the real customer-feedback data remains genuinely missing and should continue to produce a precise WAITING result until supplied or researched.

This finding does not require a new architecture, Context system, Memory system, Knowledge system, Prompt framework, Runtime primitive, state enum or Project.

STOP FOR CEO M2.5 CONTEXT REVIEW.
