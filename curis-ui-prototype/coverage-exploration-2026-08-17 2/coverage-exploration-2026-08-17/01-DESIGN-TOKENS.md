# Curis Coverage Exploration — 设计令牌与视觉方向

> 性质：**派生工作文档（Working Token Reference），NOT Frozen Authority**
> 用途：供 `prototype-builder` 批量生成 `coverage-exploration-2026-08-17` 全部高保真 HTML 原型
> 真源：Frozen `_system/tokens.css` · `Curis_UI_Frozen_Spec_2026-08-04.md` · `Curis_Workspace_Shell_Contract_And_Shared_Patterns.md` · `Curis_Product_UI_Blueprint_v1.0.html`
> 视觉方向（来自用户 brief）：安静的信息密集型工作软件 · 低表面复杂度、高功能密度 · 依靠排版/留白/字重/灰度/分隔建立层级 · 克制使用 Card/Pill
>
> **本文件只引用与转译 Frozen 真源，不重新定义任何令牌、不修改任何 Authority 文件、不在 Blueprint 外新建产品系统。**

---

## 0. 文档定位与边界

| 项 | 说明 |
|----|------|
| 这是 | prototype-builder 批量出图时的统一参考，避免每页各自发明色值/字号/间距 |
| 不是 | Frozen Authority（不写回 tokens.css / Shell Contract / Blueprint / Frozen Spec） |
| 色值 | **全部**来自 `tokens.css` 的 `--ui-*` 变量，禁止页面私有值 |
| 字号 | **全部**来自 `tokens.css` 的 `--ui-fs-1…7` 七档，禁止档外字号 |
| 间距 | **全部**来自 `tokens.css` 的 `--ui-sp-1…8` 八档，禁止字面量间距 |
| 圆角 | **全部**来自 `tokens.css` 的 `--ui-r-*` 五档 |
| 修改权 | 发现 Frozen 缺口（如 `--ui-syntax-*` 未冻结、Utility 更深背景未定义）→ 记录进 §8 GAP，不擅自补令牌 |

---

## 1. 设计原则（Coverage First）

1. **优先级铁律**：`页面完整 > 功能完整 > IA 正确 > Shared 一致 > 视觉精修`。
   覆盖探索阶段，先让清单里每个页面/状态都存在且可浏览；功能可占位、IA 可后校、视觉可最后打磨。不要为单个页面卡在像素级反复重做。
2. **安静、信息密集、低表面复杂度、高功能密度（Low Surface Complexity, High Functional Density）**。
   第一眼简单；开始工作后正确能力自然出现。优先对象点击、`+`、`···`、Popover、Collapse/Expand、Hover Action、按需 Context/Utility、Focus View。
3. **层级靠排版/留白/字重/灰度/分隔，不靠颜色区分**。
   语义色（success/warning/danger）只作「小文字/图标/标签/指示线」信号，绝不铺大色块。状态区分优先用字重 + `--ui-text-2/3` 灰度 + 分隔线。
4. **克制 Card/Pill；列表行优先于卡片**。
   Employee Row、业务列表、结果列表、专家列表一律用普通列表行（plain list row），不默认套 Card。Card 仅用于确实需要视觉聚合的容器。
5. **直接复用 Frozen 令牌与 Shared Pattern，不为圆角/间距反复重做**。
   所有视觉度量一查 tokens.css 即可得，无需重新推导。Shared Pattern（Employee Row / Conversation / Composer / Result Reference / Decision Banner / Employee Detail / Utility）按 Shell Contract 原样采用。

---

## 2. 视觉方向锚定（Sensibility Anchor · 仅参考）

Curis 是自有 Frozen 系统，不替换、不混用外部 Design System。但为帮助 prototype-builder 校准「安静、克制、信息密集」的**观感**，以下学派可作风格坐标参考（来自本专家 71 套设计系统库的视觉方向分类，仅用于对齐手感，不引入其令牌）：

- **Linear / Notion 学派**：以排版、灰度、紧凑间距、低对比分隔建立层级；克制色彩与表面；功能密度高但第一眼安静。← Curis 最贴近此坐标。
- **刻意避免**：消费级高饱和（Spotify 绿/红滥用）、汽车级强对比装饰（Tesla/BMW）、电商大卡流（Shopify/Airbnb）、AI 产品霓虹强调（Claude/Mistral 的强 accent 满屏）。

> 一句话手感：**像 Linear 那样安静克制，像 Notion 那样信息密集，但用 Curis 自己的 `--ui-*` 令牌实现。**

---

## 3. 色彩策略（引用 tokens.css · 不重定义）

> 浅色为默认低风险展示；**深色是 Frozen 默认主题**。所有色值仅引用下方变量，禁止字面量。

### 3.1 用途映射

| 语义用途 | 变量 | 浅色 | 深色 | 备注 |
|---------|------|------|------|------|
| **应用画布（页面底）** | `--ui-bg` | `#f5f5f7` | `#1a1c1f` | 全局最低层背景 |
| **主内容表面** | `--ui-surface` | `#ffffff` | `#222529` | 卡片/面板/主区表面 |
| **抬升表面 / 抽屉 / Context** | `--ui-surface-2` | `#f7f8fa` | `#2b2f34` | 次级表面、Utility 容器 |
| **低对比分割线** | `--ui-line` | `#e5e7eb` | `#343940` | 所有分隔、Pane 边界、列表行线 |
| **主文字** | `--ui-text` | `#1a1c1f` | `#f3f4f6` | 标题、正文、强调 |
| **次要文字** | `--ui-text-2` | `#4b5563` | `#a7adb6` | 副标题、标签、状态说明 |
| **弱化文字** | `--ui-text-3` | `#626b76` | `#a3aab4` | 元信息、占位、空态 |
| **主操作背景** | `--ui-action-primary-bg` | `#30333a` | `#32f08c` | 视口主按钮（浅=深实心；深=品牌绿） |
| **主操作悬停** | `--ui-action-primary-hover` | `#17181a` | `#0fdc78` | hover 态 |
| **主操作文字** | `--ui-action-primary-fg` | `#ffffff` | `#0c0c0d` | 主按钮文字 |
| **激活态 / 焦点 / 品牌信号** | `--ui-accent` | `#1a1c1f` | `#32f08c` | 当前项指示线、焦点环、`active` 态 |
| **成功** | `--ui-success` | `#21895d` | `#3fcf86` | **仅**小文字/图标/标签/指示线 |
| **注意（Decision Banner）** | `--ui-warning` | `#b87922` | `#d89a3a` | **仅**小文字/图标/标签/指示线 |
| **风险 / 阻塞 / 失败** | `--ui-danger` | `#c43f3f` | `#e57373` | **仅**小文字/图标/标签/指示线 |

### 3.2 色彩纪律

- 语义三色 `--ui-success/-warning/-danger` **绝不**用作大面积填充或整块背景；它们只出现在：状态文字、图标、小标签、左侧指示线（如 Employee 状态、Needs CEO 警告条）。
- 主操作在浅色主题用深色实心、深色主题用品牌绿——**不**在浅色铺大绿块（Frozen 已定）。
- 焦点环统一 `--ui-focus-color: var(--ui-accent)`，禁止 `outline: none` 而不给替代。
- 任何「新状态色」需求先用现成语义色表达；缺真值记进 §8 GAP，不新增 `--ui-*`。

---

## 4. 字号 / 字重层级

> 7 档字号为唯一真源，下限 12px。层级主要靠**字重 + 灰度 + 留白**拉开，不靠堆字号。

### 4.1 语义 → 字号映射

| 角色 | 令牌 | 值 | 行高 | 字重（建议，非 Frozen 令牌，可直接写） |
|------|------|----|------|----------------------------------------|
| 页面标题 Page Title | `--ui-fs-6` | 24px | `--ui-lh-tight` | 600 |
| 区块标题 Section Title | `--ui-fs-5` | 20px | `--ui-lh-tight` | 600 |
| 卡片标题 / 导语 Card Title | `--ui-fs-4` | 16px | `--ui-lh` | 600 |
| 正文 Body（默认） | `--ui-fs-3` | 14px | `--ui-lh` | 400 |
| 次要正文 / 表格 / 标签 | `--ui-fs-2` | 13px | `--ui-lh` | 400（强调 500） |
| 元信息 / 说明 / 徽标 | `--ui-fs-1` | 12px | `--ui-lh` | 400（弱化用 `--ui-text-3`） |
| 大数字 / 展示位 | `--ui-fs-7` | 28px | `--ui-lh-tight` | 600/700 |

### 4.2 字重约定（非 Frozen 令牌，直接写数值）

- `400` 正文 / 元信息；`500` 次级强调（标签、状态词）；`600` 标题 / 卡片标题 / 按钮文字；`700` 仅大数字或极强调。
- 不引入 `300` 以下细体（CEO 长时间阅读界面，过细字重降低可读性）。
- 层级示例：页面标题 24/600/白 → 区块标题 20/600/白 → 卡片标题 16/600/白 → 正文 14/400/`--ui-text-2` → 元信息 12/400/`--ui-text-3`。

---

## 5. 间距节奏

> 全部来自 `--ui-sp-1…8`（4px 基数）。Pane 内部用 sp-4/5，区块之间用 sp-7/8，超过 48px 用 sp-8 叠加。

| 场景 | 令牌 | 值 | 说明 |
|------|------|----|------|
| **页面主区内边距** | `--ui-sp-6` | 24px | 桌面默认；平板 `--ui-sp-5`(20px)；小窗 `--ui-sp-4`(16px) |
| **区块之间** | `--ui-sp-7` | 32px | 一级区域/大模块纵向间隔 |
| **区块内边距** | `--ui-sp-6` | 24px | 容器内部 padding |
| **卡片内边距（默认）** | `--ui-sp-5` | 20px | Card 内部 |
| **卡片内边距（紧凑）** | `--ui-sp-4` | 16px | 密集列表/紧凑卡 |
| **表单行间距** | `--ui-sp-4` | 16px | 控件之间 |
| **列表项纵向间距 / 行内 padding** | `--ui-sp-3` | 12px | Employee Row、列表项上下 padding；行内元素间距 |
| **按钮横向内边距** | `--ui-sp-3` | 12px | 次级/普通按钮 |
| **紧凑控件内边距 / 行内元素** | `--ui-sp-2` | 8px | 图标与文字贴合 |
| **图标与文字 / 徽标内边距** | `--ui-sp-1` | 4px | 最小贴合 |
| **空态图文垂直留白** | `--ui-sp-8` | 48px | 空态上下大留白 |
| **Pane 之间（栅格列）** | `--ui-line` 分隔 | — | Pane 之间用 1px `--ui-line` 边界，不额外加 gap；Pane 内部内容 gap 用 sp-4/5 |

> 圆角节奏：`--ui-r-xs`(4) 徽标/色块/进度条 · `--ui-r-sm`(8) 按钮/输入框/下拉 · `--ui-r-md`(12) 卡片/面板 · `--ui-r-lg`(16) 抽屉/模态 · `--ui-r-pill`(999) 胶囊标签/圆形头像图标钮。

---

## 6. 组件快速规范

> 每个组件标注：用途 / 关键令牌 / 状态 / 与 Frozen 的出处。原型直接照此落地，不复盘。

### 6.1 Button（四类）

| 变体 | 背景 | 文字 | 圆角 | 高度 | 用途 |
|------|------|------|------|------|------|
| **Primary** | `--ui-action-primary-bg` | `--ui-action-primary-fg` | `--ui-r-sm` | `--ui-ctl-h-lg`(40) 主操作 / `--ui-ctl-h`(36) | 视口主操作 |
| **Secondary** | `--ui-surface-2` | `--ui-text` | `--ui-r-sm` | 32px | 次级操作 |
| **Ghost** | transparent | `--ui-text-2` | `--ui-r-sm` | 36px | 抽屉取消、弱操作 |
| **Icon** | `--ui-surface-2` | `--ui-text` | `--ui-r-sm` 或 `--ui-r-pill` | 32×32 | 工具栏、折叠箭头 |

- **状态**：default / hover（背景转 `--ui-action-primary-hover` 或 `--ui-surface-2` 提亮）/ active / focus-visible（统一焦点环）/ disabled（opacity 0.55 + `cursor: not-allowed`）。
- **铁律**：一个视口通常只保留 **0–1 个强 Primary 按钮**（L1 渐进披露）。禁止把全部能力永久横排成按钮墙。
- 出处置 `data-spec` 或依赖 class-based spec（`?dev=1` 可查）。

### 6.2 Input / Select（表单控件）

- 高度 `--ui-ctl-h`(36) 或 `--ui-ctl-h-lg`(40)；横向 padding `--ui-sp-3`，纵向 0。
- 圆角 `--ui-r-sm`；边框 `1px solid --ui-line`。
- 聚焦：边框色 `--ui-accent` + 外环 `--ui-focus-*`。
- 字号 `--ui-fs-2`(13)；`font-family: inherit`（继承 `--ui-font`）。
- 所有输入框关联 `<label>` 或 `aria-label`（Frozen WCAG）。

### 6.3 List Row（普通列表行 · 非 Card）

- **默认容器是列表行，不是 Card**。用于：Employee Row、业务列表、结果列表、专家/Skill/Connector 列表、会议列表、资料列表。
- 结构：行内 `display:flex`，纵向 padding `--ui-sp-3`；行与行之间用 `1px --ui-line` 分隔（或 gap `--ui-sp-3`）。
- 交互：hover 轻微 `--ui-surface-2` 背景；点击行或头像/姓名进入对应动作（见 Employee Row）。
- 紧凑信息用 `--ui-fs-2` + `--ui-text-2`；元信息用 `--ui-fs-1` + `--ui-text-3`。

### 6.4 Tag / Badge（标签 / 徽标）

- 圆角 `--ui-r-pill`（胶囊）或 `--ui-r-xs`（方块徽标）；字号 `--ui-fs-1`(12)。
- 中性：`background --ui-surface-2` + `color --ui-text-2`。
- 语义（克制使用）：文字/图标用 `--ui-success/-warning/-danger`，**不**铺背景大色块；可加左侧 3px 指示线或细边框。
- `mock-badge`：所有示例数据必须带「示例数据」徽标（`background --ui-surface-2` + `--ui-text-3`）。
- 避免满屏 Pill；状态优先用文字 + 灰度表达。

### 6.5 Empty State（空态）

- 文案说「尚未建立 / 还没有…」而非「没有数据」；给出明确下一步入口（如「＋ 创建业务」）。
- 视觉：中性线性图标 + 文字，**不使用**大面积彩色插画。
- 颜色：`--ui-text-2` / `--ui-text-3`；图标用 `--ui-text-3`。
- 垂直留白 `--ui-sp-8`(48)。

### 6.6 Decision Banner（Needs CEO / Decision · §3.3 + P7）

- **warning 色系**（`--ui-warning`），**非**绿色满铺；顶部橙色横幅 + 图标 + 「需要 CEO 决策」+ 描述 + 元信息（影响/风险，可折叠）。
- 三按钮：主操作（`✓ 执行`，品牌绿 `--ui-action-primary-bg`）/ 次操作（`⛔ 驳回`，Secondary）/ 第三操作（`暂缓` 或 `替代`）。
- **复杂度感知**：简单低风险 → `[按建议处理] [其他方案] [暂缓]`；高风险/不可逆 → 仅 `[查看方案] [暂缓]`，禁止 Layer 0 直接批准。
- 三层结构：Layer 0 Banner（注意力）/ Layer 1 紧凑 Decision Package（8 要素语义组合，CEO 语言）/ Layer 2 专业证据（经 Result Reference → Utility）。8 要素是**语义**非固定 8 块 UI。
- Provenance 标记：`FACT` / `POLICY` / `EVIDENCE` / `EST`（明示为员工判断）/ `UNK`（尚未验证）。禁止编造时间/成本/风险。

### 6.7 Employee Row（Shared Workstation · §3.1）

- **两行结构普通列表行（不做 Card）**：
  - 左侧 `32px` 角色色头像（**跨两行**；色仅区分，必须配合文字/图标满足色盲可达）。
  - 第二列行1：`员工名 + 岗位`（堆叠）。
  - 第二列行2：`当前职责简述`（轻量一行）。
  - 右侧：`Employee UI Status`（用户侧投影）。
  - 最右：`▸`/`▾` 展开箭头（Conversation 收起/展开）。
- **交互**：点**头像/姓名** → Utility 打开 Shared Employee Detail（六字段，无 Conversation）；**不设独立「详情」按钮**。点箭头/行其余区 → 展开/收起 Conversation-first Workstation。
- **UI Status 投影（三态，来自真实 Runtime 事实）**：`空闲` / `工作中·<实时描述>` / `阻塞·<原因>`。禁止把 已完成/待审核/已验收/待命 当 UI Status；不伪造 blocked 真值。
- 展开 Body：自然 Conversation（居中/Bounded/可拖高）+ 底部 Compact Composer。Runtime 状态 ≠ UI 展开状态；收起不暂停真实工作。

### 6.8 Conversation Message（§3.1 + Delta-X12）

- **不 Card 化**：对话表面本身不套 Card。短消息走自然消息流。
- **居中 + Bounded·Responsive**：在 Main 可用宽度内居中，有合理 min/preferred/max readable width，不写死 px。
- **用户/员工消息区分**：用轻微背景（`--ui-surface-2` 或对齐）与角色标签，不靠重卡。
- **长内容块（bounded embedded content block）**：仅当 长文本 / Tool / Terminal / Code / Diff / Structured Result 时，用有界内嵌块承载；块内可滚动；点「完整查看」或来源引用 → Utility 看全文（Utility 不受有界限制）。块尺寸/字数不 Frozen。
- **Result Reference**：`emoji + 文字 + ▸` 形式，颜色 `--ui-accent`；点击 → 右开 Utility Surface 对应模式（如 `📎 查看差异 (+34/-93) ▸`）。**对话内不放完整 Diff/数据/视频**。
- 用户可拖右下角手柄调高；展开/收起只改 UI 不改 Runtime。

### 6.9 Composer（Shared Composer Shell · §3.5）

- 锚定在活跃 Workstation Conversation 底部。
- **固定语义槽位（所有 Employee 通用）**：Input（多行）/ `+` Add（语义冻结、文案不冻结）/ 访问权限▾ / 工作模式▾ / 已选资源（chip）/ 执行选择 Model·Agent▾ / Voice（可选）/ Send。
- 桌面推荐布局：输入区在上、底部左右分组（左：+ / 权限 / 模式 / 已选；右：执行选择 / Voice / Send）；响应式/mobile 可重排，槽位不丢。
- 容器圆角 `--ui-r-md`；控件圆角 `--ui-r-sm`；Input 字号 `--ui-fs-3`。
- Provider Adaptation：Shared 固定槽位 + **显性区分 Model-backed / Agent-backed**；Provider 决定真实可选权限/模式/能否切模型/Agent 原生设置，不写死具体 Provider。

### 6.10 Utility Panel（按需右 Pane · §2.3）

- 默认收起；展开默认宽 **360px**（Resizable，建议值非固定，可拖拽+记忆）。
- 容器背景用 `--ui-surface-2`（Frozen Spec §3.7 规定）。⚠️ Shell §2.3 提到的「更深 1 级背景 `#181a1d`」**不是 Frozen 令牌**，本轮不引入该私有值，统一用 `--ui-surface-2`（见 §8 GAP）。
- Header：模式名/子标题 + 模式切换 + ↗ Maximize + T3（展开后从 Main Header 转移，不重复开合、不设独立 ✕）。
- 操作栏：底部固定（如「提交变更 / 请求协审」），由当前模式决定。
- 代码/语法高亮：`--ui-syntax-*` 子令牌 **B 阶段未冻结**；本轮 RD Utility 代码块用临时色值，仅作占位（见 §8 GAP），正文色优先 `--ui-text` / `--ui-text-2`，等宽字体 `--ui-mono`。
- 移动端（<640px）：转全屏 overlay，不并排。

---

## 7. Coverage Exploration 特别约定

1. **不要为了圆角/间距反复重做**：一律查 tokens.css 取 `--ui-r-*` / `--ui-sp-*`，直接套用。发现没有合适档位 → 记进 §8 GAP，不要擅自加档位。
2. **页面完整 > 功能完整 > IA 正确 > Shared 一致 > 视觉精修**：
   - 先保证清单（00-PAGE-STATE-INVENTORY.md）中每个页面/状态都生成且可浏览；
   - 功能可用占位/示例数据，不必接真实 Runtime；
   - IA（导航六区顺序、Pane 职责）可后续校正；
   - Shared Pattern 一致性可后统一；
   - 视觉精修放最后。
3. **Shared Pattern 直接复用**：Navigation 六区、四 Pane Shell、Employee Row、Employee UI Status、Conversation、Composer、Result Reference、Needs CEO/Decision、Employee Detail、System Activity 全部按 Frozen Shell Contract 落地，不在页面内重新解释。
4. **示例数据必须带 `.mock-badge`「示例数据」**：深色/浅色都可见；不使用示例数据声称已连接/已授权/已完成。
5. **严格遵守 Frozen 结构**：四 Pane Shell（Nav 固定列 + Main 弹性满宽；Context/Utility 默认收起）、Pane-local Header、T1/T2/T3 位置与行为契约、Global Object Search、Utility Maximize——均按 Shell Contract，不自行改。
6. **主区自成立**：Context/Utility 全关时，CEO 仍能理解业务整体状态并完成主要工作；Context 不承载关闭后导致 Main 无法理解业务的核心信息。

---

## 8. 明确禁止（HARD PROHIBITIONS）

| # | 禁止 | 原因 / 出处 |
|---|------|------------|
| 1 | ❌ 使用旧 `terra-*` 令牌 | 历史违规私有令牌，已被 Frozen `--ui-*` 取代 |
| 2 | ❌ 新增私有 accent（如 `#387bff`、`--radius-*`） | 违反 Shell §1.4 主题与令牌纪律 |
| 3 | ❌ 把 Card 当默认容器 | 列表行优先；Card 仅用于需视觉聚合处（原则 4） |
| 4 | ❌ 在 Conversation 里堆完整 Diff/数据/视频 | 用 Result Reference → Utility（§3.4 / Delta-X12） |
| 5 | ❌ 修改任何 Frozen Authority 文件 | tokens.css / Shell Contract / UI Blueprint / Frozen Spec 一律只读 |
| 6 | ❌ 新建 Blueprint 外的产品系统 | 所有页面须能在 Product/UI Blueprint 找到依据 |
| 7 | ❌ 页面私有色值/字号/间距/圆角 | 必须引用 `--ui-*`，避免再次出现 22 字号档/18 间距档 |
| 8 | ❌ `outline: none` 不给替代焦点 | 统一 `:focus-visible` 由 tokens.css 提供 |
| 9 | ❌ Adaptive Surface 放员工列表 | Context ≠ 员工列表（Blueprint §04 / Shell §2.2） |
| 10 | ❌ 在浅色主题铺大绿块主操作 | Frozen 规定浅色主操作用深色实心 |
| 11 | ❌ 语义色（`success/warning/danger`）作大背景填充 | 仅作小文字/图标/标签/指示线信号 |
| 12 | ❌ 档外字号（<12px 或 >28px）与档外间距 | 7 档字号 + 8 档间距为唯一真源 |

### DESIGN GAP（发现后记录，不自行补令牌）

1. **`--ui-syntax-*` 子令牌未冻结**：RD Utility 代码高亮无正式令牌，本轮用临时色值占位，等 B 阶段定稿。
2. **Utility 更深专注背景未定义**：Shell §2.3 提 `#181a1d` 但非 Frozen 令牌；本轮统一用 `--ui-surface-2`，不引入私有值。
3. **Navigation 子项渲染（如「小红书运营办公室」）**：Shell §6 Open Question #7 未冻结；本轮按示例呈现，不固化规则。
4. **Mobile <640px Overlay 交互**：产品未实例化；按 Shell「转全屏 overlay」原则执行，不细化像素。
5. **Workspace Studio「当前运行版本 vs 待修改版本」视觉**：Blueprint 有语义无像素规范；本轮用轻量占位，不脑补。

---

## 9. 速查表（prototype-builder 一页抄）

```
颜色：
  画布   var(--ui-bg)            表面   var(--ui-surface)        抬升   var(--ui-surface-2)
  线     var(--ui-line)          正文   var(--ui-text)           次文   var(--ui-text-2)   弱文  var(--ui-text-3)
  主操   var(--ui-action-primary-bg/-hover/-fg)   激活/焦点 var(--ui-accent)
  语义   var(--ui-success/-warning/-danger)  ← 仅小文字/图标/标签/指示线

字号（7 档唯一真源）：
  --ui-fs-1=12  --ui-fs-2=13  --ui-fs-3=14(正文)  --ui-fs-4=16(卡标题)
  --ui-fs-5=20(区块)  --ui-fs-6=24(页面)  --ui-fs-7=28(大数字)
字重：400 正文 · 500 强调 · 600 标题/按钮

间距（8 档，4px 基数）：
  --ui-sp-1=4  --ui-sp-2=8  --ui-sp-3=12(列表行)  --ui-sp-4=16(卡紧凑/表单)
  --ui-sp-5=20(卡默认)  --ui-sp-6=24(页内边距/区块)  --ui-sp-7=32(区块间)  --ui-sp-8=48(空态/页留白)

圆角（5 档）：
  --ui-r-xs=4(徽标)  --ui-r-sm=8(按钮/输入)  --ui-r-md=12(卡/面板)  --ui-r-lg=16(抽屉/模态)  --ui-r-pill=999(胶囊/圆头像)

控件：
  --ui-ctl-h-sm=32  --ui-ctl-h=36  --ui-ctl-h-lg=40  --ui-tap-min=32(最小命中)
层级：--ui-z-base/--ui-z-sticky(100)/--ui-z-dropdown(200)/--ui-z-drawer(300)/--ui-z-modal(400)/--ui-z-toast(500)/--ui-z-devmode(9000)
动效：--ui-dur-1(120)/--ui-dur-2(200)/--ui-dur-3(320)ms · --ui-ease-standard
字体：--ui-font("Inter",system-ui,…)  --ui-mono("SF Mono",ui-monospace,…)
行高：--ui-lh-tight(1.25)  --ui-lh(1.5)  --ui-lh-loose(1.7)

铁律：0–1 个强 Primary / 列表行优先 Card / 语义色不铺大块 / 示例数据带 mock-badge / 不碰 Frozen 文件
```

---

*由设计系统专家（彩格调）依据 Frozen 真源编译 · 供 Coverage Exploration 批量出图 · 2026-08-17*
