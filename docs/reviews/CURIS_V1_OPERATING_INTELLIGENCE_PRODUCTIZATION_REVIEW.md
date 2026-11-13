# CURIS V1 OPERATING INTELLIGENCE PRODUCTIZATION REVIEW

Status: Review
Authority Class: REVIEW
Date: 2026-08-31
Issue: `CURIS-V1-OPERATING-INTELLIGENCE-PRODUCTIZATION-001`

## Verdict

**OPERATING INTELLIGENCE: IMPLEMENTED / ACCEPTED CANDIDATE**

The accepted Operating Intelligence composition is implemented over current canonical facts. Unknown remains distinct from zero, comparisons require a compatible definition and sample, and reports/decisions reuse existing Artifact and P7 truth. This Review does not create Product Authority or claim external business outcomes that are not connected.

## 1. Legacy Reconciliation

- `KEEP`: the legacy analytics implementation remains available as the named `LegacyOperatingPage` export for callers outside the current canonical route.
- `REWIRE`: `/ceo-office/analytics` now delegates to the accepted `OperatingIntelligence` surface.
- `SUPERSEDED IN CURRENT PATH`: KPI dashboard cards, fixture charts and inferred health scores are not consumed by the canonical route.
- `PRESERVED`: the mixed-source page was not bulk-promoted or cleaned; this Issue owns only the import/default-delegation seam.

## 2. Accepted Figma Implementation

Consumed implementation references from Figma `2Fh7DgPPfLgdbvNtnzPnk9`:

- `172:3`: company overview.
- `172:277`: scoped analysis.
- `172:551`: comparable Business view.
- `172:825`: report and decision continuity.

Implemented the accepted analyst-first hierarchy, top local tabs, 7/30-day controls, restrained Direction D surfaces, source-first facts, scoped comparison and report detail. Figma fixtures were not copied into production data.

## 3. Current Data Source Matrix

| Fact | Canonical source | Current truth |
|---|---|---|
| Company / Business / Workspace | `companies`, `canonical_businesses`, `workspaces` | VERIFIED |
| Employee / analyst | `employee_instances` plus canonical Company relation | PARTIAL; only a real matching Employee is shown |
| Work / execution | `runtime_entities`, `tasks`, `executions`, usage execution refs | VERIFIED where referenced |
| Result / acceptance | `artifacts`, `runtime_entities(ACCEPTANCE)` | PARTIAL |
| Evidence | `runtime_entities(EVIDENCE)` and owned Artifact/Usage refs | VERIFIED when present |
| Usage | append-only `ai_usage_records` with verified lineage | VERIFIED |
| Cost | provider-reported preferred; estimate labelled and excluded when reported truth exists | PARTIAL |
| Latency | `ai_usage_records.latency_ms` | PARTIAL; missing stays unknown |
| External outcome | connector-backed Outcome/receipt only | MISSING in the acceptance scenario |
| Report | existing `Artifact(analysis_report)` | PARTIAL; no automatic report generation |
| Decision | canonical `DECISION_PACKET` | VERIFIED |

No Metric Store, Analytics database, report table or second Decision system was introduced.

## 4. Overview

The overview presents a real Company scope, a real analyst Employee when one exists, current period facts, prior-period deltas, source coverage and external-result availability. The acceptance scenario showed provider cost `CNY 10.00`, latency P50 `195 ms`, acceptance rate `50%` and failure rate `25%`, each backed by source references and sample counts.

## 5. Scoped Analysis

The scope selector reads canonical Company and Business identities. Selecting `内容增长` produced only that Business's verified records and preserved the Company parent. Wrong-Business and cross-tenant references fail closed.

## 6. Comparable Benchmark

Business comparison requires the same metric definition, period, unit/currency and a minimum sample of two. Mixed currencies are not summed and results lacking a compatible basis are shown as `不可比较`; no ranking or winner is inferred.

## 7. Analyst Truth

The acceptance scenario projected the persisted Employee `衡川 / 经营分析师`. A missing analyst does not create a synthetic Employee, provider identity or autonomous analysis claim.

## 8. 7 / 30 Day Windows

Both windows resolve deterministic current and immediately preceding ranges. Baseline deltas carry current/baseline samples and source timestamps. Restart recomputes from persisted source truth; no derived cache becomes authority.

## 9. Unknown / Provenance

- `UNKNOWN`, `MISSING` and `NOT_COMPARABLE` are formal outcomes and never rendered as zero.
- Every metric carries source refs, freshness, verification, sample size, definition and an unknown reason when needed.
- Provider-reported cost is not mixed with estimates. Multiple currencies remain unknown instead of producing a false total.
- External outcomes remain `待连接`; no views, revenue, conversion or feedback value is invented.

## 10. Analysis Report

The report tab reads only persisted `analysis_report` Artifacts. It presents fact, analysis, unknown, recommendation, author, creation time and reference-first Evidence. Empty state states that no report exists; it does not synthesize one from dashboard data.

## 11. P7 Decision Continuity

Submitting an eligible report creates or returns exactly one deterministic canonical `DECISION_PACKET`. The Runtime validates option/recommendation provenance and verifies every Evidence reference belongs to the same Company before transition:

`DRAFT → READY → WAITING_CEO`

The Packet stores the report reference and SHA-256. It uses high-risk Layer 0 actions `查看方案 / 暂缓`; no one-line approval is exposed. Browser and Packaged Desktop both reread the same `WAITING_CEO` Packet after restart.

## 12. Loading / Empty / Error

- Loading uses the shared Runtime loading pattern.
- No usage/acceptance data yields unknown and honest empty guidance, not `0` metrics.
- No report yields an explicit report empty state.
- Projection failure uses shared error/retry behavior and never falls back to legacy fixtures.

## 13. Canonical Projection

Added one bounded read projection and two API seams:

- `GET /api/workspace/runtime/foundation/companies/{company_id}/operating-intelligence`
- `POST /api/workspace/runtime/foundation/companies/{company_id}/operating-intelligence/reports/{artifact_id}/decision`

The projection consumes existing Company, canonical Business/Workspace, Employee, Usage, Artifact, Result/Evidence, Acceptance and Decision truth. It adds no schema and owns no writes except the existing canonical Decision transition.

## 14. Restart

Browser evidence used repository-external SQLite `/tmp/curis-operating-browser.U4tpgj/operating.sqlite`. After backend stop/restart, Company/Business metrics, the report Artifact, its Evidence reference and the same P7 Packet remained readable.

Final Packaged Desktop evidence used isolated root `/tmp/curis-operating-desktop-final.Q4FWf2`. Full application exit stopped ports `3010/8002/8080`; reopening the same root restored the same metrics, report and `WAITING_CEO` decision. Persistence was not treated as proof that an external Employee or provider remained active.

## 15. Browser

Browser acceptance passed:

- Overview with real analyst, current facts, prior-period deltas and source coverage.
- Business-scoped analysis and intentionally non-comparable facts.
- Existing report Artifact, owned Evidence and canonical P7 action.
- backend restart and reread of the same report/decision.
- browser console errors: `0`.

Evidence:

- `/tmp/curis-operating-browser.U4tpgj/operating-overview-browser.png`
- `/tmp/curis-operating-browser.U4tpgj/operating-report-browser.png`

## 16. Packaged Desktop

Fresh current-source build:

- App: `/Users/yy/Documents/Curis AI Workspace/desktop/target/release/bundle/macos/Curis.app`
- Binary: `/Users/yy/Documents/Curis AI Workspace/desktop/target/release/bundle/macos/Curis.app/Contents/MacOS/curis-desktop`
- Binary SHA-256: `cabc9d9be89ec65af2511c3670ace505a6668979d542ca7c062d0b2c943c5f5a`

Fresh frontend standalone build, Workspace/Gateway/Guardian sidecars and Cargo/Tauri bundle all passed. Native interaction verified Overview, scoped analysis, report, Evidence and P7 state. The app was fully closed and reopened against the same isolated root. Operating Intelligence requests returned HTTP `200`; no HTTP `5xx` was recorded. A `BrokenPipeError` in the Gateway log was produced only by the test harness's explicit `Ctrl-C` shutdown, not by a product request.

Evidence:

- `/tmp/curis-operating-desktop-final.Q4FWf2/operating-overview-desktop.png`
- `/tmp/curis-operating-desktop-final.Q4FWf2/operating-report-desktop.png`

## 17. Tests / Build

- Backend focused: `6 passed`.
- Backend relevant no-regression: `53 passed` (Operating Intelligence, Organization, canonical Usage, Responsibility, Team Employee E2E, RD P7, General Workspace, Talent, DB Safety and Result/Evidence).
- Frontend focused: `3 passed`.
- Frontend relevant no-regression: `34 passed`, `0 failed`.
- Python compile: PASS.
- Scoped ESLint: PASS.
- Frontend production build: PASS.
- Fresh PyInstaller sidecars and Cargo/Tauri build: PASS.
- `git diff --check`: PASS.

A broader diagnostic still finds four stale source-contract assertions in the unrelated legacy `runtimeProvider.test.mjs`; they target pre-migration component names and are outside this Issue's Allowed Files. Relevant RuntimeProvider behavior used by the current surface was covered by the accepted regression set.

## 18. Active DB Safety

Both active databases remained byte-identical from preflight to closeout:

| Path | Size | mtime | SHA-256 | integrity_check |
|---|---:|---:|---|---|
| `data/curis.sqlite` | `1232896` | `1786873339` | `2ea2506f90f764e834d47d8f6bae3cb41c22d457757e0e9216c0ae8c39a39ec6` | `ok` |
| `backend/data/curis.sqlite` | `1277952` | `1786783659` | `a9d96a9536a5bce3b3b30f912e86a37f61d28527a8eb2d35af7a5857d29414e4` | `ok` |

No active DB initialization, migration or write occurred.

## 19. Remaining P1 / P2

- Real external business Outcome/feedback Connector is not connected.
- Cost and latency remain available only where the canonical Usage ledger has evidence.
- Automated analyst/report authoring is not implemented; this version projects a real Employee and existing report Artifact only.
- Capability/model scoped analysis remains omitted until current facts justify it.
- 1024/Dark visual polish is P2.
- External live-provider cost accuracy and real-world outcome quality were not verified by this bounded productization task.

These gaps do not invalidate the honest Company/Business insight candidate.

## 20. Changed Files

Issue-owned implementation:

- `backend/app/operating_intelligence.py`
- `backend/app/api/runtime_foundation_router.py` — one import, service initialization, bounded endpoints and report-reference safe-projection hunks only
- `backend/tests/test_operating_intelligence_projection.py`
- `frontend/app/ceo-office/analytics/page.js` — canonical import/default-delegation hunks only; prior mixed content preserved
- `frontend/app/ceo-office/analytics/OperatingIntelligence.js`
- `frontend/lib/runtimeApi.js` — Operating Intelligence wrappers only; prior mixed content preserved
- `frontend/tests/operatingIntelligence.test.mjs`
- `issues/CURIS-V1-OPERATING-INTELLIGENCE-PRODUCTIZATION-001.md`
- this Review

No commit and no push were performed. Parallel governance documents were not modified.

## Final Decision

**OPERATING INTELLIGENCE: IMPLEMENTED / ACCEPTED CANDIDATE**

CEO / ChatGPT final implementation acceptance remains the next gate.
