# Curis Visual Direction Selection Board

Status: Review

Authority Class: REVIEW

Disposition: CEO SELECTION REQUIRED — `A`, `B`, `C`, `D`, or `NONE`

Baseline: main @ c797db840bad285d7e9f1962d06eac61aa28508b

Updated: 2026-08-27

Module: Design

Owner: CEO / Design

Supersedes: none

Scope: Visual-direction comparison only. Product composition is not accepted by selecting a visual direction. No palette, token, typography, or frontend change is frozen here.

## OPTION A — Precision / Quiet

一句话感觉：精密、中性、克制，适合长期分析与经营阅读。

Color：Neutral white / charcoal，低饱和，Accent 极少。

Surface：精确边界、克制明度层级、低 elevation。

Focus：Typography + disciplined contrast。

Density：偏紧凑到平衡。

Navigation：排版式层级，小尺度 Focus / Selected cue。

Representative Frames：

1. [Board A — Precision / Quiet · `13:3`](https://www.figma.com/design/19almI2sZYcrkIW5JV6KTb/Curis-Theme-Exploration-Review%E3%80%82?node-id=13-3)
2. [Neutral Foundation — Light · `52:3`](https://www.figma.com/design/19almI2sZYcrkIW5JV6KTb/Curis-Theme-Exploration-Review%E3%80%82?node-id=52-3)
3. [Neutral Foundation — Dark · `52:4`](https://www.figma.com/design/19almI2sZYcrkIW5JV6KTb/Curis-Theme-Exploration-Review%E3%80%82?node-id=52-4)

Keep：文字清晰、Neutral hierarchy、长时间稳定、低视觉噪音。

Risk：可能过度克制，接近 developer tool / 极简编辑器；公司能量不足。

## OPTION B — Clear / Human

一句话感觉：清透、舒适、有人情味，但不依赖米黄或暖棕。

Color：Light cool-neutral + readable charcoal Dark；柔和但不脏。

Surface：以 luminance 和 spacing 建立材料感，边框较少。

Focus：柔和对比、可读节奏、较轻 Selected state。

Density：平衡到开放。

Navigation：安静、易读、低压力。

Representative Frames：

1. [Board B — Clear / Human · `13:4`](https://www.figma.com/design/19almI2sZYcrkIW5JV6KTb/Curis-Theme-Exploration-Review%E3%80%82?node-id=13-4)
2. [Operating Result — Light · `23:3`](https://www.figma.com/design/19almI2sZYcrkIW5JV6KTb/Curis-Theme-Exploration-Review%E3%80%82?node-id=23-3)
3. [Operating Result — Dark · `23:203`](https://www.figma.com/design/19almI2sZYcrkIW5JV6KTb/Curis-Theme-Exploration-Review%E3%80%82?node-id=23-203)

Keep：长时间舒适、Material quality、中文阅读、Soft-neutral foundation。

Risk：容易落入文档应用 / Productivity Tool / Enterprise SaaS；代表页面的 Mineral Blue 不应被连带视为保留。

## OPTION C — Distinct / Executive

一句话感觉：更坚定、更有经营产品气质，品牌张力来自排版与对比。

Color：强 neutral contrast；Vermilion / Mineral / Copper 仅作克制候选。

Surface：更清晰的材料关系，开放区域与精确边界并用。

Focus：Confident typography + scarce accent。

Density：平衡，Primary 与 supporting 信息反差更强。

Navigation：空间层级明确，定位感更强。

Representative Frames：

1. [Board C — Distinct / Executive · `13:5`](https://www.figma.com/design/19almI2sZYcrkIW5JV6KTb/Curis-Theme-Exploration-Review%E3%80%82?node-id=13-5)
2. [Comparison Board — A / B / C · `13:6`](https://www.figma.com/design/19almI2sZYcrkIW5JV6KTb/Curis-Theme-Exploration-Review%E3%80%82?node-id=13-6)

Keep：Primary Focus、Executive presence、品牌潜力、强层级。

Risk：控制不好会过冷、过硬、luxury-black 或 finance-like；不能继承早期黑绿实现。

## OPTION D — Neutral Foundation + Fresh Iris Company Space

一句话感觉：稳定 Neutral 上加入年轻、积极、克制的 Iris 能量，并通过空间与员工连续性形成“公司正在运行”。

Color：Neutral Foundation + sparse iris；`#806BE5` 仍是 Candidate，不是 Token。

Surface：Open canvas、broad tonal field、divider、proximity；Container 最少。

Focus：Typography-first，Iris 仅用于 focus / identity / primary action / selected cue。

Density：Calm Density，保持 40–60% quiet background，同时收拢 Operating Scene。

Navigation：公司主体与 Workspace 分组优先，小型定位 cue，弱化 feature-menu rhythm。

Representative Frames：

1. [Curis Iris Accent Validation · `61:2`](https://www.figma.com/design/19almI2sZYcrkIW5JV6KTb/Curis-Theme-Exploration-Review%E3%80%82?node-id=61-2)
2. [Employee Workstation — Work Continuity · `68:403`](https://www.figma.com/design/19almI2sZYcrkIW5JV6KTb/Curis-Theme-Exploration-Review%E3%80%82?node-id=68-403)
3. [Shell Default — Final Spatial Polish · `81:3`](https://www.figma.com/design/19almI2sZYcrkIW5JV6KTb/Curis-Theme-Exploration-Review%E3%80%82?node-id=81-3)
4. [Operating Result — Final Spatial Polish · `81:113`](https://www.figma.com/design/19almI2sZYcrkIW5JV6KTb/Curis-Theme-Exploration-Review%E3%80%82?node-id=81-113)

Keep：Neutral stability、Fresh energy、Company identity、people/responsibility continuity、low-card spatial treatment。

Risk：Product Composition 仍为 `PARTIAL`；Main 空白比例、Navigation directory 感、Iris 与 Evidence 的语义距离、Dark Company Space 均未闭环。

## Excluded from CEO options

- Warm Company / terracotta / warm-brown / brown-black：CEO 已明确否决，保留为历史探索证据。
- Black + green / terminal-like C implementation：CEO 已明确否决，只有“strong focus / executive contrast”原则被 Direction C 吸收。
- Mineral Blue as winner：CEO 已明确否决；只作为 Direction B 的历史材料参考。
- `#32f08c`：仅为 Legacy Implementation Visual Baseline；不是昨日新视觉探索中的自动候选。

## CEO response

请直接选择：`A` / `B` / `C` / `D` / `NONE`。

选择只确定下一轮要冻结的 Visual Direction，不接受这些 Frame 的 Product Composition，也不直接修改 Frontend。
