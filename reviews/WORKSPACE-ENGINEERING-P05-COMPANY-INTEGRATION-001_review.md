# WORKSPACE-ENGINEERING-P05-COMPANY-INTEGRATION-001 Review

Status: Formal Acceptance Record / IMPLEMENTED / ACCEPTED

Date: 2026-08-16

Issue: `issues/WORKSPACE-ENGINEERING-P05-COMPANY-INTEGRATION-001.md`

Evidence: `docs/reviews/workspace-engineering-p05-2026-08-16/README.md`

## Decision

`com.curis.sample.customer-feedback-office@0.1.0` is proven as a dynamically installed Workspace
that participates in one real Curis Company OS operating loop.

```text
Highest accepted layer: Operating
Earlier layers: Installed / Operational accepted by P0
Company Integrated: PASS
Operating: PASS
Evolvable: NOT ACCEPTED / NOT IMPLEMENTED
Handoff: NOT REQUIRED — no responsibility transfer occurs
Decision P7: NOT REQUIRED — no CEO judgment or governed external action occurs
```

## Identity / reference contract

PASS.

- A new Package object and `runtime_entities(PACKAGE_DOMAIN_OBJECT)` use the same ID.
- `owner_ref`, `responsibilityRef` and `evidenceRef` reject Package-authored non-empty values.
- `runtime_links` remains unchanged and only receives links after both real Core endpoints resolve
  with matching tenant/company/workspace/type/lifecycle truth.
- The operating command receives a responsibility type, not an Employee/Evidence ID.
- Wrong-scope staffing and forged Package strings fail closed before Task/state creation.

## Real Company OS chain

PASS on packaged Desktop and isolated SQLite.

| Fact | Accepted real ID |
| --- | --- |
| CustomerFeedback / Core identity | `package-object-20086bd0-cc1b-4a95-bc81-5ec6eefa1453` |
| Responsibility / Role Slot | `role-slot-p05-feedback-triage` |
| Employee | `ai-employee-p05-feedback-triage` |
| Capability Binding | `capability-binding-p05-feedback-triage` |
| Existing Capability | `core.customer-feedback-triage` |
| Task | `4d76d4c7-dbf3-434c-87bc-e5f11282a491` |
| Execution | `1` |
| Artifact | `artifact-3890f080-128a-403b-86b1-d5de59192d09` |
| Evidence | `evidence-d8999ac6-0060-4bed-99a3-69629ac3e781` |
| Result / Outcome | `outcome-938bd8a4-a01e-4f5c-a1cb-28687dd3fada` |

The success object is `TRIAGED`; `resolvable=true` and `reverseResolved=true`. The Package grants no
Capability or Computer Access: it uses an already provisioned Company capability and an active
Company OS binding.

## Failure truth

PASS.

- Fake relationship payload: HTTP `422`.
- Real failure object: `package-object-b4331078-9211-4789-9f68-69ed7b82442d`.
- Real failed Task: `e81ac8b5-328a-4dc0-8fbf-b4017d8d1610`.
- Real Execution: `2`, error `customer_feedback_summary_insufficient`.
- Object remains `NEW`; Evidence, Result and Artifact references are empty.
- Cross-company Employee injection fails before Task/state residue in focused tests.

## Restart / Desktop proof

PASS.

- Packaged app existed before the external Package files; the app bundle contains zero matches for
  the package ID, object type or Chinese label.
- The Package was installed after build without source change, rebuild or reinstall.
- The full Desktop process was stopped; port `8002` became unavailable; the exact same app binary
  and isolated DB were then started again.
- After restart, the same success and failure IDs, states, Task/Execution, Evidence/Outcome,
  Artifact and reverse links resolved from SQLite.
- Desktop UI after restart displayed the dynamic Workspace, `TRIAGED` object and all Core refs.

## Verification

- Backend bounded suite: `24 passed`.
- Frontend bounded suite: `11 passed`.
- Focused frontend ESLint: PASS.
- Python compile check: PASS.
- Desktop release build: PASS.
- Isolated acceptance DB: `integrity_check=ok`, `foreign_key_check` empty.
- Repository active DB remained byte-identical to the Issue baseline: size `1232896`, mtime
  `1786873339`, SHA-256
  `2ea2506f90f764e834d47d8f6bae3cb41c22d457757e0e9216c0ae8c39a39ec6`,
  `integrity_check=ok`.

## No regression / boundary

PASS for the bounded Package, Runtime Foundation, RD accepted execution slice, XHS calendar-note
slice and generic Workspace frontend checks. No XHS/RD/TTK migration, Shared Runtime refactor,
Frozen Company OS Authority change, second Company OS primitive, arbitrary extension, Package
update/migration, Marketplace or Evolution implementation was introduced.

## Acceptance

**WORKSPACE ENGINEERING P0.5 ACCEPTED**
