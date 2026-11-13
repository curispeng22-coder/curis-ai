# Authority Graph

Authority graph reconstructed from the current frozen Pointer plus literal links in its Current Required Input section. This is an evidence graph, not a new authority.

```text
New implementation task
  ├─ Product / design: docs/00_Context/PRODUCT_DOCUMENT_POINTER.md → Current Required Input
  │   ├─ Product Blueprint → Master Map / UI Blueprint
  │   ├─ applicable Frozen shared authority: Company OS Shared Authority; Workspace Shell Contract; ADR-0046; Visual Standard V1
  │   ├─ V1 Product Freeze + Final UI Acceptance Backlog
  │   └─ task-specific domain: Content Growth Authority / RD Spec when applicable
  └─ Development / implementation: CURRENT_STATE → Completion Reconciliation → Execution Backlog → scoped Issue / accepted evidence → source and runtime
```

The Pointer says V1 Product Freeze (2026-09-23) is current: Content Growth, Writing, Music; RD and E-commerce are outside V1. Product exploration is closed; release remains BLOCKED. HTML explorations are evidence only. Frozen authority files are identified by the pointer; accepted reviews remain implementation evidence, not product truth. No conflicting Current/Frozen semantic pair was algorithmically proven in this audit; the conflict register records no verified conflict and flags unresolved candidates as UNKNOWN.

## Explicit graph edges

| From | To / relation | Evidence |
|---|---|---|
| `docs/00_Context/PRODUCT_DOCUMENT_POINTER.md` | Routes product/design to Product Blueprint → Master Map / UI Blueprint and shared/domain authorities | Pointer Current Required Input, 2026-09-23 |
| Pointer | V1 freeze, final UI backlog | Direct Markdown links |
| Pointer | CURRENT_STATE → implementation reconciliation/backlog → scoped issues/accepted evidence | Direct Markdown links |
| Historical Research / Review / Exploration | Evidence or provenance only; not default implementation input | Pointer Reference Ledger statements |
| HTML / Figma explorations | Not Product Authority | Pointer states explorations closed / history retained |

## Default start set

Implementers first read the Pointer. For every task, then read only: `CURRENT_STATE.md`; the exact active Issue and Allowed Files; the matching approved design/current authority; the accepted review or implementation evidence for the affected capability. Read Product Blueprint, Master Map, UI Blueprint and applicable Frozen contracts for product/design work. Domain contracts are task-specific. Do not treat the full source registry as an input pack.

