# CURIS-V1-OPERATING-INTELLIGENCE-PRODUCTIZATION-001

Status: Review
Authority Class: CURRENT IMPLEMENTATION ISSUE
Date: 2026-08-31
Owner: Main Development Session

## Goal

将已接受的 Operating Intelligence Figma `172:3 / 172:277 / 172:551 / 172:825` 接到 canonical Company / Business / Workspace / Work / Execution / Result / Evidence / Usage / Cost / Acceptance truth，形成 analyst-first 的概览、作用域分析、同口径比较和 Report → P7 Decision 连续性；未知优先于虚构。

## Authority

- `docs/reviews/CURIS_V1_OPERATING_INTELLIGENCE_UI_ACCEPTANCE.md`（Frozen）
- Figma `2Fh7DgPPfLgdbvNtnzPnk9`：`172:3`、`172:277`、`172:551`、`172:825`
- `docs/reviews/CURIS_V1_PRODUCT_COMPLETION_RECONCILIATION.md`
- `docs/reviews/CURIS_V1_THREE_AREA_DESIGN_ASSET_RECOVERY.md`
- Current Result / Evidence、Usage Attribution、Execution、Decision P7 Authority
- `docs/00_Context/CURRENT_STATE.md`

## Pre-change Ownership

| Path | SHA-256 | Ownership decision |
|---|---|---|
| `frontend/app/ceo-office/analytics/page.js` | `e45c5244c7e072137a39c559e9f64716220d825d7e8c5227feadd4976de98c80` | Mixed source. 本 Issue 只拥有 canonical route delegation；旧 Dashboard 保留为命名 legacy export。 |
| `frontend/lib/runtimeApi.js` | `bb2dc7eae2ba9b4ec2f6b6050f50dced0a7b2bce91e31c9156d34959c252d330` | Mixed source. 本 Issue 只拥有 Operating Intelligence API wrappers。 |
| `backend/app/api/runtime_foundation_router.py` | `a9bb8bff6bdb55767653b7777aaa1ff72f804f19917dd105750269e48707a9d4` | Mixed source. 本 Issue 只拥有一个 import、bounded endpoints 与 Decision report reference safe projection keys。 |

## Data Source Matrix

| Fact | Current source | Truth |
|---|---|---|
| Company / Business / Workspace | `companies` / `canonical_businesses` / resolved `workspaces` | VERIFIED |
| Employee / Team | `employee_instances` + canonical assignment / execution identity | PARTIAL |
| Work / Execution | `runtime_entities(WORK)` / `tasks` / `executions` / usage execution refs | VERIFIED |
| Result / Acceptance | `artifacts` / `runtime_entities(ACCEPTANCE)` | PARTIAL |
| Evidence | `runtime_entities(EVIDENCE)` + Artifact source refs | VERIFIED when source is present |
| Usage | append-only `ai_usage_records` canonical or legacy verified lineage | VERIFIED |
| Cost | `provider_reported` verified; `estimated` separately labelled; unknown omitted | PARTIAL |
| Latency / duration | `ai_usage_records.latency_ms`; no value means unknown | PARTIAL |
| Failure | Task / provider execution status | VERIFIED |
| Feedback / Review | Acceptance / artifact review entities where present | PARTIAL |
| External outcome | Connector-backed Outcome / receipt only | MISSING in current acceptance state |
| Report | existing `Artifact` with `artifact_type=analysis_report` | PARTIAL; no second Report object |

## Allowed Files

- `backend/app/operating_intelligence.py`
- `backend/app/api/runtime_foundation_router.py` — exact import/input/endpoint hunks only
- `backend/tests/test_operating_intelligence_projection.py`
- `frontend/app/ceo-office/analytics/page.js` — exact canonical delegation hunks only
- `frontend/app/ceo-office/analytics/OperatingIntelligence.js`
- `frontend/lib/runtimeApi.js` — exact API wrapper hunks only
- `frontend/tests/operatingIntelligence.test.mjs`
- this Issue
- `docs/reviews/CURIS_V1_OPERATING_INTELLIGENCE_PRODUCTIZATION_REVIEW.md`

Any expansion requires Issue amendment. No Schema, active DB, Metric Store or new Report/Decision object is authorized.

## Projection Contract

- Read-time derived only; source refs, time window, freshness, verification, sample size and unknown reason travel with every metric.
- 7D / 30D current and previous windows.
- Company and canonical Business scope; Workspace facts remain scoped through canonical parent relation.
- Cost, speed, quality/acceptance and failure stay separate.
- Comparison requires same metric, period, definition and sufficient samples; otherwise `NOT_COMPARABLE`.
- External outcomes remain `MISSING / 待连接`; never `0`.

## Report / Decision Continuity

- Only persisted `analysis_report` Artifact is a report.
- Report content must carry scope, period, facts, analysis, unknown, recommendation, evidence refs, author and created time.
- “提交为决策” reuses canonical `DECISION_PACKET`; the Packet links back to the report Artifact and Evidence refs.
- No `AnalyticsDecision`, no `ReportApproval`, no second CEO Assistant.

## Tests / Acceptance

- Projection truth and provenance; 7D/30D baseline; freshness/unknown.
- Business scope isolation and cross-tenant rejection.
- Cost source separation; latency/failure/acceptance derivation.
- Comparable and deliberately non-comparable cases.
- Existing report Artifact projection and same canonical Decision continuity.
- Restart persistence without derived-cache authority.
- Frontend overview/scoped/benchmark/report/empty/error states.
- Browser and fresh Packaged Desktop, console 0.
- Relevant CEO Desk / Organization / General Workspace / Result-Evidence / P7 / Employee / Usage / DB Safety regression.

## Stop Gates

- A second Metric Truth or new canonical Report object is required.
- Canonical Decision cannot safely reference the report/evidence.
- Cost/Usage semantics conflict with accepted attribution.
- Unauthorised Schema or active DB mutation.

## Non-goals

- No Product/Figma redesign, KPI dashboard, Health Score, Metric Registry platform, external Connector, new analytics Runtime, second Decision/Assistant, Dark/1024 polish, release, commit or push.

## Implementation Result

- Read-only projection：Company / canonical Business scope、7/30 天 current/baseline、Usage/Acceptance 来源、Unknown 与 comparable gate。
- Report：只读取现有 `analysis_report` Artifact；未自动生成 Report。
- Decision：只复用 canonical `DECISION_PACKET`，并验证 recommendation/evidence provenance。
- Browser 与 fresh packaged Desktop：概览、业务范围、比较、报告、P7、完全退出/同根重启均已实际验证。
- 外部 Outcome / Connector：仍为 `MISSING / 待连接`。
- 当前状态：`IMPLEMENTED / ACCEPTED CANDIDATE`，等待 CEO / ChatGPT Review。
