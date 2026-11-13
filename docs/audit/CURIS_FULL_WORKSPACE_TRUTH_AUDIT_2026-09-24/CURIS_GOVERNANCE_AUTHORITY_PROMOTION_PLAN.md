# Governance Authority Promotion Plan

Status: Review  
Authority Class: REVIEW / PROPOSAL — NOT PROMOTED

## Minimum durable governance set: 2 authorities

1. **`AGENTS.md` — Workspace Governance & Structure.** Keep it as the single frozen work protocol: authority routing, scope boundaries, canonical directories, exact write grants, task/worktree safety and required closeout. Incorporate only CEO-approved parts of the Part 1 Root Allowlist and Canonical Workspace Structure proposals. Keep it concise and point to current docs; do not duplicate Product or Implementation facts.
2. **`docs/00_Context/DOCUMENT_STATUS_RULES.md` — Document Lifecycle & Retention.** Keep this as the single lifecycle authority for classes/metadata, status, promotion, evidence retention, archive, deletion gates and links. If approved, incorporate narrow rules from the Part 1 Document Governance Proposal and this retention proposal. Product Freeze §14 remains controlling until formally revised.

Multi-agent file/task contracts should be a section of existing `AGENTS.md` plus the canonical Issue template/checklist, not a third authority. Tool-enforced validation can be an implementation later; no new authority is required merely to describe it.

## Part 1 proposal disposition

| Part 1 Review proposal | Disposition | Target if CEO approves |
|---|---|---|
| `CURIS_CANONICAL_WORKSPACE_STRUCTURE_PROPOSAL.md` | Merge only stable directory rules; do not create its proposed task directory without approval | `AGENTS.md` section / existing directory contract |
| `CURIS_ROOT_ALLOWLIST_PROPOSAL.md` | Merge into exact task/write-scope rules; no separate policy | `AGENTS.md` section |
| `CURIS_MULTI_AGENT_FILE_CONTRACT_PROPOSAL.md` | Put owner, Allowed Files/Directories, artifact namespace and return evidence into the existing Issue template | `AGENTS.md` + Issue template |
| `CURIS_DOCUMENT_GOVERNANCE_PROPOSAL.md` | Reconcile against Frozen status rules; merge lifecycle/retention once authorized | `DOCUMENT_STATUS_RULES.md` |
| `CURIS_EXISTING_WORKSPACE_GOVERNANCE_AUDIT.md` | Keep as audit evidence; not an Authority | Dated audit |
| Part 1 cleanup plan and structure proposals | Review input only; supersede only after CEO decision | This dated audit set |

## Existing rules: Keep / Supersede

- **KEEP:** Root `AGENTS.md` authority routing, Product/Implementation Truth separation, no broad destructive operations, exact issue scope, explicit review evidence, and existing status vocabulary.
- **KEEP:** `DOCUMENT_STATUS_RULES.md` current Draft/Review/Frozen/Deprecated vocabulary.
- **REVISE only via CEO gate:** Freeze §14 historical Exploration/Candidate physical retention; this proposal is not a revision.
- **SUPERSEDE after a decision only:** conflicting historical directory/status standards and parallel legacy workflow docs identified by Part 1. Do not mark them Deprecated or move them as part of Part 3.

Promotion order: CEO accepts the two-authority target → exact wording and cross-reference diff reviewed → formal authority issue and Allowed Files approved → update Pointer/Change Log if authority route changes → freeze only after acceptance. This Part 3 does not promote or edit any policy.
