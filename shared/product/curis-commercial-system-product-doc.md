# Curis Commercial AI Company System Product Document

Status: Product blueprint for future commercial multi-tenant system.
Date: 2026-07-08
Owner: 产品规划席

This document is a future-product blueprint. It does not replace the current AI Task Executor MVP gate or the canonical L0-L6 architecture in `knowledge/002_Product_Vision.md` and `knowledge/003_Architecture.md`.

## 1. Product Definition

Curis will become a commercial multi-tenant AI Company System.

The product has two connected but separate products:

1. **Curis Admin Platform**: platform operator console. It manages CEOs, tenants, plans, global model providers, global tool catalog, platform connectors, department type catalog, security policies, quotas, billing rules, audits, and rollout controls.
2. **Curis Workspace**: tenant-facing CEO company workspace. Each CEO enters their own company, selects departments from the platform-approved department catalog, configures allowed business platforms, chooses models from the allowed model catalog, creates or assigns AI employees, and runs company work.

The core shift:

- Models, tools, department types, external platform connector definitions, plans, quotas, and security policies are centrally managed by the Admin Platform.
- CEOs do not create platform primitives from scratch. They instantiate and configure what the Admin Platform has made available to their tenant/plan.
- Workspace remains focused on company operation: department selection, business setup, employee configuration, tasks, workflow execution, review, publishing, and optimization.

## 2. Product Split

### 2.1 Curis Admin Platform

Users:

- Platform owner.
- Operations admin.
- Model/tool integration admin.
- Security/compliance reviewer.
- Customer success/operator.

Primary jobs:

- Manage all tenant CEOs.
- Create, suspend, upgrade, downgrade, or inspect tenant companies.
- Maintain global model providers and model catalog.
- Maintain global tool registry and tool capability catalog.
- Maintain external platform connector definitions.
- Maintain department type catalog and default manifests.
- Define plans, quotas, feature gates, rate limits, and usage caps.
- Manage platform audit, incident review, and release rollout.
- Approve or block high-risk integrations and global policy changes.

Admin Platform owns:

- `tenant` and CEO account lifecycle.
- Plan and billing configuration.
- Global model provider credentials and allowed model list.
- Global tool registry.
- External connector templates and platform-level credential policies.
- Department type definitions.
- Global security policies.
- Cross-tenant reporting and platform audit.
- System-wide feature flags and rollout versions.

Admin Platform does not own:

- A CEO's daily tasks.
- A CEO's company-specific business decisions.
- Department-specific task execution.
- Employee work assignment inside a tenant company.
- Tenant-specific content outputs.

### 2.2 Curis Workspace

Users:

- CEO.
- Tenant company operator.
- Future department owner roles.

Primary jobs:

- Configure company profile and business scope.
- Select enabled departments from platform-approved department catalog.
- Configure each department's business purpose, quality line, output channels, and allowed platforms.
- Select allowed models for company or department use.
- Configure AI employees inside enabled departments.
- Submit tasks and review workflows.
- Approve publish actions.
- Review cost, task performance, quality, and ROI once future L6 opens.

Workspace owns:

- Tenant company topology.
- Enabled departments and department instances.
- Tenant-scoped platform account connections.
- Tenant-specific model selection from allowed model catalog.
- Department-level policy and quality configuration.
- AI employee configuration inside tenant company.
- Tasks, workflows, execution results, traces, approvals, and tenant memory.
- CEO dashboards and department operating views.

Workspace does not own:

- Global model provider definitions.
- Global tool definitions.
- Global connector templates.
- Department type catalog source definitions.
- Global pricing rules.
- Cross-tenant policy.
- Platform admin audit or tenant lifecycle management.

## 3. Full Product Module Map

### 3.1 Admin Platform Modules

| Module | Purpose | Key Screens |
| --- | --- | --- |
| Platform Overview | Monitor tenants, usage, incident health, revenue, model spend | Overview dashboard, health timeline |
| CEO / Tenant Management | Manage commercial customers and companies | CEO list, tenant detail, create CEO, plan/quota drawer |
| Plan & Quota Center | Define commercial packages and feature gates | Plan list, create plan, quota matrix |
| Model Provider Center | Add providers and model catalog | Provider list, add provider, add model, model pricing |
| Tool Registry | Manage platform-approved tools | Tool catalog, add tool, capability mapping |
| Connector Center | Define external business platform connectors | Connector catalog, add platform, credential policy |
| Department Type Catalog | Manage department templates available to CEOs | Type list, create department type, manifest editor |
| Security & Compliance | Manage secrets policy, risk review, audit | Audit log, risk queue, key rotation |
| Rollout & Feature Flags | Control feature availability by plan/tenant | Flag list, rollout rules, staged release |
| Platform Analytics | Cross-tenant usage and cost view | Usage trends, tenant comparison, provider spend |

### 3.2 Workspace Modules

| Module | Purpose | Key Screens |
| --- | --- | --- |
| CEO Cockpit | Company overview and next actions | Company health, pending approvals, task queue |
| Company Setup | Create company topology | Setup wizard, business scope, department selection |
| Department Center | Manage enabled departments | Department list, create department, department detail |
| Business Department | Run external business workflows | Platform binding, content pipeline, publishing state |
| HR Department | Configure AI employees and roles | Employee list, create employee, skill matrix |
| Admin Department | Cost, token, ROI and governance | Usage, cost allocation, policy decisions |
| BI Department | Analysis and visual reports | Trends, funnels, department comparison |
| Model Assignment | Select models per company/department | Model selector, fallback policy |
| Platform Accounts | Connect tenant-owned accounts | Account list, connect platform, permission check |
| Task Console | Execute AI work | Task composer, workflow detail, run history |
| Workflow Center | Define or inspect repeatable workflows | Workflow templates, state machine, queue |
| Memory & Assets | Tenant memory and generated assets | Project memory, media library, outputs |
| Governance & Audit | Approval, risk, locked actions | Approval queue, audit trail |

## 4. Data Ownership Boundary

### 4.1 Platform-Owned Data

- CEO user account.
- Tenant record.
- Plan and quota definitions.
- Global model provider definitions.
- Global model catalog and model capability metadata.
- Global tool registry.
- External connector definitions.
- Department type definitions and default manifest schema.
- Platform security policies.
- Platform audit records.
- Feature flags and rollout controls.

### 4.2 Workspace-Owned Tenant Data

- Company profile.
- Company topology.
- Enabled department instances.
- Tenant-owned platform account connection references.
- Department configuration.
- Employee instances and skill assignment.
- Task records.
- Workflow execution records.
- Execution traces and outputs.
- Tenant memory and assets.
- Tenant approvals and audit trail.
- Tenant usage and later ROI metrics.

### 4.3 Shared Contract Data

These are defined by Admin Platform and consumed by Workspace:

- Department type manifest schema.
- Tool capability classes.
- Model capability classes.
- Connector capability classes.
- Plan-gated feature matrix.
- Security policy templates.

Workspace may instantiate and configure them, but must not mutate their global definitions.

## 5. Key Object Model

### 5.1 Admin Platform Objects

| Object | Key Fields |
| --- | --- |
| CEO User | name, email, phone, auth method, status, region, risk level |
| Tenant | tenant_id, CEO owner, company name, plan, quota, status, created_at |
| Plan | name, price, task quota, token quota, enabled departments, enabled models, enabled connectors |
| Model Provider | provider name, auth mode, base URL, secret policy, status, region, compliance tags |
| Model | provider, model id, display name, capability tags, context length, cost in/out, rate limit, fallback rank |
| Tool | tool key, capability class, input schema, output schema, runtime type, approval requirement |
| Connector | platform key, platform name, auth type, scopes, webhook support, sandbox mode, compliance notes |
| Department Type | type_key, category, default manifest, required tools, suggested models, guardrails |
| Feature Flag | key, default state, plan rule, tenant override, rollout percentage |
| Platform Audit | actor, action, target, before/after, risk level, timestamp |

### 5.2 Workspace Objects

| Object | Key Fields |
| --- | --- |
| Company Profile | tenant_id, company name, industry, business scope, goals, region |
| Company Topology | enabled departments, department relationships, quality lines, approval rules |
| Department Instance | department_id, type_key, display name, owner, status, purpose, output channels |
| Employee | employee_id, department_id, role profile, skills, model preference, cost limit, status |
| Platform Account | platform key, tenant credential ref, account label, scopes, health status |
| Model Assignment | company/department scope, primary model, fallback models, budget policy |
| Task | content, department, priority, status, created_by, approval requirement |
| Workflow | task_id, steps, state, assigned employee/tool, retry/fallback policy |
| Execution Event | event_id, correlation_id, tenant_id, task_id, department_id, event_type |
| Asset | asset_id, type, hash, source task, department, storage ref |
| Approval | target type, target id, risk level, approver, decision, timestamp |

## 6. Major User Flows

### 6.1 Platform Admin Creates a CEO Tenant

1. Admin opens CEO / Tenant Management.
2. Clicks `Create CEO`.
3. Enters CEO name, email, company name, plan, region, quota package, enabled connector set, and default feature flags.
4. System creates tenant and sends invite.
5. CEO logs into Workspace and sees company setup wizard.

### 6.2 Platform Admin Adds a Model Provider

1. Admin opens Model Provider Center.
2. Clicks `Add Provider`.
3. Enters provider name, base URL, auth mode, key owner, secret rotation policy, region, compliance tags.
4. Adds model entries with model id, display name, capability tags, context length, price, rate limit, enabled plans.
5. Workspace can now select only the models available to its tenant plan.

### 6.3 Platform Admin Adds a Business Connector

1. Admin opens Connector Center.
2. Clicks `Add Platform Connector`.
3. Defines platform key, auth type, required scopes, sandbox support, webhook endpoints, media/output constraints, risk tags.
4. Security reviews the connector.
5. Connector becomes available to selected plans/tenants.
6. CEO can bind their own tenant platform account in Workspace.

### 6.4 CEO Configures a Company

1. CEO enters Workspace.
2. Completes company profile.
3. Selects departments from allowed department catalog.
4. For each department, sets purpose, output channels, quality line, platform account, model assignment, and approval policy.
5. Creates or assigns AI employees.
6. Company topology becomes active.

### 6.5 CEO Creates a Department

1. CEO opens Department Center.
2. Clicks `Add Department`.
3. Chooses department type from Admin-approved catalog.
4. Enters display name, purpose, business scope, quality line, output channel, allowed tools, model policy, approval rule.
5. If business department, selects tenant platform account.
6. Department is created under tenant company.

### 6.6 CEO Creates an AI Employee

1. CEO opens HR Department or department detail.
2. Clicks `Create Employee`.
3. Selects role profile, skills, department, model preference, cost limit, allowed tools, escalation rule.
4. System validates against plan and department policy.
5. Employee becomes available for task assignment.

### 6.7 CEO Runs Work

1. CEO opens Task Console.
2. Enters task and selects department or lets system recommend.
3. Orchestrator creates workflow.
4. Employee executes step with model/tool routing.
5. Result, trace, event stream, cost, and approval state are recorded.
6. CEO approves publish or asks for revision.

## 7. Permission Model

### 7.1 Admin Platform Roles

- Super Admin: all platform operations.
- Tenant Operator: CEO lifecycle, plan changes, support.
- Model Admin: provider/model configuration.
- Connector Admin: connector templates and platform integration definitions.
- Security Reviewer: secrets, risk, compliance, audit.
- Finance Operator: billing plans and quota policy.

### 7.2 Workspace Roles

- CEO: all tenant company decisions.
- Company Operator: daily task and department operations.
- Department Owner: department-scoped configuration and approvals.
- Reviewer: content/approval review.
- Auditor: read-only audit and reports.

## 8. Release Strategy

Recommended future build order:

1. Keep current AI Task Executor MVP stable.
2. Finish controlled execution-substance slices already being planned.
3. Solidify tenant_id and department instance foundation.
4. Build Admin Platform foundation: tenant management, model catalog, tool catalog, connector catalog, department type catalog.
5. Build Workspace company setup and department instantiation UI.
6. Add employee configuration and model assignment.
7. Add platform account binding and publish approval.
8. Add L6 analytics/ROI after event and tenant scopes are stable.

## 9. Non-Goals For This Blueprint

This document does not approve implementation. It defines the full commercial product target.

Implementation still requires gates for:

- Real multi-tenant isolation.
- Admin Platform UI.
- Department type management.
- Employee CRUD.
- External platform credential storage.
- Model provider secret handling.
- ROI / L6 economy.
- Complex dashboards.
- Cross-tenant policy.
