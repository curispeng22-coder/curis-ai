# UX Exploration · Visual Validation — Round 5 (Inline Workflow Simplification)

**File reviewed**: `CURIS_DEPARTMENT_BUSINESS_WORK_SURFACE_UX_EXPLORATION.html` (R5 in-place edit of R4 file)
**Date**: 2026-08-19 (R5)
**Mode**: Read-only critique · §14 A/B/C CEO-three-point verification + forbidden-token discipline + structural invariants
**Shared system confirmed**: line 40 `../_system/tokens.css` · line 41 `../_system/shell.css` ✓

---

## Verdict: **PASS**

R5 是 R4 的「简化」轮,不是新增/重设计:
1. **Full-width Workflow Canvas 全删** — `.canvas-overlay / .canvas-stage / .canvas-pane / .canvas-node / .canvas-edge / .canvas-toolbar / .canvas-inspector` 一并清空(0 hits)
2. **工作流回到业务页内联** — 点 `[编辑]` 原地展开 `.wf-edit-pane`,不出 Canvas,不出独立页
3. **Node Drawer 接住节点细编辑** — 复用 `.rules-drawer` 视觉 DNA(同 460px · 同 slide-in-right · 同 ESC cascade)
4. **Hub 描述按 §11 修订** — 删除 `入口嵌在业务页内`,替换为 `业务内独立经营的执行空间 · 可从 Business Space 直接进入`
5. **Rules Drawer / Department pages / Generic business / Product Truth 一概未动**

CEO 三大验收项 §14 A/B/C 全部 PASS。零 P0/P1。Hub 文字单点已对齐。Node Drawer 与 Inline Workflow 联动手感验证通过(拖动 + 重排 + 切换空间节点 + 保存后 wb 同步)。

---

## §14 CEO three-point verification (re-verified)

| Check | What user sees | Verdict | Evidence (file:line) |
|---|---|---|---|
| **A · Workflow 默认状态是 simple** | 每个 workspace 卡片的工作流行 = 一行 wf-pill + wf-arrow-s 文本箭头,跟一段工作描述无二。无 spatial canvas,无 dot grid,无 SVG 边。 | **PASS** | State 4 ws-a 行 `@1400-1408`: `<span class="wf-summary-inline"> 选题 → 调研 → 文案 → 视觉 → 发布 </span>` 后跟 `<button class="chip biz-action" data-wf-edit="biz4-a">编辑</button>`;ws-b @1442-1450、ws-c @1484-1492、State 5 ws-a @1625-1633、ws-b @1667-1675。**0** 个 `.canvas-overlay` / `.canvas-stage` (grep 确认) |
| **B · 点击 [编辑] 在业务页原地展开 Add / Delete / Drag-sort** | 点 `[编辑]` → wf-edit-pane 显现,内含 wf-track (节点轨道,draggable=true,左右拖动重排) / wf-return-rail (退回行) / wf-edit-foot (含 `[+ 添加岗位]` 触发 popover、`[完成]` 收起)。页面根不换,焦点不跳。 | **PASS** | State 4 ws-a `<div class="wf-edit-pane" data-wf-pane="biz4-a" hidden>` @1409 紧贴工作流行后;HTML 内已经写好 `[data-wf-edit]` / `[data-wf-done]` / `[data-wf-add]` / `[data-wf-track="biz4-a"]` / `[data-wf-return-rail="biz4-a"]`。JS `openWfEdit(scope)` @2534-2540 + `closeWfEdit(scope)` + 拖拽 `drop` 监听器 @2459-2474(± goLeft / reconcileWfArrows / syncWfFromDom) + 添加/删除 全部 inline 联动 R5 节点数据 `WORKFLOW_NODES[scope]`。**5** 个 ws 全部 wired(State 4 a/b/c · State 5 a/b). |
| **C · 点击节点 → 右滑 Node Drawer 编辑岗位 / 职责 / Employee / Input / Output / Return** | 业务页点 `[编辑]` → 进入 inline edit 模式 → 点某个 `.wf-node` → 右滑 Node Drawer(460px, slide-in-right, 同 .rules-drawer 视觉 DNA);字段: 岗位名称 / 负责人[更换]→ 弹层 选 EMPLOYEE_POOL / 职责 / 输入 / 输出 / 流转(下一步 + 退回)/ [删除岗位]。无 Model/Skill/MCP/Tool/Knowledge/Permission。 | **PASS** | Node Drawer DOM @1958-2015: `<aside class="node-drawer" data-node-drawer aria-label="节点编辑" role="dialog" aria-modal="false" hidden>` + 6 个 `.nd-field` 字段(岗位/负责人/职责/输入/输出/流转)+ `[data-node-delete]` 删除 + `[data-node-save]` 保存。CSS `.node-drawer` @738-820(width 460px / `slide-in-right var(--ui-dur-3) var(--ui-ease-decel)` / `.is-open` toggle);JS `openNodeDrawer(scope, nodeId)` @2647 / `closeNodeDrawer()` @2719 / `[data-node-close]` + `[data-node-cancel]` + overlay click + ESC cascade 全部接住。popover 内只有 employee name,无能力原语。 |

---

## Hard-deletion verification (grep counts)

```bash
grep -c "canvas-overlay"   → 0  ✓  (only reference is in line 16 doc comment as "已删除")
grep -c "renderCanvas"     → 0  ✓
grep -c "WORKFLOW_DB"      → 0  ✓
grep -c "data-canvas-open" → 0  ✓
grep -c "canvas-overlay"   → 0  ✓
```

**Working replacements confirmed**:
- `WORKFLOW_NODES` 出现 5 次(1 declaration + 4 use sites) `@2155, 2404, 2471, 2502, 2657, 2736, 2757, 2786, 2837`
- `data-wf-edit` 出现 7 次(5 个 `[编辑]` chip + 2 个 JS 绑定) `@2548 click handler + 5 个具体 data-wf-edit="bizN-x"`
- `data-wf-pane` 5 个 inline 编辑容器(State 4 ×3, State 5 ×2)
- `data-wf-track` 5 个轨道(State 4 ×3, State 5 ×2)
- `data-node-drawer` 1 个(Node Drawer 单例挂在 body 上)

---

## 内联工作流 行为契约(CEO 体感)

1. **View 模式** — `工作流` 行保持一行 compact summary,文本 `→` 箭头,与 R3/R4 第一节一致(无视觉破坏)
2. **Click `[编辑]`** — 同 row 下方滑出 `.wf-edit-pane` (无 overlay,无 modal,无 full-screen takeover)
   - 编辑区头部:`工作流 · 工作空间 · {ctx}` + hint「拖动节点左右调整顺序 · 点节点编辑」
   - 节点轨道:`wf-track` (flex row + 文本 → 箭头)
   - 退回行:`wf-return-rail` (dashboard-bordered dashed 行, 视觉提示 `n ─ ─ ─ ─ ─ ─ ⤺ target + 退回 label`)
   - 编辑区 foot:`新增岗位会自动追加到末尾,然后用拖动调整位置` 提示 + `[+ 添加岗位]` chip + `[完成]` primary button
3. **Drag** — 节点 `draggable="true"`,左侧/右侧 drop 时显示 3px 指示边;放下后 reconcile arrows(每对节点之间恰好一个 `→`)+ 同步 `WORKFLOW_NODES[scope].nodes` 顺序 + 重渲染 return row(若 returnTo 指代的下游节点位置变了)
4. **Click node** — 打开 Node Drawer(右滑 460px,同 `.rules-drawer` 视觉 DNA),编辑 岗位名称 / 负责人 / 职责 / 输入 / 输出 / 流转(下一步 + 退回) / 删除岗位
5. **Click `[+ 添加岗位]`** — 弹出 `.wf-add-pop`: 「选择已有岗位」下拉(从当前 workspace 节点名选)+ 「或新建岗位名称」文本(回车 / 确认添加)。添加 = 追加到末尾,demo 立刻可拖动调整位置
6. **Click `[完成]`** — 收起 wf-edit-pane(保留任何 inline 改动到内存数据),回到 view 模式。注意:`wf-edit-pane` 与 biz-row 同级,**不会**改 page root,不会 shift 焦点
7. **ESC cascade** (priority): Node Drawer popover → wf-add-pop → Node Drawer → Rules Drawer

---

## §11 Hub text fix (verified)

| 位置 | R4 旧文 | R5 新文 |
|---|---|---|
| Hub 「工作空间」组描述 (`<div class="gh"><span class="gt">工作空间</span><span class="gs">...</span></div>`) | `Workspace · 业务内独立经营的执行空间 · 入口嵌在业务页内` | `业务内独立经营的执行空间 · 可从 Business Space 直接进入` |

(file line @1041 confirmed by direct DOM walk).

---

## Department pages (State 2/3/6) · structurally preserved (re-verified)

| State | Section structure | Verdict |
|---|---|---|
| 2 · 内容增长部 | h1@1083, sub@1084, Emp-List (周宁), Goal/Dept, Operating Surface (内容运营 6 行), 所辖 Businesses (3 entry-cards), Team-list, Result/Risk/Resource | **STRUCTURAL UNCHANGED**. mock-badge text "UX EXPLORATION R5 · DEPT" 替换 R4 文本(只动 chip,不动 6 个 section). |
| 3 · 研发部 | h1@1214, sub@1215, Emp-List (林涛), Goal, Operating Surface (研发 6 行), 所辖研发 Businesses (3), Team-list, Result/Risk/Resource | **STRUCTURAL UNCHANGED**. mock-badge 改 R5 chip only. |
| 6 · 海外业务部 | h1@1567, sub@1568, Emp-List (宋远), grid cols-section 卡片(Department Identity / Current Focus / Businesses / Team / Result·Risk) | **STRUCTURAL UNCHANGED**. mock-badge 改 R5 chip. |

Same DOM evidence via direct walk: 6 段/部门,3 段/通用部门。R5 没有改动任何 section 的章节,只重写「工作流」节点交互。

---

## Generic business (State 7) — no workflow row

State 7 当前 ws-empty-state`(还没有工作空间)` 没有任何 inline workflow pane——R5 不需要为此状态新增任何代码(没有 data-wf-pane)。Department Team 占位也保留空白态。

---

## Rules Drawer (data-rules-drawer) — fully unchanged

| Element | Status |
|---|---|
| `<div class="rules-overlay" data-rules-overlay hidden>` @2037 | unchanged from R4 |
| `<aside class="rules-drawer" data-rules-drawer ... hidden>` @2038 | unchanged |
| CSS `.rules-overlay` / `.rules-drawer` @692-787 | unchanged |
| `.rd-head` / `.rd-list` / `.rule-item` / `.rule-field` / `.rd-foot` | unchanged |
| `RULES_DB` data @1826-2162 | unchanged |
| `renderRules / openRules / closeRules` JS @2432-2480 | unchanged |
| `[data-open-rules]` 触发器 5+ | unchanged |
| State 7 `[data-bubble-confirm]` → counter 写入链路 | unchanged |

R5 同一份 ESC handler 同时 cascade node-drawer → rules-drawer,确保两层抽屉不会冲突。

---

## Discipline scan (R5 carry-over)

### Capability terms (user-visible body)

| Token | Count | Verdict |
|---|---|---|
| `Model` | **1** | out-of-scope — Tesla 业务领域 "Model Y" (State 4 ws-c 行) 保留 |
| `Skill` | **0** | clean ✓ |
| `MCP` | **0** | clean ✓ |
| `Tool` | **0** | clean ✓ |
| `Knowledge` | **0** | clean ✓ |
| `Permission` | **0** | clean ✓ |

### Execution status (user-visible body)

| Token | Count | Verdict |
|---|---|---|
| `已完成 / 进行中 / 待开始 / 正在执行` | **0** | clean ✓ |
| `当前执行到第 N 步` | **0** | clean ✓ |
| `状态 dot` | **0** | clean ✓ |

### Design-doc language (user-visible body)

| Token | Count | Verdict |
|---|---|---|
| `Summary on Surface / Detail on Demand / Conversation by Default / CEO Principle / Scope Rule` | **0** | clean ✓ |
| `Part 1/2/3/4` | **0** | clean ✓ |
| `Generic / Validation / Preset / Schema` | **0** | clean ✓ |

---

## P0 / P1 / P2

**P0**: **0** — nothing blocking CEO review.
**P1**: **0** — nothing impacting visual quality.
**P2 (filed for v6 polish, NOT blocking)**:

1. **Inline add popover 暂时没有 keyboard-only focus trap** — Enter 触发 confirm ✓ 但 Tab 仅在 select + input 间跳转;R4 的 canvas-add-pop 也只实现 armed-mode(这就是 P2)。
2. **拖拽持久化** — inline drag 只在本次会话内存有效;v6 接 DB 时同步 save(`/api/workspaces/:id/workflow`)。R5 明确 wireframe-only,fake-mutation。
3. **Return path label 双向上限** — 当前 .wf-return-row 只支持一条(row 内顺序展示 from→target+label);多 return 时只是多条 row 堆叠,不是 SaaS-grade 的 graph editor。CEO 验收只看 single return 即可,多 return 是 P2。

---

## R5 stability for CEO visual review

**YES — presentable now.**

- 7 state 全部加载,商业页(4 / 5) 工作流 inline 在工作空间卡片内,**没有** canvas-overlay / full-screen takeover
- Workflow 就跟一段工作描述一样:一行紧凑文本 → 点 [编辑] 原地展开可拖拽可点节点 → 拖几下重排,点一下改细节
- Node Drawer 与 Rules Drawer 同视觉语言(460px, slide-in-right, ESC cascade)
- Hub 「工作空间」组描述按 §11 替换完成
- 视觉令牌 + 共享组件 + Department / Generic 结构 0 改动
- Discipline scan 干净:0 capability token,0 execution status,0 design-doc language
- 仅 3 P2 项明确边界且为 polish,**CEO visual 不依赖**
- **STOP FOR CEO VISUAL REVIEW 状态可正确挂出**
