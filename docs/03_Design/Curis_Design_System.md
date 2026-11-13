# Curis Design System

Status: Frozen

Baseline:
main @ c0e1855f

Updated:
2026-08-10

---

## 1. Desktop First

Curis is Desktop First, not Desktop Only. Desktop is the primary acceptance
surface for the Local Owner workflow. Current responsive behavior supports
smaller viewports, but it does not represent a separately completed Web or
Mobile product.

## 2. Company OS And Workspace

Company OS primary navigation is one fixed design system:

- One primary navigation order and one utility area
- One page-header grammar, one search behavior and one Global Assistant entry
- One pattern for filters, lists, detail entry, empty/loading/error/permission
  states and decisions
- Every primary page first defines its real company place, then derives its
  information and interactions

Workspace is the only variable product surface. A Workspace reuses identity,
security, accessibility, feedback and semantic tokens, but may use a different
layout and interaction model. An R&D Workspace may resemble an IDE, a financial
Workspace a market terminal, and a content Workspace a creation studio.

Workspace must not be implemented as the same Dashboard with a new title,
color or card set.

完整 Desktop 产品还必须显式提供 CEO 能够经营公司所需的能力入口：模型、Skill、Tool、
连接器、知识、权限、成本、AI 员工配置、会议、日历和结果反馈。Local Desktop 只改变
连接方式和部署方式，不能把这些入口降级为后台预留或从 UI 中省略。

UI is derived from the reviewed Business Runtime:

- each screen identifies the Runtime stage and persisted business state it
  represents
- actions expose valid business transitions, not arbitrary button events
- the responsible Owner, required Input, expected Output and Next Stage are
  visible when needed for action
- feedback, delay, failure, rejection, retry, cancellation and archive states
  receive real product treatment
- a polished happy-path screen cannot compensate for an incomplete lifecycle

## 3. Desktop Shell

当前 Desktop Shell 是唯一交付应用壳层，
也是目标 Company OS 壳层的基础：

- Desktop at `1280px` and above: persistent `220px` navigation
- Tablet from `1024px` to `1279px`: compact navigation behavior
- Below `1024px`: `286px` navigation drawer
- One `52px` Top Bar, one Main content region and one Global Assistant layer
- Content owns vertical scrolling and must not create page-wide horizontal
  overflow

Company OS pages must reuse the shell rather than creating another Sidebar,
Top Bar or Assistant column. Workspace pages may use a Workspace-specific
inner layout, but they remain inside the same identity, Assistant and trusted
runtime boundary.

### 3.1 Navigation hierarchy

侧栏只表达 CEO 经营公司的稳定路径，不按页面临时拼装：

- 公司：CEO 工作台、经营、业务、AI 团队、能力中心、工作空间
- 经营工具：会议工作台、决策室
- 办公室：由已配置的业务空间生成的部门办公室入口
- 公司资源：成果库、知识库、财务、日历
- 设置与帮助固定在底部；不把 Assistant 作为侧栏栏目或第三列

所有页面使用同一 `220px` 侧栏、品牌标识、分组标题、左对齐导航项和
active 状态。能力中心必须作为公司级入口可达，不能隐藏在组织页或某个员工详情内。
Workspace 内部可以有自己的工作台导航，但不能复制或改写 Company OS 侧栏。
办公室入口是 Workspace 的运行入口，不是与公司级栏目平级的新产品模块。

## 4. Visual Stance: Calm Executive Workspace

Curis 的全局视觉语言从“操作台 / Dashboard”转为“安静的 CEO 工作空间”。
参考 Linear、Codex、ChatGPT 与 Apple 的共同原则：让内容、上下文和下一步行动
成为主角，界面本身保持克制。

### 4.1 基本判断

- 一个页面只讲一个主叙事；不要同时展示多个同等优先级的控制面板。
- 结构优先使用留白、字号、行高和层级；不要依赖彩色边框、阴影和卡片堆叠。
- 卡片只用于聚合一组经营信息，不用于包裹每一条消息、事实或事件。
- 会议、Assistant 和团队交接优先使用自然讨论流；结构化标签作为轻量语义标记出现。
- 一个视口只保留一个主要行动，其余行动降级为文字链接、次级按钮或上下文抽屉。
- 颜色用于表达需要 CEO 注意的状态，不用于给所有内容分类。

### 4.2 视觉禁用项

- 禁止渐变、霓虹背景、彩色大面积面板和高饱和多色卡片并列。
- 禁止把事实、观点、决议、承诺分别做成完整的彩色容器。
- 禁止用多栏边框把页面切割成后台控制台；区域之间优先使用留白和低对比细线。
- 禁止把状态数量、运行指标和按钮同时放大到同一视觉层级。
- 禁止用装饰性图表、仪表盘或颜色替代真实证据和经营语义。

### 4.3 主题模式

Curis 只定义三种主题模式：`系统`、`浅色`、`深色`。

- `系统`：跟随操作系统外观设置，是默认模式。
- `浅色`：使用浅灰画布（`#f5f5f7`）与白色卡片（`#ffffff`），保持卡片与背景之间的清晰层次；边界仍保持低对比，避免界面碎片化。
- `深色`：使用深灰色纯色表面，不使用纯黑背景。
- 三种模式只改变表面、文字、边界和对比度，不改变页面结构、组件行为或经营语义。
- 主按钮的视觉强度随主题切换：深色使用品牌绿，浅色使用深色实心按钮；按钮职责不变，避免浅色界面被绿色大面积占据。
- 用户切换主题后，状态语义保持一致；只有主动作的表面色和对应文字色切换。

### 4.4 对话空间规则

- 消息流采用头像、身份、时间、文本和轻量语义标签的连续阅读节奏。
- 事实 / 观点 / 决议 / 承诺使用小型标签或图标，不改变整条消息的背景色。
- 证据、来源、执行关联默认收起，需要时在原地展开。
- 会议右侧只保留“会议产出”摘要；确认、关联和回滚在上下文抽屉中完成。
- Assistant 以自然发言、建议和交接出现，不单独制造第二套聊天页面。

### 4.5 首次到达与公司空间

- 首次进入不是功能 tour、注册表单或空 Dashboard，而是“空白但不空旷”的 CEO 办公室。
- 空间中必须先有 Assistant 身份、欢迎语、下一步和未来公司结构的轮廓，再逐步生成 Company、Business、AI Team 和 Workspace。
- 引导每完成一个经营表达，就在空间中生成一个可见对象：公司牌匾、业务区域、AI 员工、部门办公室。
- 空状态要表达“尚未建立”，不表达“系统没有内容”；不得使用假数据填充空白。
- 有温度来自语气、身份、回应和工作状态，不来自游戏化积分、夸张动画或拟人化表演。
- 公司空间采用二维办公地图或房间层级，不要求 3D；存在感来自办公室、员工、当前工作和交接动线。

### 4.6 中文用户用语

Curis 的第一位用户是没有产品培训的一人公司 CEO。界面先说人话，再保留
内部对象名；不能把投融资、研发管理或赌博隐喻直接搬到用户面前。

| 内部或旧用语 | 用户可见用语 | 原因 |
| --- | --- | --- |
| 投资组合 / 组合 | 业务版图 | CEO 看到的是公司正在经营的业务全貌 |
| 下注 / 押注 / 赌注 | 业务方向 / 经营选择 | 表达“先做什么、希望看到什么”，不制造赌博联想 |
| ROI | 投入产出 | 直接说明投入和结果的关系 |
| KPI | 工作指标 | 说明 AI 员工是否交付了有用结果 |
| Outcome | 目标结果 | 先说要看到什么变化 |
| Workflow | 流程 | 说明可以重复使用的工作步骤 |
| 外部结果 | 真实结果 | 说明来自平台、客户或真实使用的反馈 |
| Evidence | 依据 / 记录 | 说明数字或判断从哪里来 |
| 回报 | 反馈 | 说明执行结果何时回来 |
| Blueprint / Runtime / Agent | 搭建方案 / 运行 / AI 员工 | 技术词只留在内部文档或中文后的括号中 |

按钮、状态、空状态和 Assistant 回复遵循同一套词表。英文只可作为内部
对象名、路由名或中文后的开发标识，不能单独成为用户操作词；同一个概念
在全站只能有一个中文叫法。

## 5. Typography

| Use | Family | Current Rule |
| --- | --- | --- |
| Body, headings and controls | Inter / system sans | Chinese fallback: PingFang SC / Microsoft YaHei / sans-serif |
| Key values | Same sans family, weight contrast only | Avoid decorative display fonts in operating surfaces |
| Page title | 24px / 1.15 / 650 | Use for primary page hierarchy |
| Card title | 15px / 1.3 / 600 | Use for compact business sections |
| Helper text | 11px / 1.45 / 400 | Use for secondary explanations, not primary data |

Controls inherit the current body font. Monospace is reserved for identifiers,
code and technical values.

## 6. Color

目标视觉使用中性纯色与单一主强调色；语义色只在风险、关注、成功和阻塞等需要 CEO
注意的地方出现。深色主题参考 Codex 的深灰层级，不使用纯黑：

| Token | 浅色 | 深色 | Use |
| --- | --- | --- | --- |
| `ui-bg` | `#f5f5f7` | `#1a1c1f` | Solid application canvas |
| `ui-surface` | `#ffffff` | `#222529` | Primary content surface |
| `ui-surface-2` | `#f7f8fa` | `#2b2f34` | Elevated surface / drawer |
| `ui-line` | `#e5e7eb` | `#343940` | Low-contrast divider |
| `ui-text` | `#1a1c1f` | `#f3f4f6` | Primary text |
| `ui-text-2` | `#626b76` | `#a7adb6` | Secondary text |
| `ui-text-3` | `#8a929d` | `#7e8792` | Muted text |
| `ui-action-primary-bg` | `#30333a` | `#32f08c` | Primary action background |
| `ui-action-primary-fg` | `#ffffff` | `#0c0c0d` | Primary action text / icon |
| `ui-action-primary-hover` | `#17181a` | `#0fdc78` | Primary action hover |
| `ui-accent` | `#1a1c1f` | `#32f08c` | Active AI state, focus and brand signal |
| `ui-success` | `#21895d` | `#2bb673` | Confirmed / on track |
| `ui-warning` | `#b87922` | `#d89a3a` | Needs attention |
| `ui-danger` | `#c43f3f` | `#d95757` | Risk / blocked / destructive |

Color usage limits:

- 一个页面默认只出现中性色与一个主强调色。
- 深色主题的主按钮使用 `#32f08c`，hover 使用 `#0fdc78`，文字使用 `#0c0c0d`。
- 浅色主题的主按钮使用既有深色 `#30333a`，hover 使用 `#17181a`，文字使用 `#ffffff`。
- 主按钮颜色只表达“CEO 当前要执行的主要动作”；成功状态仍使用 `ui-success` 标签或图标，不把成功色铺成按钮。
- 语义色使用小面积文字、图标、标签或指示线，不使用整块彩色卡片。
- 状态必须同时提供文字或图标，不得只依赖颜色。
- 不允许在页面内引入未经设计系统登记的颜色。

实现必须使用上述主题语义 token，不得保留旧版主题 token 或新增页面私有色板。
Status color must accompany a text label or other non-color signal.

## 7. Component Rules

- 优先复用现有可访问组件原语、`EmployeeCard` 和已验证的交互模式，
  不创建页面私有组件替代已有模式。
- `ProjectCard` is a migration input. Target Company OS uses a Workspace entry
  component; Project presentation belongs inside Workspaces that need it.
- Buttons, fields and dialogs require labels, keyboard access, visible focus
  and disabled/error states.
- Modal 和 Drawer 行为使用现有可访问对话框原语提供的原生边界。
- Cards display supplied facts only. Missing facts use the shared
  `未记录` / `未分配` vocabulary.
- Tables provide a real empty state and horizontal containment when data is
  wider than the viewport.
- Product pages must not introduce a second design token system.
- Mock business data must not be displayed as live product state.
- Company OS component reuse does not require all Workspaces to share one
  layout or one card grammar.
- Feed、Timeline 和 Discussion 优先于“每条记录一个 Card”；Card 仅用于信息聚合。
- 页面默认使用低对比边界；彩色边框只能用于极少数高风险或待确认状态。
- 主按钮每个视口最多一个；批量操作和低频操作移入上下文菜单或抽屉。
- 空状态、加载状态和错误状态也必须遵守同一套安静的层级，不通过大面积警示色制造噪音。

## 8. Assistant UI Rules

- The Assistant is a root-level Global Assistant Provider/Host, not a fixed CEO
  Office secretary rail.
- CEO Office may open the panel by default; other Workspace pages use the
  shared Top Bar or floating entry.
- The panel uses the active theme's surface, border, radius and elevation tokens.
- Current panel width is capped at `390px` on larger screens and fits inside
  the viewport on Mobile.
- Identity, Snapshot, Notifications, Query and Command appear in the same
  global runtime.
- Pages provide only safe structured page context.
- The UI must show real loading, failure and blocked states; it must not imply
  execution success before the Task chain succeeds.
- Prompt internals, credentials, raw event payloads and hidden reasoning are
  not displayed.
- Closing, minimizing and cross-page navigation must preserve the Provider
  boundary defined by the current implementation.

## 9. Visual Acceptance Gate

任何页面进入前端实现或视觉 Review 前，必须同时满足以下条件；截图好看但违反任一项，不得进入 Current：

1. **壳层一致**：桌面侧栏 `220px`、顶部栏 `52px`、Assistant 抽屉最大 `390px`；页面不得私自创建第二套侧栏、顶栏或 Assistant 栏。
2. **令牌唯一**：颜色、间距、圆角、阴影和主题只引用本文件的令牌；禁止页面私有色板、CDN 样式和旧 Terra / Palette 令牌。
3. **主题完整**：只验证系统、浅色、深色三种主题；三种主题改变表面与对比度，不改变结构和语义。深色主按钮为品牌绿，浅色主按钮为深色实心。
4. **视觉克制**：无渐变、霓虹背景、多色卡片墙、纯黑背景或装饰性图表；一个视口只有一个主要动作。
5. **中文可用**：用户可见导航、按钮、状态、空状态、错误和 Assistant 文案为简体中文；ROI / KPI / GMV 等英文只能作为内部字段或中文后的开发标识。
6. **事实可读**：状态、责任、依据、时间、新鲜度、异常和下一检查点可见；示例数据必须显式标记，不能伪装成真实结果。
7. **Assistant 边界**：Assistant 是全局第一位 AI 员工的共享入口，不是固定第三栏、侧栏卡片或第二套任务系统。
8. **运行对齐**：页面动作必须对应 Business Runtime 的合法状态转换；不得用拖拽、通用“下一步”或局部组件状态绕过 CEO 验收、授权、失败和归档。

验收证据至少包括深色 / 浅色 / 系统主题截图、桌面壳层尺寸检查、无数据 / 加载 / 失败 / 未授权状态、中文术语扫描，以及从页面动作到 Runtime 状态和审计记录的对应关系。

## References

### Current Effective Sources

- `docs/00_Context/CURRENT_STATE.md`
- `docs/07_Decisions/ADR-0033-global-assistant-runtime.md`
- `docs/07_Decisions/ADR-0035-desktop-first.md`
- `docs/07_Decisions/ADR-0040-company-os-workspace-product-reset.md`
- `docs/07_Decisions/ADR-0041-business-runtime-completion-standard.md`
- `docs/07_Decisions/ADR-0042-calm-executive-visual-language.md`
- `docs/07_Decisions/ADR-0043-theme-modes-and-neutral-palette.md`
- `docs/07_Decisions/ADR-0044-first-arrival-and-company-space.md`
- `docs/01_Product/Curis_Product_Blueprint.html`
- `frontend/app/layout.js`
- `frontend/app/globals.css`
- `frontend/tailwind.config.js`
- `frontend/components/`
- `frontend/components/assistant/GlobalAssistant.js`

### Historical References

- `issues/20260729_mvp_phase1_s1_app_shell_design_system.md`
- `reviews/20260729_mvp_phase1_s1_app_shell_design_system_review.md`
- `reviews/20260730_global_assistant_runtime_v1_review.md`

### Deprecated Sources

The following are exclusion-only historical sources and are not design inputs:

- `docs/99_Archive/design/ceo-office/_archive/`
- `frontend/design-spec/ceo-office/_samples/`
- `frontend/design-spec/curis-ui-v2/`
- `docs/prototypes/curis-full-system-high-fidelity-prototype.html`
- `diagrams/ui-homepage-variants.html`

No current rule in this document is derived from a Deprecated UI source.
