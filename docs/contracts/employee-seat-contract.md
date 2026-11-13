# Employee Seat Contract

Status: Phase-7.7 Billing Readiness Contract

Owner: Admin Platform owns future seat billing. Workspace owns EmployeeInstance runtime records and usage evidence.

## Purpose

Define the commercial contract for future AI employee seat billing without changing the AI Employee System, Workflow Runtime, Employee Runtime, or Billing implementation.

## Definition

`EmployeeSeat` is a commercial view of a Workspace AI employee that may be counted against a plan or billed in the future.

It is not the same object as `EmployeeInstance`:

- `EmployeeInstance` is Workspace runtime/product state.
- `EmployeeSeat` is future commercial/billing state derived from or linked to an employee.

## Seat Types

Future seat categories:

- `standard`: ordinary AI employee.
- `professional`: specialized AI employee with higher-value capability scope.
- `advanced`: premium AI employee with future advanced capabilities.

Phase-7.7 does not enforce seat limits or bill for seats.

## Fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `employee_id` | string | Yes | Workspace EmployeeInstance id being counted. |
| `tenant_id` | string | Yes | Tenant owning the employee. |
| `employee_type` | enum | Yes | `standard` / `professional` / `advanced`. |
| `seat_type` | enum | Yes | `included` / `additional` / `trial` / `reserved`. |
| `plan_binding` | string nullable | No | Future Plan or Subscription reference. |
| `status` | enum | Yes | `active` / `disabled` / `suspended` / `deleted`. |

## Relationship To Usage

Future Billing MVP may use:

- `usage_event.employee_id`,
- `usage_event.employee_role`,
- EmployeeInstance status,
- plan quota rules,
- employee seat limit.

Rules:

- Employee seat counting must not mutate `usage_event`.
- Workspace Employee Runtime must not be changed by seat billing without a separate gate.
- Seat billing must not reveal tenant_private credential material.

## Admin / Workspace Boundary

- Workspace creates and manages EmployeeInstance under approved Workspace gates.
- Admin may later count or display seat usage through billing/reporting contracts.
- Admin must not control employee execution from this contract.
- Admin must not read tenant_private plaintext secrets.

## Not Approved

- AI employee seat billing.
- Employee runtime change.
- Employee quota enforcement.
- New employee types in Workspace.
- Complex HR system.
- Payment or invoice generation.
