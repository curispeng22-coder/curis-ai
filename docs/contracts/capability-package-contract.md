# Capability Package Contract

Status: Phase-7.7 Billing Readiness Contract

Owner: Admin Platform owns future official/marketplace package governance. Workspace owns tenant-private package references only if a future Workspace gate approves them.

## Purpose

Define the commercial contract for future paid capability packages without implementing Marketplace, Billing, package purchase, package install, or package enforcement.

## Definition

`CapabilityPackage` groups capabilities, connectors, workflow templates, and employee templates into a commercial bundle.

Example future package shape:

```json
{
  "name": "内容运营包",
  "capabilities": [],
  "connectors": [],
  "workflows": [],
  "employees": [],
  "pricing": {}
}
```

## Source Scope

Supported `source`:

- `official`: supplied and governed by Admin Platform.
- `marketplace`: future third-party or shared package, blocked until Marketplace governance gate.
- `tenant_private`: tenant-owned package, visible only inside that tenant.

Rules:

- `tenant_private` packages must not pollute official catalog.
- Workspace must not modify `official` package definitions.
- Marketplace package listing, review, revenue share, and install flow are not approved in Phase-7.7.

## Fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `package_id` | string | Yes | Stable package id. |
| `name` | string | Yes | Human-readable package name. |
| `capability_ids` | string[] | Yes | Model/tool capability ids included in the package. |
| `connector_ids` | string[] | Yes | Connector ids included in the package. |
| `workflow_ids` | string[] | Yes | Workflow template ids included in the package. |
| `employee_templates` | string[] | Yes | Employee template ids included in the package. |
| `pricing_reference` | string nullable | No | Reference to future pricing/plan rule. |
| `source` | enum | Yes | `official` / `tenant_private` / `marketplace`. |

## Relationship To Billing

Future Billing MVP may treat a package as:

- a plan feature,
- a quota grant,
- a billable `BillingSubject` with `subject_type=capability_package`,
- a marketplace revenue-share subject in a later gate.

Phase-7.7 only defines the contract. It does not calculate package fees.

## Relationship To Workspace

Workspace may display or consume capability availability only through approved catalog and selector contracts. Future package enforcement must not bypass:

- tenant isolation,
- credential redaction,
- `/api/catalog/*` official-read boundary,
- `/api/platform/*` Workspace runtime prohibition.

## Not Approved

- Marketplace.
- Package checkout.
- Package install flow.
- Package revenue share.
- Package enforcement in runtime.
- Billing implementation.
- Workspace execution-chain changes.
