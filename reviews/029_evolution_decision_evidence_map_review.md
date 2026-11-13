# Evolution Decision Evidence Map Review

Date: 2026-07-06

Reviewer seat: 系统交付席

Source issue: `issues/033_evolution_decision_evidence_map.md`

Boundary ADR: `docs/decisions/ADR-0012-evolution-decision-evidence-reliability-boundaries.md`

## Delivery Status

Status: accepted by 产品规划席.

Implementation status: backend test coverage and evidence documentation only.

## Implementation Summary

Implemented the `Evolution Decision Evidence Map` first slice inside the accepted post-v0.1 reliability boundary.

Changes:

- Added `test_stable_execution_exposes_do_not_evolve_evidence_map`.
- Added `test_threshold_trigger_exposes_controlled_proposal_evidence_map`.
- Added `test_locked_module_postpone_exposes_risk_evidence_map`.
- Extended `test_evolution_decision_api_returns_record_for_completed_task`.
- Covered existing decision, policy, threshold, proposal, simulation, rollback, locked-module risk, API, and automatic-code-modification evidence surfaces.

No production code changes were required because the existing implementation already preserved the accepted evidence behavior.

## Scope Guard

Preserved:

- AI Task Executor MVP v0.1 local/demo release.
- Tool System v1.8 loop.
- Stability > Optimization > Evolution policy.
- Chinese operation console.
- Task API payload `{ content }`.
- Existing API semantics.
- Existing persistence schema.
- Existing Evolution Governor behavior.
- Existing architecture locking behavior.
- Existing rollback record behavior.
- Project Memory, Role Profiles, Role Context, release record/tag, and source-of-truth ownership.

Not changed:

- Backend production files under `backend/app`.
- Frontend files.
- API route shapes.
- Persistence schema.
- UI.
- External services.
- Product features.
- Execution behavior.
- Automatic evolution behavior.
- Code self-modification rules.
- Architecture mutation.
- Architecture lock semantics.
- Rollback semantics.
- Future-layer scope.

## Verification Evidence

Focused evidence-map tests:

```bash
cd backend && ./.venv/bin/python -m unittest tests.test_execution_engine.ExecutionEngineTest.test_stable_execution_exposes_do_not_evolve_evidence_map tests.test_execution_engine.ExecutionEngineTest.test_threshold_trigger_exposes_controlled_proposal_evidence_map tests.test_execution_engine.ExecutionEngineTest.test_locked_module_postpone_exposes_risk_evidence_map tests.test_execution_engine.ExecutionEngineTest.test_evolution_decision_api_returns_record_for_completed_task
```

Result: PASS, 4 tests.

Backend regression:

```bash
cd backend && ./.venv/bin/python -m unittest discover tests
```

Result: PASS, 41 tests.

Known warning:

- FastAPI emits the existing Python 3.14 deprecation warning. It remains `defer-known-gap`.

Diff hygiene:

```bash
git diff --check
```

Result: PASS.

Frontend guard:

```bash
git diff --name-only HEAD -- frontend
```

Result: PASS, no frontend diff.

Backend production guard:

```bash
git diff --name-only HEAD -- backend/app
```

Result: PASS, no backend production diff.

Scope scan:

```bash
rg -n "ROI|business module|Employee CRUD|employee expansion|company organization|department|reporting line|staffing|multi-agent|agent abstraction|external channel|dashboard|API semantic|persistence/schema|new table|new execution behavior|automatic evolution behavior|code self-modification|architecture mutation|unlocking locked modules|external service|task-role association|task evidence attachment|future-layer" backend/tests/test_execution_engine.py issues/033_evolution_decision_evidence_map.md reviews/028_evolution_decision_evidence_reliability_boundaries_review.md
```

Result: PASS. Matches are limited to issue/review preservation or forbidden-scope text; no backend test drift was found.

## Quality Verification

Reviewer seat: 质量运行席

Status: PASS.

Verified on 2026-07-06 against implementation commit `ef6baa9b`.

Fresh verification commands:

```bash
cd backend && ./.venv/bin/python -m unittest tests.test_execution_engine.ExecutionEngineTest.test_stable_execution_exposes_do_not_evolve_evidence_map tests.test_execution_engine.ExecutionEngineTest.test_threshold_trigger_exposes_controlled_proposal_evidence_map tests.test_execution_engine.ExecutionEngineTest.test_locked_module_postpone_exposes_risk_evidence_map tests.test_execution_engine.ExecutionEngineTest.test_evolution_decision_api_returns_record_for_completed_task
```

Result: PASS, 4 tests.

```bash
cd backend && ./.venv/bin/python -m unittest discover tests
```

Result: PASS, 41 tests.

```bash
git diff --check
```

Result: PASS.

```bash
git diff --name-only HEAD -- frontend
```

Result: PASS, no frontend diff.

```bash
git diff --name-only HEAD -- backend/app
```

Result: PASS, no backend production diff.

```bash
rg -n "ROI|business module|Employee CRUD|employee expansion|company organization|department|reporting line|staffing|multi-agent|agent abstraction|external channel|dashboard|API semantic|persistence/schema|new table|new execution behavior|automatic evolution behavior|code self-modification|architecture mutation|unlocking locked modules|external service|task-role association|task evidence attachment|future-layer" backend/tests/test_execution_engine.py issues/033_evolution_decision_evidence_map.md reviews/029_evolution_decision_evidence_map_review.md
```

Result: PASS. Matches are limited to issue/review preservation, forbidden-scope, or verification-command text; no backend implementation drift was found.

Known warning:

- FastAPI emits the existing Python 3.14 deprecation warning. It remains `defer-known-gap`.

Quality conclusion:

- Stable do-not-evolve evidence map is covered.
- Threshold-triggered controlled proposal, simulation, and rollback evidence map is covered.
- Locked-module postpone risk evidence map is covered.
- Evolution-decision API evidence is covered.
- Backend production code remains unchanged.
- Frontend remains unchanged.
- API semantics, persistence schema, Evolution Governor behavior, architecture locking behavior, rollback behavior, automatic-evolution behavior, code self-modification rules, architecture mutation boundary, and future-layer boundaries remain preserved.
- No blockers found.

## Product Acceptance

Reviewer seat: 产品规划席

Decision: APPROVED on 2026-07-06.

Rationale:

- The slice improves confidence in existing Evolution Governor decision evidence without changing evolution behavior.
- Quality verification proves stable do-not-evolve, threshold-triggered controlled proposal, locked-module postpone, simulation, rollback, and API evidence.
- The implementation changed backend tests and evidence documentation only; backend production code, frontend, API semantics, persistence schema, Evolution Governor behavior, automatic-evolution behavior, code self-modification rules, architecture mutation boundary, and future-layer boundaries remain preserved.

Accepted scope:

- Backend evidence-map coverage for stable do-not-evolve decisions.
- Backend evidence-map coverage for threshold-triggered controlled proposal, simulation, and rollback records.
- Backend evidence-map coverage for locked-module postpone risk.
- Evolution-decision API evidence coverage.
- Source-of-truth updates for verified evidence.

Still blocked:

- API semantic changes.
- Persistence/schema/new table changes.
- UI changes.
- New execution behavior.
- Automatic evolution behavior changes.
- Code self-modification.
- Architecture mutation.
- Unlocking locked modules.
- External services or new model-provider integrations.
- ROI/economy, business modules, Employee CRUD/expansion, company organization, multi-agent routing, agent abstraction, and future-layer implementation.

Next product move:

- Open a bounded closeout gate for the post-v0.1 Execution Reliability phase.

## Handoff

Handoff: accepted by 产品规划席; main thread closeout complete.

Target seat: 总控决策席 for the reliability closeout gate.

Compact payload:

Issue: T-107 / Review post-v0.1 Execution Reliability closeout gate

Objective: Decide whether to approve closeout review planning for the post-v0.1 Execution Reliability phase.

Special Constraints: Run Evidence Reliability, Workflow Error/Fallback Evidence Map, and Evolution Decision Evidence Map are accepted. New gate is closeout planning only for post-v0.1 Execution Reliability. Preserve AI Task Executor MVP v0.1 local/demo release, Tool System v1.8 loop, Stability > Optimization > Evolution policy, Chinese operation console, Task API `{ content }`, existing API semantics, existing persistence schema, Project Memory, Role Profiles, Role Context, release record/tag, and source-of-truth ownership. No implementation, API semantic change, persistence/schema change, UI change, external service, new product feature, new execution behavior, automatic evolution behavior change, or future-layer scope.

Next Seat: 系统交付席 if approved; main thread/product revision if rejected.
