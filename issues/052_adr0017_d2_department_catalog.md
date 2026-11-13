# Issue 052 — ADR-0017 D2: 部门目录通用化（设计预留 / Reservation）

- **Owner seat**: 系统交付席
- **Status**: Boundary (ADR-0023) → gate pre-authorized (主理人, 2026-07-07 23:27) → ACCEPTED (boundary, 主理人, 2026-07-07 23:27) → 系统交付席 (Kou) implemented (c8a30781, T01–T05) → 质量运行席 implementation verification PASS-WITH-NOTES (reviews/053, 81 tests green) → **ACCEPTED (slice CLOSED) by 主理人齐活林 (产品规划席 delegation), 2026-07-08**
- **Source gate**: `issues/050_adr0017_future_gate_submission_package.md` option a (accepted by 总控决策席, 2026-07-07)
- **Boundary**: `docs/decisions/ADR-0023-d2-department-catalog-boundaries.md`

## Minimal Context

ADR-0017 future phase gate is OPEN (option a). D1 (`tenant_id` reservation) is implemented and verified PASS (ADR-0022), awaiting 产品规划席 acceptance. D2 is the second sub-decision: **部门目录通用化（业务型 + 职能型）**. Because departments are an L5 concept (forbidden zone under the current gate), D2 can only be a **design-only reservation** today — mirroring D1's "add table + contract stub" zero-behavior-change approach. This slice reserves the `department_types` system-level catalog (built once, usable by all), the Manifest seam contract (7 fields), and a read-only `DepartmentCatalog` facade. It does **not** instantiate real departments, connect external platforms, or manage employees. Real D2 implementation requires its own future gate + 安全边界席 review.

## Scope

- Additive schema: new system-level shared table `department_types` (`type_key`, `category`, `display_name`, `description`, `manifest_json`, `manifest_schema_version`, `is_system`) via `Database.initialize()` `executescript` (zero rewrite; idempotent).
- Idempotent seed (`_seed_department_catalog`, `INSERT OR IGNORE`) of the **minimal canonical type set** (4 rows: `business.general`, `function.hr`, `function.admin`, `function.bi`) with placeholder `manifest_json` — no real credentials/ROI/employee data.
- New module `backend/app/department_manifest.py`: `MANIFEST_FIELDS` (7 keys) + `DepartmentManifest` dataclass (declares structure, no parse/validate/consume).
- New module `backend/app/department_catalog.py`: read-only `DepartmentCatalog` (`list_types()`, `get_manifest(type_key)`, `assemble_company_topology(ceo_id, selected_type_keys)`) + `DepartmentType` / `CompanyTopology` dataclasses. Future hooks (`instantiate_department` / `connect_platform` / `manage_employees`) declared as signatures only.
- Tests in `backend/tests/test_d2_department.py`.

## Non-goals

- No real department instantiation, no `departments` table, no department CRUD, no `company_topology` persistence.
- No external platform integration, no credentials, no compliance surface (安全边界席 territory).
- No L6 economy/ROI measurement, no token-output-ratio, no visualization回流.
- No Employee CRUD, no L2/L5 employee layer, no role/skill config fact interface.
- No Manifest real parse/validate/consume driving tool routing or quality lines.
- No `WHERE department_id = ?` read-path filtering, no new API endpoint, no read/write semantic changes.
- No multi-agent, agent abstraction, complex UI/dashboard, vector DB, embeddings, external memory.

## Allowed files

- `backend/app/database.py` (additive `department_types` table + `_seed_department_catalog` only)
- `backend/app/department_manifest.py` (new)
- `backend/app/department_catalog.py` (new)
- `backend/tests/test_d2_department.py` (new)
- `docs/decisions/ADR-0023-d2-department-catalog-boundaries.md` (this slice's boundary)
- `issues/052_adr0017_d2_department_catalog.md` (this issue)

## Acceptance criteria

1. After `Database().initialize()`, `department_types` exists with all specified columns.
2. `department_types` contains **exactly** the minimal canonical type set (4 rows); `manifest_json` parses to placeholder structure (no real credentials/ROI/employee data).
3. `backend/app/department_manifest.py` declares `MANIFEST_FIELDS` with the 7 keys (capability_set / tool_classes / quality_lines / output_channels / roi_schema / guardrail_refs / employee_role_spec).
4. `DepartmentCatalog.list_types()` returns a non-empty catalog; `get_manifest("business.general")` returns a placeholder `DepartmentManifest`; `assemble_company_topology(ceo_id, [...])` returns an in-memory `CompanyTopology` and persists **nothing** (no `companies`/`company_topology` table created).
5. Whole codebase has **no** `WHERE department_id` read-path filter (forbidden-scope guard).
6. **No** new API endpoint; existing API semantics unchanged (route-registry diff scan).
7. `TenantContext.current_tenant_id()` still `'default'`; `is_multi_tenant()` still `False` (D1 invariant preserved).
8. Backend regression green (incl. D1 existing tests); no existing test modified; forbidden-scope scan clean.

## Verification

质量运行席:
- `git diff --name-only HEAD -- backend frontend` (scope check)
- `git diff --check` (whitespace)
- forbidden-scope keyword scan on changed `backend/app` files (`WHERE department_id`, `app.get("/api/department"`, `app.post("/api/department"`)
- `python -m unittest discover tests` (regression)
- `backend/tests/test_d2_department.py` all pass

## Completion notes

D2 部门目录 reservation boundary ACCEPTED 2026-07-07 23:27 by 主理人齐活林 (产品规划席 delegation). Gate pre-authorized under ADR-0017 option-a roadmap (design-only reservation; user retains 总控决策席 for scope-expansion/conflict only). 质量运行席 boundary verification reviews/052 PASS-WITH-NOTES (design-only, zero backend code leaked, 8-class forbidden-zone clean). 系统交付席 (Kou) implemented (c8a30781, 4 files +459: department_manifest.py / department_catalog.py / database.py additive / test_d2_department.py). 质量运行席 implementation verification reviews/053 PASS-WITH-NOTES (81 tests green, AC1–8 read-code verified, forbidden-zone independent scan clean, routing NoOne). **Slice CLOSED 2026-07-08 by 主理人齐活林 (产品规划席 delegation)**. Real D2 implementation (instantiation / external platforms / L6 / Employee CRUD) requires separate future gate (建议 `D2.impl`) + 总控决策席 + 安全边界席 review.
