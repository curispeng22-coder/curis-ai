# Curis Design System Delta — R&D Workspace

Status: Review  
Scope: R&D Workspace · Default Office — Visual Baseline v1  
Authority: `Curis_Product_UI_Blueprint.html`, `Curis_RD_Workspace_Design_Brief.md`, `Curis_Design_System.md`, and the Figma Visual Baseline v1 screenshots provided by the CEO. TraeCode is used only as a visual-language reference.

## Delta Rules

The following patterns are introduced or adjusted by the R&D Workspace Visual Baseline v1 and are **not currently defined** in the Frozen `Curis_Design_System.md`. They are recorded here for review before any write-back to the official Design System.

### 1. R&D Workspace Shell Grid

- **Pattern**: Two-zone application shell by default.
- **Structure**:
  - `220px` Primary Navigation (fixed)
  - Fluid Main Workspace (`minmax(0, 1fr)`)
- **Rationale**: Matches both the UI Blueprint base canvas and the Figma baseline. Context Sidebar and Utility Surface are on-demand and not visible in Default state.
- **Tokens**: `--ui-bg`, `--ui-surface`, `--ui-line`, `--ui-text`, `--ui-text-2`, `--ui-text-3`.

### 2. Primary Navigation — UI Blueprint Six Areas

- **Pattern**: Left nav strictly follows the six primary areas defined in `Curis_Product_UI_Blueprint.html`.
- **Order**:
  1. 首页 / CEO 工作台
  2. 业务空间
  3. 组织中心
  4. 人才市场
  5. 资料库
  6. 会议
- **Sub-navigation**: When inside a Workspace, the active Workspace appears as a sub-item under `业务空间`, not as a top-level area.
- **Rationale**: Preserves canonical navigation order; Workspaces are instances under `业务空间`, not a seventh primary area.

### 3. Employee Workstation Component

- **Pattern**: A bordered card with rounded corners (`--radius-8`) on a surface background, matching the Figma baseline.
- **Anatomy**:
  - Header (always visible, clickable):
    - `32px` role-colored avatar
    - Employee name + role stacked
    - Status tags + context tags (branch, model) on the right
    - Collapse/expand chevron
  - Body (visible only when expanded):
    - Natural Agent Conversation
    - Compact Composer anchored to bottom
- **States**:
  - `working` — expanded in Default view; status tag uses brand/green with pulsing dot
  - `waiting` — collapsed; neutral tag
  - `needs_ceo` — collapsed but attention-bearing; warning tag + danger tag
  - `completed` — collapsed; success tag (not shown in Baseline v1)
- **Correction**: Permanent professional tool buttons on the employee header (e.g., `查看差异`, `源代码`) are removed. Tools are reached from lightweight references inside the Conversation, not from the employee title.

### 4. Conversation / Diff Separation

- **Pattern**: Conversation carries natural explanation and lightweight Result references only.
- **Rule**: A full inline Diff / code block is not embedded in the Conversation. Instead, a compact reference row appears:
  - Example: `api/users.ts · 34-93 · 查看差异`
- **Interaction**: Clicking the reference opens the right-hand Utility Surface (Diff view). The Utility Surface is not rendered in the Default state.
- **Rationale**: Keeps the Conversation readable while preserving one-click access to professional evidence.

### 5. Compact Composer

- **Pattern**: Minimal input surface attached to the active Workstation Conversation.
- **Anatomy**:
  - Multi-line textarea with placeholder
  - One compact bar below:
    - Left: `+添加`, `执行`, model selector (e.g., `Q3`)
    - Right: permission/mode selector (e.g., `默认审批`), Send
- **Rationale**: Matches the Figma baseline and the UI Blueprint rule: only controls that change the current run contract are visible.

### 6. Workspace Header & Status Bar

- **Pattern**:
  - Title: `研发·默认办公室`
  - Meta: `3名AI员工 · <responsibility> · <attention count>`
  - Status bar below title: icon + short current-state sentence
- **Rationale**: Gives immediate orientation (what workspace, what responsibility, who is active, what needs attention) without adding a Dashboard.

### 7. Context Sidebar & Utility Surface (On-Demand)

- **Pattern**: Both are closed in Default state.
- **Context Sidebar** opens from a topbar control (not shown in Default Baseline v1).
- **Utility Surface** opens from the lightweight Diff reference inside the Conversation.
- **Rationale**: Prevents Default screen from becoming an IDE dashboard.

## What Was NOT Added

The following remain intentionally excluded:

- Dashboard / permanent metric widgets
- Button walls
- Employee top tabs or contact lists
- Employees placed in the Context Sidebar
- DAG as user view
- Session Manager
- Inline full Diff / code block inside Conversation
- Legacy assistant elements (`curis-companion`, `assistant-mini`)
- Full Codex / Cursor / VS Code clone

## Open Questions for Review

1. Should Workstation expansion be mutually exclusive or free-form?
2. Should the Needs CEO workstation be expanded by default, or remain collapsed with a top-level attention item?
3. Should the Context Sidebar open as an overlay or push the Main Workspace?
4. Are the role color mappings acceptable for color-blind accessibility, or do we need additional non-color indicators?
5. Should the Diff reference show file count + line count, or remain a single-file reference?

## Relationship to Official Design System

- This Delta does **not** modify `Curis_Design_System.md`.
- Upon Design Review approval, these rules may be merged into a new section of the official Design System (e.g., "Workspace Components" or "Agent Surfaces").
- This Baseline v1 Delta supersedes previous v1/v2 Delta drafts in the same design round.
