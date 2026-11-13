# CURIS V1 UI DEPENDENCY MATRIX

Status: Review

Authority Class: REVIEW

Date: 2026-08-27

Scope: V1 UI-independent delivery classification. This document does not decide final layout or visual design.

| Backlog | Classification | Do now | UI-independent deliverable | Hold boundary |
|---|---|---|---|---|
| V1-P0-001 | A — UI-INDEPENDENT | YES | FoundingRun → canonical Business + first Generic Workspace atomic persistence, IDs, resolver, retry/restart | Final First Run composition |
| V1-P0-002 | C — UI-DEPENDENT | HOLD | Keep intent/proposal command contract only | Assistant conversation layout, proposal presentation |
| V1-P0-003 | A — UI-INDEPENDENT | SECURITY BLOCKED | OS secure secret backend, restart Health, redaction | No registered Keychain backend; final provider setup visuals |
| V1-P0-004 | B — UI-CONTRACT | YES | CEO Desk first-business read model and next-action projection | Card/layout/navigation placement |
| V1-P0-005 | B — UI-CONTRACT | YES | canonical links, return target, context mismatch errors | Navigation visual placement |
| V1-P0-006 | A — UI-INDEPENDENT | YES | repeatable fresh packaged harness | Final UI acceptance remains separate |
| V1-P1-001 | B — UI-CONTRACT | YES | General Workspace overview projection | Final office home composition |
| V1-P1-002 | A — UI-INDEPENDENT | YES | canonical Team/Responsibility materialization | Employee card visuals |
| V1-P1-003 | A — UI-INDEPENDENT | PARTIAL | ordinary-language command now creates canonical Cycle/Work from existing Team truth | Team materialization and final Input component/layout |
| V1-P1-004 | B — UI-CONTRACT | YES | conversation/current-work read models | Conversation visual design |
| V1-P1-005 | A — UI-INDEPENDENT | CLOSED | Canonical/legacy attribution uses one ledger; live no-Project execution is proven | Live presentation remains UI-dependent |
| V1-P1-006 | B — UI-CONTRACT | YES | Result/Evidence read model | Utility visual hierarchy |
| V1-P1-007 | A — UI-INDEPENDENT | YES | wait/failure/retry/cancel truth | Recovery card visuals |
| V1-P1-008 | A/B | YES | persisted Handoff/P7 commands and projections | Banner/detail composition |
| V1-P1-009 | A/B | YES | history/continuation/next-cycle contract | Timeline visual design |
| V1-P1-010 | A — UI-INDEPENDENT | YES | API/current-surface packaged proof | Final UI acceptance separate |
| V1-P2-001..005 | A/B | CLOSED HEADLESS | canonical RD Work/Responsibility/Codex/usage/Result integration | UI/Packaged acceptance remains |
| V1-P2-006 | B | HOLD | headless Runtime evidence is complete | Fresh packaged RD journey |
| V1-P3-001 | C — UI-DEPENDENT | HOLD | Domain object/projection contracts may proceed separately | Content Growth final Surfaces/navigation/layout |
| V1-P3-002..004 | A/B | CLOSED HEADLESS | canonical Research/Content/Evaluation multi-Work, evidence, handoff and honest capability gaps | Final domain visual expression and real channel facts |
| V1-P3-005 | EXTERNAL | CONDITIONAL | Real connector evidence only with legitimate credentials/API | No simulated success |
| V1-P3-006 | EXTERNAL | PARTIAL | Local package reproducibility | Apple signing/notarization credentials |
| V1-P3-007..008 | A — UI-INDEPENDENT | YES | backup/restore/update core and failure truth | Settings placement |
| V1-P3-009 | A + final UI gate | PARTIAL | headless/temporary-surface whole-app harness | Final accepted UI E2E |

## UI-dependent hold list

- First Run final screen sequence and composition.
- CEO Desk final content hierarchy.
- General Workspace final Main/Context/Utility composition.
- Employee avatar/card treatment and conversation layout.
- Content Growth Topic Pool, Research, Editor, Publishing and Evaluation final Surfaces.
- Final navigation placement and responsive visual behavior.

## Current implementation decision

The Generic Workspace authority is current, while the existing `WorkspaceRuntime` accepts only RD/XHS/TTK. M1 therefore adds only a headless `GENERIC` Workspace persistence contract to the existing canonical Business Spine. It does not add a domain lifecycle, package renderer, Task system, or final UI.

M2 exposes a General Workspace read contract and an ordinary-language command over
existing Cycle/Work/Responsibility primitives. It deliberately returns `NEEDS_DECISION`
when there is no single published responsibility definition or no eligible Employee.
Canonical no-Project provider attribution is now closed; M4/M5 consume that same shared
lineage without synthetic Project or a second usage system.
