# Phase-4.5 Workspace Demo Review And Roadmap

Date: 2026-07-09

Status: review and roadmap recommendation only.

Scope: Workspace line only. No feature implementation, no core-code change, no Workflow implementation, no credential vault implementation, no Billing, no Admin Platform governance change.

## Product Progress

Curis Workspace can now demonstrate a minimal Software R&D employee loop: Workspace reads official capabilities, CEO adds tenant_private capabilities, creates an R&D employee, binds capabilities, selects the employee for task execution, and Admin can read the employee-attributed usage_event.

## 1. Workspace Demo Review

### Demo Chain

```text
Workspace reads official capability catalog
-> Workspace adds tenant_private private capability metadata
-> Workspace creates Software R&D employee
-> employee binds official / tenant_private capabilities
-> CEO creates task and selects employee
-> employee uses bound capability through current execution path
-> task result returns
-> usage_event records tenant / task / employee / capability
-> Admin reads usage_event by tenant_id
```

### Stable Links

- Workspace official capability reads are stable through `/api/catalog/*`.
- tenant_private private capability metadata is tenant-scoped and does not pollute official catalog.
- Software R&D default templates are stable for the first demo:
  - Tech Lead
  - Product Manager
  - Architect
  - Frontend Engineer
  - Backend Engineer
  - QA Engineer
- EmployeeInstance creation is stable for the minimal fields:
  - `tenant_id`
  - `company_id`
  - `department_id`
  - `template_id`
  - `name`
  - `role`
  - `instructions_override`
  - `status`
  - `enabled`
- EmployeeCapabilityBinding is stable for official and tenant_private sources.
- Task creation with selected `employee_id` is stable.
- Default Tech Lead routing is stable when no employee is selected.
- usage_event employee attribution is stable for the accepted demo path.
- Admin usage projection can read usage_event by `tenant_id`.

### Fragile Links

- tenant_private private capabilities are not fully real yet because `credential_ref` and `config_ref` are still `scheme:reference` placeholders.
- Private model/tool/connector execution depends on current adapter and local demo configuration, not a production credential vault.
- Employee execution is currently single selected employee plus default fallback, not multi-employee collaboration.
- WorkflowTemplate exists as metadata/read model only; no real SOP step orchestration.
- Admin usage_event review may require curl or a platform usage view; this is less CEO-friendly for demos.
- Browser-visible E2E is not yet frozen as a repeatable automated demo script with screenshots.

### Demo Experience Friction

- The presenter must explain that tenant_private capability configuration is metadata-only until G2 credential vault is approved.
- The presenter must explain that "employee execution" means selected employee attribution and bound capability routing, not a team workflow.
- The presenter must explain why Admin can see usage_event but cannot edit Workspace employee instances.
- The presenter must explain why only Software R&D is available and other departments are intentionally deferred.
- The presenter may need to run backend/frontend/model-gateway commands manually.

### Needs Manual Explanation

- `credential_ref` / `config_ref` are reference handles, not real secrets.
- `marketplace` is reserved in contracts but inactive.
- Employee instructions are stored metadata; they are not a full autonomous employee memory system.
- Workflow is not active; the current demo is a single task execution path.
- Admin Platform is service/governance side; Workspace owns tenant-local employees and private capability metadata.

### Not Suitable For External Demo Without Framing

- Do not present tenant_private private tools/connectors as production-ready integrations.
- Do not present the current employee system as multi-agent collaboration.
- Do not present usage/cost as billing-ready.
- Do not present `marketplace` as available.
- Do not present credential references as secure credential storage.
- Do not show raw curl/Admin query as the main customer-facing proof unless the audience is technical.

## 2. Workspace Current Capability List

### 2.1 Truly Usable Now

- AI Task Executor basic task create/run/status/history.
- Model Gateway Adapter path through New API compatible interface when local/env configuration is provided.
- official capability read model through `/api/catalog/*`.
- tenant_private private capability metadata create/list.
- Workspace capability selector combining official and tenant_private capability options.
- EmployeeTemplate read model for Software R&D.
- DepartmentInstance and EmployeeInstance metadata.
- EmployeeCapabilityBinding metadata with tenant isolation.
- Task creation with optional selected employee.
- Default Tech Lead fallback.
- usage_event write and Admin read projection by `tenant_id`.

### 2.2 Local Demo Usable

- tenant_private private model/tool/connector setup with placeholder references.
- Selected employee task execution with employee attribution.
- Admin usage_event employee-attribution review.
- Local model gateway demo.
- Local browser demo through current Workspace operation console.

### 2.3 Placeholder Only

- `credential_ref` and `config_ref` are `scheme:reference` placeholders.
- Marketplace source is contract/schema reserved only.
- WorkflowTemplate is metadata only.
- Employee default instructions and overrides are metadata only, not a full prompt/memory system.
- CompanyTemplate / full Company Pack remains future structure.
- Multi-department organization remains future scope.

### 2.4 Requires G2 Gate

- Real credential_ref / config_ref vault.
- Safe runtime resolution of tenant_private model/tool/connector credentials.
- Secret lifecycle, rotation, revocation, and audit.
- Tenant-scoped secret access policy.
- Production-grade private connector execution.
- Any UI that accepts or references real secret material.

### 2.5 Explicitly Not Doing Now

- ROI / billing / tenant packages.
- Capability marketplace.
- Content operations, investment, ecommerce, HR, or other departments.
- Complex org chart.
- Full Workflow engine.
- Multi-agent autonomous collaboration.
- Real secret custody before G2.
- Admin Platform governance changes.

### Specific Notes

- tenant_private private capability metadata is real and tenant-isolated; production execution is not fully real until G2 credential vault exists.
- `credential_ref` / `config_ref` placeholders make demos safe but require explanation; they prevent real per-tenant private integrations from being production-ready.
- Employee execution is stable as selected employee attribution plus bound capability resolution.
- Employee collaboration is not implemented; current employees are single-point execution identities, not SOP-coordinated workers.

## 3. Workspace Risk Assessment

| Risk | Level | Assessment | Mitigation |
| --- | --- | --- | --- |
| tenant_private true usability | High | Metadata is ready, but real private model/tool/connector use needs credential vault and runtime secret resolution. | Open G2 credential vault gate before claiming production private integrations. |
| Employee system is selection, not collaboration | High | Current task has one selected employee or Tech Lead fallback. It does not run Product Manager -> Architect -> Engineer -> QA steps. | Open Phase-5 Workflow MVP after G2 boundary is clear. |
| Workflow not implemented | High | R&D department demo does not yet deliver the AI company collaboration feeling. | Build minimal bounded WorkflowStep / WorkflowTrace in Phase-5. |
| Task Execution main flow stability | Medium | Current flow passed regression, but future workflow must avoid breaking accepted Task API and model gateway path. | Preserve current execution path; add workflow as bounded orchestration layer behind a gate. |
| official / tenant_private selection stability | Medium | Selector and binding work, but private connector/tool runtime meaning depends on G2. | Keep selector read model stable; add credential-backed execution only after G2. |
| usage_event attribution completeness | Low-Medium | Employee/capability attribution is present for the demo path. More workflow steps will require step-level attribution. | Extend usage_event contract only through a Workflow MVP issue. |
| Local demo stability | Medium | Local tests are green; demo still has manual startup/screenshot steps. | Run Demo Polish in parallel for seed scripts and browser E2E. |

## 4. Next Direction Evaluation

### A. G2 Gate: Real Credential Ref / Config Ref Vault

Impact:

- Converts tenant_private private model/tool/connector from safe metadata into production-usable private capabilities.
- Enables real private model channels, private tool configs, and external connector configs without storing raw secrets in Workspace rows.
- Creates the security foundation needed before serious customer demos.

If not done:

- tenant_private remains partly theatrical for private execution.
- Workspace self-extension cannot honestly claim real private integrations.
- Every demo needs explanation that references are placeholders.

Priority:

- P0 recommended.

Dependencies:

- Requires 总控决策席 and 安全边界席 gate.
- Requires Admin/Workspace boundary confirmation for where secret material is stored and how Workspace resolves references.
- Should not be implemented as ad hoc env parsing in Workspace.

### B. Phase-5 Workflow MVP

Goal:

```text
CEO creates requirement
-> Tech Lead breaks down work
-> Architect designs
-> Frontend / Backend execute
-> QA verifies
-> Tech Lead / Product Manager reports
```

Impact:

- Major improvement to AI company experience.
- Turns employee list into visible team collaboration.
- Makes R&D department feel like an organization instead of a tagged task runner.

Complexity:

- Medium-high.
- Needs WorkflowRun / WorkflowStep / WorkflowTrace semantics.
- Needs step ownership, step status, bounded retry, evidence handoff, and usage_event step attribution.
- Must preserve Task Execution main flow and avoid full multi-agent autonomy.

Dependency on G2:

- Not strictly required for official-only workflow.
- Strongly benefits from G2 if tenant_private tools/models should be used in real workflows.

Priority:

- P1 recommended after G2 gate is opened or at least after its boundary is accepted.

### C. Demo Polish

Impact:

- Improves presentation quality without changing core behavior.
- Reduces manual setup risk.
- Helps external demos and team handoff.

Scope:

- Demo seed script.
- Startup script.
- Stable browser E2E.
- Screenshot pack.
- Demo copy.
- Clear UI hints that current demo is local/demo and private references are placeholders.

Priority:

- P2 recommended.
- Can run in parallel with G2 gate planning because it should not touch core execution.

## 5. Recommended Roadmap

### P0: G2 Credential Vault Gate

Why:

- It is the biggest gap between "tenant_private metadata exists" and "tenant_private is truly useful".
- It directly affects private models, private tools, and private connectors.

Problem solved:

- Securely resolves `credential_ref` / `config_ref` for runtime execution without storing secrets in Workspace rows.

Risk if not done:

- Workspace self-extension remains local/demo only for private integrations.
- Commercial customers cannot reliably connect their own model/tool/platform credentials.

Dependencies:

- Requires 总控决策席 approval.
- Requires 安全边界席 review.
- Requires Admin/Workspace contract update for secret ownership and access rules.

### P1: Phase-5 Workflow MVP

Why:

- It is the next product leap toward the AI Company System vision.
- It makes R&D employees collaborate by SOP instead of acting as a single selected execution identity.

Problem solved:

- Adds the first real team workflow:
  `requirement_understanding -> task_breakdown -> architecture_design -> coding -> testing -> report`.

Risk if not done:

- The employee system may feel like labels on tasks rather than an AI company.

Dependencies:

- Needs a separate Workflow MVP gate.
- Can start official-only, but tenant_private-rich workflows should wait for G2.

### P2: Phase-4.5 Demo Polish

Why:

- Current demo is functionally acceptable but operationally manual.
- Better seed/startup/screenshot assets reduce demo failure risk.

Problem solved:

- Makes demos repeatable for non-engineering reviewers.

Risk if not done:

- Demo quality depends too much on operator explanation and manual commands.

Dependencies:

- No security gate if kept documentation/seed/E2E-only and no secret handling is added.

## 6. Issue Drafts

Issue drafts created:

- `issues/phase5_g2_credential_vault_gate.md`
- `issues/phase5_workflow_mvp.md`
- `issues/phase45_demo_polish.md`

## 7. Development Recommendation

Do not enter implementation immediately.

Recommended next route:

1. Submit `issues/phase5_g2_credential_vault_gate.md` to 总控决策席 and 安全边界席.
2. Run `issues/phase45_demo_polish.md` only if it remains doc/seed/E2E-only and does not touch credential custody.
3. Start `issues/phase5_workflow_mvp.md` after G2 boundary is accepted or with official-only workflow constraints.

## 8. Verification

Commands:

```bash
git diff --check -- docs/release/phase45-workspace-demo-review-roadmap.md issues/phase5_g2_credential_vault_gate.md issues/phase5_workflow_mvp.md issues/phase45_demo_polish.md knowledge/CURRENT_CONTEXT.md
```

Result: pending.

```bash
git diff --name-only -- docs/release/phase45-workspace-demo-review-roadmap.md issues/phase5_g2_credential_vault_gate.md issues/phase5_workflow_mvp.md issues/phase45_demo_polish.md knowledge/CURRENT_CONTEXT.md
```

Result: pending.

Final result:

```text
PASS
```

Scope check:

```bash
git status --short -- docs/release/phase45-workspace-demo-review-roadmap.md issues/phase5_g2_credential_vault_gate.md issues/phase5_workflow_mvp.md issues/phase45_demo_polish.md knowledge/CURRENT_CONTEXT.md
```

Result:

```text
 M knowledge/CURRENT_CONTEXT.md
?? docs/release/phase45-workspace-demo-review-roadmap.md
?? issues/phase45_demo_polish.md
?? issues/phase5_g2_credential_vault_gate.md
?? issues/phase5_workflow_mvp.md
```

No backend, frontend, Admin Platform, Workflow runtime, credential vault, Billing, ROI, or business-module implementation file was changed for Phase-4.5.
