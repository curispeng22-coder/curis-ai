# DESIGN.md — Curis CEO Office (Terra 暖奶油绿设计系统)

> 设计系统架构：Terra · 暖奶油背景 + 森林绿主色 + 暖琥珀强调
> 适用范围：Curis CEO Office / Workspace 全站前端（39 页空态正本 + 13 页示例填充态 + 状态矩阵）
> 机器可读：供 Cursor / Claude Code / Google Stitch / WorkBuddy 等 AI 编程代理直接消费，做 1:1 视觉还原
> 配套文档：`UI_设计与布局规范.md`（页面 IA / 布局 / 交互）；`_samples/`（填充态视觉样板）；`UI_设计与布局规范.md §13`（状态矩阵）

---

## 1. Visual Theme & Atmosphere

**设计哲学**：以「自然、可信、沉静」为基调的 AI 公司操作系统。用暖奶油底色降低界面侵略性，森林绿承担品牌与操作主色，暖琥珀只在 CEO 决策 / 待决 / 阻塞等需要「被看见」的语义点上出现。整体克制、留白充足、信息层级靠字体（衬线标题 vs 无衬线正文）与色彩语义区分，而非靠重阴影或强对比。

**视觉基调**：温暖、有机、专业可信（warm-oragnic-professional）。不追求科技冷感或暗色炫技。

**核心视觉特征关键词**：
- 暖奶油纸感底（warm paper surface）
- 森林绿品牌锚点（forest-green anchor）
- 衬线标题 + 无衬线正文的字体二元（serif/sans duality）
- 低饱和语义色（low-saturation semantic）
- 轻投影微浮起（soft lift, low shadow）

**光影与质感倾向**：纯扁平 + 极轻投影；无任何毛玻璃、渐变、拟物。卡片靠 1px 浅边框 + 双层极淡阴影定义边界；激活态用实色填充而非发光。

---

## 2. Color Palette & Roles

所有颜色提供 HEX（与 rgba）+ CSS 变量名 + 使用场景。

### Primary Colors
| 角色 | CSS 变量 | HEX | 使用场景 |
| --- | --- | --- | --- |
| 主色 Primary | `--primary` | `#4a7c59` | 按钮、Sidebar 背景、激活态、品牌锚点 |
| 主色深 Primary Dark | `--primary-dark` | `#2f523b` | 按钮 hover、强调文字 |
| 主色浅 Primary Light | `--primary-light` | `#e8f0e8` | 标签背景、选中态背景、图标块 |
| 主色软 Primary Soft | `--primary-soft` | `#f0f6f0` | 浅色 hover、分类标签底 |

### Brand & Dark
| 角色 | CSS 变量 | HEX | 使用场景 |
| --- | --- | --- | --- |
| 品牌深（Sidebar 文字） | — | `#eef3ee` / `#dbe7dd` | Sidebar 上文字与图标（浅色） |
| 品牌反白 | — | `#ffffff` | Sidebar 激活块、Logo 底色 |

### Accent / Interactive
| 角色 | CSS 变量 | HEX | 使用场景 |
| --- | --- | --- | --- |
| 暖琥珀 Accent | `--accent` | `#705c30` | CEO 决策文字、强调、边界说明 |
| 暖琥珀浅 Accent Light | `--accent-light` | `#f5efe3` | 强调背景、边界条背景 |

### Neutral / Gray Scale
| 角色 | CSS 变量 | HEX | 使用场景 |
| --- | --- | --- | --- |
| 背景 Background | `--bg` | `#faf6f0` | 主背景（暖奶油） |
| 表面 Surface | `--surface` | `#fffefb` | 卡片表面 |
| 表面二 Surface-2 | `--surface-2` | `#f7f2ea` | 嵌套表面、分类条底 |
| 表面三 Surface-3 | `--surface-3` | `#f0ebe0` | 占位、凹陷、禁用底 |
| 文字 Text | `--txt` | `#1f241c` | 主文字（深墨绿） |
| 文字二 Text-2 | `--txt-2` | `#4a5346` | 次文字 |
| 文字三 Text-3 | `--txt-3` | `#7a8273` | 辅助文字、占位 |
| 线条 Line | `--line` | `#e8e2d8` | 分割线、卡片边框 |
| 线条二 Line-2 | `--line-2` | `#d9d2c6` | 强调分割线、输入边框 |

### Surface & Borders
| 角色 | CSS 变量 | HEX | 使用场景 |
| --- | --- | --- | --- |
| 画布外底色 | — | `#e8e2d8` | body 居中背景（仅 mockup 框架） |
| 虚线边框 | — | `#d9d2c6` | `.empty-box` 空态虚线 |

### Semantic Colors
| 语义 | CSS 变量 | HEX | 软底 | 使用场景 |
| --- | --- | --- | --- | --- |
| 成功 / 可用 | `--green` | `#15935a` | `--green-soft` `#e8f5ed` | 可用、正常、通过 |
| AI / 信息 / 青 | `--cyan` | `#3f7d6e` | `#e6f1ee` | AI 内容、信息、官方 |
| 待决 / 阻塞 / 琥珀 | `--amber` | `#a8742a` | `--amber-soft` `#f9f0e0` | 阻塞、待决策、警告 |
| 错误 / 失败 | `--red` | `#b83230` | `--red-soft` `#fae8e7` | 错误、失败、危险 |
| 自定义 / 紫 | — | `#6b4fb0` | `#efeaf8` | 自定义能力、沉淀成果 |

### Shadow Colors
| 角色 | CSS 变量 | rgba 值 |
| --- | --- | --- |
| 阴影标准 | `--shadow` | `0 1px 2px rgba(74,85,66,.04), 0 4px 12px rgba(74,85,66,.05)` |
| 阴影浮起 | `--shadow-lg` | `0 8px 28px rgba(74,85,66,.10)` |

---

## 3. Typography Rules

### Font Family
```css
--font-serif: 'Literata', 'Noto Serif SC', 'Songti SC', serif;      /* 标题、模块名、数字 */
--font-sans:  'Nunito Sans', 'Inter', 'PingFang SC', 'Microsoft YaHei', sans-serif; /* 正文与 UI */
```
> 中文环境优先回退到 `Noto Serif SC` / `PingFang SC`；不依赖 Google Fonts CDN，离线可用系统字体。

### Type Scale
| Token | 用途 | Size | Weight | Line-Height | Letter-Spacing | 字体 |
| --- | --- | --- | --- | --- | --- | --- |
| Display Hero | 页面标题 `.pt` | 24px / 1.5rem | 700 | 1.1 | -0.01em | serif |
| Title Card | 卡片标题 `.ct` | 15px / 0.94rem | 600 | 1.3 | 0 | serif |
| Module Name | 模块卡片名 `.mc-n`/`.cc-name` | 18px / 1.13rem | 700 | 1.2 | 0 | serif |
| H3 Section | 区块标题 | 15px | 600 | 1.3 | 0 | serif |
| Body | 正文 | 14px / 0.875rem | 400 | 1.6 | 0 | sans |
| Nav-1 | 一级导航 | 14px | 600 | 1.3 | 0 | sans |
| Nav-2 | 二级导航 | 13px | 500 | 1.35 | 0 | sans |
| Label/Data | 标签/数据 | 12px | 500 | 1.4 | 0 | sans |
| Caption | 辅助说明 | 11px | 400 | 1.45 | 0 | sans |
| Button | 按钮 | 12px | 700 | 1.0 | 0.01em | sans |
| Fact Number | 事实数字 `.fv` | 20px | 700 | 1.0 | 0 | serif |

### 设计哲学
标题与数字一律衬线（Literata），营造「可信文档感」；正文与控件一律无衬线（Nunito Sans），保证屏上可读性。字重只用 400/500/600/700 四档，不做极细或极粗。字距仅在 Button 与 Display Hero 上做微负距收紧，其余 0。行高正文 1.6 保证长文呼吸。

---

## 4. Component Stylings

### Buttons
```css
.btn-new { background:var(--primary); color:#fff; border:0; border-radius:var(--radius-xs); /*8px*/
  padding:9px 16px; font:700 12px/1 var(--font-sans); cursor:pointer; }
.btn-new:hover { background:var(--primary-dark); }
.btn-ghost { background:var(--surface); color:var(--txt-2); border:1px solid var(--line-2);
  border-radius:var(--radius-xs); padding:9px 14px; font:600 12px/1 var(--font-sans); cursor:pointer; }
.btn-ghost:hover { border-color:var(--primary); color:var(--primary); }
.btn-danger { background:var(--red); color:#fff; border:0; border-radius:var(--radius-xs);
  padding:9px 16px; font:700 12px/1 var(--font-sans); cursor:pointer; }
.btn-danger:hover { background:#9c2a28; }
```
变体：Primary（实心绿）/ Ghost（描边）/ Danger（实心红）。最小触摸高度 36px（padding 9×2 + 12 = 30，加边框约 36）。

### Cards
```css
.card { background:var(--surface); border:1px solid var(--line); border-radius:var(--radius); /*16px*/
  box-shadow:var(--shadow); padding:16px; }
.card:hover { box-shadow:var(--shadow-lg); }
```
模块入口卡 `.mod-card`/`.cap-card`：padding 15–16px，hover 上浮 `translateY(-2px)` + `--shadow-lg` + 边框转 `--primary-light`，过渡 150ms。

### Inputs
```css
.field input, .field select, .field textarea {
  width:100%; padding:9px 11px; border:1px solid var(--line-2); border-radius:var(--radius-xs);
  font:400 13px/1.5 var(--font-sans); background:var(--surface); color:var(--txt); outline:0; }
.field input:focus, .field select:focus, .field textarea:focus { border-color:var(--primary); }
.field label { font:600 12px/1 var(--font-sans); color:var(--txt-2); }
```
Placeholder 用 `--txt-3`。错误态边框转 `--red` + 下方 `var(--red)` 文案。

### Navigation
```css
.sidebar { width:176px; background:var(--primary); color:#eef3ee; padding:14px 10px; }
.nav-item { display:flex; gap:9px; padding:9px 8px; border-radius:var(--radius-xs);
  color:#dbe7dd; font:600 14px/1.3 var(--font-sans); }
.nav-item:hover { background:rgba(255,255,255,.10); }
.nav-item.active { background:#fff; color:var(--primary); }
.nav-sub .ns { padding:6px 8px; border-radius:var(--radius-xs); color:#cdddd2; font:500 13px/1.35 var(--font-sans); }
.nav-sub .ns.active { color:#fff; font-weight:700; }
```
一级 176px 固定；二级缩进 28px；三级缩进 48px。激活态白色实底反色。

### Badges / Tags
```css
.tag { display:inline-flex; gap:4px; font:600 11px/1 var(--font-sans); border-radius:6px; padding:2px 8px; }
.tag.green { background:var(--green-soft); color:var(--green); }
.tag.amber { background:var(--amber-soft); color:var(--amber); }
.tag.cyan  { background:#e6f1ee; color:var(--cyan); }
.tag.violet{ background:#efeaf8; color:#6b4fb0; }
.tag.grey  { background:var(--surface-3); color:var(--txt-3); }
.st-badge { font:700 10px/1 var(--font-sans); padding:3px 9px; border-radius:5px; }
.st-available { background:var(--green-soft); color:var(--green); }
.st-blocked   { background:var(--amber-soft); color:var(--amber); }
.st-official  { background:var(--primary-light); color:var(--primary); }
.st-custom    { background:#efeaf8; color:#6b4fb0; }
```

### Modals / Dialogs
```css
.modal-mask { position:fixed; inset:0; background:rgba(31,36,28,.40); display:grid; place-items:center; z-index:50; }
.modal { background:var(--surface); border:1px solid var(--line); border-radius:var(--radius);
  box-shadow:var(--shadow-lg); padding:20px; width:480px; max-width:92vw; }
.modal-hd { font:700 18px/1.2 var(--font-serif); color:var(--txt); margin-bottom:12px; }
.modal-ft { display:flex; gap:8px; justify-content:flex-end; margin-top:16px; }
```
遮罩 `rgba(31,36,28,.40)`；入场 150ms ease（opacity + translateY 4px→0）；Esc / 点遮罩关闭。

---

## 5. Layout Principles

### Spacing System（基数 4/8）
| Token | px | 用途 |
| --- | --- | --- |
| space-1 | 4 | 图标与文字间隙 |
| space-2 | 8 | 列表行间距、标签内边距 |
| space-3 | 12 | 卡片内元素间距 |
| space-4 | 16 | 卡片 padding、区块间距 |
| space-6 | 24 | 大区块间距 |
| space-8 | 32 | 页面级分段 |
| space-12 | 48 | 页面顶部留白 |

### Grid System
- 12 栏 `grid-template-columns:repeat(12,1fr)`，栏间距 `14px`。
- 跨栏工具类：`span4 / span5 / span6 / span7 / span8 / span9 / span12`。
- 固定画布（mockup 基准）：`1536 × 1024`，`.app{width:1536px;height:1024px;overflow:hidden}`，body 居中于 `#e8e2d8`。

### Container
- 主内容容器内边距 `20px`（左右），顶部安全距离 `12px`。
- Sidebar `176px` 固定，主区 `flex:1`。

### Section Spacing
- 区块纵向间距 `14px`（与栏间距一致，保持节奏统一）。

### 留白哲学
用大量暖奶油负空间换取「可信文档感」；信息密度靠卡片栅格而非紧凑堆叠。空态不收缩布局——保留完整空间构图，仅内容区显示虚线空框。

---

## 6. Depth & Elevation

### Shadow System
| Token | CSS 值 | 用途 |
| --- | --- | --- |
| shadow-xs | `0 1px 2px rgba(74,85,66,.04)` | 输入聚焦微光 |
| shadow-sm | `0 1px 2px rgba(74,85,66,.04), 0 2px 6px rgba(74,85,66,.04)` | 静态卡片 |
| shadow（标准） | `0 1px 2px rgba(74,85,66,.04), 0 4px 12px rgba(74,85,66,.05)` | 默认卡片 |
| shadow-lg（浮起） | `0 8px 28px rgba(74,85,66,.10)` | hover / 模态 |
| shadow-2xl | `0 24px 60px rgba(31,36,28,.18)` | 画布外框（mockup 框架） |

### Surface Layers
```
background  (#faf6f0)  →  surface (#fffefb)  →  elevated (card hover / modal)  →  overlay (mask rgba(31,36,28,.40))
```

### Z-index Scale
| 层级 | 值 | 用途 |
| --- | --- | --- |
| base | 0 | 内容 |
| sticky topbar | 10 | 顶栏 |
| dropdown / popover | 30 | 分类下拉、新增能力 Popover |
| modal mask | 50 | 模态遮罩 |
| toast | 60 | 顶部通知 |

### Backdrop Effects
本系统**不使用**毛玻璃 / 模糊。所有层级靠实色 + 轻阴影区分（刻意保持扁平有机质感）。

---

## 7. Do's and Don'ts

**Do's**
1. 用 `--primary` 森林绿作唯一品牌主色；激活态用白底反色，不用发光。
2. 标题/数字用衬线（Literata），正文/控件用无衬线（Nunito Sans）。
3. 空态保留完整空间构图 + `.empty-box` 虚线框 + 明确下一步，不显示 0（事实条 0 除外，它表示真实计数）。
4. 状态色严格语义化：绿=可用/正常，琥珀=阻塞/待决，红=错误，青=AI/官方，紫=自定义。
5. 所有图标用内联 SVG sprite（`<use href="#i-...">`），不依赖外部图标字体 CDN。
6. 间距恒定：卡片 gap 14px、列表行距 8px，不随密度缩放。
7. 长文本截断用 `line-clamp`，不撑高卡片（见 §13 状态矩阵）。

**Don'ts**
1. 不要切到深海军蓝 / 暗色科技风——Terra 暖奶油绿已锁定。
2. 不要用渐变、毛玻璃、拟物、重投影营造质感。
3. 不要编造 Mock 数据 / 假项目 / 假员工 / 假指标填充界面。
4. 不要用裸加号表达层级或创建入口。
5. 不要让栅格因数据少塌成 1 列——`.cap-grid` 恒 3、`.mod-grid` 恒 5、`.dept2` 恒 2。
6. 不要让等待 Contract（后端能力）的功能显示为可操作；无写权限时按钮不渲染或禁用。
7. 不要用综合评分替代真实事实；错误文案必须脱敏。

---

## 8. Responsive Behavior

> 注：当前交付物以 **Desktop 固定画布 1536×1024** 为基准（mockup 框架）。真实前端 1:1 实现时按下表断点做流式重排，Terra token 不变。

### Breakpoints
| 断点 | 范围 | 行为 |
| --- | --- | --- |
| mobile | < 640px | 侧栏收起为抽屉；12 栏降为 1 栏堆叠；`.mod-grid` 5→1；`.cap-grid` 3→1；`.dept2` 2→1 |
| tablet | 640–1023px | 侧栏可折叠；`.mod-grid` 5→3；`.cap-grid` 3→2；`.dept2` 2→1 |
| desktop | 1024–1535px | 完整侧栏；栅格接近基准但容器自适应宽度 |
| wide | ≥ 1536px | 锁定 1536 画布或居中最大宽 1536 后留白 |

### Touch Targets
最小可点尺寸 **36×36px**（按钮 padding 9×2+12≈36；导航项 9×2+行高≈40）。

### 折叠策略
- 移动端 Sidebar 改为顶部汉堡 + 抽屉，导航项全宽。
- 事实条带（`.facts`）移动端换行；主操作按钮移到内容顶部。
- 三级详情 7 段骨架移动端改为单列纵向流。

### Font Scaling
桌面基准 14px 正文；移动端保持 14px 不缩小（避免可读性问题），仅通过栏数减少降低密度。Display Hero 在 < 640px 由 24px 降到 20px。

---

## 9. Agent Prompt Guide

### Quick Reference
- 主色 `--primary:#4a7c59`，背景 `--bg:#faf6f0`，强调 `--accent:#705c30`。
- 标题衬线 Literata，正文无衬线 Nunito Sans。
- 卡片圆角 16px，阴影 `0 1px 2px /.04, 0 4px 12px /.05`，hover 浮起 `--shadow-lg`。
- 栅格 12 栏 / gap 14px；跨栏 `.spanN`；列表行距 8px。
- 状态色：绿可用 / 琥珀阻塞 / 红错误 / 青 AI / 紫自定义。
- 空态用 `.empty-box` 虚线框，绝不填 0 或 Mock。
- 图标内联 SVG `<use href="#i-name"/>`，色 `currentColor`。
- 全站 39 页空态正本 + 13 页 `_samples/` 填充态 + `UI_设计与布局规范.md §13` 状态矩阵，三者对照还原。

### Component Prompts（可直接复制）
1. 「用 Terra 设计系统生成一个能力卡片网格：3 列 `.cap-grid`，每张卡含彩色图标块、衬线名称(18px/700)、来源徽章、分类标签、3 行描述截断、调用/评分/更新三栏统计、状态徽章、查看/编辑/运行操作。hover 上浮 2px。」
2. 「生成一个 Sidebar 导航：176px 森林绿背景，一级 14px/600 白色系文字，激活态白底反色，二级缩进 28px、三级 48px，chevron 展开收起。」
3. 「生成一个空态卡片：`.empty-box` 虚线边框 1.5px `--line-2`，圆角 12px，居中图标(26px `--line-2`)+ 说明文字 13px `--txt-3`，不显示任何数字。」
4. 「生成设置页表单：左 8 栏基本资料(公司名/行业/核心目标 textarea/负责人/邮箱/时区)，右 4 栏品牌与显示(Logo 方块 + 主题色圆点 + 语言下拉)，下方通知偏好 switch 行，全部用 `--line-2` 边框、聚焦转 `--primary`。」
5. 「生成三级详情页 7 段骨架：返回链接 → 对象名+状态 → 主操作 → 身份事实 → 关联 → 运行记录 → 错误边界，全部 Terra 卡片，长日志用等宽字体 `overflow-x:auto`。」
6. 「生成一个分页器：仅当 total>单页上限渲染，位于网格底部 +14px，复用 `.cat-bar` 圆角与 `--line` 边框，页码按钮 hover 转 `--primary`。」

### Iteration Guide（AI 生成 UI 时必守）
1. 先锁定 Terra token，不要「微调」成别的绿色——`#4a7c59` 是唯一主色。
2. 每生成一个组件，先确认它属于哪个栅格跨栏（spanN）与在哪个断点折叠。
3. 空态优先：任何列表/卡片先画 Empty，再画 Few/Full，最后 Overflow（分页）。
4. 图标必须用内联 SVG sprite，生成后核对 `<use href>` 与 `<symbol id>` 是否一一对应，避免空图标。
5. 截断规则写死：卡片描述 `line-clamp:3`、标题 `line-clamp:1`、列表副标题单行省略。
6. 不要为「好看」加渐变/阴影/发光；Terra 的质感来自留白与边框。
7. 所有数字必须来自真实事实；没有数据源时显示空态或「—」，不编。
8. 生成后截图自检：画布是否锁定 1536×1024 不溢出、导航 active 是否正确、色彩是否漂移。
9. 跨页一致性：复用同一套 shell/CSS/icon sprite，不要每页重写一套。
10. 交付前对照 `UI_设计与布局规范.md §10 设计验收清单` 逐条勾选。
