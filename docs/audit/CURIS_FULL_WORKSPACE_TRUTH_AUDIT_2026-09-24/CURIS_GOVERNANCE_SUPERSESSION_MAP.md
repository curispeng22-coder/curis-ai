# Governance Supersession Map

Status: Frozen / execution record for CEO-approved Gate 1, 2026-09-24.

## Active pair: two Governance Authorities

| Existing rule/source | Disposition after Gate 1 | Effective content | Future agent reads |
|---|---|---|---|
| Root `AGENTS.md` | KEEP; Gate 1 changes active | Work protocol, authority route, scope, root allowlist, canonical structure, Current Entrypoint navigation, task start/end, and cleanup boundaries | `AGENTS.md`, then formal Current Entrypoint |
| `docs/00_Context/DOCUMENT_STATUS_RULES.md` | KEEP; Gate 0/1 changes active | Document class/status, metadata, promotion, archive, retention, deletion and evidence rules | `DOCUMENT_STATUS_RULES.md` for lifecycle decisions |
| Part 1 Canonical Structure / Root Allowlist proposals | PARTIALLY SUPERSEDED by Gate 1 | Accepted path/allowlist rules are now in `AGENTS.md`; source proposals remain review evidence only | `AGENTS.md` |
| Part 1 Document Governance proposal | PARTIALLY SUPERSEDED by Gate 1 | Accepted lifecycle/retention rules are now in `DOCUMENT_STATUS_RULES.md`; source proposal remains review evidence only | `DOCUMENT_STATUS_RULES.md` |
| Part 1 Multi-Agent File Contract proposal | PARTIALLY SUPERSEDED by Gate 1 | Task ID, Allowed Files/Directories, Task Workspace, fail-closed, start/end and output manifest are in `AGENTS.md`; canonical Issue remains task-specific | `AGENTS.md` + active Issue/template |
| Part 3 Promotion Plan and this dated package | KEEP as audit evidence; never Authority | Decision rationale and execution record only | Read only when resuming this consolidation |
| Historical/legacy governance rules identified in Part 1 | REVIEW_REQUIRED individually; no unlisted rule is silently replaced | No blanket supersession; conflicting clauses need exact mapping before any later action | Follow only `AGENTS.md` and `DOCUMENT_STATUS_RULES.md` |

`CURIS_MULTI_AGENT_TASK_CONTRACT.md` was not created. The accepted two-authority model reuses `AGENTS.md` and `DOCUMENT_STATUS_RULES.md`; task-specific fields also live in the active Issue/template. No third governance Authority is active.

## Formal Current Entrypoint

The formal single path is `docs/00_Context/CURIS_CURRENT_ENTRYPOINT.md`. It is navigation only. The dated-audit `CURIS_CURRENT_ENTRYPOINT.md` remains audit evidence and is not moved or treated as Current Authority. `AGENTS.md` and `PRODUCT_DOCUMENT_POINTER.md` now route agents through the formal page; Product Truth still flows through the Pointer.
