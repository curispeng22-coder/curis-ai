# CURIS DEPARTMENT + BUSINESS WORK SURFACE — UX EXPLORATION · ROUND 5 (Inline Workflow Simplification)

> Visual Validation Only · **DO NOT** Reopen Product Model
> Single-file interactive HTML exploration · Wireframe-grade
> STOP FOR CEO VISUAL REVIEW

---

## 0. R4 → R5 diff narrative (concise)

R5 是 **简化** 轮,不是新增/重设计。同一份文件 in-place 编辑,**目标**:把 R4 的全屏 Workflow Canvas 收回业务页工作空间卡片内联展示,使「工作流」与「文案 + 节奏 + 团队」同一页可读可改,而不是「点 [编辑] 全屏接管」。

### R4 (2554 行 / 143 KB) — R4 baseline state
- Business 5 `.biz-section` (intro/leader/info/operating/workspace/team)
- 工作流 = 一行 `wf-summary-inline` 紧凑摘要 + `[编辑]` chip
- 点 `[编辑]` → 全屏 `.canvas-overlay` (position:fixed inset:0, 24px dot grid) + 4-toolbar armed-mode + spatial canvas-pane 140×78 + SVG edges + 退回弧 + 360px Inspector (岗位 / 负责人 / 职责 / 输入 / 输出 / 流转 / 删除)
- Hub 「工作空间」组描述:`Workspace · 业务内独立经营的执行空间 · 入口嵌在业务页内`

### R5 (2905 行 / 154 KB) — current
- 业务页骨架保留 R4(5 `.biz-section`, silent notebook divider, 不套 Card 不套 Part)
- **删除** `.canvas-overlay` / `.canvas-stage` / `.canvas-pane` / `.canvas-node` / `.canvas-edge` / `.canvas-back-line` / `.canvas-toolbar` / `.canvas-inspector` / `canvas-edge-line` 等 全部 canvas-* CSS 与 JS(grep 0 hit)
- **删除** `WORKFLOW_DB` 数据形状 → 替换为 `WORKFLOW_NODES`(每 workspace 一份节点 + 内联 input/output/returnTo/returnLabel)
- **删除** `renderCanvas()` / `drawEdges()` / `openCanvas()` / `closeCanvas()` / `openInspector()` / `closeInspector()` / `openEmpPop()` 等 8 个函数
- **新增**:Inline 编辑架构 — 每个工作空间卡片新增 `.wf-edit-pane` 容器(默认 hidden)
  - Click `[编辑]` → 原地 `removeAttribute('hidden')`,渲染 `wf-track`(节点 120×56 button + 文本 `→`)
  - 节点 `draggable=true` → 拖动重排 → drop 时 `reconcileWfArrows` + `syncWfFromDom` 同步 `WORKFLOW_NODES`
  - Track 下方 `wf-return-rail`(dashed 行,用文本 `─ ─ ─ ─ ─ ─ ⤺` 提示退回方向 + label)
  - Foot 含 `[+ 添加岗位]` → `wf-add-pop`(选已有岗位 dropdown + 新建岗位 input)+ `[完成]` primary
- **新增** Node Drawer — 复用 `.rules-drawer` 视觉 DNA(同 width 460px, 同 slide-in-right, 同 ESC cascade 优先级):字段 岗位 / 负责人[更换]→ popover EMPLOYEE_POOL / 职责 / 输入 / 输出 / 流转(下一步 + 退回)/ 删除岗位
- **删除** `[data-canvas-open]` 5 个 chip 全部替换为 `[data-wf-edit="bizN-x"]`
- Hub 描述改为「业务内独立经营的执行空间 · 可从 Business Space 直接进入」(§11 fix)

行数 2554 → 2905(+351),但 UX 路径:点 `[编辑]` **不出当前页**,Editor 感受「与工作描述同段」而非「独立画布」。CEO 三大验收项 §14 A/B/C 全部 PASS。

---

## §14 三大 CEO 验收 (验证)

### A. Workflow 默认状态是 simple ✓

打开 State 4 / 5 任一业务,工作流一行紧凑文本:
```
工作流
[ 选题 ] → [ 调研 ] → [ 文案 ] → [ 视觉 ] → [ 发布 ]                    编辑
```
跟一段工作描述无差异。**0** 个全屏 overlay · **0** 个 dot grid · **0** 个 SVG 边。

### B. Click [编辑] 在业务页原地展开 Add / Delete / Drag-sort ✓

`[编辑]` → 原地滑出 `.wf-edit-pane`(紧贴 `.biz-row` 之后,page root 不变):
```
工作流                                                          完成
[ 选题 ] → [ 调研 ] → [ 文案 ] → [ 视觉 ] → [ 发布 ]
─ ─ ─ ─ ─ ─ ⤺ 文案   (退回 → 文案)

新增岗位会自动追加到末尾，然后用拖动调整位置         [ + 添加岗位 ]
```

- `draggable=true` + `dragstart / dragover / drop` → 拖动重排,放下后 left/right 3px 指示边消失,`WORKFLOW_NODES[scope].nodes` 顺序同步,return row 重渲染
- `[+ 添加岗位]` → `wf-add-pop`(固定在按钮旁):「选择已有岗位」下拉(从当前 ws 节点名选)+「或新建岗位名称」文本输入 → 确认后追加到末尾
- 点 node → Node Drawer 弹出后,Drawer foot 的 `[删除岗位]` 一键删除(data 中 splice + 同步把其他节点上指向该 id 的 returnTo 清掉,防止悬空)
- `[完成]` → 收起 wf-edit-pane 回到 view 行,数据保留在内存

### C. Click node → Node Drawer 编辑岗位 / 职责 / Employee / Input / Output / Return ✓

```
┌────────────────────────────────────────┐
│ 文案                          [+]  [×]  │
├────────────────────────────────────────┤
│ 岗位名称                                │
│ [ 文案              ]                   │
│                                        │
│ 负责人                                  │
│ ● 林月                  [更换]         │
│                                        │
│ 职责                                    │
│ [ 撰写 ... ]                           │
│                                        │
│ 输入                                    │
│ [ 素材包 ]                             │
│                                        │
│ 输出                                    │
│ [ 初稿笔记 ]                           │
│                                        │
│ 流转                                    │
│   下一步: [ 视觉 ▾ ]                   │
│   退回:   [ 文案 ▾ ]                   │
├────────────────────────────────────────┤
│ [删除岗位]              [取消]  [保存] │
└────────────────────────────────────────┘
```

- `[更换]` → 弹层 `nd-emp-pop`(absolute, position 计算自 `[更换]` 按钮位置,viewport 内吸附 240px 宽):
  - 列出 `EMPLOYEE_POOL[bizKey]` 当前员工(陈真/林月/苏晴/何川/周璐 ... for biz4),点击即绑
  - 顶部「未绑定」选项可解绑
  - 底部「新建员工 · 输入姓名 + 回车」可即时扩展员工池
- 流转 `下一步 / 退回` 两个 dropdown,均可保存到 `WORKFLOW_NODES`,`returnRow` 自动重渲染
- `[保存]` → 写回数据 → 关闭 drawer → `renderWfTrack(scope)` 重绘轨道
- `[取消]` / `[×]` / overlay click / ESC 都会关闭(Node Drawer 是 drawer,不是 modal;主页面可以滚动)

---

## §11 Hub text fix (verified)

R4 → R5 唯一 Hub 修订:**不增不删**,只换文案。

**Old** (R4):
```html
<div class="gh"><span class="gt">工作空间</span><span class="gs">Workspace · 业务内独立经营的执行空间 · 入口嵌在业务页内</span></div>
```

**New** (R5):
```html
<div class="gh"><span class="gt">工作空间</span><span class="gs">业务内独立经营的执行空间 · 可从 Business Space 直接进入</span></div>
```

Hub 其他 11 个 cards + 2 条 inline-hint 一概不动。Spec 不让扩 Hub。

---

## 验收 A/B/C 之外 — 结构不变性 checklist

| Surface | R4 → R5 | Evidence |
|---|---|---|
| State 2 · 内容增长部(Domain Preset) | 结构不变 | 6 个 section title / 4 个 summary-block / Leader row / 4-team row / Goal card 全保留;mock-badge 改 R5 文案 |
| State 3 · 研发部(R&D Domain Preset) | 结构不变 | 同上 6 section + 4 team + Operating Surface 6 行 |
| State 6 · 海外业务部(Generic Dept) | 结构不变 | grid cols-section 卡片(Identity / Focus / Businesses / Team / Result-Risk) |
| State 7 · 宠物寄养(Generic Business 刚创建) | 结构不变 | 5 section,无 workflow pane(workspace 空),bubble-suggest 链路保留([data-bubble-confirm] → counter 写入) |
| Rules Drawer | CSS + DOM + JS + 数据 0 改动 | `data-rules-drawer` / `RULES_DB` / `openRules` / `closeRules` / ESC 优先级 |
| Department Emp-Workstation(rows + Conversation + Composer) | 结构不变 | 周宁 / 林涛 / 宋远 / 周璐 各 .emp-row 一致 |
| 业务页 quiet notebook(5 `.biz-section` + thin divider) | 结构不变 | State 4 5 section,State 5 5 section,State 7 5 section |
| Capability 原语(`Model / Skill / MCP / Tool / Knowledge / Permission`) | 不在 user-visible body | sweep count 同 R4 |
| Execution status(已完成 / 进行中 / 待开始) | 不在 user-visible body | sweep count 同 R4 |

---

## 3 个 P2 (filed for v6 polish · NOT blocking)

R5 是 wireframe-grade,**3 个 P2** 与 R4 不同(但都明确边界,不阻塞 CEO 视觉 review)。

### P2-1 · Inline add popover 无 keyboard-only focus trap

**现状**:`[+ 添加岗位]` → `wf-add-pop` 弹层;「选择已有岗位」`<select>` +「或新建岗位名称」`<input>`,Enter = confirm,Esc 关闭。WCAG 2.4.3 (focus order) 满足,但 Tab trap 在 select ↔ input ↔ [取消] ↔ [添加] 之间手测 OK。
**Production**:把 `wf-add-pop` 包成 `dialog` 角色 + Esc trap + 在弹层内循环 Tab,加 `aria-live=polite` 告知「已添加岗位」。
**为何未做**:wireframe 不阻塞 CEO review。

### P2-2 · 拖拽持久化

**现状**:`renderWfTrack` / `drop` 监听器 在内存中更新 `WORKFLOW_NODES[scope].nodes`;刷新页面后会回到 R5 demo 初始状态。
**Production**:每次 drop 后 POST `/api/workspaces/:id/workflow/reorder`,fetch 失败显示 undo;`+ 添加岗位` 同样要 POST `/api/workspaces/:id/workflow/nodes`(同步拼装 input/output/returnLabel)。
**为何未做**:R5 wireframe 仅 mock data,持久化是 v6 production 工作。

### P2-3 · Return row 数量上限

**现状**:`wf-return-rail` 渲染 `forEach(node => if (node.returnTo)…)`;多个 return 时 row 堆叠。R5 demo 只展示 single return。
**Production**:多个 return 时折成 graph editor(spec §15 n8n-style)或允许一个 Node 多 return(均非本轮范围)。R5 仍然保留「Return 一目了然」的 spec 要求,因为 single return case 视觉清晰。
**为何未做**:demonstrative 场景只有 single return,R5 wireframe 显示充分。

---

## R5 视觉差异 vs R4 — CEO 视角

| View | R4 | R5 |
|---|---|---|
| Hub 「工作空间」组描述 | `Workspace · 业务内独立经营的执行空间 · 入口嵌在业务页内` | `业务内独立经营的执行空间 · 可从 Business Space 直接进入` |
| 业务页 工作流 行(view) | `[ 选题 ] → [ 调研 ] → [ 文案 ] → [ 视觉 ] → [ 发布 ]                    编辑` | same (no change) |
| 业务页 工作流 行(edit) | full-screen `.canvas-overlay` + dot grid + spatial nodes + SVG edges + 360px Inspector | inline `wf-edit-pane` 原地展开 + draggable nodes + dashed return row + 460px Node Drawer |
| Node 详情(画布内/抽屉) | Inspector fields: 岗位 / 负责人 / 职责 / 输入 / 输出 / 流转(只读) | Node Drawer fields: 岗位 / 负责人 / 职责 / 输入 / 输出 / 流转(下一步 + 退回可改) / [删除岗位] |
| 添加节点 | toolbar `＋ 添加岗位` armed-mode | inline foot `+ 添加岗位` popover (select / new-input 双轨) |
| 退回可视化 | 红色 curved SVG path + label | dashed 文本行 ─ ─ ─ ─ ─ ─ ⤺ + 退回 label |
| Rules Drawer / Department pages / Generic business | unchanged | unchanged |

---

## 本轮交付

| File | Lines | Size | 用途 |
|------|------|------|------|
| `CURIS_DEPARTMENT_BUSINESS_WORK_SURFACE_UX_EXPLORATION.html` | 2905 | 154 KB | 单文件 7-state 可交互 wireframe (R5: Inline Workflow + Node Drawer) |
| `01-VISUAL-VALIDATION.md` | 167 | — | R5 视觉验证(§14 A/B/C 三大验收 + discipline sweep + 0 P0/P1 + 3 P2) |
| `02-DELIVERY-SUMMARY.md` | (this file) | — | R4→R5 diff narrative(简化轮,非重设计)+ §14 接受陈述 + 3 v6 polish |

---

## 真正需要 CEO 决策的 — vs R4 持平

R2 / R3 记录的 2 个 Decision 仍 pending(Workspace 是否独立为一级视角 / 林涛一人多 Leadership 数据模型)。

**R5 没有引入**新 Decision 项,因为 wireframe 不重构产品 schema,只简化 UX 路径。

**P2 polish 不需要 CEO 现场拍**,v6 production 工作前置已记:
- 拖拽 + 加/删 → 接 DB endpoint
- Add popover → focus trap + aria-live
- Multi-return → graph editor(超出 wireframe 范围)

---

**停止态**: CURIS DEPARTMENT + BUSINESS WORK SURFACE UX EXPLORATION — **ROUND 5 (INLINE WORKFLOW + NODE DRAWER)** — COMPLETE — **STOP FOR CEO VISUAL REVIEW**
