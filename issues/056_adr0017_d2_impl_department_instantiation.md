# Issue 056 — ADR-0017 D2.impl: 部门真实实例化（Department Instantiation）（真实落库切片）

- **Owner seat**: 系统交付席
- **Status**: Boundary (ADR-0026) → GATE APPROVED (总控决策席 2026-07-08 + 安全边界席 review 随选确认) → 系统交付席 implementation (T01–T03) DONE (`7617ed2c` + 主理人一致性修复 `4ec02a59`) → 质量运行席 implementation verification DONE (reviews/059 PASS-WITH-NOTES, routing NoOne, 114 tests green, `67ab1616`) → **主理人 accept CLOSED (2026-07-08)**.
- **Source gate**: `issues/050_adr0017_future_gate_submission_package.md` option a (accepted by 总控决策席, 2026-07-07) — **本切片超出该 option-a 预授权范围（仅 design-only reservation），故作为独立小 gate 提交包。**
- **Boundary**: `docs/decisions/ADR-0026-d2-impl-department-instantiation.md`

## Minimal Context

ADR-0017 future phase gate is OPEN (option a). D1 (`tenant_id` reservation) ACCEPTED (ADR-0022). D2 (部门目录通用化 reservation) CLOSED (ADR-0023 + issue 052, 81 tests green, Kou c8a30781). D3 (职能型部门自可观测 reservation) CLOSED (ADR-0024 + issue 054). D4 (两级治理 reservation) CLOSED (ADR-0025 + issue 055). D2 reservation 的 `assemble_company_topology` 仅纯内存组装、不持久化——系统至今无任何「真实存在的部门实例」。本切片（D2.impl）是 D2 从 reservation 走向实现的**最小、最必要**一步：**真实实例化部门并落库**。新增公司级 `departments` 表（沿用 D1 `tenant_id` 预留列，当前单租户恒 `'default'`）+ `DepartmentCatalog` 真实 `create_department`/`list_departments`/`get_department` 方法，从既有 `department_types` 目录类型实例化部门。类型字典本身的管理（增删改 `department_types`）仍锁定（`manage_department_types` 属 ADR-0025 4 个 LOCKED_ACTIONS 之一，本切片不触碰）。**本切片超出 ADR-0017 option-a 预授权（仅 design-only reservation，明确禁止真实实例化），故作为独立小 gate 提交包，待 总控决策席批准 + 安全边界席 review 后方可实现。**

> ⚠️ **与 D2/D3/D4 的衔接**：本切片演进 `DepartmentCatalog` 从「纯内存组装」到「可真实创建/列举/读取部门实例」，但保留既有 `list_types`/`get_manifest`/`assemble_company_topology` 签名与行为——D3 `DepartmentObservability`（读 `department_types`+`evolution_events`）与 D4 `CompanyGovernance`（复用 `assemble_company_topology` 内存投影作治理作用域）的接口与 import 路径**不被破坏**。`assemble_company_topology` 保留以支持 D4 治理 reservation 兼容。

## Scope

- New company-level table `departments` in `backend/app/database.py` (additive, inside `initialize()`'s `executescript`): columns `department_id` (PK, text), `tenant_id` (text not null default 'default', reuses D1 reserved column), `type_key` (text not null, logical ref to `department_types.type_key`), `display_name` (text not null), `status` (text not null default 'active'), `created_at` / `updated_at` (text not null default current_timestamp). **No seed** (instances are runtime-created), **no FOREIGN KEY** constraint (consistent with ADR-0023 no-FK style; type_key validated at app layer via `get_manifest`).
- `backend/app/department_catalog.py` (incremental): add `Department` dataclass; add `create_department(type_key, display_name, tenant_id=None, department_id=None, status='active')`, `list_departments(tenant_id=None)`, `get_department(department_id, tenant_id=None)`. `create_department` injects `tenant_id = TenantContext.current_tenant_id()` (currently `'default'`), validates `type_key` via `get_manifest` (unknown → `KeyError`), generates `department_id = uuid.uuid4().hex` if not provided, persists a row, returns `Department`. `instantiate_department` future hook **fulfilled** by delegating to `create_department`. `connect_platform` / `manage_employees` remain `raise NotImplementedError` (still forbidden). Existing `list_types` / `get_manifest` / `assemble_company_topology` signatures and behavior **unchanged** (D4 reservation compatibility).
- Real persistence verified by cross-connection round-trip (separate `Database().connect()` after create returns the persisted instance).
- Tests in `backend/tests/test_d2_impl_department.py`.

## Non-goals

- No Employee CRUD, no L2/L5 employee layer, no role/skill config: `manage_employees` stays `raise NotImplementedError`; `backend/app/employee.py` untouched.
- No external service / platform integration, no credentials, no compliance surface: `connect_platform` stays `raise NotImplementedError` (安全边界席 territory).
- No real multi-tenant isolation: still single-tenant `'default'`; only fill D1 `tenant_id` reserved column sentinel; no tenant-scoping/filtering logic; `TenantContext.is_multi_tenant()` stays `False`.
- No L6 economy/ROI, no token-output-ratio, no visualization: `roi_schema` not filled.
- No auto code modification (`auto_modify_code`): no auto-modify path.
- No complex UI / frontend changes: pure backend data layer + facade; **no new API endpoint**; no frontend files touched.
- No vector DB, embeddings, external memory.
- No `manage_department_types` (ADR-0025 LOCKED_ACTION): this slice instantiates from existing types, does NOT manage type definitions; `department_types` table not written; D4 `CompanyGovernance.manage_department_types` stays future-hook placeholder.
- No lift of human-approval gate, no cross-company policy: `lift_human_approval_gate` / `cross_company_policy` remain locked.
- No write to `evolution_events`: D3 append-only invariant preserved; audit trail (e.g. `governance.department.created`) is a future governed enhancement, out of this slice's minimal scope.
- No modification of D3/D4 facades: `department_observability.py` / `governance.py` interfaces unchanged; `assemble_company_topology` unchanged.
- No pre-emptive unneeded structures (`company_topology` table, `tasks.department_id` column) — only `departments` table added.

## Allowed files

- `backend/app/database.py` (modify, **additive only**: add `CREATE TABLE IF NOT EXISTS departments` inside `executescript`; no seed, no FK, no change to existing tables)
- `backend/app/department_catalog.py` (modify, incremental: add `Department` dataclass + `create_department`/`list_departments`/`get_department`; fulfill `instantiate_department` by delegating to `create_department`; keep `connect_platform`/`manage_employees` as `NotImplementedError`; preserve `list_types`/`get_manifest`/`assemble_company_topology`)
- `backend/tests/test_d2_impl_department.py` (new)
- `docs/decisions/ADR-0026-d2-impl-department-instantiation.md` (this slice's boundary / gate package)
- `issues/056_adr0017_d2_impl_department_instantiation.md` (this issue)

## Forbidden files

- `backend/app/department_observability.py` (D3 facade — interface must stay intact)
- `backend/app/governance.py` (D4 facade — `manage_department_types` locked, interfaces stable; keep untouched)
- `backend/app/tenant_context.py` (D1 single-tenant invariant — keep untouched)
- `backend/app/evolution_event_log.py` (no new write path — keep untouched)
- `backend/app/department_manifest.py` (no Manifest field consumption; keep as-is)
- `backend/app/employee.py` (Employee CRUD forbidden — keep untouched)
- All frontend files (no UI changes)
- `backend/app/main.py` and route registration (no new API endpoint — keep unchanged)

## Acceptance criteria

1. After `Database().initialize()`, `departments` table exists with all specified columns (`department_id`, `tenant_id`, `type_key`, `display_name`, `status`, `created_at`, `updated_at`); **no FOREIGN KEY** constraint; `department_types` seed unchanged (still 4 rows, not rewritten).
2. `backend/app/department_catalog.py` adds `Department` dataclass and `create_department(type_key, display_name, tenant_id=None, department_id=None, status='active')`, `list_departments(tenant_id=None)`, `get_department(department_id, tenant_id=None)`; `assemble_company_topology` / `list_types` / `get_manifest` signatures and behavior unchanged.
3. `create_department("business.general", "华东业务部")` returns a `Department` with `tenant_id == 'default'`, `type_key == 'business.general'`, `status == 'active'`, non-empty `department_id`, non-empty `created_at`/`updated_at`.
4. `create_department` validates `type_key` via `get_manifest`; unknown `type_key` (e.g. `"unknown.dept"`) raises `KeyError`.
5. **Real persistence (cross-connection round-trip)**: after `create_department` and a fresh `Database().connect()`, `list_departments()` includes the instance and `get_department(id)` returns it (true DB round-trip, not in-memory).
6. `instantiate_department` future hook is fulfilled (delegates to `create_department`, no longer raises `NotImplementedError`); `connect_platform` / `manage_employees` still raise `NotImplementedError`.
7. Single-tenant invariant: every persisted `departments` row has `tenant_id == 'default'`; `TenantContext.current_tenant_id()` still `'default'`; `is_multi_tenant()` still `False`; no multi-tenant isolation logic added.
8. Forbidden-scope guard clean (independent keyword scan on changed `backend/app` files): no Employee CRUD (`manage_employees(` only `NotImplementedError`; no employee table/write), no external platform (`connect_platform(` only `NotImplementedError`; no credential/secret/external-SDK code), no L6/ROI, no `auto_modify_code` real path, no `manage_department_types(` real call (only D4 future hook), no `department_types` write, no new API endpoint (`app.get("/api/depart"`, `app.post("/api/depart"` zero hits), no `evolution_events` write (`insert into evolution_events`, `\.record\(` zero hits), no vector/embedding.
9. D3/D4 facades unaffected: `DepartmentObservability` (D3) and `CompanyGovernance` (D4) still importable; their public method signatures unchanged; `assemble_company_topology` still returns in-memory `CompanyTopology` (D4 reservation compatibility). Backend regression green (incl. D1–D4 existing tests); no existing test modified.
10. `git diff --name-only -- backend/app/department_observability.py backend/app/governance.py backend/app/tenant_context.py backend/app/evolution_event_log.py backend/app/department_manifest.py backend/app/employee.py` is empty (these base/facade modules untouched); `git diff --name-only -- backend/app/database.py` shows only the additive `departments` table creation (no structural drops/alters of existing tables).

## Verification

质量运行席:
- `git diff --name-only HEAD -- backend frontend` (scope check)
- `git diff --check` (whitespace)
- forbidden-scope keyword scan on changed `backend/app` files (`manage_employees(`, `connect_platform(`, `WHERE department_id`, `app.get("/api/depart"`, `app.post("/api/depart"`, `insert into evolution_events`, `\.record\(`, `manage_department_types(`, `auto_modify_code`, `vector`, `embedding`)
- `python -m unittest discover tests` (regression, incl. D1–D4)
- `backend/tests/test_d2_impl_department.py` all pass (incl. cross-connection round-trip + `type_key` KeyError + single-tenant invariant)

## Completion notes

_D2.impl 部门真实实例化 boundary (ADR-0026) submitted 2026-07-08 by 高见远 (架构师) as independent small-gate package — **EXCEEDS ADR-0017 option-a pre-authorization (design-only reservation only)**; pending 总控决策席 approval + 安全边界席 review. Scope: additive `departments` table (reuses D1 `tenant_id` reserved column, single-tenant `'default'`) + `DepartmentCatalog.create_department`/`list_departments`/`get_department` (fulfills `instantiate_department` hook); `connect_platform`/`manage_employees` stay `NotImplementedError`; `manage_department_types` (ADR-0025 LOCKED) untouched; D3/D4 facades interfaces preserved; no new API endpoint; no `evolution_events` write. Forbidden-scope independent scan is a hard gate (any forbidden keyword hit → reject). **Status 流水位: Boundary (ADR-0026) → GATE APPROVED** (总控决策席 2026-07-08 + 安全边界席 review 随选确认). 系统交付席 (Kou) now implementing T01–T03; 质量运行席 (Yan) verification follows.

**ACCEPTED & CLOSED (主理人齐活林, 产品规划席 delegation, 2026-07-08)** — D2.impl 部门真实实例化切片正式收口。
- 系统交付席 (Kou) 实现：`7617ed2c`（departments 表 additive + DepartmentCatalog 三真实方法，114 tests 全绿）；主理人一致性修复 `4ec02a59`（删除过时 reservation 契约断言，保 clean checkout 全绿）。
- 质量运行席 (Yan) 实现验证：`reviews/059` PASS-WITH-NOTES，路由 NoOne，独立实跑 114 全绿，AC1–AC10 逐条读码核实通过，禁止区独立 grep 全绿，`database.py` 纯 additive 建表、基座/facade 零改动，commit `67ab1616` 仅动 review 文件。
- 主理人独立复核：`git show 67ab1616 --stat` 确认仅 +98 行 reviews/059（未触碰实现）；项目 `.venv` 独立重跑 `unittest discover` 实证 114 OK。
- 禁止区（Employee CRUD / 外部平台 / 真实多租户 / L6 ROI / 自动改码 / 复杂 UI / 向量库）与 ADR-0025 四个 LOCKED_ACTIONS 全程零触碰；D3/D4 facade 接口完好；单租户纪律保持（`tenant_id` 恒 `'default'`）；不写 `evolution_events`。
- 非阻断注记（N1：测试实际 14 例 vs 文档称 10，真实 114 全绿已实证，纯文档口径差异，无需改码）已知悉，不影响 accept。
- **结论：D2.impl 是 ADR-0017 四个子决策中首个从 reservation 走向真实落库的实现切片，收口成功。后续真实增强（Employee CRUD / 外部平台 / L6 ROI / manage_department_types 落地 / evolution_events 审计写 / 多租户隔离 / 新 API endpoint / 向量内存）均须各自独立小 gate + 总控决策席 + 安全边界席 review，不得借本切片夹带落地。**_
