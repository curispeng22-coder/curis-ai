# AGENT-COMPUTER-ACCESS-RUNTIME-P0-001：Codex 电脑访问事实链

**Status:** IMPLEMENTED / ACCEPTED
**Date:** 2026-08-15
**Owner:** Curis 主开发
**Authority:** ADR-0046；`AGENT_COMPUTER_ACCESS_RUNTIME_DELTA_PLAN.md` P0

## Goal

Repair only the Codex Adapter's access-truth path:

```text
requested_intent
→ native mapping
→ configured state
→ effective evidence
→ session/result audit snapshot
```

Requested intent must never be projected as granted or effective access. Full Computer
Access remains unsupported and is never enabled.

## Authority files

1. `docs/00_Context/CURRENT_STATE.md`
2. `docs/07_Decisions/ADR-0046-local-agent-computer-access-authority.md`
3. `docs/04_Development/AGENT_COMPUTER_ACCESS_RUNTIME_DELTA_PLAN.md`
4. `docs/01_Product/Agent_Adapter_Contract.md`
5. `docs/01_Product/Agent_Adapter_Compatibility_Registry.md`
6. `docs/01_Product/AI_Capability_UI_Contract.md`

## Current gap

`CodexCliAdapter` currently returns constructor `sandbox` as `permissions`, while the
Codex `exec resume` invocation neither re-declares nor verifies access. That response
is only requested/configured input, not effective evidence.

## Runtime truth model

- `requested_intent`: `ASK_WHEN_NEEDED`, `AUTO_WITHIN_BOUNDARY`, or
  `REQUEST_WIDEST_NATIVE_ACCESS`.
- `native_mapping`: the current Codex CLI argument mapping and whether it can be
  applied for this invocation.
- `configured_state`: `CONFIGURED` only proves the CLI accepted an applicable
  new-session mapping; `NOT_CONFIGURABLE` records a provider operation that cannot
  redeclare the mapping.
- `effective_state`: `UNKNOWN` without provider-native effective status or a permitted,
  non-destructive verification probe.
- `verification_state`: `UNVERIFIED` until such effective evidence exists; it is not
  inferred from persistence or command success.
- `evidence`: source, observation time and provider limitation; no credential, private
  prompt or hidden reasoning.
- `verified_at`: null unless effective access is actually verified.

Resume creates a new snapshot. It may retain requested history, but cannot inherit prior
effective/granted state. If the current Codex resume interface cannot declare access,
the snapshot records `NOT_CONFIGURABLE / UNVERIFIED / UNKNOWN` and the provider
limitation.

## Allowed files

```text
backend/app/agent_adapter.py
backend/app/main.py
backend/app/tool_executor.py
backend/app/orchestrator.py
backend/app/result_store.py
backend/tests/test_agent_adapter.py
backend/tests/test_agent_computer_access_runtime_p0.py
issues/AGENT-COMPUTER-ACCESS-RUNTIME-P0-001.md
reviews/AGENT-COMPUTER-ACCESS-RUNTIME-P0-001_review.md
```

## Explicit exclusions

- Computer Access UI, Registry P1, P2 adapters, Claude Code, WorkBuddy, TRAE and any
  generic Permission Engine.
- Product Blueprint, Frozen ADR/design contracts, XHS, RD, TTK, Workspace shell,
  capability catalog expansion and activity database.
- Real Full Computer Access, dangerous bypass flags, OS/TCC/Keychain/MDM changes,
  Agent config changes, UI automation and network installation.
- Schema migration or a parallel access/session persistence system. Existing Result /
  Artifact / Usage audit paths are the only permitted persistence route.

## P0 phases

| Phase | Scope | Completion condition |
| --- | --- | --- |
| P0.1 | Map Codex requested intent to supported new-session arguments; return separate configured/effective snapshot. | New session cannot report requested sandbox as effective. |
| P0.2 | Resume creates a fresh snapshot and records non-configurable/unverified state where Codex cannot re-declare access. | Old effective state is never copied into resume output. |
| P0.3 | Carry the snapshot through the existing tool/orchestrator/result audit path. | Restarted audit read preserves requested history and fresh UNKNOWN effective state. |
| P0.4 | Focused tests and isolated SQLite persistence verification. | New, resume, unsupported, restart and existing Codex execution checks pass. |

## Acceptance scenarios

1. New `ASK_WHEN_NEEDED` / `AUTO_WITHIN_BOUNDARY` sessions show their mapping, command-acceptance configuration evidence and `effective_state=UNKNOWN` unless native effective evidence exists.
2. Resume does not pass a stale sandbox argument or previous effective state; it records a new `NOT_CONFIGURABLE / UNVERIFIED / UNKNOWN` snapshot and provider limitation.
3. `REQUEST_WIDEST_NATIVE_ACCESS` creates no Codex command and reports `UNSUPPORTED` / not configurable; it never reports active/granted/effective.
4. Existing result/audit persistence retains requested and snapshot facts across a fresh Runtime restart, while a stored prior effective value cannot make a later resume effective.
5. Existing Codex new-session/resume output, Agent discovery/binding and Result/Artifact paths retain their current behavior.

## Review requirements

The Review must include changed files, isolated SQLite path, exact new/resume/unsupported
snapshots, restart readback, focused test output, no-regression result and remaining P1/P2.
No API 200, successful command, or stored old record alone proves effective access.

**AGENT COMPUTER ACCESS RUNTIME P0 IMPLEMENTATION CLOSED**

**AGENT COMPUTER ACCESS RUNTIME P0 FINAL ACCEPTANCE REVIEW REQUIRED**

**READY FOR RD IMPLEMENTATION PLANNING**
