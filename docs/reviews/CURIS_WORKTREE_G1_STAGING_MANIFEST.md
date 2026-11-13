# CURIS WORKTREE G1 STAGING MANIFEST

Status: Review  
Date: 2026-08-16  
Round: 2.5 — G1 Exact Staging Manifest  
Owner decision source: CURIS_WORKTREE_RECONCILIATION_DECISIONS.md  
Issue: issues/AGENT-COMPUTER-ACCESS-RUNTIME-P0-001.md  
Review: reviews/AGENT-COMPUTER-ACCESS-RUNTIME-P0-001_review.md  
Canonical root: /Users/yy/Documents/Curis AI Workspace/docs/

## 1. Manifest purpose

本文件只定义下一轮第一次真实 staging 的 G1 边界。

G1 = Agent Computer Access Runtime P0。

本文件不是 staging 命令，也不授权当前执行 staging。

本轮已完成：

- 重新读取 G1 Issue、Allowed Files 和 Explicit Exclusions。
- 重新读取 G1 Review、Acceptance、36-test baseline 和 isolated SQLite evidence。
- 重新检查 G1 whole-file candidates 的实际内容。
- 重新检查 main.py、tool_executor.py、orchestrator.py、result_store.py 的真实 diff。
- 重新判断 G1 dependency closure。
- 重新排除 AI Capability、Talent Market、RD、Shared Runtime、Strategy Meeting 和 Desktop 产物。

本轮没有：

- git add
- git add -p
- git commit
- git push
- 测试或 regression
- 源码修改
- 旧 Review / CURRENT_STATE / Pointer / Change Log 修改

## 2. G1 Product and Runtime Semantics

G1 只提交以下事实链：

~~~text
requested_intent
→ native_mapping
→ configured_state
→ effective_state
→ verification_state
→ evidence / verified_at
→ session/result audit snapshot
~~~

必须保留的语义：

- ASK_WHEN_NEEDED 和 AUTO_WITHIN_BOUNDARY 映射到支持的新 session sandbox 参数。
- 新 session command accepted 只产生 CONFIGURED，不产生 effective permission claim。
- 没有 provider-native evidence 时，effective_state 仍为 UNKNOWN，verification_state 仍为 UNVERIFIED。
- Resume 不带 stale sandbox 参数，不继承旧 effective/granted 状态。
- Resume 生成 fresh snapshot：NOT_CONFIGURABLE / UNVERIFIED / UNKNOWN，并记录 provider limitation。
- REQUEST_WIDEST_NATIVE_ACCESS / Full Computer Access 在启动外部进程前 fail-closed。
- Full Access 不得被自动降级、绕过或伪装成 active/granted/effective。
- Snapshot 通过既有 ToolExecutor → Orchestrator → ResultStore / Usage audit 路径保存。
- 不建立新的 Schema、Parallel Access Store、Computer Access UI 或 Permission Engine。

## 3. Authority and Allowed File Recheck

### 3.1 Issue facts

Issue status:

> IMPLEMENTED / ACCEPTED

Issue Goal 明确只修 Codex Adapter access-truth path。

Issue Allowed Files:

~~~text
backend/app/agent_adapter.py
backend/app/main.py
backend/app/tool_executor.py
backend/app/orchestrator.py
backend/app/result_store.py
backend/tests/test_agent_adapter.py
backend/tests/test_agent_computer_access_runtime_p0.py
issues/AGENT-COMPUTER-ACCESS-RUNTIME-P0-001.md
reviews/AGENT-COMPUTER-ACCESS-RUNTIME-P0-001_review.md
~~~

Issue Explicit Exclusions include:

- Computer Access UI、Registry P1、P2 adapters、Claude Code、WorkBuddy、TRAE。
- Product Blueprint、Frozen ADR/design contracts、XHS、RD、TTK、Workspace shell。
- Capability catalog expansion。
- Real Full Computer Access、bypass flags、OS/TCC/Keychain/MDM changes。
- Schema migration or parallel access/session persistence system。
- Active database。

### 3.2 Review facts

Review decision:

> AGENT COMPUTER ACCESS RUNTIME P0 IMPLEMENTED / ACCEPTED

Review records:

- isolated SQLite path and restart readback。
- new / resume / Full unsupported snapshots。
- py_compile passed。
- formal focused baseline: 36 passed。
- no active database, credential, external task or platform call。
- no Computer Access UI。
- no Full Computer Access。
- no provider-effective verification claim beyond available evidence。

ADR-0046 is an Authority file, but it is explicitly outside the G1 Issue Allowed Files and belongs to a separate Frozen docs-only commit. It must not be added to the G1 code commit.

## 4. Whole-file candidates

These files can be included as whole files in the future G1 staging operation, after final path/status check:

| Path | Why whole-file is safe | Other initiative content | Safe to Stage? |
|---|---|---|---|
| backend/app/agent_adapter.py | Untracked file is the Codex Adapter implementation; imports only standard library; methods implement requested/configured/effective separation, resume fresh snapshot and Full fail-closed | No observed XHS/RD/Talent Market/Shared Runtime code | YES, whole-file candidate |
| backend/tests/test_agent_adapter.py | Tests new/resume separation, Full rejection and opaque manifest references | No other initiative test | YES, whole-file candidate |
| backend/tests/test_agent_computer_access_runtime_p0.py | Uses isolated tmp SQLite and existing ToolExecutor/ResultStore path; tests snapshot propagation and persistence | No active DB; no new initiative feature test | YES, whole-file candidate |
| issues/AGENT-COMPUTER-ACCESS-RUNTIME-P0-001.md | Exact G1 Issue and allowed scope | No other initiative implementation | YES, whole-file candidate |
| reviews/AGENT-COMPUTER-ACCESS-RUNTIME-P0-001_review.md | Exact G1 Formal Acceptance Record | It references broader regression dependencies but does not claim their ownership | YES, whole-file candidate |

### 4.1 Whole-file caveats

- Untracked does not mean already approved for commit; final staged path audit is still required.
- Do not include ADR-0046 in the same G1 code commit.
- Do not include any other file under backend/app/agent_conversion, runtime, capability, model gateway or frontend.
- The matching Issue / Review may be included with G1, but their status text must not be changed.

## 5. Hunk candidates

### 5.1 backend/app/main.py

Current modified diff contains multiple unrelated initiatives in the same file:

- local dotenv loading
- Runtime trace
- AI Capability provider protocol and local provider behavior
- AI Capability router
- Strategy Meeting
- Talent Market endpoints and recruit flow
- RD runtime execution and long-running worker
- connector projection

Therefore whole-file staging is prohibited.

The actual G1-related code is the Codex CLI branch in the tenant-private agent execution path:

~~~text
Git hunk:
@@ -1886,29 +1955,47 @@ create_app

G1 subrange candidate:
new lines approximately +1982–2009
~~~

G1 purpose:

- import CodexCliAdapter only for the codex-cli agent kind。
- construct the adapter with cwd, sandbox, requested_intent and timeout。
- execute through existing execute_attempt path。
- allow the agent kind branch to run without a resolver-managed API key。
- preserve fail-closed unsupported configuration behavior。

The same Git hunk also contains non-G1 additions around new lines +1955–1981:

- provider_type and base_url extraction。
- local-no-auth behavior for ollama / lm_studio。
- provider_protocol and chat_path。
- ModelGatewayAdapter protocol changes。

These belong to AI Capability / Model Provider work and must not be staged with G1.

Decision:

> MIXED HUNK — MANUAL SPLIT REQUIRED

G1 main.py staging status:

> G1 BLOCKED BY MIXED HUNK for the full runtime integration path until this hunk is manually split.

Do not stage:

- import asyncio at the top of main.py; it supports RD long-running execution。
- local dotenv loader。
- Runtime trace hunk。
- AI Capability router。
- Strategy Meeting model or endpoints。
- Talent Market endpoints / recruit / skill install。
- RD runtime foundation router and rd_task:auto execution block。
- connector projection。
- unrelated one-line workflow adjustment。

### 5.2 backend/app/tool_executor.py

There are two relevant diff hunks:

~~~text
Hunk A:
@@ -78,24 +78,31 @@ class ToolExecutor

New response propagation fields:
session_id
progress
artifacts
permissions
computer_access
resume_supported
cancel_supported

Hunk B:
@@ -140,25 +147,26 @@ class ToolExecutor

The same Agent result fields are propagated into the chain result.
~~~

G1 purpose:

- carry the Agent Adapter result, including computer_access snapshot, through the existing ToolExecutor response path。
- retain requested/configured/effective facts instead of dropping them。
- retain existing Agent session/artifact/resume/cancel output needed by the accepted Result/Artifact path。

Recheck result:

- These hunks are in a G1 Allowed File。
- They contain Agent result propagation, not XHS/RD/Talent Market code。
- No RD code_change Artifact or RD Evidence field is added in this file hunk。
- The word artifacts refers to Agent result output; it is not the RD code-change Artifact creation path in runtime/workspace.py or main.py。

Decision:

> G1-ONLY ADAPTER RESULT PROPAGATION HUNKS — STAGE AFTER STAGED-DIFF CHECK

Safe to stage:

- Hunk A and Hunk B together with G1, provided the staged diff contains only the listed Agent result keys and no neighboring initiative changes.

### 5.3 backend/app/orchestrator.py

Git hunk:

~~~text
@@ -412,24 +412,30 @@ class Orchestrator
~~~

G1 additions:

- session_id
- agent_artifacts
- agent_permissions
- computer_access
- resume_supported
- cancel_supported

Purpose:

- merge Agent Adapter output into the existing final result。
- preserve computer_access snapshot and Agent audit metadata through orchestration。

Recheck result:

- The hunk is in the G1 Allowed Files。
- It does not add RD cycle, RD Artifact, Evidence, XHS, Talent Market or Shared Runtime logic。
- agent_artifacts is Agent result metadata, not RD code-change Artifact persistence。

Decision:

> G1-ONLY HUNK — SAFE AFTER STAGED-DIFF CHECK

### 5.4 backend/app/result_store.py

Git hunk:

~~~text
@@ -716,24 +716,30 @@ class ResultStore
~~~

G1 additions:

- session_id
- agent_artifacts
- agent_permissions
- computer_access
- resume_supported
- cancel_supported

Purpose:

- add Agent result and computer_access snapshot into the existing optional usage-audit payload。

Critical reconciliation result:

- This hunk does not add RD code_change Artifact creation。
- It does not add RD Evidence creation or RD Artifact Review。
- RD-specific Artifact creation remains in separate runtime / execution code outside this hunk。
- The field agent_artifacts is an Agent result projection and is covered by the G1 Review’s existing Result/Artifact/Audit path language。

Decision:

> G1-ONLY HUNK — SAFE AFTER STAGED-DIFF CHECK

If a future staged diff shows additional RD-specific Artifact / Evidence lines adjacent to this hunk, stop and reclassify:

> MIXED HUNK — MANUAL SPLIT REQUIRED

## 6. G1 Dependency Closure

### 6.1 Required for G1

Required direct files:

- backend/app/agent_adapter.py
- backend/app/tool_executor.py G1 result propagation hunks
- backend/app/orchestrator.py G1 result merge hunk
- backend/app/result_store.py G1 audit payload hunk
- backend/app/main.py Codex branch subrange after manual split
- two G1 tests
- G1 Issue
- G1 Review

Existing dependencies are reused:

- existing capability resolution and tenant context。
- existing ToolExecutor / Orchestrator / ResultStore / Usage audit route。
- existing SQLite Database behavior through test-isolated paths。
- standard-library subprocess / JSON / filesystem handling in agent_adapter.py。

### 6.2 Not required and explicitly excluded

G1 does not require new files from:

- capability registry expansion。
- AI Capability router or provider protocol changes。
- model_gateway.py。
- Talent Market / Agent conversion。
- Runtime Foundation / Workspace Runtime。
- RD Workspace / long-running execution。
- XHS / TTK。
- Strategy Meeting。
- Desktop source or packaged runtime。
- active database or database schema migration。
- Computer Access UI or Permission Engine。

### 6.3 Closure result

Ideal result:

> NO UNRELATED INITIATIVE DEPENDENCY

Qualification:

- Direct G1 tests do not need AI Capability, Talent Market, RD or Shared Runtime new files。
- Runtime integration through main.py needs the Codex branch subrange, but that subrange is currently embedded in a mixed hunk。
- Therefore G1 source/test closure is logically complete, while full runtime integration staging is blocked until manual hunk split。
- Do not enlarge G1 scope to make the mixed hunk easy to stage。

## 7. Proposed Commit Semantics

Suggested commit message:

~~~text
feat(runtime): persist local agent computer access truth
~~~

Suggested commit description:

~~~text
- separate requested, configured and effective computer-access facts
- persist access snapshots through existing Agent result and audit paths
- map supported new-session Codex sandbox modes explicitly
- create a fresh unverified snapshot on resume
- reject Full Computer Access before process launch
- never infer effective access from command acceptance or prior state
~~~

The commit must explicitly say:

- requested/configured/effective truth is separated。
- effective access remains UNKNOWN without provider evidence。
- resume does not inherit a prior effective claim。
- Full Computer Access remains unsupported and fail-closed。
- persistence uses existing Result / Artifact / Usage audit paths only。

The commit must not claim:

- Full Computer Access is supported。
- unrestricted access。
- approval bypass。
- OS/TCC/Keychain/MDM changes。
- automatic permission grant。
- Package automatically receives computer access。
- RD long-running reliability is part of G1。
- AI Capability provider protocols are part of G1。

## 8. Minimum Regression Plan

This is a plan only. No tests were run in Round 2.5.

### 8.1 Compile check

~~~text
backend/.venv/bin/python -m py_compile \
  backend/app/agent_adapter.py \
  backend/app/main.py \
  backend/app/tool_executor.py \
  backend/app/orchestrator.py \
  backend/app/result_store.py
~~~

This checks the partial main.py result after manual hunk split without touching an active database.

### 8.2 G1 focused tests

~~~text
backend/.venv/bin/python -m pytest -q \
  backend/tests/test_agent_adapter.py \
  backend/tests/test_agent_computer_access_runtime_p0.py
~~~

These use direct adapter behavior and isolated temporary SQLite paths.

### 8.3 Necessary existing regression dependencies

~~~text
backend/.venv/bin/python -m pytest -q \
  backend/tests/test_codex_agent_backend.py \
  backend/tests/test_runtime_bridge_private_model.py
~~~

These are existing Agent / Codex / ResultStore bridge regressions, not new Talent Market or AI Capability feature acceptance.

### 8.4 Formal Review baseline

The formal Review recorded:

~~~text
backend/.venv/bin/python -m pytest -q \
  backend/tests/test_agent_adapter.py \
  backend/tests/test_agent_computer_access_runtime_p0.py \
  backend/tests/test_ai_capability_registry.py \
  backend/tests/test_codex_agent_backend.py \
  backend/tests/test_runtime_bridge_private_model.py

36 passed
~~~

The 36-pass command is the broader acceptance baseline. The first G1 staging validation should use the narrower commands above and must not pull G6 AI Capability implementation into the G1 commit merely because its test appeared in the historical 36-pass baseline.

### 8.5 Isolation rules

- Tests must use isolated temporary SQLite paths。
- Do not use data/curis.sqlite, backend/data/curis.sqlite, any root Database object file or active issue pipeline DB。
- Do not run external Codex tasks or platform calls as part of staging validation。
- Do not run XHS, RD, Talent Market or Workspace Engineering new-feature tests in the G1 staging check。
- Do not alter the current worktree while validating the staged patch。

## 9. Precise Stage Preview

### 9.1 Whole files

~~~text
backend/app/agent_adapter.py
backend/tests/test_agent_adapter.py
backend/tests/test_agent_computer_access_runtime_p0.py
issues/AGENT-COMPUTER-ACCESS-RUNTIME-P0-001.md
reviews/AGENT-COMPUTER-ACCESS-RUNTIME-P0-001_review.md
~~~

ADR-0046 is not in this G1 code commit. It is a separate Frozen docs-only staging candidate:

~~~text
docs/07_Decisions/ADR-0046-local-agent-computer-access-authority.md
~~~

### 9.2 Partial files

~~~text
backend/app/main.py
  - manually split the mixed agent execution hunk
  - include only the CodexCliAdapter branch and agent-kind gate around new lines +1982–2009
  - exclude provider_type/base_url/local-no-auth/provider_protocol/chat_path additions
  - exclude dotenv, Runtime trace, AI Capability router, Strategy Meeting, Talent Market, RD and connector hunks

backend/app/tool_executor.py
  - Hunk A: @@ -78,24 +78,31 @@
  - Hunk B: @@ -140,25 +147,26 @@
  - include only the Agent result propagation keys listed in §5.2

backend/app/orchestrator.py
  - Hunk: @@ -412,24 +412,30 @@
  - include Agent result merge fields listed in §5.3

backend/app/result_store.py
  - Hunk: @@ -716,24 +716,30 @@
  - include Agent audit payload fields listed in §5.4
~~~

### 9.3 Explicit excludes

~~~text
backend/app/model_gateway.py
backend/app/ai_capability_registry.py
backend/app/capability_catalog.py
backend/app/capability_registry.py
backend/app/catalog_constants.py
backend/app/agent_conversion/**
backend/app/runtime/**
backend/app/api/runtime_foundation_router.py
backend/app/database.py
frontend/**
docs/03_Design/Curis_Company_OS_Shared_Authority.md
docs/03_Design/Curis_Content_Growth_Domain_Authority.md
docs/01_Product/**
docs/02_Architecture/**
docs/03_Design/**
docs/05_Workspace_Engineering/**
desktop/**
data/**
backend/data/**
backend/curis.sqlite
backend/curis_dev.db
root <app.database.Database object at ...> files
curis-ui-prototype/**
curis-ui-prototype.bak/**
.workbuddy/**
artifacts/**
previews/**
delivery/**
AGENTS.md
.gitignore
~~~

The three Frozen Authority documents are excluded from the G1 code commit even though they may be separately stageable.

### 9.4 Blockers

Current blockers:

1. main.py G1 Codex branch is embedded in a mixed hunk with AI Capability provider changes.
2. The exact first staging operation must manually split that hunk; no automatic split is authorized.
3. The G1 staging preview cannot be considered complete until the staged diff confirms that no provider, Talent Market, RD, Strategy Meeting or Runtime lines entered main.py.
4. If the future staged result_store.py hunk contains RD-specific code_change Artifact / Evidence lines beyond the currently observed diff, stop and reclassify it as MIXED HUNK — MANUAL SPLIT REQUIRED.

Not blockers:

- No dependency on new capability registry files。
- No dependency on model_gateway provider protocol changes。
- No dependency on Runtime Foundation or RD source files for the direct G1 tests。
- No dependency on active databases。
- ADR-0046 being separate is intentional, not a G1 blocker。

## 10. G1 Readiness Decision

G1 is not ready for an all-at-once staging command.

Correct readiness label:

> SAFE AFTER HUNK SPLIT

More precisely:

- Whole-file candidates: ready for precise staging after final status/path check。
- tool_executor.py: G1 propagation hunks are stageable after staged-diff check。
- orchestrator.py: G1 result merge hunk is stageable after staged-diff check。
- result_store.py: G1 audit payload hunk is stageable after staged-diff check; current observed hunk has no RD code-change Artifact/Evidence logic。
- main.py: G1 BLOCKED BY MIXED HUNK until manual split。
- Full G1 commit: not authorized in this round。

## 11. Exact Next Step

After Owner Review, the next operation should be one manually prepared staging action using only §9.1 and the verified partial hunks in §9.2.

Before any future commit:

1. Confirm staged paths exactly match §9.1 and §9.2。
2. Inspect staged diff for excluded initiative markers。
3. Run the narrow G1 compile and focused tests in §8。
4. Run git diff --cached --check。
5. Stop and request review before staging any other Group。

## 12. Document Registration

- Absolute path: /Users/yy/Documents/Curis AI Workspace/docs/reviews/CURIS_WORKTREE_G1_STAGING_MANIFEST.md
- Status: Review
- Source: G1 Issue / Review, actual G1 source and test files, current diffs in main.py / tool_executor.py / orchestrator.py / result_store.py, and Round 2.5 Owner Correction.
- Pointer / CURRENT_STATE / CHANGE_LOG: not modified.
- Next step: Owner decides whether to authorize the first real G1 staging after manual main.py hunk split.

> NO FILES STAGED  
> NO TESTS RUN  
> NO SOURCE MODIFIED  
> NO COMMITS CREATED  
> NO PUSH PERFORMED
