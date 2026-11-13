# CURIS VISUAL TOKEN MIGRATION MAP

Status: Review

Authority Class: REVIEW / IMPLEMENTATION MIGRATION MAP

Disposition: IMPLEMENTATION MIGRATION REQUIRED — NO CODE CHANGE AUTHORIZED

Baseline: main @ c797db840bad285d7e9f1962d06eac61aa28508b

Updated: 2026-08-27

Module: Design / Frontend

Owner: Frontend / Design QA

Supersedes: none

Input: `docs/03_Design/CURIS_VISUAL_STANDARD_V1.md`.

This document maps current implementation to Direction D. It does not change Frontend, tokens, components, Figma, Product, Runtime, Schema, or DB.

## 1. Migration decision

```text
CURRENT VISUAL STANDARD ACCENT: #806BE5
LEGACY IMPLEMENTATION ACCENT:  #32f08c
CODE MIGRATION:                REQUIRED, NOT EXECUTED
PRODUCT COMPOSITION:           NOT FROZEN
DARK COMPANY SPACE:            VALIDATION REQUIRED
STATE COLOR TOKENS:            VALIDATION REQUIRED
```

Classification meanings:

| Class | Meaning |
| --- | --- |
| KEEP | Structure or semantic indirection already supports migration. |
| REMAP | Keep the consumer/API, change the semantic assignment. |
| REPLACE TOKEN | Current literal/token value conflicts with Direction D. |
| VISUAL QA | Do not change blindly; validate contrast, semantics, density, and state in real screens. |
| LEGACY | Historical/secondary implementation; not visual authority. Migrate only if it remains active. |

## 2. Target mapping — specification only

This table defines the intended mapping. It is not a CSS patch.

| Semantic role | Current implementation | Direction D target | Action |
| --- | --- | --- | --- |
| Brand accent | Dark `#32f08c`; Light `#1a1c1f` | `#806BE5` in Light; Dark may use `#806BE5` pending validation | REPLACE TOKEN + VISUAL QA |
| Dark companion | none | `#9A89F0` remains candidate only | DO NOT ADD until validation |
| Light canvas | `#f5f5f7` | `#F7F8FA` | REPLACE TOKEN |
| Light base | `#ffffff` | `#FFFFFF` | KEEP |
| Light Surface 1 | `#f7f8fa` | `#F1F3F5` | REPLACE TOKEN |
| Light Surface 2 | no direct equivalent | `#E9EDF1` | REMAP after component audit |
| Light border | `#e5e7eb` | `#DDE2E7` | REPLACE TOKEN + contrast QA |
| Light primary text | `#1a1c1f` | `#1D232A` | REPLACE TOKEN |
| Light secondary text | `#4b5563` | `#4D5661` | REPLACE TOKEN |
| Light muted text | `#626b76` | `#7C8794` | REPLACE TOKEN + readability QA |
| Dark canvas | `#1a1c1f` | `#181A1D` | REPLACE TOKEN |
| Dark base/surface | `#222529` | `#1F2125` | REMAP + VISUAL QA |
| Dark Surface 1 | `#2b2f34` | `#25292E` | REPLACE TOKEN |
| Dark Surface 2 | no direct equivalent | `#2D3238` | REMAP after component audit |
| Dark elevated | shadow-led / no dedicated color | `#343A41` | REMAP for true elevation only |
| Dark border | `#343940` | `#3C434B` | REPLACE TOKEN + contrast QA |
| Dark primary text | `#f3f4f6` | `#F4F6F8` | REPLACE TOKEN |
| Dark secondary text | `#a7adb6` | `#C3CAD2` | REPLACE TOKEN |
| Dark muted text | `#a3aab4` | `#8F99A4` | REPLACE TOKEN + readability QA |
| Primary action foreground | Light white; Dark near-black for green | not frozen until `#806BE5` contrast is validated in both themes | VISUAL QA; never keep the old pair blindly |
| Success / Warning / Danger | exact old frontend green/amber/red values | semantic meanings frozen; exact values open | REMAP + TOKEN VALIDATION |
| Unknown / Unavailable / Working | incomplete or inconsistently mapped | separate semantics required | REMAP + TOKEN VALIDATION |

## 3. Source map

### 3.1 `frontend/app/globals.css`

| Area | Class | Migration note |
| --- | --- | --- |
| `--ui-*` semantic namespace | KEEP | One shared semantic namespace is the correct migration seam. Do not create page-private palettes. |
| Dark/Light/System selectors | KEEP | Theme model already supports the frozen model. |
| `--ui-accent`, `--ui-action-primary-*` | REPLACE TOKEN | Current Dark green and Light ink mappings conflict with `#806BE5`. Validate foreground/hover/focus pairings before replacement. |
| Foundation values | REPLACE TOKEN | Remap to the V1 Light/Dark Foundation table. Add a role only when a real consumer needs Surface 2/Elevated. |
| `--ui-success`, `--ui-warning`, `--ui-danger` | VISUAL QA | Keep meanings; do not promote current values to V1. Validate semantic collision and contrast first. |
| `--ui-focus-color` | REMAP | May reference Iris, but focus must also have outline/shape and pass contrast. |
| spacing/radius/z-index/control sizes | KEEP | Not superseded by Direction D; continue as implementation utilities until separately reviewed. |
| shadow values | VISUAL QA | Keep only for true elevation/overlay; Direction D prefers luminance and tonal fields. |
| typography scale | KEEP AS LEGACY IMPLEMENTATION | Reuse until typography implementation is validated; it is not the frozen final V1 type scale. |
| reduced-motion media rule | KEEP | Already meets the required accessibility direction. |
| `--ceo-*` bridges | LEGACY | Preserve only for compatibility; migrate consumers toward semantic `--ui-*` roles. |

### 3.2 `frontend/lib/theme.js`

| Area | Class | Migration note |
| --- | --- | --- |
| CSS-variable indirection | KEEP | Consumers already avoid hardcoded hex values. |
| `COLORS.primary`, `accent`, text, line, state roles | REMAP | Values should flow from migrated `--ui-*` tokens. |
| `primaryLight`, `accentLight`, state soft aliases all pointing to `surface-2` | VISUAL QA | Confirm distinct semantic purpose without creating colored Card surfaces. |
| shared overlay/drawer/input/button styles | KEEP + VISUAL QA | Accessibility structure is reusable; audit Card default, elevation, and primary-action contrast. |
| comments declaring old Frozen palette | REPLACE TOKEN | Update only during implementation migration so comments match the new authority. |

### 3.3 `frontend/tailwind.config.js`

| Area | Class | Migration note |
| --- | --- | --- |
| `ui.*` aliases to CSS variables | KEEP | Correct shared indirection. |
| `primary`, `accent`, state aliases | REMAP | Consume migrated semantic tokens. |
| `cyan` and `violet` aliases pointing to Accent | REMAP | Remove misleading color-name semantics or limit to compatibility; do not imply multiple brand palettes. |
| hardcoded `curis` color aliases | LEGACY | Audit consumers, then replace with semantic roles if still active. |
| comments coupling Primary foreground to bright green | REPLACE TOKEN | The old contrast rationale no longer applies to Iris; rerun contrast QA. |
| spacing/radius/type compatibility aliases | KEEP AS IMPLEMENTATION | Direction D does not freeze their exact values; review during typography/component validation. |

### 3.4 Terra shared components

| File / group | Class | Migration note |
| --- | --- | --- |
| `TerraPrimitives.js` | KEEP + REMAP + VISUAL QA | Keep accessible primitives and semantic classes. Audit primary foreground, `verified` using Accent, progress using Primary, avatar/metric Accent, hover elevation, and Card default usage. |
| `TerraSidebar.js` | VISUAL QA | Keep current-location semantics. Validate small Iris marker, company identity, ordinary-entry quietness, and avoid saturated selected backgrounds. Exact width/layout is not frozen by Direction D. |
| `TerraShell.js` | KEEP + VISUAL QA | Keep Light/Dark/System persistence. Shell composition remains governed elsewhere; do not infer layout from Figma `81:*`. Audit Assistant/avatar accent usage. |
| `TerraState.js` | REMAP | Sample/verified badges currently use Accent; Verified/Evidence must not equal Iris. Empty/error structure may remain. |
| `PipelineGraphView.js` | REMAP + VISUAL QA | Running currently uses Primary; separate Working from Brand. Keep approved/rejected semantics textual and validate new state tokens. |
| `FirstRunGate.js`, `TaskLauncher.js` | VISUAL QA | Replace hardcoded `text-white` assumptions with the validated Primary foreground token. |
| `RuntimeCapabilitySwitcher.js`, `TerraResourcePicker.js` | VISUAL QA | Selected/focus may use sparse Iris; ordinary hover should not create Accent-everywhere behavior. |
| `TerraConfirm.js` | VISUAL QA | Warning meaning remains; exact color awaits state-token validation. |
| `DevMode.js` | KEEP + REMAP | Keep diagnostic token inspection; update expected token values only after migration. |

### 3.5 Hardcoded application values

| File | Class | Migration note |
| --- | --- | --- |
| `frontend/app/ceo-office/settings/page.js` | LEGACY + REPLACE TOKEN | `primaryColor` and `accentColor` default to `#32f08c`; replace or decouple from visual-system defaults during migration. `bgColor #1a1c1f` also reflects the old foundation. |
| `frontend/app/layout.js` | VISUAL QA | `lang="zh-CN"` is correct. Inter injection is an implementation baseline, not a frozen font choice; benchmark a Chinese-first stack. |

### 3.6 `ai-tech-workspace`

| File / area | Class | Migration note |
| --- | --- | --- |
| `ai-tech-workspace/css/tokens.css` | LEGACY + REPLACE TOKEN | Duplicate old green/neutral tokens. Migrate only if this prototype remains an active implementation surface. It is not visual authority. |
| `ai-tech-workspace/css/shell.css` | LEGACY + VISUAL QA | Widespread Accent use includes links, selected cells, progress, working dots, messages, resize handles, avatars, and keywords. Each use needs semantic review; bulk hex replacement would make Iris mean everything. |
| `ai-tech-workspace/js/app.js` | LEGACY + REMAP | Avatar and link styling consume Accent directly. Reassign to identity, action, or ordinary-link semantics before token replacement. |

## 4. Semantic collision audit required

Before any token replacement, every current use of `--ui-accent` / `ui-primary` must be classified as one of:

- Brand Presence;
- Primary Action;
- Selected / Active;
- Focus;
- Current Identity;
- Success / Proven;
- Warning / Risk;
- Evidence;
- Working;
- ordinary link/hover;
- decorative use.

Only the first five are default Iris candidates. Success, Warning, Risk, Evidence, Working, ordinary links, progress, and decorative uses require remapping or explicit validation.

## 5. Minimal migration order

No step is executed by this document.

1. Validate `#806BE5` foreground, hover, pressed, disabled, and focus pairs in Light and Dark.
2. Validate state-color tokens and semantic collision independently from Brand.
3. Map the V1 Neutral Foundation into the existing `--ui-*` semantic seam.
4. Update `globals.css` and System-theme mappings in one bounded implementation issue.
5. Keep `theme.js` and Tailwind consumers on semantic indirection; repair misleading aliases/comments.
6. Audit shared Terra primitives before page-level consumers.
7. Migrate hardcoded settings defaults and active legacy surfaces.
8. Run Light/Dark/System visual QA, Chinese typography QA, keyboard/focus QA, reduced-motion QA, and representative screen regression.

## 6. Do not do

- Do not globally replace `#32f08c` with `#806BE5`.
- Do not map Iris onto Success, Working, Evidence, progress, or Verified.
- Do not create a second token namespace.
- Do not use `81:113` as a frontend layout specification.
- Do not alter Product/IA/Shell composition during token migration.
- Do not freeze `#9A89F0`, state colors, or final font tokens without validation.
- Do not treat existing successful rendering as Visual QA for Direction D.

— MIGRATION MAP READY · IMPLEMENTATION NOT STARTED —
