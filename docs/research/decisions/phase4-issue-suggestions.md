# Phase-4 Issue Suggestions

Status: Phase-3.5 Research -> Decision -> Contract output

Rule: every development issue must cite competitor research, domain research, adopted decisions, and the relevant contract file. These are suggestions only, not approved implementation issues.

## Suggested Issue Sequence

### 1. Phase-4 Gate: AI Employee System MVP Boundary

References:

- `docs/research/decisions/adopted-patterns.md`
- `docs/research/decisions/rejected-patterns.md`
- `docs/contracts/employee-template-contract.md`
- `docs/contracts/department-template-contract.md`
- `docs/contracts/workflow-template-contract.md`

Objective: approve Phase-4 scope as metadata-first Software R&D department and employee template system.

Do not implement: employee runtime, workflow engine, marketplace, ROI, real credentials, Task Execution mutation.

### 2. Software R&D DepartmentTemplate First Slice

References:

- `docs/research/competitors/paperclip-companies.md`
- `docs/research/domain/department-template-research.md`
- `docs/contracts/department-template-contract.md`

Objective: implement or expose the official Software R&D DepartmentTemplate metadata.

Acceptance: official template is read-only in Workspace; tenant_private remains tenant-scoped; no multi-department UI.

### 3. R&D EmployeeTemplate First Slice

References:

- `docs/research/competitors/crewai.md`
- `docs/research/competitors/metagpt.md`
- `docs/research/competitors/chatdev.md`
- `docs/research/domain/employee-template-research.md`
- `docs/contracts/employee-template-contract.md`

Objective: implement official Tech Lead, Product Manager, Architect, Frontend Engineer, Backend Engineer, and QA Engineer templates as metadata.

Acceptance: templates are queryable, source-scoped, and do not execute tasks.

### 4. Template CapabilityBinding Metadata

References:

- `docs/research/competitors/openclaw-agents.md`
- `docs/research/competitors/gpts.md`
- `docs/research/domain/capability-catalog-research.md`
- `docs/contracts/capability-type-contract.md`

Objective: bind employee templates to model/tool/connector capability types without embedding provider credentials or tool configs.

Acceptance: no capability_type expansion beyond model/tool/connector.

### 5. Software R&D SOP Metadata

References:

- `docs/research/competitors/metagpt.md`
- `docs/research/competitors/chatdev.md`
- `docs/research/competitors/crewai-examples.md`
- `docs/research/domain/software-dev-sop-research.md`
- `docs/contracts/workflow-template-contract.md`

Objective: reserve the six-step R&D SOP metadata and step ownership.

Acceptance: no automatic workflow engine; no Task Execution mutation.

### 6. Phase-4 Workspace Read Model / UI Planning Gate

References:

- `docs/contracts/company-template-contract.md`
- `docs/contracts/department-template-contract.md`
- `docs/contracts/employee-template-contract.md`

Objective: decide what CEO can see in Workspace: department template, employee templates, and capability bindings.

Acceptance: simple operational UI only; no complex dashboard or multi-department expansion.
