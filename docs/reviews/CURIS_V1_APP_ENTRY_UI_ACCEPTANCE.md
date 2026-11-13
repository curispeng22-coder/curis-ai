# CURIS V1 — APP ENTRY UI ACCEPTANCE

**Status:** Frozen
**Authority Class:** FROZEN / UI ACCEPTANCE RECORD
**Disposition:** APP ENTRY PRODUCT / INTERACTION ACCEPTED; APP ENTRY UI ACCEPTED; FIGMA CURRENT DESIGN BASELINE
**Implementation:** PENDING ENGINEERING RECONCILIATION (not implemented)
**Date:** 2026-08-28

## Accepted design source

- Figma: [Curis V1 — App Entry & CEO Assistant Experience](https://www.figma.com/design/2Fh7DgPPfLgdbvNtnzPnk9/Curis-V1-App-Entry-CEO-Assistant-Experience)
- File key: `2Fh7DgPPfLgdbvNtnzPnk9`
- Core Frames: `1:2`, `1:83`, `1:188`, `1:424`, `1:624`, `1:821`, `1:1052`, `1:1292`, `1:1515`, `1:1727`, `1:1990`, `1:2211`, `1:2428`

This Figma file is the current App Entry UI design baseline, not an exploration or visual fixture. UI acceptance does not claim Frontend, Runtime, Schema, credential storage, or provider implementation.

## Accepted product / interaction chain

```text
Welcome
→ Create Company or Skip → Empty Curis
→ CEO Display Identity + Company Name
→ Company Created
→ CEO Assistant first presence
→ No Model → Model Configuration
→ Model Enabled → Assistant Conversation Ready
→ Company Ready / No Business
→ CEO Intent → conversational Create Business flow
→ Structured Surface → Business / Workspace
```

Skip enters the real Empty Curis Shell and never creates fake Company, Business, Workspace, Employee, Result, Evidence, Meeting, or operating data.

## Accepted shared patterns

- Seven primary navigation areas with linear icons and Sparse Iris selected cue.
- CEO Display Name + optional Avatar; shared Avatar Pattern is Upload + Curis Cartoon Preset + Fallback.
- CEO Assistant, Team Leader and AI Employee share Identity + Conversation + Composer patterns.
- Composer semantic slots: Input, `+`, access, work mode, selected resources, Model·Agent, Voice, Send.
- Model management and model use are separate: management handles Provider / Credential / Model / Enable / Disable / Default / Advanced; Conversation Model Selector chooses the current enabled model.
- Structured surfaces carry confirmation, Decision, Result, Evidence and durable references; Conversation carries ongoing collaboration.
- Empty Curis and Empty Company remain truthful, distinct states.

## Supersession and implementation boundary

Older onboarding, First Run, Prototype, fixture and original Trae candidates are `SUPERSEDED FOR CURRENT UI` where they conflict with this baseline; files remain for historical provenance. Polish and implementation gaps (dynamic provider data, avatar upload/crop, secure credential persistence, accessibility, keyboard interaction, componentization, history and dynamic model states) do not reopen UI design.

The next UI work is CEO Desk **LIMITED COMPOSITION DELTA**, using the accepted CEO Desk Page Contract and existing Figma references; do not start a new App Entry exploration.

## Required status vocabulary

Use `OPEN`, `DESIGN CANDIDATE`, `UI ACCEPTED`, `IMPLEMENTATION READY`, `IMPLEMENTED`, and `SUPERSEDED` consistently. `UI ACCEPTED` means product and visual design are accepted for implementation; it does not mean implemented.

**APP ENTRY UI ACCEPTANCE REGISTERED**
