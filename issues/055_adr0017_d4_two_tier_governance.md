# Issue 055 — ADR-0017 D4: 两级治理（Two-Tier Governance）（设计预留 / Reservation）

- **Owner seat**: 系统交付席
- **Status**: Boundary (ADR-0025) → gate pre-authorized (主理人, 2026-07-08) → **ACCEPTED (boundary, 主理人齐活林, 2026-07-08, reviews/057)** → GATE APPROVED (D4 reservation, ADR-0017 option-a pre-authorized roadmap) → 系统交付席 implementation (T01–T04) → 质量运行席 implementation verification (reviews/058 PASS-WITH-NOTES, 100 tests) → **ACCEPTED (slice CLOSED, 主理人齐活林, 2026-07-08, 产品规划席 delegation)**
- **Source gate**: `issues/050_adr0017_future_gate_submission_package.md` option a (accepted by 总控决策席, 2026-07-07)
- **Boundary**: `docs/decisions/ADR-0025-d4-two-tier-governance-boundaries.md`

## Minimal Context

ADR-0017 future phase gate is OPEN (option a). D1 (`tenant_id` reservation) ACCEPTED (ADR-0022, 69 tests green). D2 (部门目录通用化 reservation) CLOSED (ADR-0023 + issue 052, 81 tests green, Kou c8a30781, Yan reviews/053 PASS-WITH-NOTES). D3 (职能型部门自可观测 reservation) CLOSED (ADR-0024 + issue 054, 90 tests green, 零 schema 增量, Kou 22c5cd55, Yan reviews/055 PASS-WITH-NOTES). D4 is the fourth (last) sub-decision: **两级治理（Two-Tier Governance）** — split governance into (①) CEO-level (config + audit within own `CompanyTopology`: enable/disable department type, adjust quality lines, select/unselect plugins, view governance audit, but scoped strictly to own company, must not touch other CEOs' topology, must not touch system-level `department_types` add/remove, must not lift human-approval gate, must not auto-modify code) and (②) platform/system-level (retains governance over `department_types` add/remove, cross-company policy, global guardrails — this reservation only reserves the existence/seam, does NOT implement a platform admin backend). Because two-tier governance is an L5 concept (forbidden zone under the current gate), D4 can only be a **design-only reservation** today — mirroring D1/D2/D3's "read-only facade + scope-boundary + invariant" zero-behavior-change approach. This slice reserves a read-only scope wrapper (`GovernanceScope`) + a restricted-proposal facade (`CompanyGovernance`: `get_governance_scope` / `list_company_departments` / `propose_department_toggle` / `list_governance_audit`), reusing D2 `DepartmentCatalog.assemble_company_topology` (`CompanyTopology` as the CEO-level scope boundary) and ADR-0016 D3 `evolution_events` (audit read-only projection seam). It does **not** persist any governance state, lift any gate, auto-modify code, instantiate departments, or connect external platforms. Real D4 implementation requires its own future small gate(s) + 总控决策席 + 安全边界席 review.

> ⚠️ **与 D2/D3 的衔接**：本 reservation 直接复用 D2 的 `CompanyTopology`（`assemble_company_topology` 内存投影，不持久化）作为 CEO 级治理作用域边界，复用 ADR-0016 D3 的 `evolution_events` 作为治理审计只读接缝（不新增写）。`database.py` 零改动、零 schema 增量，与 D3 同构、完全可逆。

## Scope

- New module `backend/app/governance.py`: read-only scope wrapper `GovernanceScope` (wraps D2 `CompanyTopology` + `locked_actions` + `selectable_type_keys` read-only list) + restricted-proposal facade `CompanyGovernance` with `get_governance_scope(ceo_id, selected_type_keys)`, `list_company_departments(ceo_id, selected_type_keys)`, `propose_department_toggle(ceo_id, type_key, enabled, selected_type_keys)`, `list_governance_audit(ceo_id, limit=50)`; plus `DepartmentGovernanceView` / `GovernanceProposal` dataclasses. Future hooks `apply_proposal(...)` / `manage_department_types(...)` declared as signature-only placeholders (`raise NotImplementedError`).
- `get_governance_scope(ceo_id, selected_type_keys)`: wraps `DepartmentCatalog.assemble_company_topology(ceo_id, selected_type_keys)` into `GovernanceScope`; `locked_actions` declares platform-level/gate-lift locked actions; `selectable_type_keys` is the full system catalog key list from `DepartmentCatalog.list_types()` (read-only). No persistence, no tenant write.
- `list_company_departments(ceo_id, selected_type_keys)`: projects `CompanyTopology.manifests` into `DepartmentGovernanceView` list; each view `requires_human_approval=True` (gate not lifted); `quality_lines` only placeholder structure (not consumed).
- `propose_department_toggle(ceo_id, type_key, enabled, selected_type_keys)`: validates `type_key` exists via `DepartmentCatalog.get_manifest(type_key)` (index role; `KeyError` if unknown), then constructs a `GovernanceProposal` (`status='proposed'`, `requires_human_approval=True`) — **no persistence, no `EvolutionEventLog.record` call, no gate lift, no `department_types` write**.
- `list_governance_audit(ceo_id, limit)`: read-only projection of `EvolutionEventLog.get_all()` filtered by `event_type` prefix `'governance.'`, truncated to `limit`. No new write (D3 append-only invariant preserved).
- Scope-boundary reuse: `DepartmentCatalog` (D2) for `CompanyTopology` assembly + `type_key` validation; `EvolutionEventLog` (ADR-0016 D3) for audit read-only projection. Injected via constructor (`database`).
- Tests in `backend/tests/test_d4_governance.py`.

## Non-goals

- No platform-level admin backend, no cross-company policy engine: `manage_department_types` is only a future hook; `department_types` add/remove is platform-level and NOT implemented/written in this reservation (seam only).
- No lifting of human-approval gate, no lifting of auto-code-modification ban, no auto code modification: every change `requires_human_approval=True`; `apply_proposal` is future hook only.
- No real department instantiation, no `departments` / `companies` / `company_topology` table; `CompanyTopology` remains in-memory projection only (consistent with D2).
- No external platform integration, no credentials, no compliance surface (安全边界席 territory).
- No L6 economy/ROI, no token-output-ratio.
- No Employee CRUD, no L2/L5 employee layer, no role/skill config fact interface; `employee_role_spec` only a placeholder contract field, not consumed.
- No new write path: event log keeps ADR-0016 append-only invariant; D4 is read-only/proposal (`propose_department_toggle` does not call `record`).
- No new API endpoint, no read/write semantic changes, no breakage of existing 90 tests.
- No multi-agent, agent abstraction, complex UI/dashboard, vector DB, embeddings, external memory.
- No touch of D1 `TenantContext` invariant (single-tenant sentinel `'default'`).
- No touch of system-level `department_types` add/remove (i.e. no write to that table); no pre-emptive unneeded structures outside `database.py`.

## Allowed files

- `backend/app/governance.py` (new)
- `backend/tests/test_d4_governance.py` (new)
- `docs/decisions/ADR-0025-d4-two-tier-governance-boundaries.md` (this slice's boundary)
- `issues/055_adr0017_d4_two_tier_governance.md` (this issue)

> 注：`backend/app/database.py` **不在允许文件内** —— 本 reservation 零 schema 增量（`department_types` 与 `evolution_events` 均已存在），完全可逆（与 D3 同构）。

## Acceptance criteria

1. `backend/app/governance.py` declares `CompanyGovernance` with `get_governance_scope` / `list_company_departments` / `propose_department_toggle` / `list_governance_audit` methods and `apply_proposal` / `manage_department_types` future hook placeholders; plus `GovernanceScope` / `DepartmentGovernanceView` / `GovernanceProposal` dataclasses.
2. `get_governance_scope(ceo_id, ["business.general","function.hr"])` returns `GovernanceScope` whose `topology` is the D2 in-memory `CompanyTopology` (not persisted), `locked_actions` is non-empty (declares `manage_department_types` / `lift_human_approval_gate` / `auto_modify_code` / `cross_company_policy`), `selectable_type_keys` equals `DepartmentCatalog.list_types()` full key list (read-only list).
3. `list_company_departments(ceo_id, ["business.general","function.hr"])` returns `list[DepartmentGovernanceView]` (length 2); each `requires_human_approval == True` (gate not lifted).
4. `propose_department_toggle(ceo_id, "function.hr", False, selected)` returns `GovernanceProposal` with `status == "proposed"`, `requires_human_approval == True`, `proposed_at` as UTC ISO8601; unknown `type_key` raises `KeyError`.
5. `propose_department_toggle` has **no** `record(` call / no write statement / no write to `department_types` (`\.record\(`, `insert into`, `update `, `delete from` zero hits) — pure in-memory proposal (no persistence, no gate lift).
6. Whole codebase has **no** `WHERE department_id` read-path filter (forbidden-scope guard).
7. **No** new API endpoint; existing API semantics unchanged (route-registry diff scan: `app.get("/api/govern"`, `app.post("/api/govern"` zero hits).
8. `backend/app/governance.py` has **no** real call to `apply_proposal` / `manage_department_types` (both are future hooks raising `NotImplementedError`).
9. `TenantContext.current_tenant_id()` still `'default'`; `is_multi_tenant()` still `False` (D1 invariant preserved).
10. Backend regression green (incl. D1–D3 existing tests); no existing test modified; forbidden-scope scan clean; `git diff --name-only -- backend/app/database.py` empty (zero schema delta).

## Verification

质量运行席:
- `git diff --name-only HEAD -- backend frontend` (scope check)
- `git diff --check` (whitespace)
- forbidden-scope keyword scan on changed `backend/app` files (`WHERE department_id`, `app.get("/api/govern"`, `app.post("/api/govern"`, `\.record\(`, `insert into`, `update `, `delete from`, `manage_department_types(`, `apply_proposal(`)
- `python -m unittest discover tests` (regression)
- `backend/tests/test_d4_governance.py` all pass

## Completion notes

_D4 两级治理 reservation boundary ACCEPTED + gate (D4 reservation) 2026-07-08 by 主理人齐活林 (产品规划席 delegation) under ADR-0017 option-a pre-authorized roadmap. 质量运行席 boundary verification reviews/056 PASS-WITH-NOTES (design-only confirmed, zero backend code leaked, forbidden-zone clean, reused base DepartmentCatalog/CompanyTopology/EvolutionEventLog/TenantContext signatures matched). 系统交付席 (Kou) implemented (T01–T04, b97728d4, 2 files: governance.py / test_d4_governance.py, +393). 质量运行席 implementation verification reviews/058 PASS-WITH-NOTES (100 tests green; AC1–10 read-code verified; forbidden-zone independent scan clean; database.py zero delta; routing NoOne). **Slice CLOSED 2026-07-08 by 主理人齐活林 (产品规划席 delegation)**. Real D4 implementation (提案落地 apply_proposal / 平台级管理后台 manage_department_types / 真实公司持久化 / 解除任何 gate / 跨公司策略 / 外部平台) requires separate future gate(s) (建议 D4.impl / D4.platform) + 总控决策席 + 安全边界席 review. 本 slice 零 schema 增量、零 database.py 改动、完全可逆。ADR-0017 四个子决策（D1✅ D2✅ D3✅ D4✅）reservation 边界与实现全部收口。_
