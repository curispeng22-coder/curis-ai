# Phase 1A AI Company Runtime Full Foundation

Status: Completed

Implementation commit: `a39becb3`

Owner seat: 系统交付席

## Minimal Context

- `docs/contracts/company-runtime-contract.md`
- `docs/contracts/department-runtime-contract.md`
- `docs/contracts/project-runtime-contract.md`
- `docs/contracts/skill-runtime-contract.md`
- `docs/contracts/tool-runtime-contract.md`
- `docs/contracts/workflow-runtime-contract.md`

## Scope

Build the Workspace backend foundation for the AI R&D Company product hierarchy:

```text
Company -> Department -> Project -> Employee -> Skill -> Tool/Model -> Workflow/Task substrate -> Knowledge Memory
```

Implement Company template lineage, a default Engineering Department, Department manager/runtime metadata, Employee template lineage, Project-owned Task and Workflow references, SkillRuntime plus EmployeeSkillBinding, and a ToolRuntime / EmployeeToolBinding projection over the existing Tool Registry and capability bindings.

## Non-Goals

- Billing, Payment, Invoice, Marketplace, ROI, or Admin Commercial Configuration.
- CEO Office UI, Meeting, Secretary, or Employee Persona.
- Complex department types, workflow redesign, direct provider SDK calls, or plaintext credential handling.
- Marketplace activation. The source enum may remain reserved, but Workspace cannot create or execute Marketplace records.

## Security Constraints

- Skill prompt guidance is bounded, redacted, length-limited, and cannot select tools or resolve credentials.
- Tool execution continues through Tool Router; tenant_private credential references continue through the existing Credential Vault resolver path.
- Workspace must not call `/api/platform/*`.

## Acceptance Criteria

- Company, Department, Project, Employee, Skill, Tool, Task, and Workflow records retain tenant and company/project lineage as applicable.
- Default Engineering Department is available per Company without modifying official templates.
- Employee Skill and Tool bindings are tenant-isolated and reuse the current capability-binding authority.
- Skill guidance reaches the existing execution prompt as non-authoritative context only.
- Existing Task, Workflow, Credential Vault, UsageEvent, and AuditEvent behavior remains regression-safe.

## Verification

- Focused Phase 1A foundation backend tests.
- Full backend regression.
- tenant isolation, secret scan, and Workspace `/api/platform/*` boundary scan.

## Completion Notes

- `knowledge/CURRENT_CONTEXT.md` is updated and `docs/release/phase1-company-runtime-foundation-report.md` is published.
- Recorded verification on 2026-07-10: 23 focused tests and 452 full backend regression tests passed; `git diff --check`, scoped secret scan, and Workspace runtime `/api/platform/*` scan passed.
- This completed Issue is the latest executable runtime baseline. Phase-1C remains design-only until a separate executable UI Issue is created and approved.
