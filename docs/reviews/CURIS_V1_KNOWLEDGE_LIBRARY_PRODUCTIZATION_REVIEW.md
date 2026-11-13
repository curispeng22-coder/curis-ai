# CURIS V1 KNOWLEDGE LIBRARY PRODUCTIZATION REVIEW

Status: Review
Authority Class: REVIEW
Date: 2026-09-01
Issue: `CURIS-V1-KNOWLEDGE-LIBRARY-PRODUCTIZATION-001`
Disposition: IMPLEMENTED / ACCEPTED CANDIDATE

## Verdict

**KNOWLEDGE LIBRARY: IMPLEMENTED / ACCEPTED CANDIDATE**

The previously recorded canonical projection blocker was resolved by the accepted Knowledge Scope and Typed Work Reference contracts. Curis now has one canonical Knowledge truth, explicit Company / Business / Workspace scope, one generic typed Work relation, bounded execution context, reverse Work/output projection, archival protection and the accepted Overview / Browse / Detail / Work Picker product surfaces.

No external connector, semantic search, vector retrieval, source version system or second Knowledge/Context/Citation truth was introduced.

## 1. Legacy Reconciliation

- Kept the existing `knowledge_entries` identity and `KnowledgeService` write authority.
- Kept manual content and local `.md` / `.txt` import with source path, hash and timestamp truth.
- Kept `context_packages` as an execution-derived snapshot, not a reference authority.
- Kept legacy Project / Department fields for compatibility reads only; they do not impersonate Business or Workspace.
- Replaced the current product path's Project-style scope selectors, card dashboard and ID-first detail composition.

## 2. Canonical Scope

Existing `knowledge_entries` now stores explicit `company_id`, `target_type` and `target_ref` for `COMPANY`, `BUSINESS` or `WORKSPACE`.

Writes verify the current tenant and canonical parent chain. Business and Workspace filters never infer scope from Project, Department, tag, title or path. Legacy unmapped rows remain compatibility data and do not appear as canonical Business/Workspace records.

## 3. Typed Work Reference

One generic `typed_object_references` relation records:

`WORK --USES_REFERENCE--> KNOWLEDGE`

The relation keeps source/target type and identity plus tenant/company/workspace ownership. Duplicate additions are idempotent. Cross-tenant, cross-company, incompatible scope, missing and archived Knowledge references fail closed.

No Work-private `work_knowledge_links` table and no reverse truth table were added.

## 4. Context Integration

The accepted General Workspace execution seam resolves explicit Work references first, then fills only the remaining bounded budget from legal automatic candidates.

- maximum Knowledge context remains bounded to three items;
- explicit and automatic records are deduplicated by stable Knowledge identity;
- whole Library, Workspace, Conversation and History are not injected;
- provider prompt evidence proves selected Knowledge content is resolved through the existing execution path;
- invalid explicit references reject the execution instead of being ignored or invented.

## 5. Reverse Use and Outputs

Knowledge detail derives `Used By Work` from the same typed relation. Work names come from the canonical Cycle problem/expected result rather than internal release keys.

Related Result / Evidence / Artifact references are projected only through:

`Knowledge → Work → existing output truth`

No direct Knowledge→Result relation was added. Missing output truth is shown as no related result.

## 6. Archive and Delete Protection

- Referenced Knowledge can be archived without breaking historical resolution.
- Archived Knowledge cannot be newly attached to Work.
- A database trigger rejects hard delete while a typed reference exists.
- Missing local source does not delete the Knowledge record; the UI reports source unavailability honestly.

## 7. API and Service Surface

The existing Knowledge API was extended for canonical create/import/list/filter, bounded offset batches, recent-use ordering, Work reference read/write, reverse Used By, related outputs and archive.

All routes reuse `KnowledgeService`; `main.py` does not maintain a second ownership resolver.

## 8. Accepted Frontend

The implementation consumes Figma `187:2`, `187:276`, `187:550` and `187:824` as product structure, not fixture truth.

- Overview: real counts, recent/common/attention/source coverage, add/import actions.
- Browse/Search: row-first layout, scope/source/sort controls, true snippets and explicit load more.
- Detail: reading-first body, source/scope/status, Used By and related outputs; IDs/hash remain collapsed technical details.
- Work Picker: real Work problem/expected result, only legally scoped records, existing refs disabled, persisted selection and exact return.
- General Workspace: each persisted Work exposes `添加参考资料` with its real `work_ref`; the inert composer control was not repurposed because it has no persisted Work identity.

No Figma fixture data is used in production.

## 9. Scale and Return Restoration

The isolated acceptance state contains 105 Knowledge records across Company, Business and Workspace scopes.

- first batch: 30 rows;
- explicit load more: 60 visible after one action;
- exact search: one expected match;
- filters and sort remain query-driven;
- list/detail return uses query plus session state for filter, loaded batches and scroll restoration;
- canonical data is never written for UI navigation state.

## 10. Runtime / Failure Evidence

Isolated Browser root: `/tmp/curis-knowledge-browser.HrpdjR`

- a canonical Work consumed explicit Knowledge through the real employee execution seam;
- a deterministic local provider produced a real ResultStore task and persisted result reference;
- reverse Knowledge→Work→Result was readable after reopen;
- cross-company and cross-tenant references were rejected;
- archived reference addition and referenced hard delete were rejected;
- backend stop produced the user-facing runtime read failure with retry; restart recovered the same data;
- no external live-model quality or cost claim is made.

## 11. Browser Acceptance

At 1440×900, the isolated Browser run verified Overview, Browse, Search, Load More, reading-first Detail, real Work context in the picker, existing-reference disable state, typed reference write, exact return and backend failure/recovery. Unexpected console errors and warnings: 0.

Evidence:

- `/tmp/curis-knowledge-library-evidence/browser-overview.png`
- `/tmp/curis-knowledge-library-evidence/browser-browse.png`
- `/tmp/curis-knowledge-library-evidence/browser-detail.png`
- `/tmp/curis-knowledge-library-evidence/browser-picker.png`

## 12. Fresh Packaged Desktop Acceptance

Fresh application:

`/Users/yy/Documents/Curis AI Workspace/desktop/target/release/bundle/macos/Curis.app`

Executable SHA-256:

`cabc9d9be89ec65af2511c3670ace505a6668979d542ca7c062d0b2c943c5f5a`

Isolated app-data: `/tmp/curis-knowledge-desktop.HannLb`

The fresh package verified Overview, Browse, Detail, real Work entry, Work Picker, one new persisted reference, exact Workspace return and reverse Used By/Result projection. The acceptance fixture's originally incomplete Generic Workspace snapshot was repaired only in isolated data by applying the existing `CanonicalBusinessSpine._generic_blueprint` shape and initial-version semantics; no production workaround was added.

The Work's reference count moved from 3 to 4 through the packaged UI. Curis and all three sidecars then exited completely. Relaunching the same package with the same isolated app-data restored 105 Knowledge records, 4 Work references, recent-use ordering, detail Used By and related Result truth.

Evidence:

- `/tmp/curis-knowledge-library-evidence/desktop-overview.png`
- `/tmp/curis-knowledge-library-evidence/desktop-browse.png`
- `/tmp/curis-knowledge-library-evidence/desktop-detail.png`
- `/tmp/curis-knowledge-library-evidence/desktop-picker.png`
- `/tmp/curis-knowledge-library-evidence/desktop-picker-return.png`
- `/tmp/curis-knowledge-library-evidence/desktop-restart.png`

Packaged logs contained no traceback, unhandled exception, 500 error or frontend runtime error. `D1 toolchain unavailable` remained an honest optional-capability message and did not affect Knowledge acceptance.

## 13. Persistence Evidence

The final packaged isolated SQLite reported:

- `knowledge_entries = 105`
- `Work USES_REFERENCE = 4`
- `runtime_workspace_versions = 1`
- `pragma integrity_check = ok`

Persistence is backed by SQLite and reread after a complete process/sidecar stop, not by frontend memory.

## 14. Tests and Build

- Backend focused + shared no-regression: **43 passed**.
- Frontend Knowledge contract: **1 passed**.
- Target ESLint: PASS.
- Python compile: PASS.
- Frontend production build: PASS.
- Fresh Workspace/Gateway/Guardian runtime build: PASS.
- Fresh Cargo/Tauri `Curis.app` build: PASS.
- `git diff --check`: PASS.

Covered regressions include General Workspace contract/P1, canonical usage attribution, Team Operating real Employee E2E, RD real execution, XHS Calendar/Note Runtime and Backend DB Safety.

## 15. Active DB Safety

Both repository active SQLite files remained byte-identical from preflight to final verification:

- `data/curis.sqlite`: size `1232896`, mtime `1786873339`, SHA-256 `2ea2506f90f764e834d47d8f6bae3cb41c22d457757e0e9216c0ae8c39a39ec6`, integrity `ok`
- `backend/data/curis.sqlite`: size `1277952`, mtime `1786783659`, SHA-256 `a9d96a9536a5bce3b3b30f912e86a37f61d28527a8eb2d35af7a5857d29414e4`, integrity `ok`

All schema, migration, Runtime, Browser and Desktop work used repository-external SQLite.

## 16. Changed Files

Owned implementation scope:

- `backend/app/database.py`
- `backend/app/knowledge_service.py`
- `backend/app/api/team_operating_router.py`
- `backend/app/main.py`
- `frontend/app/ceo-office/knowledge/page.js`
- `frontend/app/ceo-office/knowledge/entries/[id]/page.js`
- `frontend/lib/knowledge.js`
- `frontend/components/v1/GeneralWorkspaceOperating.js` — exact Work picker entry only
- `backend/tests/test_v1_knowledge_library_productization.py`
- `backend/tests/test_mvp_phase5_s10_knowledge_management.py` — exact stale assertion migration only
- `frontend/tests/knowledgeLibraryProductization.test.mjs`
- current Issue and this Review

The repository's unrelated preserved dirty/untracked state was not reset, cleaned, staged, committed or pushed.

## 17. Remaining P1 / P2

Not implemented by design:

- PDF, DOCX, image, web or external Knowledge connectors;
- semantic/vector search, RAG, Knowledge Graph;
- source versions or paragraph anchors;
- automatic promotion/dedup/conflict engine;
- full retention/ACL platform;
- external live-provider quality or cost validation.

These are not blockers for the accepted V1 manual and local `.md` / `.txt` Company Reference Space.

## Final Decision

**EMPLOYEE / WORK KNOWLEDGE REFERENCE: IMPLEMENTED**

**KNOWLEDGE LIBRARY: IMPLEMENTED / ACCEPTED CANDIDATE**

**NO COMMIT · NO PUSH**
