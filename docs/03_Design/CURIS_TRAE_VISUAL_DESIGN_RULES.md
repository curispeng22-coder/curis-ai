# CURIS TRAE VISUAL DESIGN RULES

Status: Frozen
Authority Class: FROZEN / DESIGN INPUT
Disposition: Minimal qualification input derived from `CURIS_VISUAL_STANDARD_V1.md`
Scope: Trae Master Shell visual qualification only

> 只定义当前视觉语言。产品结构、页面构图、Runtime、Frontend、Figma 与 token migration 另有权威；本文件不授权修改它们。

## COLOR

### Primary Brand Accent

- Iris: `#806BE5`
- 只用于 Primary Action、Selected / Active、Focus、当前身份提示和少量品牌存在。
- 不用于大面积背景、全部标题、全部员工、普通状态、Evidence、Success、Verified、Working、Unknown 或装饰性渐变/Glow。
- `#32f08c` 是 Legacy Implementation Token / Superseded as Brand Accent；不得在新设计中使用。

### Neutral Foundation

Light palette:

| Role | Value |
|---|---|
| Canvas | `#F7F8FA` |
| Base | `#FFFFFF` |
| Surface 1 / 2 | `#F1F3F5` / `#E9EDF1` |
| Elevated | `#FFFFFF` |
| Border | `#DDE2E7` |
| Primary / Secondary / Muted text | `#1D232A` / `#4D5661` / `#7C8794` |

Dark palette:

| Role | Value |
|---|---|
| Canvas | `#181A1D` |
| Base | `#1F2125` |
| Surface 1 / 2 | `#25292E` / `#2D3238` |
| Elevated | `#343A41` |
| Border | `#3C434B` |
| Primary / Secondary / Muted text | `#F4F6F8` / `#C3CAD2` / `#8F99A4` |

Dark Company Space is still subject to validation. Keep contrast, focus, status text and reduced-motion behavior explicit. Color never carries state alone.

## HIERARCHY

Use the frozen hierarchy:

`PRIMARY → SECONDARY → TERTIARY → QUIET`

Build focus in this order:

`Typography → Spacing → Alignment → Contrast → Divider / Tonal Surface → Iris Accent`

Default budget: one PRIMARY focus per viewport, one obvious Primary Action, at most two visibly accented areas. The page must remain understandable if Iris is removed.

## SURFACE

Use this progression:

`Open Canvas → Tonal Field → Divider / Proximity → Raised Surface → Card`

- Open Canvas and Tonal Field carry most of the surface.
- Raised Surface / Shadow express real elevation or overlay only.
- Card is scarce: independent object, focus/selection, action group or overlay.
- No Card Wall, KPI Wall, Employee Wall, Conversation Card Wall or one-card-per-row treatment.

## DENSITY

Use Calm Density: rich working information, readable Chinese text, stable whitespace and progressive disclosure. Do not simulate simplicity by deleting real operating content. Do not make every item equally loud.

## EMPLOYEE

Show responsibility, ownership and continuity through the shared Employee language: identity, role, scope, current responsibility/work, status and conversation affordance. Employee is not the page subject and must not become an Employee Wall or monitoring wall.

## RESULT / DECISION / EVIDENCE

- Result = produced outcome.
- Decision = choice, responsibility and action.
- Evidence = source and traceability.

Use visual weighting, structure, source and action relationships to distinguish them; do not assign three decorative color systems or treat Evidence/Verified as Iris.

## NAVIGATION

Keep the company identity quieter than the current work focus. Use sparse Iris cues for selected/active/focus states. Do not add navigation, restore old five/six-area navigation, or create a Global Topbar. Search, Recent, Notifications and CEO Assistant remain Global Capability, not a new primary area.

## TRAE FREEDOM

Trae may choose typography treatment, grid, spacing, pane proportions, collapse handling, icon weight, selected marker, divider/surface/depth composition, density, light/dark composition and short interruptible micro-interactions. This freedom is visual expression only; it cannot change the locked Shell responsibilities or invent page/product structure.

## FORBIDDEN

Dashboard Wall · Card Wall · Agent Monitor · Employee Wall · Global Topbar · Glow · gradients · old green brand system · warm beige / terracotta · Mineral Blue as primary brand · Runtime/Workflow Console · new navigation · new business module · page-specific product redesign.

## CORE QUALIFICATION INPUT

Trae must read only:

1. `docs/reviews/CURIS_MASTER_SHELL_VISUAL_EXECUTION_CONTRACT.md`
2. `docs/03_Design/CURIS_TRAE_VISUAL_DESIGN_RULES.md`

资格测试仍只输出同一中性 fixture 的 A/B/C 与 Default / Context Expanded / Deep Work 三状态；不把 fixture 或静态稿当作 Product Contract、Runtime 能力或最终页面设计。

— TRAE VISUAL DESIGN RULES · STOP FOR CEO VISUAL REVIEW —
