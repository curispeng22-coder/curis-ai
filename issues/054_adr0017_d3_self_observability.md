# Issue 054 — ADR-0017 D3: 职能型部门「自可观测 / 元循环」（设计预留 / Reservation）

- **Owner seat**: 系统交付席
- **Status**: Boundary (ADR-0024) → gate pre-authorized (主理人, 2026-07-08) → ACCEPTED (boundary, 主理人, 2026-07-08) → 系统交付席 (Kou) implemented (22c5cd55, T01–T04) → 质量运行席 implementation verification PASS-WITH-NOTES (reviews/055, 90 tests green) → **ACCEPTED (slice CLOSED) by 主理人齐活林 (产品规划席 delegation), 2026-07-08**
- **Source gate**: `issues/050_adr0017_future_gate_submission_package.md` option a (accepted by 总控决策席, 2026-07-07)
- **Boundary**: `docs/decisions/ADR-0024-d3-self-observability-boundaries.md`

## Minimal Context

ADR-0017 future phase gate is OPEN (option a). D1 (`tenant_id` reservation) ACCEPTED (ADR-0022, 69 tests green). D2 (部门目录通用化 reservation) CLOSED (ADR-0023 + issue 052, 81 tests green, Kou c8a30781, Yan reviews/053 PASS-WITH-NOTES). D3 is the third sub-decision: **职能型部门「元循环」与自可观测** — 把 ADR-0016 D3 的追加写事件日志升级为部门的硬依赖，使职能型/业务型部门能读取**自己**的运行指标与事件流，形成 meta-loop。Because self-observability is an L6 concept (forbidden zone under the current gate), D3 can only be a **design-only reservation** today — mirroring D1/D2's "read-only facade + index placeholder" zero-behavior-change approach. This slice reserves a read-only `DepartmentObservability` facade (analogous to D2's `DepartmentCatalog`), reusing ADR-0016 D3 `evolution_events` (read-only projection) and ADR-0023 D2 `department_types`/`DepartmentCatalog` (index). It does **not** compute real statistics/BI, instantiate departments, connect external platforms, or build visualizations. Real D3 implementation requires its own future small gate(s) + 总控决策席 + 安全边界席 review.

> ⚠️ **与 ADR-0016 D3 的区别**：ADR-0016 D3 = 写侧「追加写事件日志」（已落地，`evolution_events` + `EvolutionEventLog`，追加写不变式）。本 ADR-0017 D3 = 读侧「把自可观测升级为部门硬依赖」（reservation，只读消费写侧基座，不重写写路径）。两者不复用同一张表之外的关系。

## Scope

- New module `backend/app/department_observability.py`: read-only `DepartmentObservability` facade with `get_department_event_stream(type_key, limit=50)` and `get_department_metrics(type_key)`, plus `DepartmentMetrics` dataclass. Future hook `suggest_self_improvement(type_key, observation)` declared as signature-only placeholder (`raise NotImplementedError`).
- `get_department_event_stream(type_key, limit)`: validates `type_key` exists via `DepartmentCatalog.get_manifest(type_key)` (index role; `KeyError` if unknown), then returns a **read-only projection** of `EvolutionEventLog.get_all()` truncated to `limit` (most recent N). No department→event real association, no statistics.
- `get_department_metrics(type_key)`: wraps the read-only projection into `DepartmentMetrics`. `available_fields` statically declares `["call_count", "success_rate", "quality_line_hits"]` as **future-computable** fields; this slice computes/backfills **none** of them (no mean/rate/trend).
- Index reuse: `DepartmentCatalog` (D2) for `type_key` validation; `EvolutionEventLog` (ADR-0016 D3) for the event read-only projection. Injected via constructor (`database`, `event_log`).
- Tests in `backend/tests/test_d3_observability.py`.

## Non-goals

- No real statistics / aggregation / BI / visualization / charts: `get_department_metrics` only returns a read-only projection of the raw event stream; does **not** compute call_count / success_rate / quality_line_hits / mean / rate / trend.
- No L6 economy/ROI, no token-output-ratio.
- No real department instantiation, no `departments` table, no extension of `department_types` persistence, no department→event FK.
- No external platform integration, no credentials, no compliance surface (安全边界席 territory).
- No Employee CRUD, no L2/L5 employee layer, no role/skill config fact interface; `employee_role_spec` only a placeholder contract field, not consumed.
- No new write path: event log keeps ADR-0016 append-only invariant; D3 is read-only (no `record` call from the facade).
- No new API endpoint, no read/write semantic changes, no breakage of existing 81 tests.
- No multi-agent, agent abstraction, complex UI/dashboard, vector DB, embeddings, external memory.

## Allowed files

- `backend/app/department_observability.py` (new)
- `backend/tests/test_d3_observability.py` (new)
- `docs/decisions/ADR-0024-d3-self-observability-boundaries.md` (this slice's boundary)
- `issues/054_adr0017_d3_self_observability.md` (this issue)

> 注：`backend/app/database.py` **不在允许文件内** —— 本 reservation 零 schema 增量（`evolution_events` 与 `department_types` 均已存在），完全可逆。

## Acceptance criteria

1. `backend/app/department_observability.py` declares `DepartmentObservability` with `get_department_event_stream` / `get_department_metrics` methods and a `suggest_self_improvement` future hook placeholder.
2. `get_department_event_stream("function.admin", 10)` returns `list[dict]` (≤ 10 items), each with `event_id` / `correlation_id` / `event_type` / `payload` / `created_at` (raw event-stream read-only projection); unknown `type_key` raises `KeyError`.
3. `get_department_metrics("function.bi")` returns `DepartmentMetrics` with `available_fields == ["call_count","success_rate","quality_line_hits"]` and **no computed numeric metric fields** (no `call_count`/`success_rate`/`quality_line_hits` keys or backfilled values).
4. Whole codebase has **no** `WHERE department_id` read-path filter (forbidden-scope guard).
5. **No** new API endpoint; existing API semantics unchanged (route-registry diff scan: `app.get("/api/observ"`, `app.post("/api/observ"` zero hits).
6. `backend/app/department_observability.py` has **no** `record(` call / no write statement (`\.record\(`, `insert into`, `update `, `delete from` zero hits).
7. `TenantContext.current_tenant_id()` still `'default'`; `is_multi_tenant()` still `False` (D1 invariant preserved).
8. Backend regression green (incl. D1/D2 existing tests); no existing test modified; forbidden-scope scan clean; `git diff --name-only -- backend/app/database.py` empty (zero schema delta).

## Verification

质量运行席:
- `git diff --name-only HEAD -- backend frontend` (scope check)
- `git diff --check` (whitespace)
- forbidden-scope keyword scan on changed `backend/app` files (`WHERE department_id`, `app.get("/api/observ"`, `app.post("/api/observ"`, `\.record\(`, `insert into`, `update `, `delete from`)
- `python -m unittest discover tests` (regression)
- `backend/tests/test_d3_observability.py` all pass

## Completion notes

_D3 自可观测 reservation boundary ACCEPTED + gate (D3 reservation) 2026-07-08 by 主理人齐活林 (产品规划席 delegation) under ADR-0017 option-a pre-authorized roadmap. 质量运行席 boundary verification reviews/054 PASS-WITH-NOTES (design-only confirmed, zero backend code leaked, 10-class forbidden-zone clean, reused base signatures matched). 系统交付席 (Kou) implemented (22c5cd55, 2 files +287: department_observability.py / test_d3_observability.py). 质量运行席 implementation verification reviews/055 PASS-WITH-NOTES (90 tests green; AC1–8 read-code verified; forbidden-zone independent scan clean; database.py zero delta; routing NoOne). **Slice CLOSED 2026-07-08 by 主理人齐活林 (产品规划席 delegation)**. Real D3 implementation (真实指标关联 / 统计 / 可视化 / meta-loop 自愈 / Employee CRUD / 外部平台) requires separate future gate(s) (建议 D3.impl) + 总控决策席 + 安全边界席 review. 本 slice 零 schema 增量、零 database.py 改动、完全可逆。_
