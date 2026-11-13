# SHARED-EMPLOYEE-EXECUTION-TRUST-001 Review

**Status:** IMPLEMENTED / ACCEPTED
**Record Type:** Formal Acceptance Record
**Date:** 2026-08-17
**Issue:** `issues/SHARED-EMPLOYEE-EXECUTION-TRUST-001.md`

## Decision

Shared Employee / Provider execution trust closure is accepted in bounded scope. Runtime
`AI_EMPLOYEE` remains the canonical business identity. Company Employee, Provider capability and
session are execution provenance only and cannot overwrite Responsibility Holder or Current
Executor.

## Canonical identity and callback evidence

- Runtime Employee: `runtime-employee-reviewer`
- Company execution Employee: `company-employee-reviewer`
- explicit bridge: `VERIFIED_EXPLICIT_BRIDGE`
- append-only assignment event: `execution.identity_bound`
- Provider evidence: `usage.task_execution`, session `session-codex-1`
- callback actor: `runtime-employee-reviewer`, `verification_status=VERIFIED`
- forged session, changed Task employee, missing assignment and conflicting bridge fail closed.
- absence of Provider evidence may persist as `UNVERIFIED`; it is not converted to success.

The same callback provenance is readable from Runtime Evidence and Outcome Result References.
Provider-native Handoff ACK verification confirms the current `SENT` target and the same Task /
session provenance while leaving the Handoff at `SENT`; the Domain remains the only owner of the
actual transition.

## Persistence and database evidence

Evidence root:

`/tmp/curis-employee-execution-trust.szTaGG`

Primary SQLite:

`/tmp/curis-employee-execution-trust.szTaGG/pytest/test_explicit_bridge_callback_0/identity.sqlite`

```text
size: 1134592
SHA-256: 47b7e7197a2a101867c3517f3185b031798650eec114a4aa1c8322cbd1d0825b
integrity_check: ok
foreign_key_check: 0 rows
```

After a new `Database` instance initialized and reopened the same SQLite, the explicit bridge,
Task assignment event, UsageEvent/session callback provenance, Evidence/Outcome owner and Handoff
target remained readable. No persisted row was interpreted as an active Provider process.

## Verification

Repository-external SQLite with all three variables resolving to one path:

```text
CURIS_DB
CURIS_DB_PATH
CURIS_WORKSPACE_DB
```

Focused + no-regression: `26 passed`.

Coverage includes canonical identity tests, Shared projection, RD real execution, Artifact Review,
Responsibility Handoff, XHS Calendar/Note Runtime, Workspace Package Company integration, Codex
Adapter, Computer Access P0 and Backend test DB safety. Python compile and `git diff --check` pass.

## Active database truth

Before and after:

```text
size: 1232896
mtime: 1786873339
SHA-256: 2ea2506f90f764e834d47d8f6bae3cb41c22d457757e0e9216c0ae8c39a39ec6
integrity_check: ok
foreign_key_check: 0 rows
```

The active database was not opened for initialization, migrated, cleaned or modified.

## Workspace to Department conclusion

Current authority and schema expose Project→Department and Employee affiliation facts, but no
direct authoritative Workspace↔Department relation. The Shared read model continues to project
only those existing facts. A direct relation needs a separate Authority/Schema decision covering
cardinality, lifecycle and migration; this Issue intentionally does not infer it from name,
business type, Project or Employee.

## RD / Workspace Engineering unblock

Stable interface: `EmployeeExecutionIdentity.bind()`, `record_task_assignment()`,
`verify_task_callback()` and `verify_handoff_ack()`. RD can create a real target Provider Task,
record its assignment, then use the verifier evidence before its existing Domain Handoff ACK
transition. Workspace Engineering can resolve Package/Core Result provenance without defining a
Package Employee identity.

## Remaining gaps

- Existing CEO/manual Handoff response is not reclassified as Provider-native ACK; Domain adoption
  of the Shared verifier is a separate bounded change.
- Direct Workspace↔Department authority/schema remains undecided.
- Provider permission/mode/model truth and Computer Access P1/P2 remain unchanged.
