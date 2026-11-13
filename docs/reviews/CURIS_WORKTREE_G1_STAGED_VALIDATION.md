# Curis Worktree G1 Staged Validation

**Status:** Review  
**Date:** 2026-08-16  
**Scope:** G1 — Agent Computer Access Runtime P0 precise staging and validation  
**Authorization:** Precise G1 staging + staged diff checks + G1 focused regression only

## 1. Exact staged files

The index contains exactly these nine paths:

```text
backend/app/agent_adapter.py
backend/app/main.py
backend/app/orchestrator.py
backend/app/result_store.py
backend/app/tool_executor.py
backend/tests/test_agent_adapter.py
backend/tests/test_agent_computer_access_runtime_p0.py
issues/AGENT-COMPUTER-ACCESS-RUNTIME-P0-001.md
reviews/AGENT-COMPUTER-ACCESS-RUNTIME-P0-001_review.md
```

Whole-file candidates staged:

- `backend/app/agent_adapter.py`
- `backend/tests/test_agent_adapter.py`
- `backend/tests/test_agent_computer_access_runtime_p0.py`
- `issues/AGENT-COMPUTER-ACCESS-RUNTIME-P0-001.md`
- `reviews/AGENT-COMPUTER-ACCESS-RUNTIME-P0-001_review.md`

Partial staged files:

- `backend/app/main.py`
- `backend/app/tool_executor.py`
- `backend/app/orchestrator.py`
- `backend/app/result_store.py`

`docs/07_Decisions/ADR-0046-local-agent-computer-access-authority.md` was not staged.

Staged summary: 9 files changed, 752 insertions, 8 deletions.

## 2. Exact staged hunks

### `backend/app/main.py`

Only the G1 execution path is staged:

- `cap_type == "agent"` no longer requires a resolved provider API key before entering the agent branch, allowing the local Codex CLI adapter path.
- `agent_kind == "codex-cli"` constructs `CodexCliAdapter` with `cwd`, `sandbox`, `requested_intent`, and bounded `timeout`, then runs it through the existing `execute_attempt` path.
- The existing OpenAI-compatible branch remains fail-closed and is kept as the `elif` branch; no provider configuration fields were staged.
- Unsupported agent execution uses the explicit fail-closed configuration-rejected message.

The staged `main.py` diff does not include provider type/base URL/local-no-auth/protocol/chat-path changes, dotenv loading, Runtime trace, AI Capability routes, Strategy Meeting routes, Talent Market routes, RD execution, or connector projection.

### `backend/app/tool_executor.py`

Only Agent result propagation fields were staged:

```text
session_id
progress
artifacts
permissions
computer_access
resume_supported
cancel_supported
```

The fields are carried through the existing direct result and chained result paths.

### `backend/app/orchestrator.py`

Only the Agent result merge fields were staged:

```text
session_id
agent_artifacts
agent_permissions
computer_access
resume_supported
cancel_supported
```

### `backend/app/result_store.py`

Only the corresponding Agent audit payload fields were staged:

```text
session_id
agent_artifacts
agent_permissions
computer_access
resume_supported
cancel_supported
```

### Whole-file G1 additions

`agent_adapter.py`, its two focused test files, and the G1 Issue/Review are the exact
whole-file candidates authorized by `CURIS_WORKTREE_G1_STAGING_MANIFEST.md`.

## 3. `main.py` split method

The mixed `main.py` patch was handled in two steps:

1. Interactive staging skipped all non-G1 hunks.
2. The shared agent/provider hunk was not staged wholesale. A precise index-only patch
   inserted the Codex CLI branch and changed the existing provider branch to `elif`
   without changing the working-tree provider condition or adding provider fields.

The working tree remains unchanged by this extraction. The ordinary working diff still
contains the provider, Runtime trace, AI Capability, Strategy Meeting, Talent Market,
RD, and connector changes.

## 4. Explicit excludes verification

No excluded path is staged. In particular, the index does not contain:

- ADR-0046
- frontend files
- active SQLite, database migration, WAL or SHM files
- `desktop/target`, `node_modules`, `.runtime`, `.next`, `.workbuddy`, artifacts or previews
- `AGENTS.md` or `.gitignore`
- XHS, RD, Shared Runtime expansion, Strategy Meeting, Talent Market, AI Capability,
  Workspace Engineering, Content Growth or other initiative implementation files

The G1 Issue and Review mention other initiatives in their explicit boundary and future
scope prose. Those are documentation references, not staged implementation hunks.

## 5. Staged whitespace check

Command:

```text
git diff --cached --check
```

Result: **BLOCKED / non-zero**. It reported Markdown hard-break trailing whitespace in
the newly staged G1 Issue and Review:

```text
issues/AGENT-COMPUTER-ACCESS-RUNTIME-P0-001.md:3-5
reviews/AGENT-COMPUTER-ACCESS-RUNTIME-P0-001_review.md:3-6
```

These files were staged as the exact authorized whole-file candidates. No whitespace
normalization was applied because this round does not authorize rewriting the Issue or
Review content. This is the only staged-check blocker observed.

## 6. Compile result

Command:

```text
backend/.venv/bin/python -m py_compile \
  backend/app/agent_adapter.py \
  backend/app/main.py \
  backend/app/tool_executor.py \
  backend/app/orchestrator.py \
  backend/app/result_store.py
```

Result: **PASS**.

## 7. G1 focused test result

Command:

```text
backend/.venv/bin/python -m pytest -q \
  backend/tests/test_agent_adapter.py \
  backend/tests/test_agent_computer_access_runtime_p0.py
```

Result: **PASS — 5 passed in 0.24s**.

The G1 tests use isolated temporary SQLite paths and mocked/local runners. No external
Codex task was started.

## 8. Bridge regression result

Command:

```text
backend/.venv/bin/python -m pytest -q \
  backend/tests/test_codex_agent_backend.py \
  backend/tests/test_runtime_bridge_private_model.py
```

Result: **PASS — 24 passed in 7.35s**.

The run emitted existing FastAPI deprecation warnings only; no test failure occurred.

## 9. Working-tree preservation check

Post-validation status still shows:

- `MM backend/app/main.py`: the G1 hunk is staged while all other `main.py` initiative
  changes remain unstaged.
- `M backend/app/database.py` and other backend/runtime files remain unstaged.
- frontend changes remain unstaged.
- G2/G3/G5/G6/G7/G8/G9 candidate files and local/temporary artifacts remain untracked
  or unstaged.
- `.gitignore`, `AGENTS.md`, CURRENT_STATE, Pointer and Change Log remain unstaged.

The remaining tracked working-tree diff is still present across 69 files, including the
non-G1 `main.py` provider, Strategy Meeting, Talent Market, RD, and connector hunks.
No reset, restore, clean, delete, move, or commit operation was performed.

## 10. Blockers and deviations

Blocker:

- `git diff --cached --check` fails on intentional Markdown hard-break trailing spaces
  in the two exact whole-file G1 documentation candidates.

No G1 code-scope deviation was found. The staged implementation paths and hunk content
remain within the authorized G1 manifest.

## 11. Commit readiness recommendation

**G1 implementation and regression validation: READY.**

**G1 commit readiness: NOT READY until the staged whitespace check is resolved or an
explicit owner decision accepts those existing Markdown hard-break spaces.**

This round intentionally stops before any commit or push. The validation report itself
is not staged.

```text
AUTHORIZED: PRECISE G1 STAGING + VALIDATION
NOT AUTHORIZED: COMMIT / PUSH / NEXT GROUP
```
