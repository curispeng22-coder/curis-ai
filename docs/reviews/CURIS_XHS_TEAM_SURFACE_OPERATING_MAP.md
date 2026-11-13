# CURIS XHS — TEAM × SURFACE OPERATING MAP

**Authority Class:** RESEARCH

**Status:** Review

**Disposition:** CEO REVIEW REQUIRED

**Date:** 2026-08-21

**Case status:** CANDIDATE EXAMPLE ONLY

**Authority Effect:** NONE

> This map applies the Team × Surface candidate to one example. It does not freeze Surface taxonomy, responsibilities, Employee names, headcount, workflow, Package, or implementation.

## 1. Example identity

```text
Company
└─ Department: 内容增长部
   └─ Business: 小红书运营
      └─ Workspace: AI 科技
         ├─ one Workspace Operating Team responsibility boundary
         └─ multiple Professional Surfaces
```

The Operating Team has one Workspace Leader / Operating Owner Assignment and the minimum responsibility coverage needed by the current operating plan. One Employee may carry several responsibilities; shared Employees may serve other Workspaces through separate scoped Assignments.

## 2. Candidate operating chain

```text
Research & Insight
  → Content Operating
  → Performance & Growth
  → Feedback
  ↘ Commercialization (optional)
  → Workspace Leader Review
  → current Cycle Decision
```

Operating Overview, Team, and Knowledge may exist as shared/scoped projections. Calendar remains a view inside Content Operating. None of them owns execution.

## 3. Research & Insight Surface

| Item | Candidate mapping |
|---|---|
| Responsibility requirements | market/audience signal research; competitor/trend/keyword analysis; insight synthesis; hypothesis formation |
| Possible Employees | Workspace Leader or any existing research/strategy-capable Employee with a valid Workspace Assignment |
| Work in | Workspace Goal/Strategy, current Cycle plan, Brand Brief, prior Growth Signals, Comment Insights, external source refs |
| Result out | Research Result, Insight, evidence-backed Topic/Hypothesis candidates, source/evidence refs |
| Handoff / collaboration | Consult subject specialist without changing Holder; transfer only when content strategy must own the next Result |
| Leader review | Material audience/positioning change, weak evidence, strategic contradiction, or proposed Strategy Envelope change |

Presence rule: show the responsible research Holder when real Work exists; do not populate a decorative researcher roster.

## 4. Content Operating Surface

| Item | Candidate mapping |
|---|---|
| Responsibility requirements | content strategy/topic selection; Note production; brand/compliance review; publishing preparation; authorized publishing |
| Possible Employees | Existing strategy, writing/creative, review/compliance, or publishing-capable Employees; one Employee may carry more than one responsibility |
| Work in | Accepted Research Result, Topic/Hypothesis, Brand Brief, prior performance, approved Cycle plan |
| Result out | Note/version, review outcome, approved publishing package, publishing receipt/Result, Artifact refs |
| Handoff / collaboration | Strategy→production→review→publishing only when accountability changes; revision stays with same Holder when responsibility is unchanged |
| Leader review | Material brand risk, policy/compliance uncertainty, external commitment, strategy change, repeated quality failure |

Calendar and Publishing Queue are projections of Note × time/status. They are not separate Work or Runtime systems.

## 5. Performance & Growth Surface

| Item | Candidate mapping |
|---|---|
| Responsibility requirements | performance ingestion/validation; experiment evaluation; growth diagnosis; next-action recommendation |
| Possible Employees | Existing analytics/growth-capable Employee or Leader with a scoped Assignment |
| Work in | Publishing Result, Performance Records, Experiment refs, Comment Insights, Cycle success/evidence contract |
| Result out | Growth Signal, Evaluation, evidence strength, bounded optimization proposal |
| Handoff / collaboration | Return evidence-backed insight to content strategy; consult Research for ambiguity; escalate material strategy/budget change |
| Leader review | Evaluation sufficiency, strategy continuation/adjustment, risk, resource priority, next-cycle proposal |

The same publishing Result and Evidence may project in Content and Growth without duplication.

## 6. Feedback Surface

| Item | Candidate mapping |
|---|---|
| Responsibility requirements | comment/DM classification; user-question response preparation; sentiment/risk/lead detection; feedback synthesis |
| Possible Employees | Existing community/feedback/support-capable Employee; compliance or Leader involvement only when required |
| Work in | Comment/DM/User Question refs from official or compliant channels; Note and Account context |
| Result out | Response candidate/record, Comment Insight, risk flag, research signal, commercial lead |
| Handoff / collaboration | Feedback→Research for recurring insight; Feedback→Content for revision/topic; Feedback→Commercial for qualified lead; escalate risk to Leader |
| Leader review | Reputational risk, policy issue, high-value opportunity, material audience shift, unresolved response boundary |

Feedback may remain a lightweight independent Surface or a scoped view under Insight. That UI choice does not change responsibility truth.

## 7. Commercialization Surface — optional

| Item | Candidate mapping |
|---|---|
| Responsibility requirements | opportunity qualification; offer/proposal; brand fit/compliance; delivery coordination; settlement/finance linkage |
| Possible Employees | Authorized commercial-capable Employee, Workspace Leader, or shared specialist with scoped Assignment |
| Work in | Qualified Feedback lead, performance evidence, Brand Brief, commercial policy, approval constraints |
| Result out | Brand Deal/lead state, proposal, approval/commitment record, delivery Result, settlement Evidence refs |
| Handoff / collaboration | Commercial→Content for deliverables; consult compliance/finance; Leader/CEO gate for material or irreversible external commitments |
| Leader review | Brand fit, price/terms, resource conflict, protected strategy/budget boundary, external commitment |

Commercialization should remain hidden when the Workspace stage does not require it. Optional visibility does not create or delete the underlying Team.

## 8. Leader review across Surfaces

The Workspace Leader has one continuous responsibility projection across the Workspace:

| Surface | Leader attention, not routine dispatch |
|---|---|
| Research | evidence weakness, positioning/strategy implication |
| Content | plan coherence, material brand/compliance risk, repeated quality exception |
| Growth | evaluation sufficiency, continue/adjust/wait/escalate proposal |
| Feedback | reputation/risk/escalation and material customer insight |
| Commercial | external commitment, budget, terms, brand fit, delivery risk |

Ordinary WHO routing remains automatic. Leader attention is triggered by real result, exception, unresolved requirement, or decision need—not by visiting a Surface.

## 9. Example one-Cycle trace

```text
Cycle: AI 科技 / observation window N

Work R — research responsibility
  Result: evidence-backed Topic/Hypothesis set
  → projected in Research and Content

Work C — content strategy/production/review/publishing responsibilities
  Results: accepted Note + publishing receipt
  → projected in Content, Growth, and Feedback

Work G — growth/evaluation responsibility
  Result: Growth Signal + Evaluation
  → projected in Growth and Operating Overview

Work F — feedback responsibility (may run in parallel after publishing)
  Result: Comment Insight / risk / lead
  → projected in Feedback, Research, Content, optional Commercial

Leader Review
  → current Decision: CONTINUE / ADJUST / WAIT / ESCALATE / PAUSE / STOP
```

This trace is a candidate operating map, not accepted XHS Runtime evidence. Work R/C/G/F may be one continuous Work or several linked Work items depending on objective and Result contracts. Handoff occurs only on accountability transfer.

## 10. Employee presence examples

| Situation | What the Surface may show |
|---|---|
| Research Result already complete | Result owner/history; no active Executor |
| Content Work waiting for review | Current Holder, review collaborator/request, concise wait reason |
| Publishing task executing | Holder plus verified Current Executor; never infer from open UI |
| Growth reads publishing Result | Relevant analytics responsibility; publishing Employee need not appear as active |
| Feedback produces a commercial lead | Feedback Holder; optional pending Handoff target after valid transfer |
| CEO opens Team | Workspace Leader, scoped responsibility coverage, unresolved gaps, active material Work |

## 11. One Employee across Surfaces

Candidate example without freezing identity:

```text
Employee E
├─ Assignment A: content strategy @ AI 科技
├─ Assignment B: performance evaluation @ AI 科技
└─ optional Assignment C: Workspace Leader @ AI 科技
```

Employee E may appear in Content, Growth, and Overview because the Assignments/Work are relevant. There is still one Employee identity, one shared Workstation, and isolated context per Assignment/Work.

## 12. Context package example

When a Growth projection opens the responsible Employee Workstation, the bounded context may include:

- Company/Department/Business/Workspace refs;
- Employee + performance-evaluation Assignment;
- current Cycle and Growth Work refs;
- Publishing Result, Performance Record, Experiment, and Evidence refs;
- approved Goal/Strategy/Success Contract refs;
- source Surface = Performance & Growth and return target.

It must not preload unrelated Workspace conversations, every XHS account, all Research history, or another Surface's full state.

## 13. Candidate gaps

| Gap | Classification |
|---|---|
| Exact XHS responsibility vocabulary and coverage | RESEARCH / CANDIDATE |
| Named Employees and headcount | Intentionally not frozen |
| Surface → responsibility requirement declaration | PACKAGE DECLARATION GAP |
| Work/Result/Evidence projection rules | PACKAGE DECLARATION GAP |
| Cross-Surface Employee presence and shared Workstation entry | UI PROJECTION GAP |
| Autonomous Plan→XHS ContentItem/Result bridge | PARTIAL / IMPLEMENTATION GAP from current review evidence |
| Publishing and analytics providers | PARTIAL / dynamic external capability boundary |
| Cross-Surface XHS E2E | MISSING ACCEPTANCE EVIDENCE |
| Surface Runtime | **NOT REQUIRED** |

## 14. Review stop

This candidate stops for CEO Review. It does not authorize headcount, Employee naming, Operating Definition acceptance, Package changes, UI redesign, Runtime work, schema/database changes, prototype changes, implementation, commit, or push.
