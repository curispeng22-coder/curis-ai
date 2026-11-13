# Tasks

Status: Deprecated

## Current Gate State

- Current phase: Phase-1C CEO Office UI First Slice.
- Current executable Issue: `issues/phase1c_ceo_office_ui_first_slice.md`.
- Current owner: 系统交付席.
- Implementation status: approved for bounded frontend-only implementation.
- Design source of truth: `docs/design/phase1c-ceo-office-ui-v3.md`.
- Runtime baseline evidence: `issues/phase1a_ai_company_runtime_foundation.md` and `docs/release/phase1-company-runtime-foundation-report.md`.

## Active

| ID | Task | Owner | Status | Verification |
| --- | --- | --- | --- | --- |
| T-224 | Implement Phase-1C CEO Office UI first slice | 系统交付席 | TODO | `issues/phase1c_ceo_office_ui_first_slice.md`; expected review `reviews/phase1c_ceo_office_ui_first_slice_review.md` |
| T-137 | Decide next bounded phase after execution summary memory | 产品规划席 | DONE | Chose Option A: open ADR-0017 future gate (2026-07-07) |
| T-138 | Review ADR-0017 future gate (issues/049 + 050) | 总控决策席 | DONE | Option a accepted — gate OPEN (2026-07-07) |
| T-139 | Accept ADR-0017 D1 `tenant_id` reservation (boundary + implementation) | 主理人(齐活林) | DONE | issue 051 accepted 2026-07-07 23:27 (slice acceptance delegated to 主理人) |
| T-140 | Open ADR-0017 D2 reservation gate (pre-authorized under option a) | 主理人(齐活林) | DONE | ADR-0017 option-a roadmap pre-authorizes D1–D4 design-only reservations; escalate only on conflict/scope-expansion |
| T-141 | Accept ADR-0017 D2 reservation boundary (design-only) | 主理人(齐活林) | DONE | issue 052 accepted 2026-07-07 23:27 |
| T-142 | Implement ADR-0017 D2 reservation (T01–T05: manifest+catalog contracts, department_types table + seed, read-only DepartmentCatalog, tests) | 系统交付席 (Kou) | DONE | c8a30781 (4 files +459) |
| T-143 | Verify ADR-0017 D2 reservation implementation | 质量运行席 (Yan) | DONE | reviews/053 PASS-WITH-NOTES, 81 tests green, routing NoOne |
| T-144 | Accept ADR-0017 D2 reservation slice | 主理人(齐活林) | DONE | issue 052 closed 2026-07-08 (产品规划席 delegation) |
| T-145 | Define ADR-0017 D3 (self-observability) reservation boundary | 系统交付席 (Gao) | DONE | ADR-0024 + issues/054, Yan boundary verify reviews/054 PASS-WITH-NOTES |
| T-146 | Define ADR-0017 D4 (two-tier governance) reservation boundary | 系统交付席 (Gao) | DONE | superseded-by T-150 (same boundary work) |
| T-147 | Implement ADR-0017 D3 reservation (T01–T04: observability facade + DepartmentMetrics, tests, forbidden-scope guards) | 系统交付席 (Kou) | DONE | 22c5cd55 (2 files +287) |
| T-148 | Verify ADR-0017 D3 reservation implementation | 质量运行席 (Yan) | DONE | reviews/055 PASS-WITH-NOTES, 90 tests green, routing NoOne |
| T-149 | Accept ADR-0017 D3 reservation slice | 主理人(齐活林) | DONE | issue 054 closed 2026-07-08 (产品规划席 delegation) |
| T-150 | Define + verify + accept ADR-0017 D4 (two-tier governance) reservation boundary | 系统交付席 (Gao) + 质量运行席 (Yan) + 主理人(齐活林) | DONE | ADR-0025 + issues/055 + reviews/056 (Yan PASS-WITH-NOTES) + reviews/057 (主理人 accept+gate), 2026-07-08 |
| T-151 | Implement ADR-0017 D4 reservation (T01–T04: governance.py read-only facade + dataclasses, test_d4_governance.py, zero schema delta) | 系统交付席 (Kou) | DONE | b97728d4 (2 files +393: governance.py / test_d4_governance.py), 100 tests green, zero schema delta |
| T-152 | Verify ADR-0017 D4 reservation implementation | 质量运行席 (Yan) | DONE | reviews/058 PASS-WITH-NOTES, 100 tests green, routing NoOne, b9302e39 |
| T-153 | Accept ADR-0017 D4 reservation slice | 主理人(齐活林) | DONE | issue 055 CLOSED 2026-07-08 (产品规划席 delegation); ADR-0017 D1✅D2✅D3✅D4✅ reservations all收口 |
| T-154 | Approve D2.impl (部门真实实例化) independent small gate | 总控决策席 + 安全边界席 | DONE | ADR-0026 + issue 056 gate approved 2026-07-08 (超出 ADR-0017 option-a 预授权) |
| T-155 | Implement D2.impl (T01–T03: departments table + DepartmentCatalog 真实方法 + 测试) | 系统交付席 (Kou) | DONE | 7617ed2c (+4ec02a59 一致性修复), 114 tests green |
| T-156 | Verify D2.impl implementation | 质量运行席 (Yan) | DONE | reviews/059 PASS-WITH-NOTES, routing NoOne, 114 tests green, 67ab1616 |
| T-157 | Accept D2.impl slice | 主理人(齐活林) | DONE | issue 056 CLOSED 2026-07-08 (产品规划席 delegation); ADR-0017 首个真实实现切片收口 |
| T-158 | Implement Workspace Capability Integration Phase-1 | 系统交付席 | DONE | issues/064_workspace_capability_integration_phase_1.md implemented; reviews/061 PASS; ADR-0028 Workspace catalog + UsageEvent first slice; 159 backend tests green |
| T-159 | Implement Workspace Model Gateway Adapter | 系统交付席 | DONE | issues/065_workspace_model_gateway_adapter.md implemented; reviews/062 PASS; 161 backend tests green; default model calls route through New API-compatible ModelGatewayAdapter |
| T-160 | Implement Workspace Official Model Catalog | 系统交付席 | DONE | issues/066_workspace_official_model_catalog.md implemented; reviews/063 PASS; 163 backend tests green; Workspace can read active official model catalog metadata |
| T-161 | Implement Workspace Official Tool Catalog | 系统交付席 | DONE | issues/067_workspace_official_tool_catalog.md implemented; reviews/064 PASS; 163 backend tests green; Workspace can read active official tool catalog metadata |
| T-162 | Prepare New API local deployment | 系统交付席 | DONE | New API container is running locally with DeepSeek channel; `/v1/models` and `/v1/chat/completions` verified; Workspace run writes required usage_event |
| T-163 | Define Model Gateway production security boundary | 安全边界席 | DONE | ADR-0029 + reviews/066 PASS-WITH-GUARDRAILS; production follow-up `issues/070_model_gateway_runtime_secret_guardrails.md` required before production external-model operation |
| T-164 | Implement Model Gateway runtime secret guardrails | 系统交付席 | DONE | issues/070 implemented; reviews/067 evidence; 16 focused guardrail tests and 203 backend tests green |
| T-165 | Verify Model Gateway runtime secret guardrails | 质量运行席 | DONE | reviews/067 Quality Verification PASS; 16 focused guardrail tests and 203 backend tests green; secret/scope/frontend guards passed; routed to 产品规划席 |
| T-166 | Accept Model Gateway runtime secret guardrails | 产品规划席 | DONE | Accepted reviews/067 quality evidence; commit b01edfd4 verified with 16 focused guardrail tests and 203 backend tests green |
| T-167 | Review Workspace Tenant Model Preference Foundation gate | 总控决策席 | DONE | Approved 2026-07-08; route to 系统交付席 for boundary definition |
| T-168 | Define Workspace Tenant Model Preference Foundation boundaries | 系统交付席 | DONE | ADR-0030 + reviews/068; backend-only metadata preference boundary ready for quality verification |
| T-169 | Verify Workspace Tenant Model Preference Foundation boundaries | 质量运行席 | DONE | reviews/068 Quality Verification PASS for commit 9dd75340; boundary-only scope preserved |
| T-170 | Accept Workspace Tenant Model Preference Foundation boundaries | 产品规划席 | DONE | Accepted reviews/068; opened issues/072 backend-only first slice |
| T-171 | Implement Workspace Tenant Model Preference first slice | 系统交付席 | DONE | issues/072 implemented; reviews/069 evidence; 4 focused tenant preference tests and 207 backend tests green |
| T-172 | Verify Workspace Tenant Model Preference first slice | 质量运行席 | DONE | reviews/069 Quality Verification PASS; commit a0d3a54b, 4 focused tests and 207 backend tests green; secret/scope/frontend guards passed |
| T-173 | Accept Workspace Tenant Model Preference first slice | 产品规划席 | DONE | Accepted reviews/069 quality evidence for commit a0d3a54b; 4 focused tests and 207 backend tests green |
| T-174 | Review Workspace Model Preference UI gate | 总控决策席 | DONE | Approved 2026-07-08; route to 系统交付席 for frontend-only selector |
| T-175 | Implement Workspace Model Preference UI first slice | 系统交付席 | DONE | issues/073 implemented; reviews/070 evidence; 14 frontend view-model tests, lint, and build green |
| T-176 | Verify Workspace Model Preference UI first slice | 质量运行席 | DONE | reviews/070 Quality Verification PASS; commit 5727410f, 14 frontend tests/lint/build green; backend/Admin/shared guard passed |
| T-177 | Accept Workspace Model Preference UI first slice | 产品规划席 | DONE | Accepted reviews/070 quality evidence for commit 5727410f; 14 frontend tests, lint, and build green |
| T-178 | Verify Workspace Model Preference local E2E evidence | 质量运行席 | DONE | reviews/071 PASS; real local backend/frontend verified preference read/save/reset and Task API content-only boundary |
| T-179 | Review Model Gateway Local Demo Release Candidate gate | 总控决策席 | DONE | Approved 2026-07-08; route to 系统交付席 for documentation/evidence-only RC package |
| T-180 | Prepare Model Gateway Local Demo Release Candidate package | 系统交付席 | DONE | docs/release/model-gateway-local-demo-rc.md + reviews/072; documentation/evidence only |
| T-181 | Verify Model Gateway Local Demo Release Candidate package | 质量运行席 | DONE | reviews/072 Quality Verification PASS for commit 9bfc7d8b; evidence map, runbook, known gaps, source-of-truth, and behavior-file guard passed |
| T-182 | Accept Model Gateway Local Demo Release Candidate package | 产品规划席 | DONE | reviews/072 accepted by 产品规划席 on 2026-07-08; local/demo RC package accepted, hosted production remains blocked |
| T-183 | Review Model Gateway Post-RC Next Phase gate | 总控决策席 | DONE | Option A approved 2026-07-08; route to 系统交付席 for documentation/evidence-only release closeout |
| T-184 | Prepare Model Gateway Local Demo first-version release closeout | 系统交付席 | DONE | docs/release/model-gateway-local-demo-first-version-release-record.md + reviews/073; documentation/evidence only |
| T-185 | Verify Model Gateway Local Demo first-version release closeout | 质量运行席 | DONE | reviews/073 Quality Verification PASS for commit 0801231d; release decision, operator handoff, checklist, known gaps, source-of-truth, secret scan, and behavior-file guard passed |
| T-186 | Accept Model Gateway Local Demo first-version release closeout | 产品规划席 | DONE | reviews/073 accepted by 产品规划席 on 2026-07-08; local/demo first-version release closeout completed, hosted production remains blocked |
| T-187 | Review post-first-version Workspace Company Foundation gate | 总控决策席 | DONE | Option A approved 2026-07-08; route to 系统交付席 for Workspace Company Foundation boundary definition |
| T-188 | Define Workspace Company Foundation boundaries | 系统交付席 | DONE | ADR-0031 + reviews/074; boundary-only, no behavior changes |
| T-189 | Verify Workspace Company Foundation boundaries | 质量运行席 | DONE | reviews/074 Quality Verification PASS for commit 651bdb99; boundary-only scope, forbidden locks, first-slice boundary, read-model gap rule, source routing, and behavior guard passed |
| T-190 | Accept Workspace Company Foundation boundaries | 产品规划席 | DONE | reviews/074 accepted by 产品规划席 on 2026-07-08; ADR-0031 accepted as boundary, implementation remains separately gated |
| T-191 | Review Workspace Company Foundation first-slice gate | 总控决策席 | DONE | Option A approved 2026-07-08; route to 系统交付席 for frontend-only local/demo company frame |
| T-192 | Implement Workspace Company Foundation first slice | 系统交付席 | DONE | reviews/075 READY_FOR_QUALITY_VERIFICATION; frontend-only company frame, 16 frontend tests/lint/build evidence, no backend/API/schema/runtime changes |
| T-193 | Verify Workspace Company Foundation first slice | 质量运行席 | DONE | reviews/075 Quality Verification PASS for commit dfd60689; 16 frontend tests, lint, build, API/payload scan, forbidden-scope scan, secret scan, and behavior guard passed |
| T-194 | Accept Workspace Company Foundation first slice | 产品规划席 | DONE | reviews/075 accepted by 产品规划席 on 2026-07-08; frontend-only local/demo company frame accepted for first Workspace Company Foundation slice |
| T-195 | Review Workspace Company Foundation local/demo evidence gate | 总控决策席 | DONE | Option A approved 2026-07-08; route to 质量运行席 for verification-only local/demo evidence |
| T-196 | Verify Workspace Company Foundation local/demo evidence | 质量运行席 | DONE | reviews/076 PASS; browser-visible screenshot evidence captured, local backend/frontend smoke passed, no secret-like metadata found |
| T-197 | Accept Workspace Company Foundation local/demo evidence | 产品规划席 | DONE | reviews/076 accepted by 产品规划席 on 2026-07-08; verification-only evidence closed |
| T-198 | Review Workspace Company Department Catalog Summary gate | 总控决策席 | DONE | Option A approved 2026-07-08; route to 系统交付席 for frontend-only summary using existing read-only catalog API |
| T-199 | Implement Workspace Company Department Catalog Summary | 系统交付席 | DONE | reviews/077 accepted; frontend-only existing company frame, existing GET /api/catalog/department-types only |
| T-200 | Verify Workspace Company Department Catalog Summary | 质量运行席 | DONE | reviews/077 PASS; 18 frontend tests, lint, build, API scan, and forbidden-scope scan passed |
| T-201 | Accept Workspace Company Department Catalog Summary | 产品规划席 | DONE | reviews/077 accepted by 产品规划席 on 2026-07-08 |
| T-202 | Review Workspace Department Catalog local/demo evidence gate | 总控决策席 | DONE | Option A approved 2026-07-08; verification-only browser evidence for accepted department summary |
| T-203 | Verify Workspace Department Catalog local/demo evidence | 质量运行席 | DONE | reviews/078 PASS; browser-visible screenshot evidence captured, local backend/frontend smoke passed, no secret-like metadata found |
| T-204 | Accept Workspace Department Catalog local/demo evidence | 产品规划席 | DONE | reviews/078 accepted by 产品规划席 on 2026-07-08; verification-only evidence closed |
| T-205 | Review Workspace Department Activation boundary gate | 总控决策席 | DONE | Option A approved 2026-07-08; boundary-only future tenant-local department activation |
| T-206 | Define Workspace Department Activation boundaries | 系统交付席 | DONE | ADR-0032 + reviews/079; boundary-only, no implementation |
| T-207 | Verify Workspace Department Activation boundaries | 质量运行席 | DONE | reviews/079 PASS; boundary-only scope and forbidden locks passed |
| T-208 | Accept Workspace Department Activation boundaries | 产品规划席 | DONE | reviews/079 accepted by 产品规划席 on 2026-07-08 |
| T-209 | Review Workspace Department Activation first-slice gate | 总控决策席 | DONE | issues/083 approved 2026-07-08; backend-only metadata activation |
| T-210 | Implement Workspace Department Activation first slice | 系统交付席 | DONE | reviews/080 accepted; backend-only tenant-local activation metadata |
| T-211 | Verify Workspace Department Activation first slice | 质量运行席 | DONE | reviews/080 PASS; focused backend tests and 255-test backend regression passed |
| T-212 | Accept Workspace Department Activation first slice | 产品规划席 | DONE | reviews/080 accepted by 产品规划席 on 2026-07-08 |
| T-213 | Review Workspace Department Activation UI gate | 总控决策席 | DONE | issues/084 approved 2026-07-08; frontend-only existing activation APIs |
| T-214 | Implement Workspace Department Activation UI | 系统交付席 | DONE | reviews/081 accepted; frontend-only company-frame selector using existing activation APIs |
| T-215 | Verify Workspace Department Activation UI | 质量运行席 | DONE | reviews/081 PASS; 21 frontend tests, lint, build, API scan, and scope scan passed |
| T-216 | Accept Workspace Department Activation UI | 产品规划席 | DONE | reviews/081 accepted by 产品规划席 on 2026-07-08 |
| T-217 | Split issue-080 department catalog evidence from activation drift | 系统交付席 | DONE | reviews/077 scope split resolved; activation behavior belongs to accepted issues 083/084, issue-080 evidence remains bounded to catalog summary + reviews/078 browser evidence |
| T-218 | Complete Workspace Admin shared-contract integration gaps | 系统交付席 | DONE | issues/085 + reviews/082; usage.model_call/tool_call/task_execution projection, tenant_private namespace, 279 backend tests green |
| T-219 | Verify Workspace Admin shared-contract integration | 质量运行席 | DONE | 7 focused ADR-0028 tests, 50 gateway/catalog/preference tests, 38 execution-engine tests, 279 full backend tests, scope/secret scans passed |
| T-220 | Accept Workspace Admin shared-contract integration | 产品规划席 | DONE | reviews/082 accepted; Workspace/Admin联调补齐完成，runtime仍不调用 /api/platform/* 写接口 |
| T-221 | Implement Workspace Self-Extension MVP | 系统交付席 | DONE | issues/086 + reviews/083; tenant_private model/tool/connector typed endpoints, unified selector, optional task capability selection |
| T-222 | Verify Workspace Self-Extension MVP | 质量运行席 | DONE | TDD red confirmed; 10 ADR-0028 focused tests, 42 Phase-3 focused tests, 38 execution-engine tests, 298 full backend tests, scope/secret scans passed |
| T-223 | Accept Workspace Self-Extension MVP | 产品规划席 | DONE | reviews/083 accepted; private execution writes usage_event with capability_source=tenant_private |

## Backlog

| ID | Task | Owner | Status |
| --- | --- | --- | --- |

## Done

| ID | Task | Owner | Completed |
| --- | --- | --- |
| T-136 | Close out Project Memory Execution Summary to user | 产品规划席 | 2026-07-07 |
| T-135 | Accept Project Memory Execution Summary | 产品规划席 | 2026-07-07 |
| T-134 | Verify Project Memory Execution Summary | 质量运行席 | 2026-07-07 |
| T-133 | Implement Project Memory Execution Summary | 系统交付席 | 2026-07-07 |
| T-132 | Accept Project Memory Execution Summary boundaries | 产品规划席 | 2026-07-07 |
| T-131 | Verify Project Memory Execution Summary boundaries | 质量运行席 | 2026-07-07 |
| T-130 | Define Project Memory Execution Summary boundaries | 系统交付席 | 2026-07-07 |
| T-129 | Review Project Memory Execution Summary gate | 总控决策席 | 2026-07-07 |
| T-128 | Decide next bounded phase after verification automation | 产品规划席 | 2026-07-07 |
| T-127 | Close out Local/Demo API Smoke Helper to user | 产品规划席 | 2026-07-07 |
| T-126 | Accept Local/Demo API Smoke Helper | 产品规划席 | 2026-07-07 |
| T-125 | Verify Local/Demo API Smoke Helper | 质量运行席 | 2026-07-07 |
| T-124 | Implement Local/Demo API Smoke Helper | 系统交付席 | 2026-07-07 |
| T-123 | Accept local/demo verification automation boundaries | 产品规划席 | 2026-07-07 |
| T-122 | Verify local/demo verification automation boundaries | 质量运行席 | 2026-07-07 |
| T-121 | Define local/demo verification automation boundaries | 系统交付席 | 2026-07-07 |
| T-120 | Review local/demo verification automation gate | 总控决策席 | 2026-07-07 |
| T-119 | Decide next bounded phase after operator polish | 产品规划席 | 2026-07-07 |
| T-118 | Close out Local/Demo Operator Release Notes Package to user | 产品规划席 | 2026-07-06 |
| T-117 | Accept Local/Demo Operator Release Notes Package | 产品规划席 | 2026-07-06 |
| T-116 | Verify Local/Demo Operator Release Notes Package | 质量运行席 | 2026-07-06 |
| T-115 | Implement Local/Demo Operator Release Notes Package | 系统交付席 | 2026-07-06 |
| T-114 | Accept local/demo operator polish architecture boundaries | 产品规划席 | 2026-07-06 |
| T-113 | Verify local/demo operator polish architecture boundaries | 质量运行席 | 2026-07-06 |
| T-112 | Define local/demo operator polish architecture boundaries | 系统交付席 | 2026-07-06 |
| T-111 | Review local/demo operator polish gate | 总控决策席 | 2026-07-06 |
| T-110 | Accept post-v0.1 Execution Reliability closeout review | 产品规划席 | 2026-07-06 |
| T-109 | Verify post-v0.1 Execution Reliability closeout review | 质量运行席 | 2026-07-06 |
| T-108 | Conduct post-v0.1 Execution Reliability closeout review | 系统交付席 | 2026-07-06 |
| T-107 | Review post-v0.1 Execution Reliability closeout gate | 总控决策席 | 2026-07-06 |
| T-106 | Accept Evolution Decision Evidence Map | 产品规划席 | 2026-07-06 |
| T-105 | Verify Evolution Decision Evidence Map | 质量运行席 | 2026-07-06 |
| T-104 | Implement Evolution Decision Evidence Map | 系统交付席 | 2026-07-06 |
| T-103 | Accept Evolution Decision Evidence Reliability architecture boundaries | 产品规划席 | 2026-07-06 |
| T-102 | Verify Evolution Decision Evidence Reliability architecture boundaries | 质量运行席 | 2026-07-06 |
| T-101 | Define Evolution Decision Evidence Reliability architecture boundaries | 系统交付席 | 2026-07-06 |
| T-100 | Review Evolution Decision Evidence Reliability gate | 总控决策席 | 2026-07-06 |
| T-099 | Accept Workflow Error/Fallback Evidence Map | 产品规划席 | 2026-07-06 |
| T-098 | Verify Workflow Error/Fallback Evidence Map | 质量运行席 | 2026-07-06 |
| T-097 | Implement Workflow Error/Fallback Evidence Map | 系统交付席 | 2026-07-06 |
| T-096 | Accept Workflow Error/Fallback Observability architecture boundaries | 产品规划席 | 2026-07-06 |
| T-095 | Verify Workflow Error/Fallback Observability architecture boundaries | 质量运行席 | 2026-07-06 |
| T-094 | Define Workflow Error/Fallback Observability architecture boundaries | 系统交付席 | 2026-07-06 |
| T-093 | Review Workflow Error/Fallback Observability gate | 总控决策席 | 2026-07-06 |
| T-092 | Accept Run Evidence Reliability first slice | 产品规划席 | 2026-07-06 |
| T-091 | Verify Run Evidence Reliability first slice | 质量运行席 | 2026-07-06 |
| T-000 | Align project to Sprint 0 Tool System v1.5 gate | 产品规划席 | 2026-07-06 |
| T-001 | Initialize low-token multi-role workflow | 产品规划席 | 2026-07-06 |
| T-002 | Create Sprint 0 acceptance issue | 产品规划席 | 2026-07-06 |
| T-003 | Verify Sprint 0 execution loop | 质量运行席 | 2026-07-06 |
| T-004 | Review Sprint 0 completion with 总控决策席 | 总控决策席 | 2026-07-06 |
| T-007 | Open Tool System v1.6 Meta Development System gate | 产品规划席 | 2026-07-06 |
| T-008 | Implement Tool System v1.6 Meta Development System | 系统交付席 | 2026-07-06 |
| T-009 | Open Tool System v1.8 Controlled Self-Evolution gate | 产品规划席 | 2026-07-06 |
| T-010 | Implement Tool System v1.8 Controlled Self-Evolution Kernel | 系统交付席 | 2026-07-06 |
| T-011 | Verify Tool System v1.8 Controlled Self-Evolution Kernel | 质量运行席 | 2026-07-06 |
| T-012 | Accept Tool System v1.8 quality evidence | 产品规划席 | 2026-07-06 |
| T-005 | Draft Sprint 1 company visualization PRD slice | 产品规划席 | 2026-07-06 |
| T-013 | Review Sprint 1 company visualization gate | 总控决策席 | 2026-07-06 |
| T-006 | Define Sprint 1 architecture boundaries | 系统交付席 | 2026-07-06 |
| T-014 | Plan Sprint 1 architecture-boundary verification | 质量运行席 | 2026-07-06 |
| T-015 | Accept Sprint 1 architecture-boundary verification plan | 产品规划席 | 2026-07-06 |
| T-016 | Implement Sprint 1 visualization first slice | 系统交付席 | 2026-07-06 |
| T-017 | Verify Sprint 1 visualization first slice | 质量运行席 | 2026-07-06 |
| T-018 | Accept Sprint 1 visualization first slice | 产品规划席 | 2026-07-06 |
| T-019 | Close out Sprint 1 visualization first slice to user | 产品规划席 | 2026-07-06 |
| T-020 | Decide next Sprint 1 visualization follow-up | 产品规划席 | 2026-07-06 |
| T-021 | Implement Sprint 1 CEO-readable visualization polish | 系统交付席 | 2026-07-06 |
| T-022 | Verify Sprint 1 CEO-readable visualization polish | 质量运行席 | 2026-07-06 |
| T-023 | Accept Sprint 1 CEO-readable visualization polish | 产品规划席 | 2026-07-06 |
| T-024 | Close out Sprint 1 CEO-readable visualization polish to user | 产品规划席 | 2026-07-06 |
| T-025 | Decide next Sprint 1 follow-up or Sprint 2 entry | 产品规划席 | 2026-07-06 |
| T-026 | Review Sprint 2 unified task console gate | 总控决策席 | 2026-07-06 |
| T-027 | Define Sprint 2 architecture boundaries | 系统交付席 | 2026-07-06 |
| T-028 | Plan Sprint 2 architecture-boundary verification | 质量运行席 | 2026-07-06 |
| T-029 | Accept Sprint 2 architecture-boundary verification plan | 产品规划席 | 2026-07-06 |
| T-030 | Implement Sprint 2 unified task console first slice | 系统交付席 | 2026-07-06 |
| T-031 | Verify Sprint 2 unified task console first slice | 质量运行席 | 2026-07-06 |
| T-032 | Accept Sprint 2 unified task console first slice | 产品规划席 | 2026-07-06 |
| T-033 | Decide next Sprint 2 follow-up or Sprint 3 entry | 产品规划席 | 2026-07-06 |
| T-034 | Review Sprint 2 Project Memory Foundation gate | 总控决策席 | 2026-07-06 |
| T-035 | Define Project Memory Foundation architecture boundaries | 系统交付席 | 2026-07-06 |
| T-036 | Plan Project Memory Foundation architecture-boundary verification | 质量运行席 | 2026-07-06 |
| T-037 | Accept Project Memory Foundation architecture-boundary verification plan | 产品规划席 | 2026-07-06 |
| T-038 | Implement Project Memory first slice | 系统交付席 | 2026-07-06 |
| T-039 | Verify Project Memory first slice | 质量运行席 | 2026-07-06 |
| T-040 | Accept Project Memory first slice | 产品规划席 | 2026-07-06 |
| T-041 | Decide next Sprint 2 follow-up or Sprint 3 entry | 产品规划席 | 2026-07-06 |
| T-042 | Review Sprint 3 lightweight role and responsibility gate | 总控决策席 | 2026-07-06 |
| T-043 | Define Sprint 3 lightweight role architecture boundaries | 系统交付席 | 2026-07-06 |
| T-044 | Plan Sprint 3 lightweight role architecture-boundary verification | 质量运行席 | 2026-07-06 |
| T-045 | Accept Sprint 3 lightweight role architecture-boundary verification plan | 产品规划席 | 2026-07-06 |
| T-046 | Implement Sprint 3 role profiles first slice | 系统交付席 | 2026-07-06 |
| T-047 | Verify Sprint 3 role profiles first slice | 质量运行席 | 2026-07-06 |
| T-048 | Accept Sprint 3 role profiles first slice | 产品规划席 | 2026-07-06 |
| T-049 | Close out Sprint 3 role profiles first slice to user | 产品规划席 | 2026-07-06 |
| T-050 | Review Sprint 3 role-context runtime reference gate | 总控决策席 | 2026-07-06 |
| T-051 | Define role-context runtime reference architecture boundaries | 系统交付席 | 2026-07-06 |
| T-052 | Plan role-context runtime reference architecture-boundary verification | 质量运行席 | 2026-07-06 |
| T-053 | Accept role-context runtime reference architecture-boundary verification plan | 产品规划席 | 2026-07-06 |
| T-054 | Implement role-context runtime reference first slice | 系统交付席 | 2026-07-06 |
| T-055 | Verify role-context runtime reference first slice | 质量运行席 | 2026-07-06 |
| T-056 | Accept role-context runtime reference first slice | 产品规划席 | 2026-07-06 |
| T-057 | Decide Sprint 3 closeout or Sprint 4 entry | 产品规划席 | 2026-07-06 |
| T-058 | Review Sprint 3 closeout and Sprint 4 entry gate | 总控决策席 | 2026-07-06 |
| T-059 | Define Sprint 4 multi-entry UI architecture boundaries | 系统交付席 | 2026-07-06 |
| T-060 | Plan Sprint 4 multi-entry UI architecture-boundary verification | 质量运行席 | 2026-07-06 |
| T-061 | Accept Sprint 4 multi-entry UI architecture-boundary verification plan | 产品规划席 | 2026-07-06 |
| T-062 | Implement Sprint 4 multi-entry UI first slice | 系统交付席 | 2026-07-06 |
| T-063 | Verify Sprint 4 multi-entry UI first slice | 质量运行席 | 2026-07-06 |
| T-064 | Accept Sprint 4 multi-entry UI first slice | 产品规划席 | 2026-07-06 |
| T-065 | Review Sprint 4 closeout and MVP readiness gate | 总控决策席 | 2026-07-06 |
| T-066 | Define AI Task Executor MVP readiness review boundaries | 系统交付席 | 2026-07-06 |
| T-067 | Plan AI Task Executor MVP readiness boundary verification | 质量运行席 | 2026-07-06 |
| T-068 | Accept AI Task Executor MVP readiness boundary verification plan | 产品规划席 | 2026-07-06 |
| T-069 | Conduct AI Task Executor MVP readiness review | 系统交付席 | 2026-07-06 |
| T-070 | Verify AI Task Executor MVP readiness review | 质量运行席 | 2026-07-06 |
| T-071 | Accept AI Task Executor MVP readiness review | 产品规划席 | 2026-07-06 |
| T-073 | Localize operation console UI to Chinese | 系统交付席 | 2026-07-06 |
| T-072 | Decide MVP release-candidate or stabilization follow-up | 产品规划席 | 2026-07-06 |
| T-074 | Review AI Task Executor MVP release-candidate gate | 总控决策席 | 2026-07-06 |
| T-075 | Define AI Task Executor MVP release-candidate boundaries | 系统交付席 | 2026-07-06 |
| T-076 | Verify AI Task Executor MVP release-candidate boundaries | 质量运行席 | 2026-07-06 |
| T-077 | Accept AI Task Executor MVP release-candidate boundaries | 产品规划席 | 2026-07-06 |
| T-078 | Open release-candidate stabilization/documentation implementation issue | 产品规划席 | 2026-07-06 |
| T-079 | Implement release-candidate stabilization/documentation package | 系统交付席 | 2026-07-06 |
| T-080 | Verify release-candidate stabilization/documentation package | 质量运行席 | 2026-07-06 |
| T-081 | Accept release-candidate stabilization/documentation package | 产品规划席 | 2026-07-06 |
| T-082 | Open first-version local/demo release verification issue | 产品规划席 | 2026-07-06 |
| T-083 | Verify first-version local/demo release candidate | 质量运行席 | 2026-07-06 |
| T-084 | Accept first-version local/demo release candidate verification | 产品规划席 | 2026-07-06 |
| T-085 | Close first-version local/demo release candidate and decide v0.1 release record | 产品规划席 | 2026-07-06 |
| T-086 | Review post-v0.1 next-phase gate | 总控决策席 | 2026-07-06 |
| T-087 | Define post-v0.1 execution reliability architecture boundaries | 系统交付席 | 2026-07-06 |
| T-088 | Verify post-v0.1 execution reliability architecture boundaries | 质量运行席 | 2026-07-06 |
| T-089 | Accept post-v0.1 execution reliability architecture boundaries | 产品规划席 | 2026-07-06 |
| T-090 | Implement Run Evidence Reliability first slice | 系统交付席 | 2026-07-06 |
