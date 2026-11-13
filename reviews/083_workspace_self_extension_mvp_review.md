# Review 083: Workspace Self-Extension MVP

Date: 2026-07-09
Owner: 系统交付席 / 质量运行席 / 产品规划席
Issue: `issues/086_workspace_self_extension_mvp.md`
Status: ACCEPTED_BY_PRODUCT

## Product Progress

Curis Workspace can now let each tenant add private model/tool/connector metadata, view official and private capabilities together, and execute a task with a tenant-private capability while usage events preserve tenant-private attribution.

## Scope

- Backend-only Workspace Self-Extension MVP.
- Tenant-private model/tool/connector configuration is Workspace-owned.
- Official capability catalogs remain Admin-owned and read-only to Workspace through `/api/catalog/*`.
- Task creation remains backward-compatible: `content` is still the only required field.
- Optional task fields allow capability selection:
  - `capability_source`
  - `capability_type`
  - `capability_id`
- `credential_ref` and `config_ref` remain opaque `scheme:reference` placeholders.
- No marketplace, ROI, complex employee system, business module, Admin UI, real credential hosting, provider SDK, direct provider call, New API source change, or `/api/platform/*` Workspace write path was added.

## Changed Files

- `backend/app/main.py`
- `backend/app/database.py`
- `backend/app/result_store.py`
- `backend/app/orchestrator.py`
- `backend/tests/test_adr0028_workspace_integration.py`
- `backend/tests/test_d5_workspace_integration.py`
- `issues/086_workspace_self_extension_mvp.md`
- `reviews/083_workspace_self_extension_mvp_review.md`
- `PROJECT_STATUS.md`
- `TASKS.md`
- `knowledge/CURRENT_CONTEXT.md`
- `knowledge/PROJECT_MEMORY.md`

## Implementation Evidence

Tenant-private typed endpoints:

- `POST /api/workspace/private-models`
- `GET /api/workspace/private-models`
- `POST /api/workspace/private-tools`
- `GET /api/workspace/private-tools`
- `POST /api/workspace/private-connectors`
- `GET /api/workspace/private-connectors`

Unified Workspace selector:

- `GET /api/workspace/capabilities/selector`
- Returns official and tenant-private entries with explicit `source` labels.

Task capability selection:

- `POST /api/task` keeps `content` required and adds optional:
  - `capability_source`
  - `capability_type`
  - `capability_id`
- Tenant-private selection is validated against the current tenant before task creation.
- Tenant-private execution uses the existing model gateway tool path and rewrites selected capability attribution to the tenant-private id/source.

UsageEvent attribution:

- Private execution writes usage events with `capability_source=tenant_private`.
- Tool usage event records `capability_type=tool` and `capability_id=<tenant-private-tool-name>` for the selected private tool.
- Admin-compatible fields from issue 085 are preserved.

Isolation:

- Tenant-private data stays in `tenant_private_capabilities`.
- List/read filters by current `X-Tenant-Id`.
- Private entries do not appear in `/api/catalog/capabilities`.
- Admin official capability module remains free of `tenant_private` references.
- Admin `/api/platform/*` route section does not reference `tenant_private`.

## TDD Evidence

Red run before implementation:

```text
cd backend && ./.venv/bin/python -m unittest tests/test_adr0028_workspace_integration.py
```

Expected failures confirmed:

```text
AssertionError: 404 != 201
AssertionError: 404 != 200
AssertionError: 400 != 200
```

Focused integration run after implementation:

```text
cd backend && ./.venv/bin/python -m unittest tests/test_adr0028_workspace_integration.py
```

Result:

```text
Ran 10 tests
OK
```

Focused Phase-3 regression:

```text
cd backend && ./.venv/bin/python -m unittest tests/test_model_gateway_adapter.py tests/test_tenant_model_preference.py tests/test_d5_workspace_integration.py tests/test_adr0028_workspace_integration.py
```

Result:

```text
Ran 42 tests
OK
```

Execution-engine regression:

```text
cd backend && ./.venv/bin/python -m unittest tests/test_execution_engine.py
```

Result:

```text
Ran 38 tests
OK
```

Full backend regression:

```text
cd backend && ./.venv/bin/python -m unittest discover tests
```

Result:

```text
Ran 298 tests
OK
```

Whitespace check:

```text
git diff --check -- backend/app/main.py backend/app/database.py backend/app/result_store.py backend/app/orchestrator.py backend/tests/test_adr0028_workspace_integration.py backend/tests/test_d5_workspace_integration.py
```

Result: passed.

## Scope Checks

Runtime platform endpoint scan:

```text
rg -n "/api/platform/" backend/app/result_store.py backend/app/orchestrator.py backend/app/tool_executor.py backend/app/model_gateway.py backend/tests/test_adr0028_workspace_integration.py backend/tests/test_d5_workspace_integration.py
```

Result:

- Workspace runtime files do not call `/api/platform/*`.
- Matches appear only in tests verifying Admin protection/projection.

Secret scan:

```text
rg -n "api_key|password|secret|Authorization|Bearer|sk-[A-Za-z0-9_-]{10,}" backend/app/main.py backend/app/database.py backend/app/result_store.py backend/app/orchestrator.py backend/tests/test_adr0028_workspace_integration.py backend/tests/test_d5_workspace_integration.py
```

Result:

- Matches are expected in guarded metadata comments, Admin auth handling, and tests.
- No new real credential storage or secret display was introduced.

Tenant-private / selector scan:

```text
rg -n "private-models|private-tools|private-connectors|capabilities/selector|tenant_private|requested_capability" backend/app/main.py backend/app/database.py backend/app/result_store.py backend/app/orchestrator.py backend/tests/test_adr0028_workspace_integration.py backend/tests/test_d5_workspace_integration.py
```

Result:

- Required Workspace private endpoints, selector, task capability fields, and usage attribution are present.

## Known Gaps

- Tenant-private model/tool/connector runtime implementations remain metadata-first. Private execution currently routes through the existing model gateway tool path and records the selected tenant-private capability attribution.
- `credential_ref` and `config_ref` are validated only as opaque references; real secret hosting and resolution are still not implemented.
- No frontend UI was added for private configuration in this backend MVP.
- Marketplace, ROI, packages, billing, and production identity governance remain future-gated.

## Quality Result

Quality Result: PASS.

Commands: TDD red run, focused integration, focused Phase-3 regression, execution-engine regression, full backend regression, whitespace check, endpoint scope scan, tenant-private scan, and secret scan.

Evidence: CEO can add tenant-private model/tool/connector metadata; Workspace can read official and tenant-private capabilities together; tenant-private task selection records private source in usage events; tenant isolation and official catalog protection passed.

Risks: Worktree contains unrelated pre-existing dirty files from previous accepted work; they were not used as evidence for this issue.

Blocked / Pass: Pass; no blockers found.

Next Seat: main thread closeout.

Handoff: final closeout
