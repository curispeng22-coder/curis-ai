# CURIS VISUAL STANDARD V1

Status: Frozen

Authority Class: FROZEN / DESIGN

Disposition: CEO SELECTED D — CURRENT VISUAL LANGUAGE

Baseline: main @ c797db840bad285d7e9f1962d06eac61aa28508b

Updated: 2026-08-27

Module: Design

Owner: CEO / Design

Supersedes:

- `docs/03_Design/Curis_Design_System.md` visual-language and brand-accent clauses that define `#32f08c` as the Curis brand accent.
- `docs/reviews/CURIS_CURRENT_VISUAL_SYSTEM_TRUTH.md` conclusions that lock `#32f08c` or mark `#806BE5` superseded.
- Earlier visual-direction A/B/C/D candidate status.

Does not supersede: Product Blueprint, UI Blueprint, Master Map, Shell Authority, Product IA, pane responsibilities, Runtime, capability truth, or any page-composition contract.

## 1. CEO decision

```text
CURIS VISUAL DIRECTION:
D — FROZEN

PRIMARY BRAND ACCENT:
#806BE5

LEGACY BRAND ACCENT:
#32f08c — SUPERSEDED

PRODUCT COMPOSITION:
NOT FROZEN

DARK COMPANY SPACE:
VALIDATION STILL REQUIRED
```

Direction D is **Neutral Foundation + Fresh Iris Company Space**.

A, B, and C no longer exist as parallel Curis themes. Direction D absorbs only their validated principles:

- A: precision, neutral hierarchy, disciplined contrast, low visual noise.
- B: comfort, material quality, softer luminance separation, long-session readability.
- C: confident primary focus, scarce accent, restrained executive presence.

No further A/B/C/D direction exploration is authorized by this standard.

## 2. Scope boundary: visual language only

The following Figma nodes are visual evidence:

- [Neutral Foundation — Light · `52:3`](https://www.figma.com/design/19almI2sZYcrkIW5JV6KTb/Curis-Theme-Exploration-Review%E3%80%82?node-id=52-3)
- [Neutral Foundation — Dark · `52:4`](https://www.figma.com/design/19almI2sZYcrkIW5JV6KTb/Curis-Theme-Exploration-Review%E3%80%82?node-id=52-4)
- [Curis Iris Accent Validation · `61:2`](https://www.figma.com/design/19almI2sZYcrkIW5JV6KTb/Curis-Theme-Exploration-Review%E3%80%82?node-id=61-2)
- [Iris Accent Comparison Board · `61:3`](https://www.figma.com/design/19almI2sZYcrkIW5JV6KTb/Curis-Theme-Exploration-Review%E3%80%82?node-id=61-3)
- [Employee Workstation — Work Continuity · `68:403`](https://www.figma.com/design/19almI2sZYcrkIW5JV6KTb/Curis-Theme-Exploration-Review%E3%80%82?node-id=68-403)
- [Shell Default — Final Spatial Polish · `81:3`](https://www.figma.com/design/19almI2sZYcrkIW5JV6KTb/Curis-Theme-Exploration-Review%E3%80%82?node-id=81-3)
- [Operating Result — Final Spatial Polish · `81:113`](https://www.figma.com/design/19almI2sZYcrkIW5JV6KTb/Curis-Theme-Exploration-Review%E3%80%82?node-id=81-113)

They do not freeze page composition.

The following are explicitly **not frozen**:

- all `68:*`, `75:*`, and `81:*` page compositions;
- any three-employee main layout;
- the specific Operating Result layout;
- the specific Main whitespace ratio;
- navigation width or exact navigation layout;
- Spatial Field dimensions;
- employee arrangement, count, or placement.

Future design work must use this visual standard to design the authorized page structure. It must not redraw `81:113` as a page template.

## 3. Brand accent

### 3.1 Primary

`#806BE5` is the Curis Primary Brand Accent.

Decision provenance:

```text
Iris Validation
→ Company Presence
→ Spatial Identity
→ Final Spatial Polish
→ CEO selects Direction D
```

### 3.2 Legacy

`#32f08c` is a `LEGACY IMPLEMENTATION TOKEN` and is `SUPERSEDED AS BRAND ACCENT`.

It may remain temporarily in existing frontend code, but it does not represent the Current Visual Standard. Its presence means `IMPLEMENTATION MIGRATION REQUIRED`, not visual authority.

### 3.3 Dark companion

`#9A89F0` remains `DARK ACCENT CANDIDATE`.

Evidence is insufficient to freeze it: the Iris validation board labels it as an optional Dark tone while preserving the original `#806BE5` baseline. Until Dark Company Space validation is completed, Dark may use `#806BE5` with contrast and interaction-state QA.

## 4. Neutral Foundation

These values were recorded directly in the selected Neutral Foundation boards. They freeze the visual relationship and the listed exploration values as the V1 foundation reference. Implementation token names and migration remain separate work.

### 4.1 Light

Intent: bright, neutral, clean, soft.

| Role | V1 reference value | Relationship |
| --- | --- | --- |
| Canvas | `#F7F8FA` | Quiet application field |
| Base | `#FFFFFF` | Primary reading/working plane |
| Surface 1 | `#F1F3F5` | Subtle grouping |
| Surface 2 | `#E9EDF1` | Stronger tonal separation |
| Elevated | `#FFFFFF` | True raised/overlay surface only |
| Border | `#DDE2E7` | Low-contrast divider/boundary |
| Primary text | `#1D232A` | Main reading and focus text |
| Secondary text | `#4D5661` | Supporting content; remains readable |
| Muted text | `#7C8794` | Tertiary/quiet metadata |
| Disabled | `#AAB2BC` | Unavailable content/control cue |

Forbidden foundation casts: obvious blue, yellow, beige, warm brown, or dirty white.

### 4.2 Dark

Intent: neutral graphite, dimensional, comfortable.

| Role | V1 reference value | Relationship |
| --- | --- | --- |
| Canvas | `#181A1D` | Full-area graphite field; not pure black |
| Base | `#1F2125` | Primary reading/working plane |
| Surface 1 | `#25292E` | First luminance step |
| Surface 2 | `#2D3238` | Stronger material separation |
| Elevated | `#343A41` | True raised/overlay surface only |
| Border | `#3C434B` | Quiet structural boundary |
| Primary text | `#F4F6F8` | Main reading and focus text |
| Secondary text | `#C3CAD2` | Supporting text with long-session readability |
| Muted text | `#8F99A4` | Tertiary/quiet metadata |
| Disabled | `#626B75` | Unavailable content/control cue |

Forbidden dark foundations: blue-black, brown-black, luxury black, pure-black full canvas, terminal black, or accent-tinted canvas.

## 5. Visual hierarchy

The frozen hierarchy is:

```text
PRIMARY
SECONDARY
TERTIARY
QUIET
```

Focus construction order:

```text
Typography
→ Spacing
→ Alignment
→ Contrast
→ Divider / Tonal Surface
→ Iris Accent
```

Typography is first; accent is last. A page must remain understandable if Iris is removed. Large purple areas, purple title systems, or repeated accent blocks must not create hierarchy.

Default attention budget:

- one PRIMARY focus per viewport;
- no more than one obvious Primary Action;
- at most two visibly accented areas;
- supporting content actively recedes without becoming unreadable.

## 6. Iris usage

Allowed first-priority uses:

- Primary Action;
- Selected / Active cue;
- keyboard or interaction Focus;
- current identity cue;
- important interaction;
- small brand presence.

Iris is not the default color for:

- large backgrounds;
- all titles;
- all employees;
- all results;
- Evidence;
- ordinary status;
- Success / Proven / Verified;
- decorative gradients or glow.

Brand must remain distinguishable from Success, Risk, Evidence, Working, Unknown, and Unavailable. Color never carries status alone.

## 7. Surface language

Frozen priority:

```text
Open Canvas
→ Tonal Field
→ Divider / Proximity
→ Raised Surface
→ Card
```

Card is scarce, not the default information container.

Card may be used for:

- an independent object requiring a clear boundary;
- selection or focus;
- action grouping;
- overlay or true elevation.

Card must not become:

- Card Wall;
- KPI Wall;
- Employee Wall;
- Conversation Card Wall;
- one Card per metadata row, result, message, or section.

Shadow expresses real elevation only. Tonal separation should precede border; border should precede shadow.

## 8. Spatial language

Direction D freezes these visual characteristics:

- open space;
- broad tonal fields;
- quiet grouping;
- proximity-led relationships;
- calm density;
- low-container treatment.

A Spatial Field is a visual-language technique, not a page-composition contract. Its exact size, position, geometry, and content are open per authorized page design.

Every implementation must preserve:

- low container dependency;
- clear aggregation;
- one obvious focus;
- meaningful, comfortable density.

## 9. Density

The frozen density principle is `CALM DENSITY`.

Calm Density means rich content may exist, while only the most important layer is visually dominant at one time.

It is not:

- a minimal landing page;
- decorative emptiness;
- a sparse editor with floating islands;
- a dense dashboard or card grid.

Quiet space must serve hierarchy and continuity. It must not make Main look unfinished or content-free.

## 10. Typography

Frozen principles:

- Chinese-first;
- high readability;
- clear hierarchy;
- long-session comfort;
- regular or medium body weight; no overuse of Light;
- consistent English and numeric treatment;
- tabular numbers where comparison requires them.

`FONT FAMILY = OPEN IMPLEMENTATION CHOICE`.

The selected Figma evidence uses Chinese-capable families, but no final family was frozen. Implementations must benchmark Chinese rendering and fallbacks before choosing.

Previously recorded exploration ranges may guide implementation; they are not final tokens:

| Role | Relationship | Exploration range — not token |
| --- | --- | --- |
| Primary Result / Display | Highest content focus | `28–36`, weight around `600` |
| Page Title | Page identity below or equal to the active result according to context | `22–24`, weight around `600` |
| Section | Clear section boundary without competing with PRIMARY | `17–18`, weight `500–600` |
| Object / Work item | Stronger than body, lower than section | `15–17`, weight around `500` |
| Body | Default long-session reading | `14–15`, weight around `400` |
| Supporting | Secondary explanatory content | `13–14`, weight around `400` |
| Metadata | Quiet provenance/time/state detail | `11–12`, weight `400–500` |
| Caption | Lowest readable annotation; never gray-on-gray | `11–12`, visually below Metadata by placement/contrast |

Final font family and exact typography tokens require implementation validation; they do not reopen Direction D.

## 11. Navigation visual language

Navigation IA and seven-area structure come from Current Product/UI authority and are not redefined here.

Frozen visual rules:

- company identity is stronger than feature-menu feeling;
- current location is unambiguous;
- selected cue is sparse and small-scale;
- Iris is used as a cue, not a full selected background;
- ordinary entries stay quiet;
- grouping is created through spacing, typography, and hierarchy;
- high-saturation navigation blocks are forbidden.

The `81:*` frames are visual references only. Their width, alignment, grouping geometry, and layout are not frozen.

## 12. Employee presence

Employee presence communicates:

- responsibility;
- ownership;
- continuity.

It is not decorative avatar usage or runtime monitoring.

When relevant, employee expression prioritizes:

1. Name.
2. Role / responsibility.
3. Current relationship to the work.
4. Status or return time when relevant.
5. Conversation affordance.

Forbidden: Employee Wall, Agent Monitor, avatar grid, or multiple employees becoming the default Main subject.

## 13. Result, Decision, and Evidence

### Result

Result may become PRIMARY. It answers:

- what happened;
- why it matters;
- what happens next.

### Decision

Decision is elevated only when the CEO must make a real judgment. Ordinary progress must not be wrapped as a Decision.

### Evidence

Evidence supports Result and remains visually below it by default. Full evidence belongs in progressive disclosure, Deep View, or Utility when needed.

Result, Decision, and Evidence must not be distinguished through three large colored cards.

## 14. State colors

Frozen semantic meanings:

- Success / Proven: confirmed positive outcome or verified completion.
- Warning: attention needed without confirmed failure.
- Danger / Risk: real risk, failure, blocked state, or destructive action.
- Unknown: truth is not yet established.
- Unavailable: action or capability cannot currently be used.
- Working: active continuation, not Success and not Brand.

Exact state-color tokens are not frozen by Direction D. The latest exploration tested semantic collision, but did not fully validate Success, Warning, Danger, Unknown, Unavailable, and Working across real Light/Dark Company Space.

`TOKEN MIGRATION / VALIDATION REQUIRED`.

Existing frontend greens and warnings remain implementation legacy until contrast, semantic collision, and Light/Dark validation pass. Iris must never substitute for Verified, Evidence, Success, or ordinary Working.

## 15. Theme model

The Curis Theme Model is:

- Light;
- Dark;
- System.

Direction D is frozen across this model. Light Company Space evidence is more complete. Dark foundation and Iris comparison evidence exist, but a full Dark Company Space is not validated.

```text
VISUAL DIRECTION = FROZEN
DARK APPLICATION = NEEDS VALIDATION
```

Dark validation is an application gate, not permission to reopen the visual direction.

## 16. Motion

Motion is:

- short;
- quiet;
- interruptible;
- reduced-motion aware.

Motion may serve:

- Pane transition;
- Focus change;
- Context reveal;
- Result arrival;
- Decision arrival;
- Employee response.

Forbidden: continuous glow, ambient AI animation, decorative motion, looping status theater, or motion that replaces state language.

## 17. Explicitly superseded

The following no longer represent Curis Current Visual Standard:

- `#32f08c` as Curis brand accent;
- warm beige or yellow foundation;
- terracotta or warm-brown brand logic;
- brown-black Dark;
- Mineral Blue as primary brand;
- black + bright-green terminal logic;
- AI gradient or glow;
- old frontend palette as visual authority.

Existing implementation may continue temporarily. Its status is `IMPLEMENTATION MIGRATION REQUIRED`.

## 18. Acceptance boundary

Direction D implementation passes only when:

1. removing Iris still leaves the hierarchy understandable;
2. Iris is scarce and semantically distinct from state colors;
3. Light uses the frozen neutral relationship without blue/yellow/beige cast;
4. Dark uses graphite luminance layering without black/blue/brown tint;
5. one PRIMARY focus is evident within two seconds;
6. rich content remains present without Card Wall or decorative emptiness;
7. employees read as responsible colleagues, not monitored agents;
8. Result, Decision, and Evidence keep distinct semantic weight;
9. keyboard focus, contrast, target size, text alternatives, and reduced motion pass QA;
10. the page composition comes from current Product/UI authority, not copied from `68:*`, `75:*`, or `81:*`.

— CURIS VISUAL DIRECTION D FROZEN —
