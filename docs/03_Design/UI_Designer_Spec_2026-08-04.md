# UI 设计师 · 视觉定稿规范（2026-08-04）

> 接收指令：`docs/03_Design/UI_Designer_Handoff_2026-08-04.md`
> 角色：UI Designer（视觉定稿 / 重审）
> 适用范围：第一版 Desktop 新增表面（P0-1~5 + P1-6~7），**不在 `curis-ui-prototype/` 原型内**，由前端按本规范接入。
> 令牌体系：冻结系统 `_system/tokens.css`（`--ui-*` / `terra-*` 同一语义）。**禁止引入任何页面私有 hex 或新调色板**，所有颜色一律走令牌，以同时适配暗色（Frozen 默认）与亮色主题。
> 术语：沿用冻结中文映射 —— 投入产出 / 工作指标 / AI 员工 / 运行现场 / 搭建方案 / 工作空间；**effect_class 中文 = 只读 / 检索 / 写入 / 执行**。
> 无障碍：正文 4.5:1、大字号 3:1（WCAG 2.1 AA）；语义色仅用于小字标签/图标/指示器（令牌注释已限定），文本一律用满色令牌（已全站验证 0 对比度失败）。

---

## 0. 通用组件基线（所有 P0/P1 表面共用）

| 令牌 | 取值（暗色默认 / 亮色） | 用途 |
|---|---|---|
| 卡片底 | `--ui-surface` | 所有卡片/面板背景 |
| 卡片次级底 | `--ui-surface-2` | 气泡、输入框、嵌套块 |
| 描边 | `--ui-line` | 卡片/分隔线/输入框边框 |
| 正文 | `--ui-text` | 标题、主要文字 |
| 次要文字 | `--ui-text-2` | 标签、元信息、占位 |
| 主操作 | `--ui-action-primary-bg` / `--ui-action-primary-fg` | 主按钮（暗色=绿底深字，亮色=深底白字） |
| 品牌/激活 | `--ui-accent` | 当前步、焦点、品牌信号 |
| 语义 | `--ui-success` / `--ui-warning` / `--ui-danger` | 仅小字标签/图标/指示点 |
| 圆角 | `--ui-radius` (12px) / `--ui-radius-sm` (8px) | 卡片 / 胶囊·输入框 |
| 阴影 | `--ui-shadow` | 卡片轻投影 |
| 字阶 | `--ui-fs-1` 12 / `-2` 13 / `-3` 14 / `-4` 16 / `-5` 20 / `-6` 24 / `-7` 28 | 唯一真源，禁止档外字号 |
| 等宽 | `--ui-mono` | token 数、延迟、ID 等机器字段 |

**卡片规范（统一）**：`bg:var(--ui-surface)`，`border:1px solid var(--ui-line)`，`border-radius:var(--ui-radius)`，`padding:16px`，块间距 `--ui-fs-3`(14)→ 网格 `gap:12px`。任何表面（经营日卡 / 能力卡 / 轨迹卡 / 向导卡）均套用此基线，保证跨页密度一致。

**图标基线**：线性 SVG，`viewBox="0 0 24 24"`，`stroke="currentColor"`，`stroke-width="1.5"`，`stroke-linecap/linejoin="round"`，`fill="none"`；导航/标签用 16px，卡片头部用 18–20px。颜色随 `currentColor` 自动跟随令牌与主题。

---

## P0-1 · effect_class 副作用标签（胶囊组件）

**风险分级着色**（颜色 = 风险等级，标签文字 = 具体类，颜色仅 4 选 3 档）：

| 类 | 中文 | 风险 | 文本色 | 描边 | 底纹 | 图标(16) |
|---|---|---|---|---|---|---|
| `read` | 只读 | 无变更 | `--ui-success` | `1px solid rgba(63,207,134,.35)` | `rgba(63,207,134,.10)` | 眼睛 |
| `retrieve` | 检索 | 无变更 | `--ui-success` | `1px solid rgba(63,207,134,.35)` | `rgba(63,207,134,.10)` | 放大镜 |
| `write` | 写入 | 变更数据 | `--ui-warning` | `1px solid rgba(216,154,58,.35)` | `rgba(216,154,58,.10)` | 铅笔 |
| `exec` | 执行 | 运行代码/动作 | `--ui-danger` | `1px solid rgba(229,115,115,.35)` | `rgba(229,115,115,.10)` | 闪电 |

> 理由：只读/检索同属"非变更"，共享绿色系，靠图标+中文区分；写入(变更)琥珀、执行(副作用)红，符合"风险越高越醒目"。仅用冻结语义色，无新色。

**组件规格**：`display:inline-flex; align-items:center; gap:4px; padding:2px 8px; border-radius:999px; font-size:var(--ui-fs-1); font-weight:500; line-height:1.4; white-space:nowrap;` 文本显示中文（只读/检索/写入/执行），英文 `effect_class` 仅作 `title` 属性 tooltip。

**图标 SVG**：
- 只读（眼睛）：`<svg viewBox="0 0 24 24" ...><path d="M2 12s3.5-6 10-6 10 6 10 6-3.5 6-10 6-10-6-10-6z"/><circle cx="12" cy="12" r="3"/></svg>`
- 检索（放大镜）：`<svg viewBox="0 0 24 24" ...><circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/></svg>`
- 写入（铅笔）：`<svg viewBox="0 0 24 24" ...><path d="M12 20h9"/><path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4z"/></svg>`
- 执行（闪电）：`<svg viewBox="0 0 24 24" ...><path d="M13 2L3 14h7l-1 8 10-12h-7z"/></svg>`

**展示位置**：
1. 能力中心卡片（P1-6）：标题行右侧一枚胶囊。
2. 向导蓝图确认页（P0-4）：岗位名旁的"授权"胶囊组，可并列多枚（如 `授权：只读 · 检索`），用 `gap:4px` 横排。

---

## P0-2 · 经营日卡片（CEO Office「今日经营概览」）

**层级**：CEO Office 主页**顶部第一个区块**，置顶；宽度跟随主内容区（最大 1200px 容器）。

**结构**（自上而下）：
1. **Header**：左 `今日经营概览`（`--ui-fs-5`, `--ui-text`, 600）；右 `周期 day:2026-08-04`（`--ui-fs-1`, `--ui-text-2`）。
2. **brief 摘要**：`--ui-fs-3`, `--ui-text-2`，最多 3 行，超出省略。
3. **pulse 指标格**（5 项，CSS Grid `repeat(5,1fr)`；≤768px 降为 `repeat(2,1fr)`）：每项 = 标签(`--ui-fs-1`, `--ui-text-2`) + 大数字(`--ui-fs-7`, `--ui-text`, 600) + 单位(`--ui-fs-2`, `--ui-text-2`) + 趋势箭头（↑ `--ui-success` / ↓ `--ui-danger` / → `--ui-text-2`，`--ui-fs-2`）。
4. **matters 分级 Tag 行**：最多展示 3 条，超出折叠"查看全部 N 条"。每条 = 圆点 + 文案(`--ui-fs-2`, `--ui-text`)：
   - `risk` → `--ui-danger`（红点）
   - `attention` → `--ui-warning`（琥珀点）
   - `info` → `--ui-success`（绿点）

**视觉**：套用通用卡片基线；指标格内部用 `gap:16px`，格与格之间不画线（靠间距分隔），保持呼吸感。

---

## P0-3 · 运行轨迹只读视图（runtime-trace）

**容器**：纵向列表，按 `run_id` **分组**；组头 = `run_id` + `task_ref` + 时间范围(`--ui-fs-1`, `--ui-text-2`)。

**事件行规格**（`min-height:48px`；`padding:8px 12px`；行间 `1px solid var(--ui-line)`）：
- 左：事件类型 Tag（小胶囊，复用 P0-1 胶囊样式但**单色实心点**区分）：`model_call`→`--ui-accent`，`tool_call`→`--ui-warning`，`workflow`→`--ui-accent`，`task`→`--ui-text-2`（中性）。
- 中：能力名（`--ui-fs-3`, `--ui-text`）+ 下方 meta 行（`--ui-fs-1`, `--ui-text-2`, `--ui-mono`）：`tok ${tokens_in}/${tokens_out} · ${cache_hit ? '缓存✓' : '—'} · ${latency_ms}ms`。
- 右：时间（`--ui-fs-1`, `--ui-text-2`，右对齐）。

**时间线形态**：采用**紧凑分行列表 + 类型色点**（非长竖向轴线）——高密度下分行更可读；若未来单 run 深度回看，可升级为左轴时间线（本规范不强制）。

**分页**：`limit=100`，列表底部"加载更多"按钮（`--ui-action-primary-bg` 次一级或 ghost）。

**token/缓存字段呈现**：`cache_hit` 用 `✓`(`--ui-success`) / `—`(`--ui-text-2`)；token 数用 `--ui-mono`；延迟 `ms` 单位随数字。

---

## P0-4 · 业务引导向导页（/guide）

**步骤条**（顶部，4 步：选模板 → 对话 → 蓝图确认 → 成功）：
- 当前步：`--ui-accent` 文字 + 实心圆点 + 连接线高亮；已完成步：打勾(`--ui-success`)；未达步：`--ui-text-2` 灰。
- 字号 `--ui-fs-2`；步骤条下方 `1px solid var(--ui-line)` 分隔。

**对话态 vs 表单态一致性**：同一卡片外框（通用卡片基线）不变；切换仅换内部：
- 对话态：`textarea`（`--ui-surface-2` 底, `1px solid var(--ui-line)`, `border-radius:var(--ui-radius-sm)`, `font-size:var(--ui-fs-3)`）+ 发送按钮（主操作）+ AI 追问气泡（气泡 `bg:var(--ui-surface-2)`, `border-radius:var(--ui-radius-sm)`, 左对齐）。
- 确认态：表单字段，每字段 `label`(`--ui-fs-2`, `--ui-text-2`) + `input/select`（`--ui-surface-2` 底 + `--ui-line` 边框）+ 岗位"授权"胶囊组（P0-1 组件）。

**manual_fallback 兜底态**：当 `mode=manual_fallback`，卡片顶部显示**提示横幅**（`bg:rgba(216,154,58,.10)`, `1px solid rgba(216,154,58,.35)`, 左 `⚠`(`--ui-warning`)），文案"已切换为手动填写，请补全以下信息"，下方渲染完整表单；视觉上明确"兜底"，不伪装成 AI 对话。

**按钮层级**：主操作（下一步 / 确认创建）→ `--ui-action-primary-bg` 实心；次操作（上一步 / 取消）→ ghost 文字按钮（`--ui-text-2`，hover `--ui-text`）。

---

## P0-5 · onboarding 双选择（保存公司后）

**主次建议（明确结论）**：验收口径核心路径为「创建公司 → 引导创建业务」，故**反转主次**——
- **主按钮（实心绿）**：`创建业务工作台（引导）→`（`--ui-action-primary-bg` + `--ui-action-primary-fg`），承载核心转化。
- **次按钮（描边）**：`进入总裁办公室`（`background:transparent; border:1px solid var(--ui-line); color:var(--ui-text-2)`，hover `border:var(--ui-accent)`）。

**理由**：引导创建业务是用户首次在浏览器跑通真实闭环的关键一步，应在视觉上最突出；"进入总裁办公室"作为可跳过的高级入口降级为次。

**布局**：两按钮纵向或横向并排（≥768px 横排、移动端纵排），间距 `--ui-fs-3`(14)；主按钮在前（左/上）。

---

## P1-6 · 能力中心卡片（与重审报告对齐）

- 网格卡片，统一套用**通用卡片基线**；每张卡：类型图标 + `label`(`--ui-fs-4`, `--ui-text`) + 来源标签（`official`/`tenant_private`，小字 `--ui-fs-1`, `--ui-text-2`）+ **effect_class 胶囊**（P0-1 组件，标题右）+ 启用开关（标准 switch，开=`--ui-accent`）。
- 密度与经营日卡一致（padding 16 / gap 12），避免重审报告中指出的"分组/密度不一致"。
- 来源标签不引入新色：official 用 `--ui-text-2`，tenant_private 用 `--ui-accent` 小字区分。

---

## P1-7 · 员工能力绑定错误态（TerraBoundary 规范）

- **错误横幅**（TerraBoundary 风格）：左 `3px` 实色条 `--ui-danger` + 左 `⚠` 图标(`--ui-danger`) + 标题(`--ui-fs-3`, `--ui-text`, 600) + 友好中文正文 + 可折叠详情。
- **文案规范**（中文、不抛技术栈）：
  - 授权拒绝：`该岗位未开放「执行」类能力授权，无法绑定。请在岗位模板中开放对应授权后重试。`
  - 能力不存在：`所选能力不可用，请刷新能力列表后重试。`
- 横幅底 `bg:rgba(229,115,115,.10)`，`border:1px solid rgba(229,115,115,.35)`，`border-radius:var(--ui-radius-sm)`，`padding:12px 14px`。
- 不阻断整页，仅在该绑定抽屉/表单内联展示；详情（technical）默认折叠，避免吓到非技术用户。

---

## 前端接入验收清单（checklist）

- [ ] 所有颜色 100% 走 `--ui-*` / `terra-*` 令牌，全仓 grep 无新增 `#hex`/`rgb()` 字面量（除令牌定义处）。
- [ ] 7 个表面均套用通用卡片基线（同 padding/radius/描边），跨页密度一致。
- [ ] effect_class 胶囊：4 类中文标签 + 风险分级着色 + 16px 图标，位于能力卡与向导授权处。
- [ ] 经营日卡置顶、matters 三级点色正确、pulse 趋势箭头方向正确。
- [ ] 运行轨迹按 run_id 分组、meta 行含 tok/缓存/延迟、分页"加载更多"。
- [ ] 向导步骤条 4 步、对话/表单同框、manual_fallback 横幅明确。
- [ ] onboarding 主次反转（创建业务=实心主、进入总裁办公室=描边次）。
- [ ] 错误态用 TerraBoundary 横幅 + 中文友好文案，技术细节折叠。
- [ ] 暗色/亮色双主题下令牌自动翻转，无硬编码反白；对比度维持 WCAG AA（正文 4.5:1）。
- [ ] 字号全部落在 `--ui-fs-1`~`--ui-fs-7` 七档，无档外字号。

---

**UI Designer 定稿日期**：2026-08-04 ｜ **状态**：定稿，可交付前端接入 ｜ **QA**：令牌/对比度/字号三项红线已写入验收清单。
