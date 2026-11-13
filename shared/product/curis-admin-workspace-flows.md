# Curis Admin Platform + Workspace Flow Diagrams

Status: Future blueprint.
Date: 2026-07-08

This file captures the product flows for the commercial two-product design: Admin Platform and Workspace.

## 1. Two-Product Operating Model

```mermaid
flowchart LR
    PlatformAdmin[平台管理员] --> Admin[Curis Admin Platform]
    Admin --> Tenant[CEO / Tenant]
    Admin --> Catalog[模型 / 工具 / 连接器 / 部门类型目录]
    Admin --> Policy[计划 / 配额 / 安全策略]
    Tenant --> Workspace[Curis Workspace]
    Catalog --> Workspace
    Policy --> Workspace
    Workspace --> Company[CEO 的 AI 公司]
    Company --> Departments[部门]
    Departments --> Employees[AI 员工]
    Employees --> Tasks[任务 / 工作流 / 结果]
```

## 2. Admin Platform Creates CEO Tenant

```mermaid
sequenceDiagram
    actor Admin as 平台管理员
    participant AP as Admin Platform
    participant Tenant as Tenant Service
    participant Catalog as Feature/Plan Catalog
    participant Mail as Invite Service
    participant WS as Workspace

    Admin->>AP: Create CEO
    AP->>AP: Validate email / plan / region
    AP->>Catalog: Resolve enabled features/models/connectors
    AP->>Tenant: Create tenant + CEO owner
    Tenant-->>AP: tenant_id
    AP->>Mail: Send invitation
    Mail-->>Admin: Invite sent
    Admin->>AP: Open tenant detail
    WS-->>Tenant: CEO first login reads tenant limits
```

Create CEO fields:

- CEO name
- Email
- Phone
- Company name
- Region
- Plan
- Token quota
- Task quota
- Enabled department types
- Enabled connector set
- Enabled model group
- Billing owner
- Invite mode
- Risk level
- Notes

## 3. Admin Adds Model Provider and Models

```mermaid
flowchart TD
    A[Open Model Center] --> B[Add Provider]
    B --> C[Enter provider metadata]
    C --> D[Set secret policy and region]
    D --> E[Add model entries]
    E --> F[Set capability tags and price]
    F --> G[Assign allowed plans]
    G --> H[Security review if needed]
    H --> I[Publish to model catalog]
    I --> J[Workspace model selector can consume allowed models]
```

Provider fields:

- Provider name
- Provider key
- Base URL
- Auth mode
- Secret reference
- Data region
- Compliance tag
- Key rotation interval
- Status
- Default rate limit

Model fields:

- Provider
- Model id
- Display name
- Capability tags
- Context length
- Input token price
- Output token price
- Rate limit
- Tool-use support
- Vision/audio/video support
- Allowed plans
- Fallback rank

## 4. Admin Adds Tool

```mermaid
flowchart TD
    A[Open Tool Center] --> B[Create Tool]
    B --> C[Define tool key and capability class]
    C --> D[Define input/output schema]
    D --> E[Set runtime type and timeout]
    E --> F[Set approval/retry policy]
    F --> G[Assign allowed plans]
    G --> H[Publish to tool registry]
    H --> I[Workspace can use via allowed department/model policies]
```

Tool fields:

- Tool key
- Display name
- Capability class
- Runtime type
- Input schema
- Output schema
- Approval requirement
- Retry policy
- Timeout
- Allowed plans
- Security notes

## 5. Admin Adds External Business Platform Connector

```mermaid
flowchart TD
    A[Open Connector Center] --> B[Add Connector]
    B --> C[Define platform key/name]
    C --> D[Set auth type and required scopes]
    D --> E[Set sandbox/webhook/output support]
    E --> F[Define credential policy]
    F --> G[Security Boundary Review]
    G -->|Approved| H[Publish connector template]
    G -->|Rejected| R[Return risk notes]
    H --> I[CEO can bind tenant-owned account in Workspace]
```

Connector fields:

- Platform key
- Platform name
- Auth type
- Required scopes
- Sandbox support
- Webhook callback
- Supported output types
- Publishing approval requirement
- Credential policy
- Compliance notes
- Allowed plans

## 6. Admin Maintains Department Type Catalog

```mermaid
flowchart TD
    A[Open Department Type Catalog] --> B[Create or edit type]
    B --> C[Select category: business/function]
    C --> D[Define capability set and tool classes]
    D --> E[Define output channels and quality lines]
    E --> F[Attach default model group and guardrails]
    F --> G[Set employee role spec]
    G --> H[Assign allowed plans]
    H --> I[Gate/Security review if type changes platform behavior]
    I --> J[Publish department type]
    J --> K[Workspace department wizard can instantiate type]
```

Department type fields:

- Type key
- Category
- Display name
- Description
- Capability set
- Tool classes
- Output channels
- Quality lines
- Default model group
- ROI schema placeholder
- Guardrail references
- Employee role spec
- Allowed plans

## 7. CEO First-Time Company Setup

```mermaid
sequenceDiagram
    actor CEO as CEO
    participant WS as Workspace
    participant Admin as Admin Catalogs
    participant Company as Company Topology
    participant Dept as Department Center

    CEO->>WS: First login
    WS->>Admin: Load plan limits + allowed catalogs
    WS-->>CEO: Show company setup wizard
    CEO->>WS: Fill company profile
    CEO->>Dept: Select department types
    Dept->>Admin: Validate allowed department types
    Dept->>Company: Create department instances
    CEO->>WS: Assign models and platform accounts
    WS->>Company: Activate topology
    WS-->>CEO: CEO Cockpit
```

Company setup steps:

1. Company profile.
2. Business scope.
3. Department selection.
4. Model assignment.
5. Platform account binding.
6. Employee setup.
7. Approval policy.
8. Activation checklist.

## 8. CEO Creates Department

```mermaid
flowchart TD
    A[Department Center] --> B[Add Department]
    B --> C[Choose department type from allowed catalog]
    C --> D[Fill display name and purpose]
    D --> E[Select quality line and output channels]
    E --> F[Assign model policy]
    F --> G{Business department?}
    G -->|Yes| H[Select platform account]
    G -->|No| I[Set internal function policy]
    H --> J[Set approval policy]
    I --> J
    J --> K[Create department instance]
    K --> L[Department detail page]
```

Department instance fields:

- Department type
- Display name
- Purpose
- Business scope
- Owner
- Quality line
- Output channels
- Allowed tools
- Primary model
- Fallback model
- Platform account
- Approval policy
- Cost limit
- Status

## 9. CEO Creates AI Employee

```mermaid
flowchart TD
    A[HR Department / Employee Center] --> B[Create Employee]
    B --> C[Select department]
    C --> D[Select role profile]
    D --> E[Assign skill tags]
    E --> F[Choose primary/fallback model]
    F --> G[Set allowed tools and cost limit]
    G --> H[Set escalation triggers]
    H --> I[Create employee]
    I --> J[Employee appears in skill matrix]
```

Employee fields:

- Employee name
- Department
- Role profile
- Skill tags
- Primary model
- Fallback model
- Allowed tools
- Cost limit
- Work schedule
- Escalation triggers
- Output style
- Status

## 10. CEO Connects a Platform Account

```mermaid
flowchart TD
    A[Platform Accounts] --> B[Connect Account]
    B --> C[Choose platform connector]
    C --> D[Show required scopes]
    D --> E[OAuth/API key credential step]
    E --> F[Security validation]
    F -->|OK| G[Store tenant credential reference]
    F -->|Fail| R[Show risk/failure state]
    G --> H[Account available to departments]
```

Workspace stores tenant-specific credential references. Admin Platform owns connector definitions and credential policy.

## 11. CEO Runs a Task

```mermaid
sequenceDiagram
    actor CEO
    participant WS as Workspace Task Console
    participant Orch as Orchestrator
    participant Emp as AI Employee
    participant Router as Tool Router
    participant Model as Model Router
    participant Store as Result Store
    participant Approval as Approval Queue

    CEO->>WS: Submit task
    WS->>Orch: Create task/run
    Orch->>Orch: Generate workflow
    Orch->>Emp: Step package
    Emp->>Model: Prompt/context
    Emp->>Router: Tool need
    Router->>Emp: Tool result/fallback
    Emp->>Store: Step result + trace
    Store-->>WS: Task detail update
    WS-->>CEO: Review result
    CEO->>Approval: Approve publish or request revision
```

## 12. Admin vs Workspace Decision Matrix

| Decision | Admin Platform | Workspace |
| --- | --- | --- |
| Which models exist on platform | Owns | Reads allowed subset |
| Which model a department uses | Defines allowed list | CEO chooses |
| Which external connectors exist | Owns | CEO binds tenant account |
| Which departments types exist | Owns | CEO instantiates department |
| Which departments are active in a company | Can limit by plan | CEO chooses |
| Employee creation | Sets plan/limits | CEO creates employees |
| Task execution | Observes aggregate only | Owns execution |
| Tenant-specific business content | No access by default | Owns |
| Cross-tenant risk policy | Owns | Must comply |
| Company ROI decisions | Defines metrics availability | CEO uses results |

## 13. End-State Flow

```mermaid
flowchart TD
    AdminSetup[Admin configures models/tools/connectors/departments/plans]
    AdminSetup --> TenantInvite[Admin creates CEO tenant]
    TenantInvite --> CEOSetup[CEO configures company]
    CEOSetup --> DeptSetup[CEO enables departments]
    DeptSetup --> EmployeeSetup[CEO configures AI employees]
    EmployeeSetup --> TaskRun[Company executes tasks]
    TaskRun --> Events[Events + traces + memory]
    Events --> Analytics[Department/admin/BI analysis]
    Analytics --> Optimize[CEO optimizes company]
    Optimize --> TaskRun
```
