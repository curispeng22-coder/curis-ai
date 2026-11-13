# Curis Workspace Research Index

Status: Phase-3.5 Workspace Research

Purpose: prepare Phase-4 AI Employee System MVP with evidence-backed template fields, contract suggestions, and a minimal Software R&D department workflow. This folder is research and planning only. It must not change the current Task Execution runtime.

## Scope

This research supports the future Curis AI Company System while preserving the current AI Task Executor and Phase-3 Demo Freeze.

Allowed:

- competitor research
- template field recommendations
- contract suggestions
- Phase-4 implement/reserve decisions

Forbidden:

- complete employee execution system
- Task Execution main-flow changes
- ROI, billing, or marketplace implementation
- real credential storage
- Admin Platform governance changes
- hard-coding research results into runtime behavior

## Research Layout

```text
docs/research/
  competitors/   P0 and P1 product or framework research
  domain/        Curis module-level synthesis
  decisions/     adopted and rejected design decisions
```

## P0 Competitor Files

- `competitors/paperclip.md`
- `competitors/paperclip-companies.md`
- `competitors/metagpt.md`
- `competitors/chatdev.md`
- `competitors/crewai.md`
- `competitors/crewai-examples.md`
- `competitors/autoagents.md`
- `competitors/openclaw-agents.md`
- `competitors/dify.md`
- `competitors/coze.md`
- `competitors/gpts.md`
- `competitors/taskade.md`
- `competitors/new-api.md`
- `competitors/one-api.md`
- `competitors/litellm.md`

## Domain Research Files

- `domain/ai-company-template-research.md`
- `domain/employee-template-research.md`
- `domain/department-template-research.md`
- `domain/software-dev-sop-research.md`
- `domain/workflow-engine-research.md`

## Decision Files

- `decisions/adopted-patterns.md`
- `decisions/rejected-patterns.md`
- `decisions/phase4-issue-suggestions.md`

## Contract Files

Contracts live outside this folder in `docs/contracts/`.

- `docs/contracts/company-template-contract.md`
- `docs/contracts/department-template-contract.md`
- `docs/contracts/employee-template-contract.md`
- `docs/contracts/workflow-template-contract.md`
- `docs/contracts/capability-type-contract.md`

No development issue may bypass this chain:

```text
Research -> Decision -> Contract -> Issue -> Development
```

## Phase-4 Research Conclusion

Curis Phase-4 should implement a minimal AI Employee System MVP around a single Software R&D department:

- one `CompanyTemplate` contract, mostly reserved
- one `DepartmentTemplate` for Software R&D
- six official R&D `EmployeeTemplate` records
- tenant-scoped `EmployeeInstance` metadata
- `CapabilityBinding` to official or tenant_private capabilities
- a minimal sequential SOP: requirement understanding -> task breakdown -> architecture design -> coding -> testing -> report

Phase-4 should not implement automatic hiring, full autonomous workflow engines, employee memory, marketplace templates, ROI, budget enforcement, or multi-department UI.
