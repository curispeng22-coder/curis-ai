# Curis V1 — visual fidelity closure

Status: Review
Authority Class: REVIEW / IMPLEMENTATION ISSUE
Disposition: IN PROGRESS — NOT ACCEPTED
Task ID: CURIS-V1-VISUAL-FIDELITY-CLOSURE-20261008
Owner: Curis Delivery / current main development session
Authorization: CEO 2026-10-08 approved visual-first delivery, then explicitly instructed continuing the established workflow. No commit/push.

## Goal and first slice

### CEO authorization — native titlebar / Utility tabs

2026-10-08 CEO approved removing the visible CEO Office title, merging pane controls with macOS window controls, and multiple Utility tabs with a real add picker. Latest refinement selects Company search beside the Curis brand below the titlebar. Exact additional allowed files: `desktop/tauri.conf.json` (window title/style/traffic-light positioning and window-drag permission only), `frontend/components/writing/WritingWorkspace.js` (existing Utility read sections as stable tab descriptors only), `frontend/components/v1/V1Sidebar.js` (brand action slot only). Existing shell JS/CSS/tests allowed hunks extend to scoped UI tab state, picker, tab mount/close and native header spacing. No backend/schema/object creation/provider/Authority edit. Pre-change config SHA `ec2f3ea29d5b2f564a12699ab8196ad54a8cf3f9645d4a40dff2ebd964045da2`; Writing SHA `6fb6650f4d52d9ae4fd48f860980474c19e8ac00919d6a8ae873869c9e2a7fcc`; Shell hashes are preceding return. Same task/artifact/generated directories; protected DB baseline unchanged. Tabs hold scoped UI references, not copied canonical objects. Legacy callers retain their existing single-pane content; no fake Result/Employee tabs. Acceptance: fresh isolated native topbar, native controls/drag, real plus picker, two tabs, independent close, collapse preserving tabs, and scope isolation checks. Full-object integration outside this initial framework must not be falsely certified.

### CEO follow-up — header alignment and fold motion

CEO confirmed the four-pane shape and requested aligned collapse controls and smoother switching. Extend the existing owned shell hunks only: header inset, fixed grid-track placement/transition, resize gesture protection, and focused assertions. No page composition or business function changes. Pre-change SHA: JS `59ce7fccfec92e659f13a016b4eae1b6922becd610f8c1841b32ec0ec0ef029c`; CSS `7705fa2500d92349882bb69b4df6421160176cfc83215ce47e98e81299717424`; test `a600a54707108e3cd9e66ba0d98299a45a6d1003256f1549664245db7a55c4d1`. Acceptance: same button centerline, interruptible short transition, reduced-motion alternative, pointer resize without lag or text selection, and fresh isolated native verification. This does not promote full-page acceptance.

Return: alignment and 200ms fold transition implemented; fresh native fold/recovery and resize verified; all three buttons measured centerY 32.5px. Build `-ixPlYwBE1i60qep7zxOQ`; 11 focused checks PASS. Protected DB fingerprints unchanged. Evidence appended to FOUR_PANE_NATIVE_RETURN.md, screenshot NATIVE_ALIGNED_FOLD_CONTROLS.jpg. Motion hand-feel awaiting CEO review; no measured FPS claim or full-product promotion.

Actual packaged desktop must match the accepted design before new functional integration. First slice is shared Navigation / optional object directory / Main / optional detail, recent conversations, user center and pane headers. Preserve existing canonical handlers. Do not deliver an empty shell or treat selector samples as visual acceptance.

## Inputs

- AGENTS → Current Entrypoint → Pointer Current Required; applicable Frozen Shell and UI Blueprint.
- artifacts/tasks/CURIS-V1-APP-VISUAL-INTERACTION-COMPLETION-20261005/design-delivery/FINAL_UI_HANDOFF.md (Oct5 accepted visual baseline), SCREEN_ROUTE_REGISTRY.json, SOURCE_SEAL.json.
- Sealed P002 src/App.jsx, styles.css, pane-layout.jsx; registered Render images. Product authority governs semantics; accepted interactive source governs pane placement where renders show historical global headers.
- Oct8 IMPLEMENTATION_VISUAL_AUDIT_20261008.md and FULL-PRODUCT-TEST HANDOFF_FOR_NEXT_CODEX.md are evidence, not new authority.

## Exact Allowed Files / owned hunks — slice 1

2026-10-08 CEO confirms four-pane frame; authorizes three shared interaction corrections: omit visible directory header title across consumers while retaining accessible names/toggle; plus directly creates a new UI-only tab with in-tab content selection; maximize expands the existing active tab in the layout, never a modal over the whole app. Owned files only WorkspacePaneShell.js / module.css / d0Shell.test.mjs plus this Issue and existing evidence return. No Writing/runtime/schema/data changes. Pre-change hashes: JS `da79f7c119001de456a069d22e9f90b86b871337b552267f9527032d7d8f3348`, CSS `05018d78291b2f30169bf58df610351e7709304b91d15f1bcefc35cb4ee63ae1`, test `6ee71370076e8ec8a5d6e7a94f356c4c399f7492d02caddcc8df60fd0418bb83`. Same external root/generated dirs/protected DB fingerprints. Acceptance: native title absent, consecutive plus clicks create separate blank tabs, close/collapse retain siblings, inline expand preserves navigation and existing content/state, restore returns original pane layout. Output Review / REVIEW_REQUIRED pending native evidence.

- This issue.
- frontend/components/workspace/WorkspacePaneShell.module.css: shared typography, surfaces, nav spacing, pane headers; preserve search/overlay/maximize behavior.
- frontend/components/workspace/WorkspacePaneShell.js: accessible skip/landmark and header branding only; no business API, scope or execution changes.
- frontend/components/v1/V1Sidebar.js: brand/primary-navigation presentation and user menu identity, keeping all routes and handlers.
- frontend/components/v1/ConversationQuickAccess.js: presentation classes only; no ordering, persistence, polling or dismissal changes.
- frontend/app/globals.css: font-stack/header-height presentation tokens only. Do not replace palette, theme semantics or unrelated CSS.
- frontend/tests/d0Shell.test.mjs: scoped assertions for owned presentation/landmarks.

Allowed generated directories: frontend/.next; desktop/.runtime; desktop/target; artifacts/tasks/CURIS-V1-APP-VISUAL-INTERACTION-COMPLETION-20261005/visual-correction-20261008/ (evidence and retained candidate package only). No other source edits without an explicit amendment before writing. Do not alter accepted prototype or handoff.

## Pre-change hashes

| File | SHA-256 |
|---|---|
| WorkspacePaneShell.js | 6a3d9e670de7d94eb8f01778a793b9f04c12583c6fdf328dd03530dea40e28d8 |
| WorkspacePaneShell.module.css | 40997b65f78f564b19cb4d8bcf75b5e76add1da2718f107e00d097c61015983f |
| V1Sidebar.js | 70a0c520fc37d2e635aba46be4bdb64eace3d7363c1ea2c00e19344ff91c535e |
| ConversationQuickAccess.js | 03f8d472a67192b8b1c38feb9a7d20f9bc652141f73f6310bfc37c762d2918d3 |
| globals.css | 738a98ea8dd483f169536cc20061816112ae0477f8e2191f6bde2d1e56f42d8e |
| d0Shell.test.mjs | f07a2d1aecd25bd5a065baeebc772485f96a367c4f425221335cd1b35c5197de |

Mixed-source state: 151 modified tracked / 835 untracked at initial inventory; no staged changes observed. Owned files already contain preserved work. Patch only reviewed hunks; do not whole-file restore.

## Protected DB read-only baseline

Immutable read-only integrity_check = ok for all three. These are current fingerprints, not proof that previous agents never mutated them. Prior repo DB incident remains separate and unresolved.

| Absolute path | Size | mtime epoch | SHA-256 |
|---|---:|---:|---|
| /Users/yy/Documents/Curis AI Workspace/data/curis.sqlite | 1425408 | 1791400965 | 62dd8986339b257fb58d8585f9bae2c6720167c9eeec717c2542203601acc237 |
| /Users/yy/Documents/Curis AI Workspace/backend/data/curis.sqlite | 1421312 | 1791277187 | 26312302efed7f8d63ef041e8b5b4e700e6e52d64dd413fece2108285125fdc2 |
| /Users/yy/Library/Application Support/com.curis.desktop/data/curis.sqlite | 1552384 | 1791451481 | 3d8164d8def917d46f06ddf25b2113ac1526f78c224ad902aae2547254adbb8e |

## Acceptance / stop gates

- Focused shell/sidebar assertions, owned ESLint and production build; no cloud call or backend tests importing a protected DB.
- Explicit CURIS_DESKTOP_DATA_ROOT pointing to newly created external isolated root; verify protected paths cannot be selected. Do not use the handoff's default `open` or `killall` commands.
- Existing default app occupies 8002/8080/3010. User must normally quit before isolated launch; never kill default instance. Confirm all ports released first.
- 1440×900 actual native app: nav, recent list, user menu, selected links and representative real content; all pane combinations, resizers, maximize/recover; no permanent empty panel.
- No generic “上下文” label in user-facing auxiliary headers; actual object/directory/detail labels.
- Four-pane = optional columns, not every route forced into four visible columns. Sealed P002 desktop nav is 190px; old render dimensions alone cannot silently override the latest interactive baseline.
- Screenshots plus package manifest/hash/build ID. Browser checks supplement, never replace native evidence. CEO visual gate precedes further page batches and new functional integration.
- Stop on protected DB unexpected mutation, unowned conflicting edits, permission blocker or real authority conflict. Do not rollback preserved work. No add/commit/push/reset/clean/stash.

## Output / next gate

Outputs retained in scoped correction directory, REVIEW_REQUIRED. No acceptance promotion yet. Slice 1 visual verification → CEO confirmation → page composition batches → functional integration → product tests / final fresh package. Source changes alone are not desktop acceptance.

## Slice 1 return — 2026-10-08

Owned presentation patches implemented in the six listed frontend files. Preserved existing scope keys, geometry, pane handlers, conversation ordering/polling/dismissal, API calls and seven routes. No backend or business function edit. Sealed design inputs: 32/32 hashes match. Focused shell tests 6/6 and conversation compatibility 3/3 PASS; owned ESLint PASS; production frontend and fresh Workspace/Gateway/Guardian/Recovery builds PASS; fresh Tauri app bundle PASS; scoped git diff check PASS. These are build/compatibility evidence, not visual acceptance.

Candidate: `desktop/target/release/bundle/macos/Curis UI Review.app`; separate temporary productName override passed to CLI, no tauri.conf.json edit. Existing Curis.app binary remains c7d85eff1e8ed88ecec19f2fb91071caefa87276ac5ba93a05488d72bb92754d. Native review NOT RUN: default instance still holds 8002/8080/3010; user requested to quit normally. Do not launch or kill it automatically. No new functional batch until visual gate.

Evidence return: `artifacts/tasks/CURIS-V1-APP-VISUAL-INTERACTION-COMPLETION-20261005/visual-correction-20261008/SLICE_1_RETURN.md`, REVIEW_REQUIRED. All three protected DB baseline fingerprints rechecked identical and integrity ok after builds. Historical mutation incident is not thereby closed.

## Native follow-up after normal exit

CEO normal exit confirmed; listeners released before isolated launch. Fresh candidate now runs against `/private/tmp/curis-ui-frame-review.GR7BgF` with explicit data root and all DB aliases. Normal App Entry and formal test Company creation used. Native navigation collapse/recovery and user menu verified. Organization shows 2 departments / 7 employees / 0 Business. CEO Desk and Business compositions remain old and are NOT visually accepted. Employee Detail → full Conversation reports identity cannot read; cause unverified, functional follow-up outside this slice. Auxiliary panes / resize / maximize still pending, not inferred from tests. Native evidence and exact limitations recorded in SLICE_1_RETURN.md and NATIVE_BUSINESS_FRAME.png. Three protected DB fingerprints remain byte-identical after inspection; integrity ok. No commit/push or acceptance promotion.

## CEO frame clarification — visible panel boundaries

Return: FOUR_PANE_NATIVE_RETURN.md in the approved correction artifact directory. Native four panes visibly open on an actual locally-created published Writing Workspace; directory and Utility fold/recover, pointer resize, maximize/recover verified. Fresh package resource BUILD_ID QkZxi5bGnisBfNeSNmknX. Tests 10/10, ESLint, standalone/sidecars/Tauri build and scoped diff check PASS. Three protected DB fingerprints unchanged. FRAME REVIEW_REQUIRED, NOT full-page visual acceptance. Existing maximize icon and drag text selection recorded as bounded polish follow-ups; no functionality batch started.

Geometry owned hunk amendment: subtract the frame's 16px Main horizontal inset and 8px Utility outer inset from available room before existing overlay decision; preserve 600px actual Main minimum, width ranges and narrow-state policy. No new geometry system.

## Topbar and Utility tab native return

Latest bounded return: directory visible header removed; plus directly creates a UI-only tab; maximize expands existing tab inline, not a modal; directory/Main/Utility zero-gutter contiguous surfaces with thin draggable boundaries. Native light/dark, plus/select/close/fold/recover and inline expand/Escape restore verified. Pointer directory 210→230→210 and Utility 340→360→340 passed. Focused tests 11/11, lint, runtime build/fresh Tauri bundle and scoped diff check PASS. Final protected DB fingerprints unchanged, integrity ok. Evidence in FOUR_PANE_NATIVE_RETURN.md latest section and three NATIVE_CONTIGUOUS / INLINE_TAB_EXPANDED final screenshots. Review / REVIEW_REQUIRED; no full-product acceptance or next functionality batch. This latest instruction supersedes historical inset/picker/modal presentation below.

CEO follow-up: contiguous directory/Main/Utility surfaces in both themes, no card gutters or interior rounding; 1px boundaries with existing pointer/keyboard splitters resize proportions. Owned CSS frame margins/borders/radii and existing geometry inset subtraction/test assertions extended accordingly. Do not change themes or business content. Previous visible frame separation is superseded only in surface treatment, not four-pane identity or fold behavior.

Latest CEO placement implemented: search beside Curis brand; native hidden title / Overlay; same header track; shared scope-bound UI tab holder and real plus picker. Writing's existing responsibility/version sections supply two descriptors, not fabricated objects. Native open/select/individual close/duplicate-open/collapse-and-recover PASS in fresh explicit external-root package, BUILD_ID `IQQv5ZHFstM7Lt6rw_1gO`, binary SHA `8a9c375b3cdf29d1f7072bd00f328a9d85e4651c95214cbe081fb2979907224d`. Current shell assertions 9/9, lint/build/diff PASS. Three protected DB fingerprints unchanged, integrity ok. Evidence: FOUR_PANE_NATIVE_RETURN.md and NATIVE_TITLEBAR_UTILITY_TABS.jpg in allowed artifact directory. Native traffic-light pixel alignment obscured by OS sharing badge; window drag displacement not independently evidenced. Full object-tab integration / full Writing visual acceptance remains next gate after CEO frame review. Review / REVIEW_REQUIRED, no acceptance promotion, no commit/push.

Authorization: CEO supplied native three-pane reference and accepted making the four-pane structure visually legible before page content. Same Task and allowed source files; extend owned WorkspacePaneShell.js hunks ONLY to panel-control icons/titles and directory header close button, invoking existing handlers. No new state, content, runtime, routes or forced empty pane. WorkspacePaneShell.module.css owned frame/background/border/margin and header clipping hunks; d0Shell.test.mjs corresponding assertions. Reference indicates structural separation, not authorization to copy its dark palette. Pre-change SHA: JS 91964977e85c2f3d0e65e2fb467f5a00123e6787cf802f52b0b3d9a799595be9; CSS 33e7f626c2ae28b6002ea398e27890d8dacb1859e9e3107726164690b7db355e; test ea044a52d5f5167841025c75d678cb2cee5944abb8c593a096d58e977901551b. Acceptance requires an actual legitimate surface with both auxiliary panes, not a generic empty-company screenshot. Default remains Nav+Main.
