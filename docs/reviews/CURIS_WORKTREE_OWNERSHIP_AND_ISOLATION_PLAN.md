# CURIS WORKTREE OWNERSHIP AND ISOLATION PLAN

Status: Review  
Date: 2026-08-16  
Round: 2 — File / Hunk Ownership Matrix + Generated / Local State Isolation Plan  
Source audit: docs/reviews/CURIS_WORKTREE_CLEANUP_AUDIT.md  
Branch: main  
HEAD: adb52210a  
Document authority: /Users/yy/Documents/Curis AI Workspace/docs/

## 1. Executive Conclusion

本轮仍然只做只读分析和计划，没有进入 staging。

结论比第一轮更明确：

1. G1 Agent Computer Access P0、G2 XHS、G3 RD Phase 0/1 的逻辑归属清楚，但共享文件仍需 hunk 级拆分。
2. G4 RD Phase 2A / long-running 是 Review Required candidate，不能作为正式已验收成果提交。
3. G5 Shared Runtime 尚未形成可以独立提交的稳定边界。backend/app/runtime/workspace.py 约 2,847 行，同时包含 Staffing、RD execution、Content Growth / XHS / TTK 等业务逻辑；backend/app/api/runtime_foundation_router.py 约 1,286 行，同时包含 Company、Workspace、Cycle、Content、Simulation、Staffing 和 RD execution API。
4. G6 Talent Market / AI Capability 是候选实现与 Review 文档，且 backend/app/main.py、database.py、model_gateway.py 和前端 CEO 工作台有混合修改。
5. G7 Frozen Authority / ADR 文档可以作为 docs-only staging 候选，但仍应先做 staged path 检查。
6. 根目录产品文档副本与 docs/ canonical 文件均已确认 diverged，根目录只能作为 Migration Source / Duplicate / Historical Source，不能覆盖 docs/。
7. Desktop 目录不能整体忽略：源码、资源和 lockfile 与 4.7 GB target、29 MB node_modules、742 MB .runtime 混在一起。
8. 根目录 16 个异常 Database object 文件实际都是 SQLite 数据库副本，不是空文件，也不是普通文本；在确认数据归属前不能删除、移动或提交。

因此：

> SHARED RUNTIME INDEPENDENT COMMIT NOT YET SAFE  
> NO STAGING IN THIS ROUND

## 2. Audit Scope and Evidence Rules

### 2.1 本轮禁止事项均未执行

- 未执行 git add、git commit、git push。
- 未执行 git reset、git checkout --、git restore、git clean。
- 未删除或移动任何文件。
- 未修改业务代码、产品文档内容、Issue / Review 状态或 .gitignore。
- 未清理数据库、build、cache 或 WorkBuddy 文件。
- 未执行 regression、build 或产品验收。

### 2.2 证据来源

- git status --short --branch
- git diff --stat
- 重点文件 git diff --unified=0 / git diff --unified=...
- git ls-files --others --exclude-standard
- 第一轮审计报告
- 对应 Issue / Review / Authority 文档
- CURRENT_STATE.md、PRODUCT_DOCUMENT_POINTER.md、CHANGE_LOG.md
- 文件类型、大小、mtime、hash 和目录层级的只读检查

### 2.3 计数基线

| 项目 | 结果 |
|---|---:|
| modified status entries | 72 |
| untracked status entries | 293 |
| 实际未跟踪文件数 | 23,548 |
| desktop/target/ 实际未跟踪文件数 | 22,627 |
| Desktop source 未跟踪条目 | 整个 desktop/ 目录目前未被 Git 跟踪 |
| 当前分支 / HEAD | main / adb52210a |
| 文档记录基线 | main @ c0e1855f446a55aa3a384006cfcfed987713033 |

## 3. File Ownership Matrix

说明：对源码和治理资产使用文件级 owner；对生成物使用隔离策略；对混合文件使用“主 owner + shared / mixed”，而不是按目录猜测。

### 3.1 G1 — Agent Computer Access P0

| File | Type | Issue / Review | Status | Shared? | Stage Safety | Action |
|---|---|---|---|---|---|---|
| backend/app/agent_adapter.py | untracked backend source | AGENT-COMPUTER-ACCESS-RUNTIME-P0-001 / matching Review | Formal Acceptance Record | No, except callers | SAFE AFTER HUNK SPLIT of callers | Include whole file after path review |
| backend/tests/test_agent_adapter.py | untracked test | same | Accepted focused test | No | SAFE AFTER HUNK SPLIT group | Include with G1 |
| backend/tests/test_agent_computer_access_runtime_p0.py | untracked test | same | Accepted focused test | No | SAFE AFTER HUNK SPLIT group | Include with G1 |
| backend/app/main.py | modified source | same; also G4/G5/G6 | P0 behavior accepted but file mixed | Yes | Not safe as whole file | Stage only verified Agent execution hunk |
| backend/app/tool_executor.py | modified source | same; existing tool propagation | Accepted P0 behavior | Yes with existing executor | Not safe as whole file | Stage P0 hunk only |
| backend/app/orchestrator.py | modified source | same; snapshot propagation | Accepted P0 behavior | Yes with task orchestration | Not safe as whole file | Stage P0 hunk only |
| backend/app/result_store.py | modified source | same; result / access snapshot | Accepted P0 behavior | Yes with RD artifacts | Not safe as whole file | Stage P0 hunk only |
| docs/01_Product/Curis_Agent_Computer_Access_Contract_Candidate.md | untracked product contract | ADR-0046 / P0 Review references | Candidate | No code | REVIEW REQUIRED | Keep as review reference |
| docs/07_Decisions/ADR-0046-local-agent-computer-access-authority.md | untracked decision | ADR-0046 | Frozen | No | SAFE NOW as docs-only candidate | Exact-path staging candidate |

### 3.2 G2 — XHS accepted slice

| File | Type | Issue / Review | Status | Shared? | Stage Safety | Action |
|---|---|---|---|---|---|---|
| frontend/components/xhs/XhsWorkspacePhaseOne.js | untracked frontend source | XHS-WORKSPACE-INSTANCE-001 | XHS implementation accepted | XHS-specific | SAFE AFTER shared API split | Include |
| frontend/app/ceo-office/workspace/xhs/page.js | untracked route | same | Accepted bounded route | XHS-specific | SAFE AFTER path check | Include |
| backend/tests/test_xhs_calendar_note_runtime.py | untracked test | same | 14-pass acceptance suite | No | SAFE AFTER path check | Include |
| frontend/tests/runtimeWorkspaceUi.test.mjs | untracked test | same; also RD | Shared Runtime regression | Yes | SAFE AFTER TEST OWNERSHIP REVIEW | Split assertions or keep with shared group |
| backend/app/runtime/workspace.py | untracked source | same; also G3/G4/G5/content | Mixed | Yes | Not safe | Manual split required |
| backend/app/api/runtime_foundation_router.py | untracked source | same; also G3/G4/G5/content | Mixed | Yes | Not safe | Manual split required |
| frontend/lib/runtimeApi.js | untracked API client | same; also RD/G5 | Mixed API surface | Yes | Not safe | Split endpoint blocks or defer |
| docs/04_Development/XHS_IMPLEMENTATION_GAP_AUDIT.md | untracked development doc | same | Formal implementation record | No code | SAFE AFTER paired code review | Include with G2 record |
| docs/04_Development/XHS_RUNTIME_ARCHITECTURE_REVIEW.md | untracked development doc | same | Review record | No code | REVIEW REQUIRED | Include only with exact XHS scope |
| issues/XHS-WORKSPACE-INSTANCE-001.md | untracked Issue | same | Implemented / Accepted | No | SAFE AFTER source scope check | Include with G2 |
| reviews/XHS-WORKSPACE-INSTANCE-001_review.md | untracked Review | same | XHS Implementation Accepted | No | SAFE AFTER source scope check | Include with G2 |

XHS acceptance does not include a real external publish or analytics connector. That boundary must remain in the commit message and Review record.

### 3.3 G3 — RD Phase 0/1 accepted

| File | Type | Issue / Review | Status | Shared? | Stage Safety | Action |
|---|---|---|---|---|---|---|
| backend/app/agent_adapter.py | untracked source | RD-WORKSPACE-INSTANCE-001 | Phase 0/1 accepted; also G1 | Yes | Not as a duplicate file | Share with G1 or split ownership |
| backend/tests/test_rd_workspace_real_execution.py | untracked test | same | Phase 0/1 real execution accepted | RD-specific | SAFE AFTER path check | Include |
| frontend/components/rd/RdRealExecutionComposer.js | untracked frontend | same | Phase 0/1 / Phase 2A overlap | Yes with G4 | Not as whole RD accepted | Split by phase or defer |
| frontend/components/runtime/WorkspaceRuntimeView.js | untracked frontend | same; also G5/content | Mixed | Yes | Not safe | Manual split required |
| frontend/tests/rdWorkspaceExecution.test.mjs | untracked test | same | RD focused test | RD-specific | SAFE AFTER path check | Include with phase status |
| backend/app/main.py | modified source | same; also G1/G4/G5/G6 | Mixed | Yes | Not safe | Stage only verified Phase 0/1 hunk |
| backend/app/runtime/workspace.py | untracked source | same; also G2/G4/G5/content | Mixed | Yes | Not safe | Manual split required |
| issues/RD-WORKSPACE-INSTANCE-001.md | untracked Issue | same | Phase 0/1 accepted, later Review Required | No | SAFE AFTER status check | Preserve exact status |
| reviews/RD-WORKSPACE-INSTANCE-001_review.md | untracked Review | same | Phase 0/1 accepted; Phase 2A/reliability Review Required | No | SAFE AFTER status check | Do not relabel |

### 3.4 G4 — RD Phase 2A / long-running candidate

| File | Type | Evidence | Status | Shared? | Stage Safety | Action |
|---|---|---|---|---|---|---|
| frontend/components/rd/RdWorkspacePhaseTwo.js | untracked frontend | RD Review Phase 2A | Design fidelity pass / Review Required | RD-specific | REVIEW REQUIRED | Separate candidate commit |
| frontend/components/rd/RdRealExecutionComposer.js | untracked frontend | RD Review Phase 2A | Phase overlap | Yes with G3 | REVIEW REQUIRED | Split by phase |
| frontend/components/workspace/WorkspacePaneShell.js | untracked shell | RD Review Phase 2A | Shared shell used by XHS/RD | Yes | Not safe | Shared shell review first |
| frontend/tests/rdWorkspaceExecution.test.mjs | untracked test | RD Review | Phase 2A / reliability coverage | RD-specific | REVIEW REQUIRED | Candidate group |
| backend/app/runtime/execution_adapter.py | untracked runtime bridge | RD Review / runtime foundation | Reliability bridge | Yes with G5 | REVIEW REQUIRED | Separate adapter candidate |
| backend/app/main.py | modified source | RD long-running worker | Implemented / Review Required | Yes | Not safe | Manual split |
| issues/RD-WORKSPACE-INSTANCE-001.md | untracked Issue | same | mixed phase status | No | REVIEW REQUIRED | Preserve exact status |
| reviews/RD-WORKSPACE-INSTANCE-001_review.md | untracked Review | same | Review Required | No | REVIEW REQUIRED | Pair with candidate code |

### 3.5 G5 — Shared Runtime

| File | Type | Observed boundary | Status | Shared? | Stage Safety | Action |
|---|---|---|---|---|---|---|
| backend/app/runtime/foundation.py | untracked source | tenant/company/workspace scope, entity/link/transition persistence | Foundation candidate | Mostly shared | SAFE AFTER schema/API review | Candidate core |
| backend/app/runtime/registry.py | modified source | state machine registry | Shared foundation | Yes | SAFE AFTER focused review | Verified changes only |
| backend/app/runtime/states.py | modified source | lifecycle state definitions | Shared foundation | Yes | SAFE AFTER focused review | Verified changes only |
| backend/app/runtime/models.py | modified source | runtime schema/model definitions | Shared foundation | Yes | SAFE AFTER migration review | Pair with DB schema hunk |
| backend/app/runtime/store.py | modified source | runtime storage | Shared foundation | Yes | SAFE AFTER focused review | Pair with models/schema |
| backend/app/runtime/__init__.py | modified source | Runtime package exports | Shared | Yes | SAFE AFTER import review | Only required export |
| backend/app/runtime/simulation.py | untracked source | generic persistence plus RD-001, XHS-001, TTK-001, ORG-001 policy | Mixed shared/domain | Yes | Not safe as pure G5 | Split generic mechanics from scenario policy |
| backend/app/runtime/execution_adapter.py | untracked source | bound child execution, RD / legacy refs | Mixed | Yes | Not safe as pure G5 | Split generic bridge from RD behavior |
| backend/app/runtime/legacy_execution_adapter.py | untracked source | legacy workflow/content refs | Shared adapter candidate | Yes | SAFE AFTER contract check | Verify lifecycle isolation |
| backend/app/runtime/workspace.py | untracked source | workspace, staffing, supply, RD cycle, content item, publication, interactions | Mixed | Yes | Not safe | MIXED FILE — MANUAL SPLIT REQUIRED |
| backend/app/api/runtime_foundation_router.py | untracked source | company, workspace, cycle, content, simulation, staffing, receipt, interaction APIs | Mixed | Yes | Not safe | MIXED FILE — MANUAL SPLIT REQUIRED |
| frontend/components/runtime/RuntimeProvider.js | untracked frontend | global runtime bootstrap / snapshot | Shared candidate | Yes | SAFE AFTER UI review | Candidate core |
| frontend/components/runtime/RuntimeStates.js | untracked frontend | runtime loading/error/empty states | Shared candidate | Yes | SAFE AFTER UI review | Candidate core |
| frontend/lib/runtimeApi.js | untracked API client | company/workspace/cycle/content/simulation/staffing APIs | Mixed API surface | Yes | Not safe | MIXED FILE — MANUAL SPLIT REQUIRED |
| frontend/components/workspace/WorkspacePaneShell.js | untracked shell | navigation/context/utility panes, resize, compact overlay | Shared shell candidate | Yes | Not independently accepted | Review separately |
| frontend/components/runtime/WorkspaceRuntimeView.js | untracked UI | RD cycle UI plus XHS/TTK content UI plus simulation controls | Mixed | Yes | Not safe | MIXED FILE — MANUAL SPLIT REQUIRED |
| frontend/tests/runtimeProvider.test.mjs | untracked test | shared provider | Shared | Yes | SAFE AFTER core review | Include with G5 candidate |
| frontend/tests/runtimeMaterialization.test.mjs | untracked test | shared materialization | Shared | Yes | SAFE AFTER core review | Include with G5 candidate |
| frontend/tests/runtimeFirstArrival.test.mjs | untracked test | first arrival / runtime bootstrap | Shared | Yes | SAFE AFTER core review | Include with G5 candidate |
| frontend/tests/runtimeApi.test.mjs | untracked test | Runtime API client | Shared/mixed | Yes | SAFE AFTER API split | Include after endpoint ownership |

**Finding:** current code does not support a safe independent G5 commit. foundation.py and selected model/state/store pieces are candidates for a future minimal core, but workspace.py, runtime_foundation_router.py, runtimeApi.js, WorkspaceRuntimeView.js and simulation.py contain domain-specific behavior.

### 3.6 G6 — Talent Market / AI Capability candidate

| File family | Ownership | Status | Shared? | Stage Safety | Action |
|---|---|---|---|---|---|
| backend/app/ai_capability_registry.py | AI Capability | Review | No direct XHS/RD | REVIEW REQUIRED | Candidate only |
| backend/app/agent_conversion/coze_adapter.py | Talent Market adapter | Review | No | REVIEW REQUIRED | Candidate only |
| backend/app/agent_conversion/openclaw_adapters.py | Talent Market adapter | Review | No | REVIEW REQUIRED | Candidate only |
| backend/app/agent_conversion/external_candidates.py | Talent Market discovery | Review | No | REVIEW REQUIRED | Candidate only |
| backend/app/agent_conversion/production_line.py | Talent Market production line | Review | No | REVIEW REQUIRED | Candidate only |
| backend/app/capability_catalog.py | AI Capability | Review candidate | Yes with DB | Not safe whole file | Hunk split |
| backend/app/capability_registry.py | AI Capability | Review candidate | Yes | Not safe whole file | Hunk split |
| backend/app/catalog_constants.py | Capability catalog | Review candidate | Yes | SAFE AFTER dependency check | Related hunk only |
| backend/app/model_gateway.py | Provider protocols | Review candidate | Yes with execution | Not safe whole file | Hunk split + provider tests |
| backend/app/employee_templates.py | Default skill/tool binding | Review candidate | Yes with organization | Not safe whole file | Hunk split |
| backend/app/main.py | Talent routes and provider routing | Mixed | Yes | Not safe | Manual split |
| backend/app/database.py | Capability ownership columns and query APIs | Mixed | Yes with Runtime / legacy meeting | Not safe | Manual split + isolated migration review |
| frontend/app/ceo-office/talent-market/page.js | Talent Market UI | Review | No direct XHS/RD | REVIEW REQUIRED | Candidate only |
| frontend/lib/talentMarket.js | Talent Market API client | Review | No | REVIEW REQUIRED | Candidate only |
| backend/tests/test_talent_market.py | Talent Market test | Review | No | REVIEW REQUIRED | Candidate only |
| backend/tests/test_ai_capability_registry.py | AI Capability test | Review | No | REVIEW REQUIRED | Candidate only |
| issues/20260814_talent_market_001.md | Talent Market Issue | Review | No | REVIEW REQUIRED | Candidate record |
| issues/20260814_talent_market_phase2_002.md | Talent Market Phase 2 Issue | Review | No | REVIEW REQUIRED | Candidate record |
| issues/20260814_ai_capability_integration_001.md | AI Capability Issue | Review | No | REVIEW REQUIRED | Candidate record |
| docs/reviews/20260814_ai_capability_integration_001_review.md | AI Capability Review | Review Required | No | REVIEW REQUIRED | Candidate record |

### 3.7 G7 — Frozen Authority / ADR

| File | Type | Status | Shared? | Stage Safety | Action |
|---|---|---|---|---|---|
| docs/03_Design/Curis_Company_OS_Shared_Authority.md | design authority | Frozen | Product-wide | SAFE NOW as docs-only | Exact-path candidate |
| docs/03_Design/Curis_Content_Growth_Domain_Authority.md | design authority | Frozen | Content Growth domain | SAFE NOW as docs-only | Exact-path candidate |
| docs/07_Decisions/ADR-0046-local-agent-computer-access-authority.md | ADR | Frozen | AI Capability / Agent | SAFE NOW as docs-only | Exact-path candidate |
| docs/00_Context/CURRENT_STATE.md | modified authority | Frozen | Product-wide | SAFE AFTER consistency check | Do not blindly stage |
| docs/00_Context/PRODUCT_DOCUMENT_POINTER.md | modified authority | Frozen | Product-wide | SAFE AFTER reference check | Match actual canonical files |
| docs/08_Change_Log/CHANGE_LOG.md | modified authority | Frozen log | Product-wide | SAFE AFTER change mapping | Only confirmed entries |

### 3.8 G8 — Product / Content Growth candidate docs and UI

| File family | Ownership | Status | Stage Safety | Action |
|---|---|---|---|---|
| docs/01_Product/Curis_Product_Master_Map_v2.0.md | Product rebaseline | Review Required | REVIEW REQUIRED | Canonical target only |
| docs/01_Product/Curis_Product_Page_Map_v1.0.md | Product page map | Review Required | REVIEW REQUIRED | Canonical target only |
| docs/01_Product/Curis_Product_Rethink_Reasoning_2026-08-13.md | Product reasoning | Review Required | REVIEW REQUIRED | Canonical dated file |
| docs/01_Product/Curis_Talent_Market_*.md | Talent Market product candidate | Review | REVIEW REQUIRED | Canonical files only |
| docs/03_Design/Curis_Content_Growth_* | Content Growth design | Frozen / Review / Research mixed | REVIEW REQUIRED | Separate Frozen Authority |
| docs/Content_Growth_Research/* | Research | Review / Research | REVIEW REQUIRED | Not implementation |
| docs/01_Product/Curis_Product_Blueprint.html | target Blueprint | Review | REVIEW REQUIRED | Target, not delivered fact |
| docs/01_Product/Curis_Product_Context.md | product context | Frozen / modified | SAFE AFTER authority check | Verify target/delivered boundary |
| frontend/app/ceo-office/page.js | product UI candidate | implementation wave | REVIEW REQUIRED | Separate from accepted Workspace |
| frontend/app/onboarding/page.js | ordinary-user UI candidate | implementation candidate | REVIEW REQUIRED | No independent acceptance |
| frontend/components/terra/* and CEO office pages | product shell candidate | mixed rebaseline | REVIEW REQUIRED | Not XHS/RD accepted scope |

### 3.9 G9 — Workspace Engineering docs

| File | Status | Stage Safety | Action |
|---|---|---|---|
| docs/05_Workspace_Engineering/Curis_Workspace_Engineering_Methodology.md | Review / Approved Candidate | REVIEW REQUIRED | Docs-only candidate |
| docs/05_Workspace_Engineering/Curis_Workspace_Engineering_Lifecycle.md | Review / Approved Candidate | REVIEW REQUIRED | Docs-only candidate |
| docs/05_Workspace_Engineering/Curis_Workspace_Engineering_Gates_and_Acceptance.md | Review / Approved Candidate | REVIEW REQUIRED | Docs-only candidate |
| docs/02_Architecture/WORKSPACE_ENGINEERING_RUNTIME_AND_EXTENSIBILITY_AUDIT.md | Review | REVIEW REQUIRED | Dynamic package runtime not implemented |
| docs/02_Architecture/WORKSPACE_PACKAGE_TECHNICAL_PROPOSAL.md | Review / Approved Candidate | REVIEW REQUIRED | Direction, not code |
| docs/02_Architecture/WORKSPACE_ENGINEERING_P0_DEFINITION.md | Review / P0 defined | REVIEW REQUIRED | Implementation State: NOT STARTED |
| docs/04_Development/WORKSPACE_ENGINEERING_P0_IMPLEMENTATION_PLAN.md | Draft / Not Started | REVIEW REQUIRED | Do not stage as implementation |

### 3.10 G10 — Issue / Review / Evidence

| Path family | Ownership | Status | Stage Safety | Action |
|---|---|---|---|---|
| issues/XHS-WORKSPACE-INSTANCE-001.md + matching Review | XHS | Accepted | SAFE AFTER source scope check | Pair with G2 |
| issues/RD-WORKSPACE-INSTANCE-001.md + matching Review | RD | Mixed accepted / Review Required | SAFE AFTER status check | Pair phase-by-phase |
| issues/AGENT-COMPUTER-ACCESS-RUNTIME-P0-001.md + matching Review | G1 | Accepted | SAFE AFTER hunk check | Pair with G1 |
| issues/20260814_* + matching Review | G6 | Review | REVIEW REQUIRED | Candidate records only |
| docs/reviews/20260813_current_state_product_drift_audit/* | Product audit | Review evidence | EVIDENCE REVIEW REQUIRED | Evidence, not source |
| docs/reviews/20260809_*desktop* | Desktop acceptance | Review / evidence | EVIDENCE REVIEW REQUIRED | Not packaged source |
| docs/reviews/align-baseline/* | UI evidence | Evidence | EVIDENCE REVIEW REQUIRED | Retain only if Review requires |

### 3.11 Repository Governance / Prototype / Unknown

| Path | Owner | Status | Stage Safety | Action |
|---|---|---|---|---|
| AGENTS.md | Repository Governance | modified | OWNER REVIEW | Do not stage with product code |
| .gitignore | Repository Governance | modified | OWNER REVIEW | No change in this round |
| .workbuddy/memory/* | Generated / Local State | mixed tracked/untracked | KEEP LOCAL / IGNORE | Do not stage |
| curis-ui-prototype/ | Prototype / Migration Source | untracked | MIGRATION SOURCE — DO NOT COMMIT | Reference only |
| curis-ui-prototype.bak/ | Prototype backup | untracked | ARCHIVE BEFORE IGNORE | Owner retention decision |
| delivery/ | Migration / historical source | untracked | MIGRATION SOURCE — DO NOT COMMIT | No current authority |
| previews/ | Preview artifact | untracked | EVIDENCE REVIEW REQUIRED | Retain only if tied to Review |
| build_rd_pages.py, rebuild_rd_default.py, reproduce_rd_baseline_v1.py | Unknown scripts | untracked | UNKNOWN / OWNER REVIEW | No current Issue proof |

## 4. Hunk Ownership Matrix

以下行号是当前 diff header 中的 new-file coordinates。未跟踪文件没有 Git hunk，因此以 whole-file review 记录。任何同一 hunk 内出现两个 owner 的，都标记为 MIXED HUNK — MANUAL SPLIT REQUIRED。

### 4.1 backend/app/main.py

| Hunk / Lines | Change Summary | Owner | Evidence | Stage Strategy |
|---|---|---|---|---|
| +3 and +19–47 | Import asyncio and load local deploy/new-api/.env into process env | AI Capability / local runtime policy | credential boundary; no dedicated accepted Issue | REVIEW REQUIRED |
| +373–378 | StrategyMeetingIn request model | Unknown / legacy Strategy Room | old Change Log only | UNKNOWN / OWNER REVIEW |
| +728–734 | TalentRecruitIn request model | Talent Market | Talent Market Issue | G6 candidate |
| +1294–1319 | Append-only runtime trace event after model call | Shared Runtime / observability | EvoFlow A2 Change Log | G5 candidate |
| +1961–2009 | Local provider no-auth, provider protocol selection, Codex CLI Agent execution | MIXED — AI Capability + G1 | provider tests and Computer Access Review | MIXED HUNK — MANUAL SPLIT REQUIRED |
| +2181–2182 | Include AI capability router | AI Capability | AI Capability Review | G6 candidate |
| +2673–2701 | Strategy Meeting GET/POST/GET API | Unknown / legacy Strategy Room | old Change Log | UNKNOWN / OWNER REVIEW |
| +2901–2913 | Talent Market candidate / production-line endpoints | Talent Market | Talent Market source and Issue | G6 candidate |
| +3092 | Existing workspace route line change | Unknown until surrounding diff split | actual diff only | HOLD |
| +3522–3564 | Talent Market employee recruit and skill/tool binding | Talent Market | Talent Market Product Map / Issue | G6 candidate |
| +3697–3703 | Skill template / tool runtime additions | Talent Market / Capability | skill runtime and capability changes | G6 candidate |
| +4297–4303 | Platform Talent Market production-line endpoint | Talent Market | candidate registry | G6 candidate |
| +4799–5035 | Runtime foundation router and inline rd_task:auto execution, file scope, tests, artifacts, access snapshot | MIXED — Shared Runtime + RD + Computer Access | RD Review, Runtime foundation, G1 Review | MIXED HUNK — MANUAL SPLIT REQUIRED |
| +5110–5121 | Connector discovery/install/authorization/health projection | AI Capability / Connector | connector registry | G6 candidate |

### 4.2 backend/app/database.py

| Hunk / Lines | Change Summary | Owner | Evidence | Stage Strategy |
|---|---|---|---|---|
| +1657–1659 | Ensure Runtime Foundation schema and Capability ownership migration | MIXED — G5 + G6 | runtime models and capability ownership | Manual split / migration review |
| +2009–2024 | strategy_meetings table and index | Unknown / legacy Strategy Room | old Change Log | Owner review |
| +2383–2397 | owner_type, owner_id, visibility columns | AI Capability | capability ownership design | G6 candidate |
| +5356–5358, +5379–5380, +5394–5396 | Persist capability owner fields | AI Capability | same | G6 candidate |
| +5515–5556 | Query capability catalog by owner / visibility / type | AI Capability | same | G6 candidate |
| +5997–6078 | Strategy Meeting persistence / read APIs | Unknown / legacy Strategy Room | old Change Log | Owner review |
| +6238 | Include default skill/tool fields in employee template read | Talent Market / Capability | Talent Market recruit route | G6 candidate |

### 4.3 orchestrator.py, result_store.py, tool_executor.py

| File / Hunk | Change Summary | Owner | Evidence | Stage Strategy |
|---|---|---|---|---|
| backend/app/orchestrator.py +424–429 | Propagate computer access information through task execution | Computer Access | G1 Review changed files | G1 only |
| backend/app/result_store.py +728–733 | Persist access snapshot / execution metadata | MIXED — G1 + RD Artifact | G1 and RD Reviews | Manual split |
| backend/app/tool_executor.py +90–96 | Tool execution access snapshot / propagation | Computer Access | G1 Review | G1 only |
| backend/app/tool_executor.py +159–160 | Existing executor propagation adjustment | Computer Access / existing runtime | G1 Review and callers | Caller compatibility first |

### 4.4 Untracked mixed files

| File | Internal sections observed | Owner | Evidence | Stage Strategy |
|---|---|---|---|---|
| backend/app/runtime/workspace.py | workspace; capability supply; staffing; operating cycles; RD execution; content items; publication; interactions | MIXED — G2/G3/G4/G5/domain | method inventory and Reviews | No whole-file staging |
| backend/app/api/runtime_foundation_router.py | company; workspace; cycle; RD; content; simulation; staffing; receipt; interaction; founding | MIXED — G2/G3/G4/G5 | route inventory | No whole-file staging |
| frontend/lib/runtimeApi.js | company/bootstrap; simulation; staffing; workspace; RD cycle; content/version; founding | MIXED — G2/G3/G4/G5 | endpoint inventory | Split endpoint blocks |
| frontend/components/workspace/WorkspacePaneShell.js | navigation/context/utility panes, resize, compact overlay | Shared shell | RD Review and XHS boundary | Separate shell candidate |
| frontend/components/runtime/WorkspaceRuntimeView.js | generic status plus RD runtime and XHS/TTK content runtime | MIXED — G3/G4/G5 | component inventory | Manual split |
| backend/app/runtime/simulation.py | generic simulation persistence plus explicit RD/XHS/TTK scenario policy | MIXED — G5 + domain | SCENARIOS and subject checks | Extract generic core |
| backend/app/runtime/execution_adapter.py | generic bridge plus RD task / content / workflow refs | MIXED — G4/G5 | execution_ref conditions | Split generic adapter |

## 5. Shared Runtime Boundary

### 5.1 Closest to business-independent foundation

- backend/app/runtime/foundation.py: tenant/company/workspace scope, runtime entity/link persistence, transition logging and execution reference attachment.
- Verified portions of backend/app/runtime/models.py, registry.py, states.py and store.py.
- frontend/components/runtime/RuntimeProvider.js: bootstrap and snapshot state, subject to API contract review.
- frontend/components/runtime/RuntimeStates.js: shared loading/error/empty states.
- Generic pane behavior in frontend/components/workspace/WorkspacePaneShell.js.
- Generic portions of backend/app/runtime/legacy_execution_adapter.py.

These are candidate foundation pieces, not an independently accepted Group 5.

### 5.2 XHS-specific

- Content item lifecycle and XHS platform constraints in runtime/workspace.py and the foundation router.
- XHS / TTK content scenario mapping in simulation.py.
- Publication receipt and manual interaction projections.
- frontend/components/xhs/XhsWorkspacePhaseOne.js and its route.
- XHS endpoint blocks in runtimeApi.js and WorkspaceRuntimeView.js.

### 5.3 RD-specific

- RD operating cycle creation, assignment, execution, failure and resume methods in runtime/workspace.py.
- rd_task:auto binding, file scope, test command, Codex execution, diff and Artifact creation in main.py.
- RD execution bridge behavior in execution_adapter.py.
- RdRealExecutionComposer.js, RdWorkspacePhaseTwo.js and RD route.
- RD endpoint blocks in the router and runtimeApi.js.

### 5.4 Why the current Shared Runtime cannot be independent

> SHARED RUNTIME INDEPENDENT COMMIT NOT YET SAFE

Reasons:

1. Runtime schema initialization is mixed with Capability and legacy Strategy Meeting changes in database.py.
2. Router and service files combine generic state persistence with RD and Content Growth lifecycle.
3. Frontend API and view files combine RD, XHS, TTK and staffing semantics.
4. Current Review evidence accepts bounded vertical slices, not a separately accepted Shared Runtime package.
5. Most shared source files are untracked, so there is no committed intra-file baseline for safe hunk staging.

## 6. Generated / Local State Isolation Matrix

Policy values use the task-approved vocabulary.

| Path / Pattern | Category | Git Status | Product Value | Data Risk | Recommended Policy |
|---|---|---|---|---|---|
| desktop/target/ | Rust build / packaged app / copied runtime | untracked; 22,627 files; ~4.7 GB | Build evidence only | High: packaged runtime contains source copies, DBs, secret-vault routes, cert bundle and local paths | KEEP LOCAL / IGNORE |
| desktop/node_modules/ | dependency install | untracked; ~29 MB | None as source | Medium | KEEP LOCAL / IGNORE |
| desktop/.runtime/ | generated runtime bundle | ignored; ~742 MB | Possible release input, but generated | High | KEEP LOCAL / IGNORE |
| frontend/.next/ | Next build output | ignored; ~718 MB | None as source | Medium | KEEP LOCAL / IGNORE |
| .cache/ | local cache | untracked; ~836 KB | None | Low/unknown | KEEP LOCAL / IGNORE |
| .workbuddy/ | local memory/output/artifacts | tracked modifications plus untracked | Agent context only | High: paths, screenshots, activity context | KEEP LOCAL / IGNORE |
| backend/curis.sqlite | empty SQLite file | untracked; 0 bytes | None | Low content risk | DELETE CANDIDATE |
| backend/curis_dev.db | empty SQLite file | untracked; 0 bytes | None | Low content risk | DELETE CANDIDATE |
| backend/data/curis.sqlite | active local SQLite | untracked | Local runtime/evidence, not source | High: tenant/activity/runtime data | ARCHIVE BEFORE IGNORE |
| backend/data/curis.sqlite.bak-20260806 | DB backup | untracked | Historical evidence possible | High | EVIDENCE REVIEW REQUIRED |
| data/curis.sqlite.bak-20260806 | DB backup | untracked | Historical reset evidence possible | High | EVIDENCE REVIEW REQUIRED |
| data/issue_pipeline.sqlite-wal | SQLite WAL | untracked; empty at audit time | No independent value | High with companion DB | KEEP LOCAL / IGNORE |
| data/issue_pipeline.sqlite-shm | SQLite shared memory | untracked; 32 KB | No independent value | High / incomplete state | KEEP LOCAL / IGNORE |
| artifacts/ | screenshots / audit artifacts | untracked; ~192 MB | Evidence may matter | Medium/high | EVIDENCE REVIEW REQUIRED |
| previews/ | HTML preview | untracked | Design evidence | Low/medium | EVIDENCE REVIEW REQUIRED |
| delivery/ | old delivery / migration material | untracked | Historical source | Medium: stale product truth | MIGRATION SOURCE — DO NOT COMMIT |
| curis-ui-prototype/ | prototype source, audit and preview | untracked; ~25 MB | Design reference | Medium | MIGRATION SOURCE — DO NOT COMMIT |
| curis-ui-prototype.bak/ | prototype backup | untracked; ~6.9 MB | Historical reference | Medium | ARCHIVE BEFORE IGNORE |
| curis-ui-prototype/.audit/ | audit scripts/screenshots/token probes | untracked | Evidence/tooling | Medium | EVIDENCE REVIEW REQUIRED |
| packaged Curis.app under desktop/target/release/bundle/macos/ | generated release artifact | nested under untracked target | Release evidence | High: bundles runtime, DB copies and dependencies | EVIDENCE REVIEW REQUIRED |
| screenshots under docs/reviews, artifacts and previews | evidence | many untracked | Review evidence | Possible paths/personal data | EVIDENCE REVIEW REQUIRED |
| root <app.database.Database object at ...> | anomalous SQLite snapshots | 16 untracked | Unknown historical DB evidence | High | UNKNOWN / OWNER REVIEW |
| root duplicate product docs | migration source / duplicate | untracked | Historical or alternate draft | Medium: conflicts with canonical docs | MIGRATION SOURCE — DO NOT COMMIT |

No policy above authorizes deletion in this round.

## 7. Desktop Source vs Generated Boundary

### 7.1 Desktop Source candidates

These are source-shaped and may become a future formal Desktop commit after a separate source review:

~~~text
desktop/Cargo.toml
desktop/Cargo.lock
desktop/package.json
desktop/package-lock.json
desktop/pnpm-lock.yaml
desktop/tauri.conf.json
desktop/build.rs
desktop/src/main.rs
desktop/src/lib.rs
desktop/runtime/backend_entry.py
desktop/runtime/gateway.py
desktop/runtime/guardian.py
desktop/scripts/build-manual-dmg.sh
desktop/scripts/build-requirements.txt
desktop/scripts/build-runtime.sh
desktop/static/index.html
desktop/Info-ATS.plist
desktop/icons/**
~~~

desktop/gen/schemas/** is source-adjacent generated schema. Confirm whether the Tauri toolchain regenerates it before staging.

### 7.2 Desktop Generated / Local State

~~~text
desktop/target/**
desktop/node_modules/**
desktop/.runtime/**
desktop/runtime/__pycache__/**
desktop/.DS_Store
~~~

desktop/target/release/bundle/macos/Curis.app and CurisCopy.app are packaged outputs. They are evidence or release artifacts, not source.

### 7.3 Desktop .gitignore policy recommendation

No .gitignore change was made. Future policy should cover:

~~~text
desktop/target/
desktop/node_modules/
desktop/.runtime/
desktop/runtime/__pycache__/
desktop/.DS_Store
~~~

Do not ignore desktop/src, desktop/runtime/*.py, desktop/scripts, desktop/static, desktop/icons, lockfiles or tauri.conf.json by directory-level rules.

## 8. Database Object Investigation

### 8.1 Read-only facts

There are 16 root files matching:

~~~text
<app.database.Database object at 0x...>
~~~

Facts:

- All 16 are untracked.
- All are SQLite 3.x databases, not text files.
- Each is 1,159,168 bytes.
- mtimes are between 2026-08-09 08:20:47 and 2026-08-09 10:28:58.
- They contain SQLite schema and Curis tables such as tool_traces.
- SHA-256 comparison shows 8 unique contents, with several duplicate pairs.
- They are not matched by backend/data/*.sqlite because they are at repository root and have no SQLite extension.
- No file contents were executed or modified.

### 8.2 Most likely source

The filename is the Python object representation of app.database.Database. The most likely explanation is that a database path parameter received a Database object and was stringified, causing SQLite to create or open a file using str(database) as the filename. This is a strong inference from the filename pattern and SQLite content, not a proven call-site finding.

Likely generation window: the repeated 2026-08-09 timestamps align with the earlier product / UI audit and runtime probing wave. The exact producer is not proven.

### 8.3 Decision

UNKNOWN / OWNER REVIEW.

They are strong DELETE CANDIDATE candidates after data-owner review, backup / evidence decision and confirmation that no test or audit references them. This round does not delete or move them.

## 9. Canonical Docs vs Migration Sources

### 9.1 Comparison results

| Root File | Canonical Docs File | Same / Diverged | Referenced? | Recommendation |
|---|---|---|---|---|
| Curis_Product_Master_Map_v2.0.md | docs/01_Product/Curis_Product_Master_Map_v2.0.md | Diverged | Canonical referenced by Pointer | MIGRATION SOURCE — DO NOT COMMIT |
| Curis_Page_Map_v1.0.md | docs/01_Product/Curis_Product_Page_Map_v1.0.md | Diverged | Canonical referenced by product docs | MIGRATION SOURCE — DO NOT COMMIT |
| Talent_Market_Integration_Contract.md | docs/01_Product/Curis_Talent_Market_Integration_Contract.md | Diverged | Canonical referenced by Pointer / ADR-0045 | MIGRATION SOURCE — DO NOT COMMIT |
| Talent_Market_Product_Map.md | docs/01_Product/Curis_Talent_Market_Product_Map.md | Diverged | Canonical referenced by Pointer / ADR-0045 | MIGRATION SOURCE — DO NOT COMMIT |
| Talent_Market_Resource_Audit.md | docs/01_Product/Curis_Talent_Market_Resource_Audit.md | Diverged | Canonical referenced by Pointer / ADR-0045 | MIGRATION SOURCE — DO NOT COMMIT |
| Curis_Product_Rethink_Reasoning.md | docs/01_Product/Curis_Product_Rethink_Reasoning_2026-08-13.md | Different naming and lineage | Canonical dated file referenced by Pointer / ADR-0045 | MIGRATION SOURCE — DO NOT COMMIT |

All six root/canonical comparisons diverged by SHA-256.

### 9.2 Authority rule

Authority is:

~~~text
docs/00_Context/CURRENT_STATE.md
→ docs/07_Decisions/* Status: Frozen
→ canonical docs/01_Product, docs/02_Architecture, docs/03_Design
→ docs/08_Change_Log
~~~

Root copies cannot override this chain. No root duplicate should be staged as current product truth without an explicit migration decision.

### 9.3 Reference inconsistency

Some canonical documents still use the short root-style name Curis_Product_Rethink_Reasoning.md, while the registered canonical file is the dated Curis_Product_Rethink_Reasoning_2026-08-13.md. This is a docs consistency issue, not a reason to promote the root duplicate.

## 10. AGENTS.md Governance Review

### 10.1 Actual change

The dirty AGENTS.md change updates only the Product Blueprint section:

- v5.0 becomes v5.1 ordinary-user-first Desktop shape.
- Adds six work areas, Talent Market and independent Workspaces.
- States conclusions were written back into the same Blueprint file.
- Keeps Workspace Model as Review Required until product/UI semantics are confirmed.

### 10.2 Support and risk

The content is supported by current product rebaseline inputs and Blueprint v5.1, but AGENTS.md is not tied to a distinct Issue / Review in this worktree audit. The documented product baseline remains c0e1855f, while actual HEAD is adb52210a and contains later documentation commits.

### 10.3 Decision

OWNER REVIEW.

Recommended handling:

- KEEP only if owner confirms AGENTS.md should track Blueprint v5.1 now.
- UPDATE REQUIRED if baseline and Current State wording should be revised together.
- REVERT CANDIDATE only if owner confirms accidental governance drift; no revert is performed here.

Do not stage AGENTS.md with feature code or product candidate documents.

## 11. Safe Staging Readiness

### 11.1 SAFE NOW

Only these docs-only Frozen authority files are close to safe for exact-path staging:

~~~text
docs/03_Design/Curis_Company_OS_Shared_Authority.md
docs/03_Design/Curis_Content_Growth_Domain_Authority.md
docs/07_Decisions/ADR-0046-local-agent-computer-access-authority.md
~~~

Conditions before staging:

- Confirm exact canonical versions.
- Confirm no generated or root duplicate file is included.
- Review references and status headers.
- Do not include modified CURRENT_STATE, Pointer or Change Log without separate approval.

### 11.2 SAFE AFTER HUNK SPLIT

- G1 Agent Computer Access P0: main.py, tool_executor.py, orchestrator.py and result_store.py shared hunks.
- G2 XHS accepted slice: runtime/workspace.py, runtime_foundation_router.py, runtimeApi.js and shared UI test.
- G3 RD Phase 0/1: main.py, agent_adapter.py, WorkspaceRuntimeView.js and shared Runtime files.
- G6 AI Capability: main.py, database.py, model_gateway.py, employee_templates.py and catalog files.
- G5 candidate core: models.py, registry.py, states.py, store.py and foundation.py, only after separating scenario/domain behavior.

Minimum staging semantics: each commit contains only the selected hunk, directly required test and matching Issue / Review.

### 11.3 REVIEW REQUIRED

- G4 RD Phase 2A / long-running reliability.
- G5 Shared Runtime as a whole.
- G6 Talent Market / AI Capability.
- G8 Product / Content Growth candidate docs and UI.
- G9 Workspace Engineering methodology / P0 docs.
- Evidence bundles, screenshots and packaged Desktop acceptance artifacts.

### 11.4 BLOCKED

- Whole-file staging of backend/app/main.py.
- Whole-file staging of backend/app/database.py.
- Whole-file staging of backend/app/runtime/workspace.py.
- Whole-file staging of backend/app/api/runtime_foundation_router.py.
- Whole-file staging of frontend/lib/runtimeApi.js or WorkspaceRuntimeView.js.
- Any staging of desktop/target, desktop/node_modules, .runtime, .next, active DBs, WAL/SHM or .workbuddy local state.
- Any staging of root duplicate product docs as canonical truth.
- Any staging of anomalous SQLite files without owner/data review.

### 11.5 Minimum regression by group

This is a future plan; no test was run in Round 2.

| Group | Minimum regression before commit |
|---|---|
| G1 | Existing Review focused 36-test Agent / capability / Codex / Runtime bridge set |
| G2 | XHS backend 14-pass set + Runtime Workspace UI 7-pass set |
| G3 | RD Phase 0/1 real execution and failure-path focused tests |
| G4 | Phase 2A UI / execution / long-running polling and persistence focused tests |
| G5 | Runtime foundation, schema migration, provider/materialization/API/UI focused tests in isolated SQLite |
| G6 | AI Capability registry, provider protocol and Talent Market tests; no external resource claim |
| G7/G8/G9/G10 | git diff --check and status/reference/status-header consistency |
| Repository Governance | staged path audit; no business test unless governance file changes runtime behavior |

## 12. Revised Commit Dependency Order

1. Owner decision on baseline and governance: AGENTS.md, root duplicate policy and anomalous SQLite retention.
2. Exact-path Frozen authority docs: G7 only, if owner confirms.
3. Generated / local isolation decision: future .gitignore and cleanup task, but no deletion in this round.
4. G1 Agent Computer Access P0: manually stage accepted hunks only.
5. Minimal Shared Runtime core candidate: only foundation.py and verified model/state/store pieces; exclude domain service/router/UI mixed files.
6. G2 XHS accepted slice: use shared core only if its contract is stable.
7. G3 RD Phase 0/1 accepted slice.
8. G4 RD Phase 2A / long-running candidate.
9. G6 Talent Market / AI Capability candidate.
10. G8 Product / Content Growth candidate docs and UI.
11. G9 Workspace Engineering docs.
12. G10 Issue / Review / Evidence registration.
13. Desktop source: separate future source commit after generated boundary is confirmed; never stage whole desktop/.

## 13. Remaining Owner Decisions

1. Are the three Frozen Authority files in §11.1 approved for exact-path staging?
2. Should dirty AGENTS.md v5.1 be kept, or should baseline / Current State wording be updated first?
3. Are the 16 anomalous SQLite files safe to archive or delete after evidence review?
4. Should backend/data/curis.sqlite be retained, archived or marked deletion candidate?
5. Are desktop/gen/schemas/** checked-in source assets or generated output?
6. Which packaged Desktop evidence must be retained outside desktop/target/?
7. Should the short-name Rethink link in canonical docs be corrected later?
8. Should legacy Strategy Meeting additions in main.py / database.py be grouped separately, deferred or rejected?
9. Is the ordinary-user CEO Office frontend wave an approved product candidate, or unclassified until a Product Issue exists?
10. Is an owner available to perform manual hunk extraction for mixed Runtime files?

## 14. Exact Next-Step Recommendation

The next operation should be owner review of this matrix, not staging.

After owner decisions:

1. Confirm G7 exact authority files and governance decisions.
2. Produce a temporary explicit staging manifest for one group only.
3. Manually stage / split only the selected hunk in a follow-up task.
4. Inspect staged paths and staged diff.
5. Run that group’s minimum focused regression.
6. Stop before the next group unless the staged result is accepted.

No automatic git add, directory-wide staging, generated-file cleanup or mixed-hunk resolution is authorized by this report.

## 15. Final Round-2 Summary

1. Already safe to enter precise staging: only the exact Frozen Authority docs, subject to owner confirmation.
2. Must be hunk-split first: G1, G2, G3, G5 and G6 shared source files, especially main.py, database.py, Runtime service/router, runtimeApi.js and WorkspaceRuntimeView.js.
3. Still Review Required: G4, G5 as a whole, G6, G8, G9 and most Evidence bundles.
4. Keep local / ignore: Desktop target, node_modules, .runtime, Next output, cache, WorkBuddy, WAL/SHM and local DB state after evidence policy.
5. Delete candidates: empty backend/curis.sqlite and empty backend/curis_dev.db; anomalous SQLite files are not yet deletion candidates until owner/data review.
6. Owner decisions required: governance baseline, anomalous DB retention, Desktop generated boundary, root duplicate policy, Strategy Meeting legacy changes and ordinary-user UI ownership.
7. Next operation: review this report and authorize one exact staging manifest; do not begin development.

## 16. Document Registration

- Absolute path: /Users/yy/Documents/Curis AI Workspace/docs/reviews/CURIS_WORKTREE_OWNERSHIP_AND_ISOLATION_PLAN.md
- Status: Review
- Source: current worktree read-only Git inspection, hunk headers and focused diff inspection, Issue / Review / Authority cross-check, Desktop and local-state inventory, SQLite file-type / size / hash inspection, canonical-vs-root document comparison and AGENTS.md governance diff.
- Pointer / CURRENT_STATE / CHANGE_LOG: not modified in this round because the task explicitly restricted changes to this new ownership / isolation plan.
- Next step: owner review and explicit decision on §13; after that, prepare one exact staging manifest.

> NO FILES STAGED  
> NO FILES DELETED OR MOVED  
> NO COMMITS CREATED  
> NO PUSH PERFORMED

