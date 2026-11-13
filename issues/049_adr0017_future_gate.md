# ADR-0017 Future Phase Gate

Date: 2026-07-07

Owner seat: 产品规划席 (proposes) / 系统交付席 (drafts boundary)

Target approval: 总控决策席

Status: Proposed — pending 总控决策席 approval.

Source ADR: `docs/decisions/ADR-0017-multitenant-department-catalog.md`

## Objective

Approve architecture boundary definition for the ADR-0017 future phase (multi-tenant CEO model + department catalog). This gate authorizes boundary definition and staged sub-decision planning ONLY; it does NOT approve implementation. ADR-0017 is explicitly OUTSIDE the current gate (Tool System v1.8 / AI Task Executor MVP v0.1) and current forbidden scope.

## Gate Brief Summary

ADR-0017 converts the v2 blueprint's L5/L6 + multi-tenant direction into one unified, phased future-phase initiative:

- **D1 — Multi-tenant CEO model (design reservation, implementation deferred)**: each login = a CEO tenant; company = a `company_topology` manifest; reserve `tenant_id` scope on aggregates (Task / Department / Employee / Asset / EvolutionLog) so future multi-tenant is "add column + middleware inject", not rewrite. No isolation, no credential scoping, no worker propagation yet.
- **D2 — Department catalog generalization (business + functional)**: each department = a Manifest config unit; business-type (external platforms) + functional-type (HR/Admin/BI) share one Manifest seam; system maintains a department-type catalog.
- **D3 — Functional-department meta-loop & self-observability**: functional departments consume company run data to produce ROI/staffing/config/visualization, feeding CEO cockpit and Evolution Governor; upgrades ADR-0016 D3 (append-only event log) from audit nice-to-have to hard dependency.
- **D4 — Two-level governance (type vs instance)**: new department TYPE still goes gate+ADR (watchmen entry); instance-level enable/disable/config goes config+audit only, human-in-loop = the CEO.

## Allowed Scope (if approved)

- Architecture boundary definition for the ADR-0017 future phase.
- Reference to `docs/decisions/ADR-0017-multitenant-department-catalog.md`.
- Source-of-truth updates (this gate issue, the ADR status).
- Staged sub-decision planning (D1 → D2 → D3 → D4), each as its own small gate.

## Required Preservation

AI Task Executor MVP v0.1 local/demo release; Tool System v1.8 loop; Stability > Optimization > Evolution policy; Chinese operation console; Task API payload `{ content }`; existing API semantics; existing execution behavior; Evolution Governor decision policy; human-approval gate for production mutation; Project Memory source-of-truth ownership; Role Profiles / Role Context; ADR-0016 outcomes (D1 runtime role wiring / D2 Governor sandbox / D3 append-only event log).

## Forbidden Scope

Everything in the current gate forbidden list, PLUS (all are future-layer, gated by this issue): actual multi-tenant isolation / credential scoping / worker tenant_id propagation; Employee CRUD or expansion; external platform integration or credentials; L6 economic reflux / ROI computation; department implementation or company organization; new execution behavior beyond planning; automatic evolution behavior changes / automatic code self-modification without approval; business modules.

## Recommended Next

On approval: 系统交付席 defines D1 (tenant_id reservation) boundary first (lowest risk, design-only); 质量运行席 verifies; 产品规划席 accepts; then first-slice issue for D1 may be opened. D2/D3/D4 follow as separate small gates.

## Handoff

Handoff: HANDOFF_REQUIRED to 总控决策席.

Compact payload:
- Issue: `issues/049_adr0017_future_gate.md`
- Objective: Approve ADR-0017 future-phase gate (boundary definition + staged planning only; no implementation).
- Preserve: see Required Preservation.
- Allow: future-phase boundary definition + source-of-truth updates + staged sub-decision planning.
- Forbid: see Forbidden Scope (all implementation of multi-tenant/departments/ROI/external remains blocked).
