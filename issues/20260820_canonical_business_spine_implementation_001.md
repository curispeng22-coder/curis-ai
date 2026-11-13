# CURIS CANONICAL BUSINESS SPINE — IMPLEMENTATION 001

Status: IMPLEMENTED / ACCEPTED
Owner: 主开发（Frontend Baseline Promotion Integration Owner）
Product Authority: Product Architecture Authority
Source Review: `docs/reviews/CURIS_CANONICAL_BUSINESS_SPINE_AUTHORITY_REVIEW.md`
Baseline: current preserved development baseline; 不 reset / clean / whole-file replace

## Objective

把已接受的 `Company → Department → Business → Workspace` 产品合同落到可验证的 canonical persisted identity、关系、创建、读取和受控 Frontend baseline。

## Allowed Scope

实现必须按 Phase 1–7 顺序推进，可在安全依赖明确时合并相邻 Phase，但不得越过 Stop Gate：

1. Canonical Business persistence / Company + Department relation
2. Legacy compatibility / migration bridge（`UNRESOLVED → QUARANTINED`）
3. Atomic Business + First Workspace creation
4. Canonical Parent Resolver / deep route
5. Business Read Model
6. Frontend baseline promotion（source manifest、provenance、owner、tracked clean slice）
7. Single / Multi / Generic E2E（isolated DB、restart、failure/recovery、deep link）

## Allowed Files（按 Phase 收窄，不是全仓授权）

| Phase | 首批可触碰文件 | 约束 |
| --- | --- | --- |
| 1 | `backend/app/database.py`、`backend/app/runtime/models.py`、对应 schema / model tests | 只建立 canonical identity / relation；先隔离 DB，禁止活动库迁移。 |
| 2 | `backend/app/runtime/` legacy adapter / resolver 文件、`backend/app/company_project_runtime.py`、migration tests | 只做可追溯 compatibility bridge；不得删除旧表或猜测 mapping。 |
| 3 | `backend/app/runtime/ceo_day_service.py`、`backend/app/runtime/workspace.py`、相关 API router / tests | 只实现 Business + First Workspace 原子事务与 Leader gate。 |
| 4 | `backend/app/shared_workspace_projection.py`、parent resolver API / tests、对应 route tests | 只消费 canonical relation；失效关系 fail-closed。 |
| 5 | Business read-model service / API 与对应 frontend data adapter / tests | 不复制 Business / Result / Assignment truth。 |
| 6 | `frontend/app/ceo-office/business/page.js`、`frontend/app/ceo-office/workspace/page.js`、`frontend/components/runtime/WorkspaceRuntimeView.js`、`frontend/lib/runtimeApi.js` 及经过 provenance 审计的 shared seams | 必须先提交 source manifest、owner、provenance；禁止 whole-file add untracked tree。 |
| 7 | 既有测试、隔离 evidence root、必要的 Browser/Desktop 验收输出 | 不把静态页面、候选包或单个 API 结果当作完成。 |

每个 Phase 开始前主开发必须在本 Issue 或子 Review 中明确实际 Allowed Files；未列出的 Domain 文件不得顺手修改。

## Ownership

- 主开发：Frontend Baseline Promotion Integration Owner，负责 source manifest、Git provenance、Allowed Files、shared route/API seam、promotion slicing、build/test/regression、clean checkout recoverability。
- XHS / Content Growth：Domain owner review。
- RD：Domain owner review。
- Shared Workspace / Business contract：Product Authority review。
- Design：只提供设计资产，不拥有源码 promotion authority。

## Non-goals

- 不把 `business_directions` 升格为 Business identity。
- 不把 Project 升格为 Business。
- 不自动把 legacy Workspace 挂到默认 Business。
- 不 whole-file add untracked tree。
- 不修改无关 Domain、Runtime Primitive、Frozen Shell 或高保真 UI。

## Stop Gates / Evidence

- active DB migration 前：备份、隔离 DB、schema diff、rollback 方案；
- ambiguous legacy mapping：进入 `UNRESOLVED → QUARANTINED`，等待责任人；
- destructive rewrite：停止并回 CEO；
- bulk frontend promotion：停止，提交 source manifest 与 owner/provenance Review；
- Product Contract conflict：停止，不创造第三种真相；
- commit / push：沿既有授权纪律单独确认。

每个 Phase 必须回交：变更文件、Allowed Files、真实测试/Browser/Desktop/SQLite 证据（适用时）、失败边界、Disposition、Owner、Next Action、Next Gate。

## Acceptance Boundary

只有同时证明 canonical relation、原子创建、Parent Resolver、read model、受控 Frontend promotion 与 E2E recovery，才可关闭本 Issue。局部 API、静态页面、迁移草稿或测试通过不能单独代表 Business Spine 完成。

## Phase 0 execution record

- Pre-change HEAD: `d3ab0ce46d3a0ebbe13b7748b6722ac0c4bf264a`.
- Staged scope: empty.
- Preserved worktree inventory: 72 tracked modifications and 358 untracked paths; no reset, clean, removal or broad staging performed.
- `backend/app/database.py` is mixed-source and contains unrelated Capability ownership, Strategy Meeting and Employee Template changes. It is excluded from this Issue to avoid ownership collision.
- Active SQLite fingerprints are recorded in the implementation Review and remain read-only.

### Phase 1 exact Allowed Files

- `backend/app/runtime/models.py` — additive canonical Business schema, relation metadata and DB-level existence guards only.
- `backend/tests/test_canonical_business_spine_schema.py` — repository-external isolated SQLite schema truth.
- this Issue and its Review.

No other Phase 1 file is owned.

## Implementation progress — 2026-08-20

### Implemented in the preserved worktree

- Phase 1: additive `canonical_businesses`, canonical Workspace relation metadata, and database existence guards.
- Phase 2: legacy relation remains explicit `UNRESOLVED`; CEO classification can move it to `QUARANTINED`; unresolved/quarantined Workspace execution fails closed.
- Phase 3: canonical Business + first DRAFT Workspace + Workspace version are created in one transaction; injected Workspace failure rolls the Business back.
- Phase 4: canonical parent resolution and shared projection consume `Workspace → Business → Department → Company`.
- Phase 5: Business Definition / derived Operating Summary / canonical Workspace Directory / existing Responsibility-based Team read model.
- Phase 7 backend prerequisite: existing Workspace Package install now creates canonical Business + first DRAFT Package Workspace atomically instead of writing `package:<id>` as free-form Business truth.

### Phase 6A accepted reconstruction

The required semantic source manifest is recorded in
`docs/reviews/CURIS_FRONTEND_BASELINE_PROVENANCE_RECONCILIATION.md`. The three
TARGET files were reconstructed with explicit ownership, focused tests and
current preserved-worktree Browser evidence.

### Phase 6B exact stop gate

An exact 22-file staged manifest was exported as Git tree
`d1c8eb9f7b455f36c1425fe41b8e1c6e201c6ef0` and tested in a repository-external
clean directory. The clean tree cannot build the promoted Business and
Workspace routes because their direct dependencies
`frontend/components/runtime/RuntimeProvider.js` and
`frontend/components/runtime/RuntimeStates.js` are still untracked and their
current contents differ materially from both known tracked sources. The
accepted RD/XHS/Studio domain routes referenced by the focused mixed regression
are also absent from the clean baseline and remain outside this Issue's
ownership. Promoting those files without a separate semantic ownership record
would violate the controlled-promotion boundary.

Current preserved-worktree Browser verification passed canonical Business,
multi-Workspace directory, Parent Resolver deep links, generic Package work
surface, legacy fail-closed and same-database Runtime restart. Packaged Desktop,
clean-checkout production build and the final commit remain blocked by the exact
dependency gate above.

### Verification

- 60 focused and accepted-runtime regressions passed against one repository-external isolated SQLite.
- Python compile and `git diff --check` passed.
- Both repository SQLite files retained their Phase 0 size, mtime and SHA-256; `integrity_check=ok`.
- No commit or push was performed. The temporary exact index promotion is
  cleared after recording its manifest; working files remain preserved.

### Final acceptance resume

- Frontend dependency closure consumed; exact 37-file tree:
  `17096f6e9c9319533f8c7d3b1fa07658f122c1ea`.
- Clean focused backend/frontend tests, ESLint, production build and Phase 7 canonical
  scenarios pass.
- Exact remaining gate: current HEAD/final tree contain no tracked `desktop/` source, so a
  clean-source Packaged Desktop cannot be built without a separately controlled Desktop
  baseline promotion. Dirty Desktop source and historical generated trees are not accepted
  substitutes.
- Commit and push remain withheld.

### Final packaged acceptance — 2026-08-21

- Accepted Desktop source closure consumed from
  `docs/reviews/CURIS_DESKTOP_SOURCE_BASELINE_CLOSURE_REVIEW.md`.
- Final exact promotion manifest: 59 files; no broad add, generated output, old `.app` or
  unrelated worktree change included.
- Clean source backend/frontend focused suites, Python compile, ESLint and production build
  passed.
- A fresh standalone frontend, Workspace/Gateway/Guardian sidecars and Tauri `.app` were
  built from the controlled clean source.
- The newly built Packaged Desktop passed canonical Single Workspace, Multi Workspace,
  Generic Business + First DRAFT Workspace, Legacy quarantine/fail-closed and same-app-data
  restart/reread scenarios.
- Both repository active SQLite fingerprints and integrity remained unchanged.
- Formal acceptance record:
  `docs/reviews/CURIS_CANONICAL_BUSINESS_SPINE_IMPLEMENTATION_001_REVIEW.md`.
- Final disposition: `IMPLEMENTED / ACCEPTED`; scoped commit created; not pushed.
