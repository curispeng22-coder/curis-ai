# Review 061: Workspace Capability Integration Phase-1

Date: 2026-07-08

Issue: `issues/064_workspace_capability_integration_phase_1.md`

## Quality Result

PASS.

## Scope Verified

- Workspace read-only official department catalog added at `GET /api/catalog/department-types`.
- Workspace execution writes `usage.model_call` events with tenant and CEO attribution.
- Usage events are exposed through admin-only `GET /api/platform/usage`.
- Missing `X-Ceo-Id` fails closed on execution paths that would write UsageEvent.
- Billing calculation, connector credentials, marketplace implementation, private credential persistence, and CEO auth implementation were not added.

## Commands

```bash
cd backend
../backend/.venv/bin/python -m unittest tests.test_adr0028_workspace_integration
../backend/.venv/bin/python -m unittest discover tests
```

## Evidence

- Targeted ADR-0028 Workspace tests: 4 tests passed.
- Backend regression: 159 tests passed.
- `git diff --check` passed for changed files.
- Forbidden-scope scan found no implementation of billing calculation, connector credentials, marketplace, private credential persistence, vector/embedding, uncontrolled code modification, or locked action lifting in changed production files.

## Known Gaps

- `X-Ceo-Id` remains a Phase-1 placeholder; formal CEO login and token issuance still require a separate ADR.
- Only department types are exposed in the Workspace catalog first slice; model/tool/connector catalogs remain future slices.
- Tenant-private model/tool/connector persistence remains future gated work.

## Handoff

Next Seat: 产品规划席

Handoff: final closeout
