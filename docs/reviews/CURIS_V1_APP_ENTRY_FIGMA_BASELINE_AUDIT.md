# CURIS V1 — FIGMA APP ENTRY BASELINE AUDIT

**Status:** Review  
**Authority Class:** REVIEW / FIGMA EVIDENCE / PRODUCT UI AUDIT  
**Disposition:** READY FOR INCREMENTAL EDIT / NOT IMPLEMENTATION READY  
**Date:** 2026-08-28  
**Owner:** Codex — Figma UI Revision Session  
**Scope:** Read-only audit of the imported App Entry / CEO Assistant Figma candidate  
**Pointer / Index Update:** None; this review does not modify Current Product Truth or Frozen visual authority

**Post-correction addendum:** The original read-only baseline evidence is preserved below. An authorized incremental Figma correction and current-run verification were completed later on 2026-08-28; see section 18.

**Current status note (2026-08-28):** This file remains historical audit evidence. Its earlier `UI ACCEPTED: NOT YET` / candidate disposition is superseded for current UI by `docs/reviews/CURIS_V1_APP_ENTRY_UI_ACCEPTANCE.md`; the Figma file is now the Current Design Baseline. The implementation, provider-data and credential gaps recorded below remain valid and do not imply Frontend / Runtime / Schema completion.

## 1. Figma file identity and audit boundary

- **File:** `Curis V1 — App Entry & CEO Assistant Experience`
- **File key:** `2Fh7DgPPfLgdbvNtnzPnk9`
- **File link:** [Open Figma file](https://www.figma.com/design/2Fh7DgPPfLgdbvNtnzPnk9/Curis-V1-%E2%80%94-App-Entry---CEO-Assistant-Experience?node-id=0-1&p=f)
- **Page:** `Page 1` (`0:1`)
- **Top-level Frames found:** 13
- **Editor type returned by Figma:** `figma`
- **Audit evidence:** current-run Figma Plugin API layer inspection plus current-run 1440 px screenshots of every top-level Frame.
- **Mutations performed:** none. No Frame, layer, component, text, color, prototype link, variable, or style was created, updated, moved, renamed, or deleted.

This review consumes the current App Entry lifecycle, Employee Conversation / Model Experience, Avatar Identity, Create Business, Frozen Master Shell, and Frozen Direction D visual contracts. It does not reassess their product decisions.

### Connector capability result

| Capability | Result | Evidence / limit |
| --- | --- | --- |
| READ | SUPPORTED / VERIFIED | The target file, Page, 13 Frames, layer trees, properties, text, colors, geometry, and screenshots were read successfully. |
| WRITE | API EXPOSED / TARGET PERMISSION NOT VERIFIED | The official `use_figma` surface exposes Figma Plugin API mutation methods. This read-only audit deliberately did not test target-file write permission. |
| CREATE | API EXPOSED / TARGET PERMISSION NOT VERIFIED | Creation APIs are exposed; no create call was made. |
| UPDATE | API EXPOSED / TARGET PERMISSION NOT VERIFIED | Update APIs are exposed; no property or content was changed. |
| DELETE | API EXPOSED / TARGET PERMISSION NOT VERIFIED | Node removal is exposed by the API; no delete call was made. |

Read access must not be interpreted as proof of edit permission. A later authorized edit session should begin with one bounded, reversible permission check or the first approved edit—not a speculative mutation.

## 2. Complete Frame inventory

| # | Frame | Node | Size | Layer evidence | Integrity | Editability |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | [Welcome to Curis 1440w light](https://www.figma.com/design/2Fh7DgPPfLgdbvNtnzPnk9/Curis-V1-%E2%80%94-App-Entry---CEO-Assistant-Experience?node-id=1-2&p=f) | `1:2` | 1440 × 900.25 | 80 descendants; 12 Text; 27 vector-like; 31 Auto Layout | PASS | EDITABLE |
| 2 | [创建你的 AI 公司 1440w light](https://www.figma.com/design/2Fh7DgPPfLgdbvNtnzPnk9/Curis-V1-%E2%80%94-App-Entry---CEO-Assistant-Experience?node-id=1-83&p=f) | `1:83` | 1440 × 900.25 | 104 descendants; 15 Text; 29 vector-like; 48 Auto Layout | PASS | EDITABLE |
| 3 | [公司创建成功 1440w light](https://www.figma.com/design/2Fh7DgPPfLgdbvNtnzPnk9/Curis-V1-%E2%80%94-App-Entry---CEO-Assistant-Experience?node-id=1-188&p=f) | `1:188` | 1440 × 900 | 235 descendants; 33 Text; 82 vector-like; 87 Auto Layout | 6 px shell overrun | EDITABLE |
| 4 | [Empty Curis — CEO Desk 1440w light](https://www.figma.com/design/2Fh7DgPPfLgdbvNtnzPnk9/Curis-V1-%E2%80%94-App-Entry---CEO-Assistant-Experience?node-id=1-424&p=f) | `1:424` | 1440 × 900 | 199 descendants; 29 Text; 67 vector-like; 74 Auto Layout | 6 px shell overrun | EDITABLE |
| 5 | [Empty Curis — Business Space 1440w light](https://www.figma.com/design/2Fh7DgPPfLgdbvNtnzPnk9/Curis-V1-%E2%80%94-App-Entry---CEO-Assistant-Experience?node-id=1-624&p=f) | `1:624` | 1440 × 900 | 196 descendants; 25 Text; 83 vector-like; 60 Auto Layout | 6 px shell overrun | EDITABLE |
| 6 | [CEO Assistant — No Model 1440w light](https://www.figma.com/design/2Fh7DgPPfLgdbvNtnzPnk9/Curis-V1-%E2%80%94-App-Entry---CEO-Assistant-Experience?node-id=1-821&p=f) | `1:821` | 1440 × 900 | 230 descendants; 33 Text; 81 vector-like; 85 Auto Layout | 6 px shell overrun | EDITABLE |
| 7 | [AI 能力设置 — 模型管理 1440w light](https://www.figma.com/design/2Fh7DgPPfLgdbvNtnzPnk9/Curis-V1-%E2%80%94-App-Entry---CEO-Assistant-Experience?node-id=1-1052&p=f) | `1:1052` | 1440 × 900 | 239 descendants; 42 Text; 75 vector-like; 94 Auto Layout | 6 px shell overrun | EDITABLE |
| 8 | [CEO Assistant — 模型已启用 1440w light](https://www.figma.com/design/2Fh7DgPPfLgdbvNtnzPnk9/Curis-V1-%E2%80%94-App-Entry---CEO-Assistant-Experience?node-id=1-1292&p=f) | `1:1292` | 1440 × 900 | 222 descendants; 35 Text; 69 vector-like; 88 Auto Layout | 6 px shell overrun | EDITABLE |
| 9 | [Empty Company — CEO Desk 1440w light](https://www.figma.com/design/2Fh7DgPPfLgdbvNtnzPnk9/Curis-V1-%E2%80%94-App-Entry---CEO-Assistant-Experience?node-id=1-1515&p=f) | `1:1515` | 1440 × 900 | 211 descendants; 32 Text; 68 vector-like; 81 Auto Layout | 6 px shell overrun | EDITABLE |
| 10 | [Create Business — Conversational Entry 1440w light](https://www.figma.com/design/2Fh7DgPPfLgdbvNtnzPnk9/Curis-V1-%E2%80%94-App-Entry---CEO-Assistant-Experience?node-id=1-1727&p=f) | `1:1727` | 1440 × 1102.59 | 262 descendants; 47 Text; 74 vector-like; 109 Auto Layout | intentional long state plus 6 px shell overrun | EDITABLE |
| 11 | [AI 能力设置 — 添加模型 1440w light](https://www.figma.com/design/2Fh7DgPPfLgdbvNtnzPnk9/Curis-V1-%E2%80%94-App-Entry---CEO-Assistant-Experience?node-id=1-1990&p=f) | `1:1990` | 1440 × 922 | 220 descendants; 40 Text; 67 vector-like; 86 Auto Layout | content-height variation plus 6 px shell overrun | EDITABLE |
| 12 | [AI 能力设置 — 高级参数 1440w light](https://www.figma.com/design/2Fh7DgPPfLgdbvNtnzPnk9/Curis-V1-%E2%80%94-App-Entry---CEO-Assistant-Experience?node-id=1-2211&p=f) | `1:2211` | 1440 × 900 | 216 descendants; 40 Text; 59 vector-like; 92 Auto Layout | 6 px shell overrun | EDITABLE |
| 13 | [CEO Assistant — 切换模型 1440w light](https://www.figma.com/design/2Fh7DgPPfLgdbvNtnzPnk9/Curis-V1-%E2%80%94-App-Entry---CEO-Assistant-Experience?node-id=1-2428&p=f) | `1:2428` | 1440 × 900 | 248 descendants; 40 Text; 76 vector-like; 98 Auto Layout | 6 px shell overrun | EDITABLE |

The expected lifecycle and the Trae-added model variations are all present. No extra top-level Frame was found.

## 3. Editability result

### PASS: the pages are not flattened

- All 13 Frames contain real editable Text layers.
- All iconography and avatar marks are editable Vector / Ellipse / Frame structures.
- Buttons, inputs, surfaces, navigation, composers, model selectors, provider choices, structured surfaces, and status treatments are separate layers.
- Image-paint count across the entire Page is **0**. No screen is a full-page raster image.
- Key layer names such as `Nav - 主导航`, `Header`, `Main`, `Conversation stream`, `Composer`, `Expanded model menu`, `Section - Model list`, and `Section - Provider` make targeted editing possible.

### Structural limit: no shared component system

- Component definitions: **0**
- Component instances: **0**
- Prototype reactions: **0**

This does not block frame-scoped editing, but repeated Shell, Navigation, Composer, Button, Avatar, and Model Selector structures are independent copies. A single edit will not propagate. Cross-frame revisions therefore require an explicit affected-Frame matrix and visual regression check.

**Editability verdict:** `EDITABLE, FRAME-SCOPED, NO SHARED-INSTANCE SAFETY NET`.

## 4. Frame integrity result

- All 13 top-level Frames exist and render completely in current-run screenshots.
- No accidental full-page clipping, missing panel, broken raster, severe overlap, or abnormal ultra-wide Frame was observed.
- The two non-900 heights (`1102.59`, `922`) correspond to content-rich Create Business and Add Model states rather than corrupted canvases.
- The selector menu in `1:2428` intentionally overlays the conversation/composer region, but its internal text spacing is broken; this is a UI defect, not layer corruption.
- Every Shell Frame from `1:188` through `1:2428` contains a `Nav - 主导航` approximately `905.5` px high inside a nominal 900 px Frame. The bottom CEO container ends around y=906, so exports render approximately 6 px taller than the declared Frame. This must be normalized before implementation handoff.
- Tiny zero-height vector segments are stroke geometry used by icons, not lost content.

**Integrity verdict:** no P0 corruption; one systematic P1 geometry overrun.

## 5. Layer structure suitability

| Area | Current structure | Incremental edit suitability |
| --- | --- | --- |
| Navigation | Named `Nav - 主导航`; seven items are independent Text + Vector groups | Good for targeted edits; repetitive across Frames |
| Context / Utility | Not consistently named or separated as semantic panes in these entry states | Usable, but no reusable pane contract in layers |
| Main | Named `Main` in Shell Frames | Good |
| Pane Header | Named `Header`, usually distinct from `Main` | Good |
| CEO Avatar / identity | Separate Vector/Ellipse/Text structures | Editable, but current avatar assets are placeholders |
| CEO Assistant | Separate identity header, conversation stream, status surface | Good |
| Conversation | Separate messages and metadata | Good |
| Composer | Separate named Frame in conversation states | Good |
| Model Selector | Separate button/menu; expanded state exists | Good; content/state consistency fails |
| Structured Surface | Separate `Understanding`, readiness, gap, and list surfaces | Editable; some surfaces use internal-system language |
| Model Configuration | Separate model list, provider, credential, connection, advanced sections | Good |

Codex can safely make precise changes to named layers. It cannot safely assume a change to one repeated layer updates sibling Frames.

## 6. Navigation consistency audit

### Pass

- All 11 Shell-based Frames contain all seven primary items in the required order: `CEO 工作台 → 业务空间 → 组织中心 → 人才与能力 → 经营洞察 → 资料库 → 会议`.
- Every item has a linear icon; `组织中心` is **not** missing its icon.
- Icons are visually consistent at roughly 16 px with approximately 1.33 px round-cap strokes.
- Text is generally 13 px, with quiet neutral entries.
- Selected states use a small Iris left cue plus Iris text/icon. No whole-row saturated purple selected background remains.
- Item spacing and icon/text alignment are visually stable across the 11 copies.

### Issues

- Navigation is copied, not componentized; consistency is presently visual coincidence rather than shared-instance enforcement.
- Selected labels change font style while unselected labels also switch between `Liberation Sans` and `WenQuanYi Zen Hei` across Frames. This is visible on `CEO 工作台` and contributes to width/weight drift.
- Empty Curis Frames show `CEO Assistant` as a persistent navigation presence with an AI status dot even though Company = 0. That is a truth-boundary issue, not a navigation IA issue.
- The approximately 905.5 px navigation height causes the systematic 6 px Frame overrun.

## 7. Chinese copy audit

### English UI copy replacement list

The following are ordinary user-facing product words and should be replaced with natural Chinese or removed:

| Current copy | Required treatment | Affected Frames |
| --- | --- | --- |
| `CEO Assistant` | `CEO 助理` in ordinary UI | `1:188`, `1:424`, `1:624`, `1:821`, `1:1052`, `1:1292`, `1:1515`, `1:1727`, `1:1990`, `1:2211`, `1:2428` |
| `Conversation` | `对话` | `1:83`, `1:188`, `1:821`, `1:1052`, `1:1990` |
| `Decision` / `Meeting` | `决策` / `会议` | `1:83` |
| `Display Name` | `显示名称` or user-facing `称呼` | `1:83` |
| `Company` | `公司` | `1:2`, `1:424`, `1:624`, `1:1515` |
| `Business` | `业务` | `1:424`, `1:624` |
| `Employee` | `员工` | `1:424` |
| `App` | `应用` or omit | `1:624` |
| `AI EXECUTION READY` | `AI 已可用` / `AI 已准备好` | `1:1292`, `1:1727` |
| `AI Ready` | `AI 已准备好` | `1:1515` |
| `Understanding` | `当前理解` | `1:1727` |
| `Provider` in ordinary guidance | `服务商` | `1:1052`, `1:1990`, `1:2211` |
| `Credential` in ordinary guidance | `凭证` | `1:1052`, `1:1990` |
| `Auto` | `自动` | `1:2428` |
| `OPEN / IMPLEMENTATION GAP`, `Implementation`, `M3 Keychain`, `OPEN` | Remove from user UI; keep only as off-canvas design annotation or implementation evidence | `1:1052`, `1:1990`, `1:2211`, `1:2428` |

`AI 能力缺口`, `确定性系统文案 · 非 AI 生成回复`, and `最近验证` are already Chinese but still read like audit/runtime language. Replace them with ordinary user language such as “还需要启用 AI 模型” and remove provenance statements that do not help the user act.

### Keep original

Keep product/brand/technical terms where they are genuinely technical: `Curis`, `OpenAI`, `Anthropic`, `Claude`, `DeepSeek`, `GPT-4o`, `API Key`, `URL`, `Token`, `Temperature`, `Top-P`, `Top-K`, `Tool Call`, and `Thinking / Reasoning` inside Advanced Settings. `Local` may remain a provider type if the product supports it.

## 8. CEO Identity / Avatar state

### Current evidence

- `1:83` includes a real editable CEO display-name input (`小敏`), CEO avatar area, `上传图片` action, optional/fallback copy, a row of eight editable preset glyphs, and a company-name input.
- Shell Frames show a separate lower-left avatar/fallback plus the display name `小敏`.
- No avatar is an Image layer. The current shown avatar is a generic vector placeholder/fallback.

### Gap

The accepted pattern is `UPLOAD + CURIS CARTOON PRESET + FALLBACK`. Upload is represented, and a fallback is visible, but the preset row uses generic UI symbols rather than a Curis cartoon avatar set. There is no visual evidence of uploaded-image crop/preview state. Cross-frame CEO avatar rendering is therefore only partially specified.

**State:** `PARTIAL / P1 BEFORE IMPLEMENTATION`.

## 9. Conversation / Model Selector state

### Pass

- No-model, enabled, Create Business, and expanded-selector conversation states all contain separate editable Composer structures.
- Model Selector buttons are separate Frames rather than text baked into a screenshot.
- `1:2428` contains a separate `Expanded model menu` with editable model/provider rows.
- The model names can be replaced because they are real Text layers.
- No per-Employee settings panel is shown inside the conversation; model usage is presented at the conversation level.

### Problems

- `1:821` repeats the same no-model state in the top status, capability-gap panel, selector, helper text, disabled input, and CTA. This is excessive state duplication.
- `1:1292` is labeled model-enabled but retains the earlier message “启用一个 AI 模型后…”, directly contradicting the enabled state.
- `1:1292` repeats readiness in the top status, readiness surface, selector, and composer helper.
- `1:2428` visually collides model and provider labels (`Claude 3.5 SonnetAnthropic`) because row spacing/column allocation is insufficient.
- `1:2428` says three models are enabled while `1:1052` shows one enabled model and one not enabled.
- `Auto / 自动选择为 OPEN` exposes an unresolved behavior as if it were usable product UI.
- Assistant identity relies mainly on a spark icon and `A` fallback; the interaction still reads closer to a generic chatbot surface than a company-level coordinator.

## 10. Model Configuration state

### Mature elements worth keeping

- Model List, Add Model, Provider selection, API Key / credential, connection validation, default model, and Advanced Settings are separate editable surfaces.
- The default path is simpler than the Advanced path; advanced parameters are placed on a separate Frame.
- Provider and model entries are replaceable Text/Vector layers, not baked images.
- `1:1990` correctly places provider choice before model and credential input.

### Temporary / unsafe elements

- `1:1052` presents `GPT-4o · 连接正常 · 默认模型 · 最近验证：刚刚` as current fact, while the design file has no implementation evidence attached.
- `Claude 3.5 Sonnet`, OpenAI, Anthropic, DeepSeek, Local, and later DeepSeek-V3 are design fixtures. Their editability is adequate, but the user-visible screen does not distinguish fixture from current capability.
- `OPEN / IMPLEMENTATION GAP` panels and `M3 Keychain` wording are review annotations placed inside product UI.
- Provider support, credential persistence, default-model resolution, health, and auto-selection behavior remain implementation-dependent.
- `1:2211` shows a fixed advanced-field set for OpenAI while also stating that provider-specific field behavior is unresolved.

**Required boundary:** keep fixtures in Figma only as clearly marked design data outside the user-facing UI; do not treat them as `CURRENT VERIFIED CAPABILITY`.

## 11. Empty Curis / Empty Company audit

### Empty Curis (`1:424`, `1:624`)

The Frames correctly avoid fake business results and explicitly say that no Business, Employee, operating data, or documents exist. However, they also show `CEO Assistant` in the navigation, an AI status cue, and a model-configuration path. This visually creates a real company-level employee presence while Company = 0. `1:624` also competes with three actions: create AI company, create Company, and view model configuration.

**Result:** state distinction is **not yet clean**; P1 correction required.

### Empty Company (`1:1515`)

The Frame correctly shows Company exists, AI enabled, Business = 0, a real CEO Assistant conversation, and a “开始第一个业务” path. It does not fabricate an existing Business or result.

The state is semantically correct, but the top status card and conversation repeat the start-business intent, and large empty vertical space separates supporting context from the composer.

**Result:** semantic PASS; visual/interactions need minor correction.

## 12. Create Business conversational state

`1:1727` correctly starts from a CEO message and inserts an editable Structured Surface inside the ongoing conversation. It is not a separate page-level Wizard.

It nevertheless drifts toward a field-extraction / CRM form pattern:

- the `Understanding` surface presents four equally weighted fields in a 2 × 2 grid;
- the primary action `确认，生成方案` encourages confirmation before the missing high-impact questions are resolved;
- `补充信息` and `换一个方向` compete with the primary path;
- the large implementation note exposes the full internal lifecycle (`Clarification → Proposal → Creating → First Landing`);
- the assistant says it can create a professional proposal without showing whether capability is actually available.

**Result:** Conversation + Structured Surface pattern exists, but the surface requires major correction to express a natural understanding summary and at most the necessary 1–2 questions rather than extracted CRM fields.

## 13. Visual consistency and Product UI review

### Direction D consistency

- `#806BE5` is present throughout all 13 Frames as the sparse brand/action/selection accent.
- No `#32f08c` legacy brand accent was found.
- Semantic green (`#2D7A5A`) is used for enabled/success states, amber/brown (`#B07D2B`) for warning/not-ready states, and teal (`#4A7A8A`) for supporting information. Brand and success are visually distinct.
- The Light Neutral Foundation is broadly consistent: `#F7F8FA`, white surfaces, `#DDE2E7` borders, dark primary text, muted secondary text.
- No Frame reverts to a black Trae-style UI, old green brand theme, large purple page background, gradient, or glow.

### A. Overall product feeling

The set reads as a coherent Desktop App shell after company creation. It does **not** yet feel implementation-finished:

- `1:2` is still a centered marketing/landing composition with four feature cards.
- Empty states use large centered cards and extensive blank canvas, producing “empty minimalism” rather than Calm Density.
- Conversation Frames resemble a clean generic AI chat tool with a status card above the composer.
- Model settings resemble a conventional SaaS settings panel.
- Company presence is carried mostly by copy (`CEO Assistant`, company created) rather than deeper identity/material continuity.

### B. Visual finish

- Surface separation is technically clear but over-dependent on rounded white cards, subtle shadows, and repeated bordered panels.
- Material finish is flat: most Frames use the same white/gray surface relationship, so primary, structured, and utility surfaces are differentiated mainly by boxes.
- Composer is editable and consistent, but visually heavy: it is a large floating card with multiple persistent controls and duplicated status copy.
- Assistant Presence is weak: one spark mark or letter avatar does not yet create a recognizable company-level colleague.
- Typography uses a visible mix of `WenQuanYi Zen Hei` and `Liberation Sans`; identical Chinese roles sometimes switch family/weight across Frames. Some Text layers return mixed/null font metadata. This looks imported rather than intentionally typeset.
- Radii cluster around 10/12/16 plus pill values; the system is close but not rigorously applied by semantic surface level.
- `1:2428` has an actual alignment failure in selector rows.

### C. Information density

| Density correction | Frames | Finding |
| --- | --- | --- |
| Increase meaningful supporting context / reduce empty drift | `1:424`, `1:624`, `1:1292`, `1:1515`, `1:2428` | Main content floats in large unused canvas; supporting state and next action are far apart. |
| Reduce repeated status information | `1:188`, `1:821`, `1:1292`, `1:1515` | The same readiness/not-ready message appears in header, card, conversation, selector, and helper text. |
| Reduce card density | `1:2`, `1:188`, `1:424`, `1:624`, `1:1052`, `1:1727`, `1:2211` | Feature, empty-state, assistant, field, and gap information is repeatedly boxed. |
| Preserve current balanced density | `1:1990` after removing internal annotations | Add Model has a legible primary flow and separated advanced entry. |

### D. Interaction clarity

- First Open has a clear primary CTA, but “先看看 Curis” does not explain that it enters a no-company browse state.
- Create Company asks for the correct three identity inputs, but internal terminology in helper copy obscures the task.
- Company Created shows Assistant first presence, but repeats model-not-ready state and does not make the next single action dominant.
- No Model points to configuration, but too many repeated cues compete.
- Enabled state provides both “开始第一个业务” and a freeform composer; the relationship between those two entry paths is not explicit.
- Empty Company repeats “开始第一个业务” in a card and the assistant prompt.
- Create Business emerges inside conversation, but the extracted-field surface feels like a wizard step.
- Prototype reactions are zero, so there is no current clickable evidence for Welcome → Create Company → Company Created → Configure Model → Enabled Conversation → Empty Company → Create Business.

### E. CEO Assistant presence

Identity, role, current responsibility, conversation, no-model state, and enabled state all exist as editable layers. The semantic role is present. Visually, however, the repeated card header, generic spark icon, `A` fallback, and system-status panels make the Assistant feel like a chatbot widget or AI module rather than the company-level coordinator. The same Conversation + Model Selector skeleton is extensible to future Employees, but the identity slot needs a completed shared Avatar / Name / Role pattern.

### F. Model experience

- Default configuration path is understandable; Advanced Settings is correctly separated.
- Provider → Model → Credential hierarchy is visible.
- The user-facing implementation-gap notices undermine trust and must be removed.
- Model health/current capability fixtures must come from real implementation truth before implementation.
- Enabled model counts and availability must agree across list, conversation, and selector.
- No-model should use one clear configuration entry rather than repeated warnings.
- `Auto` behavior is not established by the current product contract. **PRODUCT DECISION REQUIRED:** define whether automatic selection exists, what it means, and whether it belongs in V1 before showing it.

### G. CEO / Employee identity

CEO name and fallback identity are present. Upload is represented. Curis cartoon presets and uploaded-image preview are missing. The lower-left CEO region does show avatar + display name, but only as generic fallback. The layout can extend to Employee Name + Avatar + Conversation, but it needs one completed shared identity pattern before implementation.

### H. Chinese UI consistency

The largest problem is not English alone; it is internal-language leakage. `AI EXECUTION READY`, `OPEN / IMPLEMENTATION GAP`, `M3 Keychain`, `确定性系统文案`, `Capability Gap`-style wording, and “最近验证” read like audit/runtime concepts. Translate genuine product terms, but remove engineering/audit states rather than literally translating them.

### I. Cross-Frame component consistency

- Navigation is visually consistent, including the `组织中心` icon and sparse Iris selection cue.
- Composer geometry and controls are broadly consistent.
- The selected model state is not consistent: one enabled model in management, three in selector.
- Model-enabled conversation contains stale no-model copy.
- CEO Assistant status alternates among Chinese and English labels.
- Typography families/weights drift across otherwise identical components.
- No shared components or instances protect any of these repeated patterns.

## 14. Per-Frame Design Review

| Frame | Verdict | Why | Exact changes required |
| --- | --- | --- | --- |
| `1:2` Welcome | **MAJOR FIX** | Clear entry task, but it reads as a landing page; four feature cards create marketing UI and empty canvas. Skip meaning is unclear. | Keep one primary creation action; clarify browse-without-company consequence; replace the four-card feature strip with quieter supporting explanation; replace `Company` in ordinary copy. |
| `1:83` Create Company | **MAJOR FIX** | Correct fields exist, but the form is a generic floating card and avatar preset is not the accepted Curis cartoon set. Helper copy exposes internal terms. | Complete upload/preset/fallback states; use real cartoon preset previews; localize Display Name/Conversation/Decision/Meeting; simplify supporting copy and normalize typography. |
| `1:188` Company Created | **MAJOR FIX** | Correct first Assistant presence, but nested cards and repeated no-model status make it SaaS-like and action hierarchy is diffuse. | Keep identity + Assistant + one next action; consolidate no-model explanation/configuration; remove deterministic-system note from ordinary UI; reduce nested surfaces; fix shell overrun. |
| `1:424` Empty Curis — CEO Desk | **MAJOR FIX** | Company=0 is stated, but real CEO Assistant/status is implied; empty-state card wall and excessive whitespace weaken product completion. | Remove company-level Assistant presence/status until Company exists; keep no-fake-data truth; reduce four-card wall; make browse state and create-company action unambiguous; fix shell overrun. |
| `1:624` Empty Curis — Business Space | **MAJOR FIX** | Correctly says no Business, but shows Assistant/model configuration and three competing actions before Company exists. | Remove company-level Assistant/model state; retain browse explanation; use one create-company primary action and one clear return path; localize copy; fix shell overrun. |
| `1:821` CEO Assistant — No Model | **MAJOR FIX** | Correct fail-closed state and editable Composer, but the same status is repeated six times and identity reads like a chatbot module. | Consolidate to one no-model explanation + one configuration action; preserve disabled composer; localize CEO Assistant/Conversation; strengthen shared identity pattern without new functionality; fix shell overrun. |
| `1:1052` Model Management | **MAJOR FIX** | Good information architecture, but fixtures look like verified current capability and internal implementation gaps are user-visible. | Remove implementation-gap panel from product UI; source states dynamically or label them as off-canvas fixtures; reconcile enabled counts; localize ordinary terms; fix shell overrun. |
| `1:1292` Model Enabled | **MAJOR FIX** | Enabled structure is sound, but it contains stale “启用模型后” copy and repeated readiness signals. | Replace stale message; use one readiness cue; keep selector + composer; reconcile enabled count; localize status; fix shell overrun. |
| `1:1515` Empty Company | **MINOR FIX** | State truth is correct: Company exists, AI ready, Business=0, real Assistant present. | Remove duplicated start-business CTA/statement; tighten vertical relationship between state, Assistant, and composer; localize AI Ready/Company; fix shell overrun. |
| `1:1727` Create Business | **MAJOR FIX** | Conversation + Structured Surface exists, but 2 × 2 extraction grid, early confirmation, and lifecycle note make it a wizard/CRM surface. | Replace field grid with natural understanding summary; ask only necessary high-impact questions; remove lifecycle/internal note; resolve CTA competition; localize Understanding/status; fix shell overrun. |
| `1:1990` Add Model | **MAJOR FIX** | Default path is understandable and Advanced is separated, but implementation/security notes are exposed and fixture truth is ambiguous. | Remove implementation note; keep Provider/Model/API Key hierarchy; show only verified/dynamic choices; clarify validation result; normalize height/overflow. |
| `1:2211` Advanced Settings | **MINOR FIX** | Advanced placement and technical terminology are appropriate, but provider-dependent fields are shown as settled while an internal gap is exposed. | Remove implementation panel; label fields as provider-dependent where needed; keep technical terms; normalize typography and shell overrun. |
| `1:2428` Model Selector Expanded | **MAJOR FIX** | Correct interaction concept, but provider text collides, enabled count contradicts management, and unresolved Auto is exposed. | Fix row columns/spacing; reconcile list with Model Management; remove or decide Auto; remove `OPEN`; keep management entry; fix shell overrun. |

No Frame requires replacement solely because of import/editability. Major-fix verdicts refer to bounded correction of the existing candidate, not a new visual direction.

## 15. P0 / P1 / P2 issue list

### P0 — Blocks Figma editing

**None.** No flattening, unreadable file, severe layer corruption, missing top-level Frame, or inaccessible target was found.

### P1 — Must fix before implementation

1. **Empty Curis truth boundary:** `1:424`, `1:624` imply a real CEO Assistant/model state before Company exists.
2. **Contradictory model state:** `1:1292` contains no-model copy; `1:1052` and `1:2428` disagree on enabled models; Auto remains unresolved.
3. **False capability appearance:** `1:1052`, `1:1990`, `1:2211`, `1:2428` present design fixtures/internal gaps as user-facing current facts.
4. **Avatar pattern incomplete:** `1:83` and all identity consumers lack Curis cartoon preset evidence and uploaded-image preview behavior.
5. **English/internal UI language:** ordinary English and audit/runtime wording remain across most Frames.
6. **Create Business form drift:** `1:1727` resembles extracted-field confirmation rather than natural conversation plus a bounded structured surface.
7. **Model selector visual failure:** `1:2428` has model/provider text collision and state mismatch.
8. **Readiness/status duplication:** `1:188`, `1:821`, `1:1292`, `1:1515` repeat the same state across header, card, message, selector, and helper copy.
9. **Systematic Frame overrun:** all 11 Shell-based Frames render about 6 px beyond the declared Frame.
10. **Typography implementation inconsistency:** repeated components mix `Liberation Sans` and `WenQuanYi Zen Hei`; Chinese-first hierarchy is not stable.
11. **Core transition evidence absent:** all prototype reaction counts are zero; implementation handoff cannot verify the intended flow from the file alone.
12. **Landing/SaaS/chat visual drift:** `1:2`, `1:188`, `1:424`, `1:624`, `1:821`, `1:1292`, `1:1727` need bounded composition/material correction to reach Calm Density without changing Direction D.

### P2 — Visual polish

1. Normalize radii by semantic surface level instead of using 10/12/16 interchangeably.
2. Reduce repeated subtle shadows and heavy floating-card treatment, especially around Composer and empty states.
3. Tighten icon/text optical alignment in provider and status rows.
4. Reduce large nonfunctional vertical gaps in `1:424`, `1:624`, `1:1292`, `1:1515`, and `1:2428`.
5. Normalize frame heights to integers after the content/overflow correction.
6. Improve layer naming beyond generic `Container`, `Frame`, `Rectangle`, and `Text` for frequently edited subparts.
7. Establish shared components or a strict revision matrix for Navigation, Header, Assistant Identity, Composer, Model Selector, Button, and Avatar after the current corrections are accepted.

## 16. Minimum Design Correction Plan

### P1.1 — Restore lifecycle truth

- **Affected Frames:** `1:424`, `1:624`, `1:188`, `1:1292`, `1:1515`
- **Affected Components:** Shell status, CEO Assistant entry, readiness surface, CTA
- **Current Problem:** Company=0 states imply an Assistant; enabled/no-model copy conflicts; readiness is repeated.
- **Required Correction:** apply one truth table for Company existence, AI readiness, Business existence, and Assistant presence; show only one dominant status/action per state.
- **Acceptance Check:** each Frame can be classified correctly without reading its name; no Company=0 Frame presents a real Assistant; no enabled Frame says to enable a model.

### P1.2 — Reconcile the complete Model Experience

- **Affected Frames:** `1:821`, `1:1052`, `1:1292`, `1:1990`, `1:2211`, `1:2428`
- **Affected Components:** model list, selector, expanded menu, no-model state, readiness state, connection state
- **Current Problem:** model counts/statuses conflict; fixtures look verified; Auto is unresolved; selector rows collide.
- **Required Correction:** use one fixture/state matrix across all Frames, remove current-capability claims without evidence, repair selector columns, and either remove Auto or resolve it through Product Decision.
- **Acceptance Check:** the same enabled models, default model, provider, health, and selector options appear everywhere; no row overlaps at 1440 px.

### P1.3 — Complete CEO / Employee identity pattern

- **Affected Frames:** `1:83` and every Shell/Conversation identity consumer
- **Affected Components:** avatar picker, lower-left CEO identity, Assistant identity, message avatar
- **Current Problem:** generic glyph presets do not satisfy Curis cartoon presets; uploaded-image preview is unspecified.
- **Required Correction:** show Upload + Curis Cartoon Preset + Fallback in Create Company and one shared downstream rendering pattern.
- **Acceptance Check:** CEO name/avatar choice visibly persists into Shell and Conversation; missing avatar falls back cleanly; future Employee identity can reuse the same pattern.

### P1.4 — Replace ordinary/internal UI language

- **Affected Frames:** all 13
- **Affected Components:** helper text, statuses, section titles, annotations, CTA labels
- **Current Problem:** mixed English and internal audit/runtime terms reduce trust and ordinary-user clarity.
- **Required Correction:** apply the replacement list in section 7; remove implementation gaps from the UI; preserve only genuine brand/technical terms.
- **Acceptance Check:** a Chinese ordinary user can understand every primary state/action without knowing Product/Runtime terminology.

### P1.5 — Correct the Create Business structured surface

- **Affected Frames:** `1:1515`, `1:1727`
- **Affected Components:** start-business CTA, Assistant message, Understanding surface, action row
- **Current Problem:** duplicate entry actions and a field-grid/wizard feel.
- **Required Correction:** make the Assistant conversation the continuous entry; present a natural understanding summary; ask only necessary questions; remove internal lifecycle note.
- **Acceptance Check:** CEO intent naturally produces one structured object inside conversation, not a standalone form or premature proposal confirmation.

### P1.6 — Reach Calm Density without changing Direction D

- **Affected Frames:** `1:2`, `1:188`, `1:424`, `1:624`, `1:821`, `1:1292`, `1:1515`, `1:1727`
- **Affected Components:** feature strip, empty-state surfaces, Assistant header, readiness/gap surface, Composer spacing
- **Current Problem:** pages alternate between large empty canvas and stacked cards; company feeling depends on copy.
- **Required Correction:** use typography, proximity, alignment, divider, and restrained tonal fields before cards; retain one primary focus and useful supporting context.
- **Acceptance Check:** screens no longer read as landing page, dashboard card wall, or generic chat widget; they remain Direction D and preserve accepted product structure.

### P1.7 — Normalize typography and Shell geometry

- **Affected Frames:** all Shell-based Frames; repeated headers/navigation throughout
- **Affected Components:** Navigation, Header, body, metadata, shell height
- **Current Problem:** mixed font families/weights and 6 px navigation overflow.
- **Required Correction:** choose one Chinese-first implementation family/stack within the still-open Font Family choice; normalize repeated styles; make Shell/Nav/bottom identity fit declared Frame height.
- **Acceptance Check:** screenshots export at the declared Frame dimensions; repeated labels have the same family, size, weight, and line height.

### P1.8 — Add bounded interaction evidence

- **Affected Frames:** all 13, especially `1:2 → 1:83 → 1:188 → 1:1052/1:1990 → 1:1292/1:2428 → 1:1515 → 1:1727`
- **Affected Components:** primary CTA, back links, model configuration entry, selector, start-business entry
- **Current Problem:** no prototype reactions exist, so route continuity and CTA competition cannot be verified from Figma.
- **Required Correction:** after visual corrections, connect only the core lifecycle and variation transitions or annotate destinations precisely.
- **Acceptance Check:** each primary action has one unambiguous destination; Back returns to the correct parent state; no dead-end core path remains.

## 17. Final baseline decision

### Can Codex safely perform incremental edits?

**Yes, after explicit edit authorization.** The file is readable, structurally intact, fully layer-editable, and has named structures sufficient for precise node-level revisions. There is no P0 import/editability blocker.

Safety conditions for later edits:

1. Treat each repeated Shell/Composer/Selector as an independent copy until components exist.
2. Use an affected-Frame matrix for every shared visual/copy change.
3. Verify target-file write permission at the first authorized bounded edit.
4. Preserve the 13-Frame baseline before revision; do not silently restructure or delete states.
5. Resolve P1 issues before calling the candidate `UI ACCEPTED` or `IMPLEMENTATION READY`.

### Product UI readiness

- **Working baseline for incremental Figma revision:** READY
- **UI accepted:** NOT YET
- **Implementation ready:** NOT YET
- **New visual direction required:** NO
- **Product Contract change required:** only the unresolved `Auto` model-selection behavior; all other listed work is correction/implementation truth, not product redesign

**FIGMA BASELINE READY FOR INCREMENTAL EDIT**

## 18. POST-CORRECTION REVIEW — 2026-08-28

### 18.1 Correction boundary and evidence

- **Figma file:** `2Fh7DgPPfLgdbvNtnzPnk9`
- **Top-level Frames:** 13 before and after; no Frame was added or deleted.
- **Write permission:** VERIFIED by a reversible rename-and-restore check on `1:2` before the correction.
- **Editability:** retained. The Page still contains **0 Components / 0 Instances**; the approved work therefore used an explicit 13-Frame revision matrix rather than a component refactor.
- **Typography editability:** the imported `WenQuanYi Zen Hei` font could not be loaded by the Figma editing connector. All user-visible Text layers were moved to the available Chinese UI family `Chiron Hei HK`, preserving regular / medium / bold relationships. This is a working-baseline implementation choice, not a frozen typography token decision.
- **Visual verification:** every top-level Frame was re-rendered after the final correction at **1440 × 900**. All 13 exports matched the declared Frame size; top-level clipping is enabled and the prior Shell overflow is no longer visible.
- **Language scan:** no effectively visible ordinary UI copy matched the rejected English/internal-language set (`CEO Assistant`, `AI EXECUTION READY`, `OPEN / IMPLEMENTATION GAP`, `Keychain`, `Auto`, `Company`, `Business`, `Conversation`, `Provider`, `Credential`, or deterministic/audit copy).
- **Prototype evidence:** 17 current-run navigation reactions connect the bounded lifecycle, model configuration, selector, back, save, and first-business paths.

### 18.2 P1 closure map

| Original P1 | Result | Correction evidence |
| --- | --- | --- |
| P1.1 Empty Curis truth boundary | **FIXED** | `1:424` and `1:624` no longer expose a real CEO 助理, model-readiness state, business/employee/result preview, or company-level data. Both remain app-level browse/create-company states. |
| P1.2 Contradictory model state / fixture matrix | **FIXED** | One replaceable design-fixture matrix is used: GPT-4o = enabled/default, Claude 3.5 Sonnet = enabled, DeepSeek-V3 = available to add. Enabled conversations use GPT-4o; the expanded selector shows only enabled models. |
| P1.3 CEO / Employee identity pattern | **FIXED** | `1:83` now shows Upload + eight generated Curis avatar presets + name-initial fallback and an adjustment hint. The selected portrait is synchronized to all lower-left CEO identity consumers and the company-created identity surface. |
| P1.4 Ordinary/internal UI language | **FIXED** | All 13 Frames use Chinese ordinary-product language; genuine brand and technical terms such as OpenAI, Anthropic, DeepSeek, GPT-4o, API Key, Endpoint, Temperature, Top-P, and Top-K remain. Internal implementation-gap and lifecycle notes are not effectively visible. |
| P1.5 Create Business form drift | **FIXED** | `1:1515 → 1:1727` is conversation-led. The 2 × 2 extracted-field grid, premature proposal CTA, direction-switch CTA, and lifecycle note are removed from the visible flow. The structured surface contains a natural understanding plus two bounded confirmation questions. |
| P1.6 Calm Density / landing-card-chat drift | **FIXED FOR CURRENT GATE** | Welcome feature cards, duplicate readiness surfaces, redundant gap/status surfaces, and residual audit bars were removed. Conversation, composer, empty-state focus, and model-management surfaces remain recognizable without introducing a new visual direction. Remaining refinements are P2. |
| P1.7 Typography and Shell geometry | **FIXED** | One editable Chinese UI family is used across the Page. All 13 Frames are 1440 × 900, top-level clipping is consistent, and final screenshots contain no 6 px Shell overrun. |
| P1.8 Core transition evidence | **FIXED** | 17 prototype reactions cover Welcome → Create Company → Company Created, model setup/add/advanced/back/save, enabled conversation → selector, and Empty Company → Create Business. |

**Remaining P1:** none found in the current Figma correction scope.

### 18.3 Per-Frame post-correction result

| Frame | Result | Post-correction review |
| --- | --- | --- |
| [Welcome to Curis 1440w light](https://www.figma.com/design/2Fh7DgPPfLgdbvNtnzPnk9/Curis-V1-%E2%80%94-App-Entry---CEO-Assistant-Experience?node-id=1-2&p=f) `1:2` | **KEEP** | One product statement, one primary create-company action, and one explicit browse path; no four-card marketing strip. |
| [创建你的 AI 公司 1440w light](https://www.figma.com/design/2Fh7DgPPfLgdbvNtnzPnk9/Curis-V1-%E2%80%94-App-Entry---CEO-Assistant-Experience?node-id=1-83&p=f) `1:83` | **MINOR FIX** | Display name, company name, upload, eight Curis avatar presets, selected preview, and fallback are visible. Actual upload/crop behavior remains implementation work. |
| [公司创建成功 1440w light](https://www.figma.com/design/2Fh7DgPPfLgdbvNtnzPnk9/Curis-V1-%E2%80%94-App-Entry---CEO-Assistant-Experience?node-id=1-188&p=f) `1:188` | **KEEP** | Company identity, first CEO 助理 presence, one natural no-model explanation, and one configuration entry remain; duplicate readiness copy is removed. |
| [Empty Curis — CEO Desk 1440w light](https://www.figma.com/design/2Fh7DgPPfLgdbvNtnzPnk9/Curis-V1-%E2%80%94-App-Entry---CEO-Assistant-Experience?node-id=1-424&p=f) `1:424` | **KEEP** | Correct Company=0 truth boundary and a single create-company action. |
| [Empty Curis — Business Space 1440w light](https://www.figma.com/design/2Fh7DgPPfLgdbvNtnzPnk9/Curis-V1-%E2%80%94-App-Entry---CEO-Assistant-Experience?node-id=1-624&p=f) `1:624` | **KEEP** | Browse-only business-space state; no model-readiness or company-level execution promise. |
| [CEO Assistant — No Model 1440w light](https://www.figma.com/design/2Fh7DgPPfLgdbvNtnzPnk9/Curis-V1-%E2%80%94-App-Entry---CEO-Assistant-Experience?node-id=1-821&p=f) `1:821` | **KEEP** | One Assistant identity, one natural explanation, a disabled composer, and one model-configuration entry. |
| [AI 能力设置 — 模型管理 1440w light](https://www.figma.com/design/2Fh7DgPPfLgdbvNtnzPnk9/Curis-V1-%E2%80%94-App-Entry---CEO-Assistant-Experience?node-id=1-1052&p=f) `1:1052` | **MINOR FIX** | Unified fixture matrix and clean management hierarchy. Provider/model truth still requires runtime data during implementation. |
| [CEO Assistant — 模型已启用 1440w light](https://www.figma.com/design/2Fh7DgPPfLgdbvNtnzPnk9/Curis-V1-%E2%80%94-App-Entry---CEO-Assistant-Experience?node-id=1-1292&p=f) `1:1292` | **KEEP** | Readiness is expressed by one quiet cue, current selector, and unlocked composer; stale no-model wording and the duplicate readiness card are removed. |
| [Empty Company — CEO Desk 1440w light](https://www.figma.com/design/2Fh7DgPPfLgdbvNtnzPnk9/Curis-V1-%E2%80%94-App-Entry---CEO-Assistant-Experience?node-id=1-1515&p=f) `1:1515` | **KEEP** | Company exists, AI is enabled, Business=0, and the CEO 助理 conversation is the single primary entry. |
| [Create Business — Conversational Entry 1440w light](https://www.figma.com/design/2Fh7DgPPfLgdbvNtnzPnk9/Curis-V1-%E2%80%94-App-Entry---CEO-Assistant-Experience?node-id=1-1727&p=f) `1:1727` | **KEEP** | Natural conversation plus a compact structured understanding and two confirmation questions; no wizard/CRM grid. |
| [AI 能力设置 — 添加模型 1440w light](https://www.figma.com/design/2Fh7DgPPfLgdbvNtnzPnk9/Curis-V1-%E2%80%94-App-Entry---CEO-Assistant-Experience?node-id=1-1990&p=f) `1:1990` | **MINOR FIX** | Novice-first provider → model → credential → verify → enable hierarchy; no Keychain or implementation-gap copy. Actual credential storage and provider discovery remain implementation truth. |
| [AI 能力设置 — 高级参数 1440w light](https://www.figma.com/design/2Fh7DgPPfLgdbvNtnzPnk9/Curis-V1-%E2%80%94-App-Entry---CEO-Assistant-Experience?node-id=1-2211&p=f) `1:2211` | **MINOR FIX** | Technical terms are retained and user-facing implementation/audit notes removed. Provider-specific ranges remain runtime-driven. |
| [CEO Assistant — 切换模型 1440w light](https://www.figma.com/design/2Fh7DgPPfLgdbvNtnzPnk9/Curis-V1-%E2%80%94-App-Entry---CEO-Assistant-Experience?node-id=1-2428&p=f) `1:2428` | **KEEP** | GPT-4o and Claude 3.5 Sonnet are the only enabled selector options; Auto and the unavailable DeepSeek option are removed; Manage Models remains reachable. |

### 18.4 Remaining P2 / implementation-facing items

1. **No shared components:** Navigation, Composer, Selector, Button, and identity structures remain independent copies by explicit task constraint. Continue using an affected-Frame matrix until a separately authorized componentization pass.
2. **Avatar interaction detail:** upload, crop/position adjustment, preset selection behavior, persistence, and error handling are represented but not interaction-prototyped.
3. **Runtime-driven model data:** provider catalogs, actual available models, connection health, credential storage, parameter support/ranges, and restart persistence remain implementation truth; the Figma names are replaceable fixtures.
4. **Micro-polish:** optical icon alignment, exact composer elevation, and minor tonal/radius normalization can be checked during implementation visual QA. They do not reopen Direction D or the corrected lifecycle.
5. **Accessibility and keyboard behavior:** focus order, keyboard model switching, error messaging, and screen-reader naming require implementation validation.

### 18.5 Post-correction decision

- **Figma working baseline:** READY
- **P0:** none
- **P1 in authorized Figma scope:** none remaining
- **Product structure / IA:** unchanged
- **Frozen Direction D:** preserved
- **UI ACCEPTED CANDIDATE:** **YES — ready for CEO / ChatGPT review**
- **IMPLEMENTATION READY:** **NOT CLAIMED**; runtime truth, accessibility, interaction behavior, and visual QA remain separate gates

**FIGMA APP ENTRY INCREMENTAL CORRECTION COMPLETE — STOP FOR CEO / CHATGPT REVIEW**
