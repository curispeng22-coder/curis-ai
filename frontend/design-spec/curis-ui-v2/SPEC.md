# Curis CEO Office -- 全站 UI 设计规格

Status: Deprecated

> 版本: V1.0 · 2026-07-25
> 画布基准: Desktop 1536 x 1024
> 视觉风格: Terra 暖奶油 + 森林绿
> 前端直读: 本文档包含全部尺寸、色值、间距、字号，可直接用于开发

---

## 1. 设计令牌 (Design Tokens)

### 1.1 色彩系统

| 角色 | CSS 变量 | HEX | 使用场景 |
|------|----------|-----|----------|
| 主色 | `--curis-primary` | `#4a7c59` | 按钮、品牌色、侧栏背景 |
| 主色深 | `--curis-primary-dark` | `#2f523b` | 按钮 hover、主色强调态 |
| 主色浅 | `--curis-primary-light` | `#e8f0e8` | 标签背景、选中态背景 |
| 主色软 | `--curis-primary-soft` | `#f0f6f0` | hover 退让背景 |
| 暖琥珀 | `--curis-accent` | `#705c30` | CEO 决策标记、accent 强调 |
| 暖琥珀浅 | `--curis-accent-light` | `#f5efe3` | accent 退让背景 |
| 主背景 | `--curis-bg` | `#faf6f0` | 画布主背景 |
| 卡片表面 | `--curis-surface` | `#fffefb` | 卡片、面板表面 |
| 嵌套表面 | `--curis-surface-2` | `#f7f2ea` | 列表行、嵌套区域 |
| 占位表面 | `--curis-surface-3` | `#f0ebe0` | 占位符、凹陷区域 |
| 主文字 | `--curis-txt` | `#1f241c` | 标题、正文（深墨绿） |
| 次文字 | `--curis-txt-2` | `#4a5346` | 描述、次要信息 |
| 辅助文字 | `--curis-txt-3` | `#7a8273` | 提示、时间戳 |
| 分割线 | `--curis-line` | `#e8e2d8` | 卡片边框、分割线 |
| 强调分割线 | `--curis-line-2` | `#d9d2c6` | 强调边框 |
| 成功/可用 | `--state-success` | `#15935a` | 正常运行状态 |
| 成功表面 | `--state-success-surface` | `#e8f5ed` | 成功状态背景 |
| 信息/AI | `--state-info` | `#3f7d6e` | AI 内容标记 |
| 待决/阻塞 | `--state-warning` | `#a8742a` | 需要关注的状态 |
| 待决表面 | `--state-warning-surface` | `#f9f0e0` | 待决状态背景 |
| 错误 | `--state-error` | `#b83230` | 异常、失败 |
| 错误表面 | `--state-error-surface` | `#fae8e7` | 错误状态背景 |

### 1.2 字体系统

| 用途 | CSS 类 | Font Family | Size | Line Height | Weight |
|------|--------|-------------|------|-------------|--------|
| 页面标题 | `.ph-title` | `'Literata', 'Noto Serif SC', serif` | 24px | 1.1 | 700 |
| 卡片标题 | `.card-title` | `'Literata', 'Noto Serif SC', serif` | 15px | 1.3 | 600 |
| 模块卡片名 | `.module-title` | `'Literata', 'Noto Serif SC', serif` | 18px | 1.2 | 700 |
| 一级导航 | `.nav-1` | `'Nunito Sans', 'Inter', 'PingFang SC', 'Microsoft YaHei', sans-serif` | 14px | 1.3 | 600 |
| 二级导航 | `.nav-2` | `'Nunito Sans', 'Inter', 'PingFang SC', 'Microsoft YaHei', sans-serif` | 13px | 1.35 | 500 |
| 正文 | `.body-text` | `'Nunito Sans', 'Inter', 'PingFang SC', 'Microsoft YaHei', sans-serif` | 14px | 1.6 | 400 |
| 标签/数据 | `.label-text` | `'Nunito Sans', 'Inter', 'PingFang SC', 'Microsoft YaHei', sans-serif` | 12px | 1.4 | 500 |
| 辅助说明 | `.helper-text` | `'Nunito Sans', 'Inter', 'PingFang SC', 'Microsoft YaHei', sans-serif` | 11px | 1.45 | 400 |
| 按钮 | `.btn-text` | `'Nunito Sans', 'Inter', 'PingFang SC', 'Microsoft YaHei', sans-serif` | 12px | 1.0 | 700 |

**字体回退链：**
- 衬线: `--font-serif: 'Literata', 'Noto Serif SC', 'Songti SC', serif`
- 无衬线: `--font-sans: 'Nunito Sans', 'Inter', 'PingFang SC', 'Microsoft YaHei', sans-serif`

### 1.3 间距系统

间距基数: **8px**

| Token | 值 | 典型用途 |
|-------|-----|----------|
| `--space-1` | 4px | 图标与文字最小间距 |
| `--space-2` | 8px | 紧凑元素间距、列表项内部 |
| `--space-3` | 12px | 卡片内分组间距 |
| `--space-4` | 16px | 卡片内边距 (card-hd/card-bd 默认) |
| `--space-6` | 24px | 页面主区内边距 (top) |
| `--space-8` | 32px | 空态内边距 |
| `--space-12` | 48px | 大区间距 |

### 1.4 圆角

| Token | 值 | 使用场景 |
|-------|-----|----------|
| `--radius-sm` | 8px | 控件（按钮、输入框、小卡片） |
| `--radius-md` | 12px | 嵌套区块（列表行容器） |
| `--radius-lg` | 16px | 卡片主体 |
| `--radius-full` | 9999px | 标签、徽章、胶囊按钮 |

### 1.5 阴影

| Token | 值 | 使用场景 |
|-------|-----|----------|
| `--shadow-sm` | `0 1px 2px rgba(74,85,66,.04), 0 4px 12px rgba(74,85,66,.05)` | 静态卡片默认阴影 |
| `--shadow-md` | `0 2px 4px rgba(74,85,66,.04), 0 4px 12px rgba(74,85,66,.06)` | 卡片 hover 态阴影 |
| `--shadow-lg` | `0 8px 24px rgba(74,85,66,.08)` | 弹出层、浮层 |
| `--shadow-float` | `0 8px 24px rgba(74,85,66,.05)` | 浮动面板 |

---

## 2. 页面骨架

### 2.1 基准画布

| 属性 | 值 |
|------|-----|
| 画布尺寸 | 1536px x 1024px |
| body 背景 | `#e8e2d8`（画布外灰色） |
| 画布背景 | `var(--curis-bg)` `#faf6f0` |
| 画布定位 | 居中显示，`display:flex; justify-content:center` |
| 画布溢出 | `overflow:hidden` |
| 画布外投影 | `0 0 60px rgba(0,0,0,.08)` |

### 2.2 左侧产品导航

| 属性 | 值 |
|------|-----|
| 宽度 | 176px（固定） |
| 背景 | `--curis-primary` `#4a7c59` |
| 顶部内边距 | 20px |
| 底部内边距 | 16px |
| 品牌区 | `padding: 0 18px 18px`，底部分割线 `1px solid rgba(255,255,255,.12)`，下方 `margin-bottom: 8px` |
| 品牌文字 | serif / 14px / 700 / 白色 / `letter-spacing: .02em` |
| 品牌图标 | 20x20 SVG |
| 导航容器 | `padding: 0 8px`，`gap: 1px` |
| 一级导航图标 | 16x16 SVG，默认 `opacity: .7` |
| 一级导航文字 | sans / 14px / 600 / `rgba(255,255,255,.72)` |
| 一级导航项 padding | `9px 12px` / `border-radius: 8px` / `gap: 9px` |
| 二级导航图标 | 12x12 SVG，默认 `opacity: .45` |
| 二级导航文字 | sans / 13px / 500 / `rgba(255,255,255,.55)` |
| 二级缩进 | `padding-left: 40px`（含左侧 2px 活跃指示条时为 38px） |
| 子导航区域 | `padding: 4px 0 2px 0` |

### 2.3 主内容区

| 属性 | 值 |
|------|-----|
| 布局 | `flex:1; overflow-y:auto; overflow-x:hidden` |
| 内边距 | `padding: 24px 24px 20px` |
| Grid 系统 | 12 栏 `grid-template-columns: repeat(12, 1fr)` |
| 栏间距 | `gap: 14px` |
| 行间距 | `margin-bottom: 14px`（每行 grid 容器之间） |
| 页面顶部安全距离 | 内含在 `padding: 24px` 中 |

---

## 3. 全局组件

### 3.1 卡片 (.card)

| 属性 | 值 |
|------|-----|
| 标记 | `.card` |
| 背景 | `var(--curis-surface)` `#fffefb` |
| 边框 | `1px solid var(--curis-line)` `#e8e2d8` |
| 圆角 | `var(--radius-lg)` 16px |
| 阴影 | `var(--shadow-sm)` |
| 溢出 | `overflow: hidden` |

### 3.2 卡片头部 (.card-hd)

| 属性 | 值 |
|------|-----|
| 标记 | `.card-hd` |
| 内边距 | `14px 18px` |
| 底部边框 | `1px solid var(--curis-line)` |
| 布局 | `display:flex; align-items:center; justify-content:space-between` |
| 左侧内容 | `.card-hd-left`: `display:flex; align-items:center; gap:8px` |
| 标题图标 | 16x16 SVG |
| 标题文字 | `.card-title` |
| 数量徽标 | `.count-badge`: `min-width:20px; height:20px; padding:0 6px; border-radius:9999px; font-size:11px/600; background:var(--curis-surface-2); color:var(--curis-txt-3)` |

### 3.3 卡片主体 (.card-bd)

| 属性 | 值 |
|------|-----|
| 标记 | `.card-bd` |
| 内边距 | `14px 18px` |

### 3.4 卡片底部 (.card-ft)

| 属性 | 值 |
|------|-----|
| 标记 | `.card-ft` |
| 内边距 | `var(--space-3) var(--space-4)` 即 `12px 16px` |
| 顶部边框 | `1px solid var(--curis-line)` |
| 背景 | `var(--curis-surface-2)` `#f7f2ea` |

### 3.5 主按钮 (.btn-new)

| 属性 | 值 |
|------|-----|
| 标记 | `.btn-new` |
| 布局 | `display:inline-flex; align-items:center; gap:6px` |
| 内边距 | `8px 16px` |
| 背景 | `var(--curis-primary)` `#4a7c59` |
| 文字颜色 | `var(--curis-primary-foreground)` `#ffffff` |
| 边框 | `none` |
| 圆角 | `var(--radius-sm)` 8px |
| 字号 | `--font-sans` / 12px / 700 |
| 图标尺寸 | 14x14 SVG |
| 过渡 | `transition: background 0.15s` |

### 3.6 幽灵按钮 (.btn-ghost)

| 属性 | 值 |
|------|-----|
| 标记 | `.btn-ghost` |
| 布局 | `display:inline-flex; align-items:center; gap:6px` |
| 内边距 | `8px 16px` |
| 背景 | `transparent` |
| 文字颜色 | `var(--curis-txt-2)` `#4a5346` |
| 边框 | `1px solid var(--curis-line)` `#e8e2d8` |
| 圆角 | `var(--radius-sm)` 8px |
| 字号 | `--font-sans` / 12px / 600 |
| 图标尺寸 | 14x14 SVG |
| 过渡 | `transition: background 0.15s` |

### 3.7 标签 (.tag)

| 属性 | 值 |
|------|-----|
| 标记 | `.tag` |
| 布局 | `display:inline-flex; align-items:center` |
| 内边距 | `3px 10px` |
| 背景 | `var(--curis-primary-light)` `#e8f0e8` |
| 文字颜色 | `var(--curis-primary-dark)` `#2f523b` |
| 圆角 | `var(--radius-full)` 9999px |
| 字号 | `--font-sans` / 11px / 600 / `line-height: 1.3` |

### 3.8 图标容器 (.icon-box)

| 属性 | 值 |
|------|-----|
| 标记 | `.icon-box` |
| 尺寸 | `40px x 40px` |
| 布局 | `display:flex; align-items:center; justify-content:center` |
| 圆角 | `var(--radius-md)` 12px |
| 缩放 | `flex-shrink: 0` |
| 颜色变体 | `.green`: `var(--state-success-surface)` / `.cyan`: `#e8f0f0` / `.amber`: `var(--state-warning-surface)` / `.red`: `var(--state-error-surface)` / `.primary`: `var(--curis-primary-light)` / `.surface`: `var(--curis-surface-2)` |

### 3.9 状态指示点 (.status-dot)

| 属性 | 值 |
|------|-----|
| 标记 | `.status-dot` |
| 尺寸 | `8px x 8px` |
| 形状 | `border-radius: 50%` |
| 缩放 | `flex-shrink: 0` |
| 颜色变体 | `.green`: `var(--state-success)` / `.amber`: `var(--state-warning)` / `.red`: `var(--state-error)` |

### 3.10 搜索框 (.search-box)

| 属性 | 值 |
|------|-----|
| 标记 | `.search-box` |
| 布局 | `display:flex; align-items:center; gap:8px` |
| 内边距 | `7px 14px` |
| 背景 | `var(--curis-surface)` `#fffefb` |
| 边框 | `1px solid var(--curis-line)` `#e8e2d8` |
| 圆角 | `var(--radius-sm)` 8px |
| 占位文字颜色 | `var(--curis-txt-3)` `#7a8273` |
| 输入文字 | `--font-sans` / 13px / `var(--curis-txt)` |
| 图标 | SVG，`flex-shrink: 0` |
| 输入框 | `border:none; background:transparent; outline:none; width:100%` |

### 3.11 返回链接 (.back-link)

| 属性 | 值 |
|------|-----|
| 标记 | `.back-link` |
| 布局 | `display:inline-flex; align-items:center; gap:4px` |
| 字号 | `--font-sans` / 13px / 500 |
| 文字颜色 | `var(--curis-txt-3)` `#7a8273` |
| 图标尺寸 | 14x14 SVG |
| 过渡 | `transition: color 0.15s` |
| 底部间距 | `margin-bottom: 14px` |

### 3.12 分类栏 (.cat-bar / .cat-chip)

**.cat-bar 容器：**

| 属性 | 值 |
|------|-----|
| 标记 | `.cat-bar` |
| 布局 | `display:flex; align-items:center; gap:6px` |
| 内边距 | `var(--space-2) 0` 即 `8px 0` |
| 溢出 | `overflow-x: auto` |

**.cat-chip 标签：**

| 属性 | 值 |
|------|-----|
| 标记 | `.cat-chip` |
| 布局 | `display:inline-flex; align-items:center` |
| 内边距 | `5px 14px` |
| 背景 | `var(--curis-surface)` `#fffefb` |
| 文字颜色 | `var(--curis-txt-2)` `#4a5346` |
| 边框 | `1px solid var(--curis-line)` `#e8e2d8` |
| 圆角 | `var(--radius-full)` 9999px |
| 字号 | `--font-sans` / 12px / 500 |
| 过渡 | `transition: all 0.15s` |
| 活跃态 (.active) | 背景 `var(--curis-primary)` / 文字 `#ffffff` / 边框 `var(--curis-primary)` |

### 3.13 空态容器 (.empty-box)

| 属性 | 值 |
|------|-----|
| 标记 | `.empty-box` |
| 布局 | `display:flex; flex-direction:column; align-items:center; justify-content:center` |
| 内边距 | `var(--space-8) var(--space-6)` 即 `32px 24px` |
| 文字颜色 | `var(--curis-txt-3)` `#7a8273` |
| 对齐 | `text-align: center` |
| 图标 | SVG，`opacity: 0.4`，底部 `margin-bottom: var(--space-3)` 即 12px |
| 说明文字 | 13px / `line-height: 1.5` |
| 补充文字 | 11px / `var(--curis-txt-3)` / 顶部 `margin-top: 4px` |

### 3.14 业务数据边界 (.boundary)

| 属性 | 值 |
|------|-----|
| 标记 | `.boundary` |
| 内边距 | `var(--space-3) var(--space-4)` 即 `12px 16px` |
| 背景 | `var(--curis-surface-2)` `#f7f2ea` |
| 圆角 | `var(--radius-md)` 12px |
| 边框 | `1px dashed var(--curis-line)` `#e8e2d8` |
| 文字 | `--font-sans` / 11px / 400 / `var(--curis-txt-3)` / `line-height: 1.5` |
| 图标 | 14x14 SVG，`opacity: .35`，右侧 `gap: 8px` |

**行级变体 (`.boundary-box`)：**
- 内边距: `10px 18px`
- 布局: `display:flex; align-items:center; justify-content:space-between`
- 左侧图标+文字: `display:flex; align-items:center; gap:8px`
- 右侧时间戳: 11px / `var(--curis-txt-3)` / `font-variant-numeric: tabular-nums`
- 关键词加粗: `font-weight:600; color:var(--curis-txt-2)`

### 3.15 页面标识 (.page-identity)

| 属性 | 值 |
|------|-----|
| 标记 | `.page-identity` |
| 标题 | `.ph-title`: serif / 24px / 700 / `margin-bottom: 4px` |
| 副标题 | 13px / `var(--curis-txt-3)` / `margin-bottom: 10px` |
| 目标标签 | `.goal-tag`: `display:inline-flex; align-items:center; gap:5px; padding:4px 12px; background:var(--curis-primary-light); border-radius:9999px; font-size:12px/600; color:var(--curis-primary-dark)` |
| 目标标签图标 | 12x12 SVG |

---

## 4. 页面清单 (23 页)

| 序号 | 页面名 | HTML 文件 | 类型 | 对应规范章节 |
|------|--------|-----------|------|-------------|
| 1 | 总裁办公室 | `ceo-office.html` | 一级（仪表盘） | 5.1 |
| 2 | 决策中心 | `decision-center.html` | 二级 | 5.2 |
| 3 | 重要汇报 | `reports.html` | 二级 | 5.3 |
| 4 | 战略会议室 | `strategy-room.html` | 二级 | 5.4 |
| 5 | 项目中心 | `project-center.html` | 一级（仪表盘） | 5.5 |
| 6 | 项目详情 | `project-detail.html` | 三级（详情页） | 5.6 |
| 7 | 组织中心 | `org-center.html` | 一级（仪表盘） | 5.7 |
| 8 | 部门详情 | `department-detail.html` | 三级（详情页） | 5.8 |
| 9 | 能力中心 | `capability-center.html` | 一级（仪表盘） | 5.9 |
| 10 | Agent 列表 | `capability-agent-list.html` | 二级 | 5.10 |
| 11 | Skill 列表 | `capability-skill-list.html` | 二级 | 5.11 |
| 12 | Skill 详情 | `capability-skill-detail.html` | 三级（详情页） | 5.12 |
| 13 | Model 列表 | `capability-model-list.html` | 二级 | 5.13 |
| 14 | Tool 列表 | `capability-tool-list.html` | 二级 | 5.14 |
| 15 | Workflow 列表 | `capability-workflow-list.html` | 二级 | 5.15 |
| 16 | 经营分析 | `analysis.html` | 一级（仪表盘） | 5.16 |
| 17 | 头脑风暴室 | `brainstorm.html` | 一级（仪表盘） | 5.17 |
| 18 | 知识中心 | `knowledge.html` | 一级（仪表盘） | 5.18 |
| 19 | 执行工作台 | `workbench.html` | 特殊（Runtime） | 5.19 |
| 20 | 公司 Runtime | `company-runtime.html` | 特殊（Runtime） | 5.20 |
| 21 | 任务详情 | `task-detail.html` | 三级（详情页） | 5.21 |
| 22 | 汇报详情 | `report-detail.html` | 三级（详情页） | 5.22 |
| 23 | 公司设置 | `settings.html` | 特殊（表单） | 5.23 |

---

## 5. 布局规格

> 所有页面基于 12 栏 Grid，`gap: 14px`。侧栏 176px 固定，主内容区 `flex:1`，内边距 `24px 24px 20px`。每行 grid 容器之间 `margin-bottom: 14px`。

### 5.1 总裁办公室 (ceo-office.html)

| 行 | 内容 | 栏宽分配 | 说明 |
|----|------|----------|------|
| Row 1 | 页面标识 + 脉冲卡片 | 4 + 8 (3 个均分) | 页面标题区 span 4；右侧 3 个 pulse-card 在 span 8 内 `display:flex; gap:14px` 均分 |
| Row 2 | 核心项目 + 待处理汇报 + 组织健康 | 7 + 3 + 2 | hero-projects / hero-reports / hero-org-health |
| Row 3 | 部门空间 | 12 (2 列子网格) | dept-section 内 `grid-template-columns: repeat(2, 1fr); gap:14px` |
| Row 4 | 业务数据边界 | 12 | boundary-section |

### 5.2 决策中心 (decision-center.html)

| 行 | 内容 | 栏宽分配 | 说明 |
|----|------|----------|------|
| Row 1 | 页面标识 + 统计卡片 | 4 + 8 | 页面标题 span 4；右侧统计卡片在 span 8 内 flex 布局 |
| Row 2 | 待决策列表 + 决策统计 | 7 + 5 | 左：待决事项列表卡片；右：统计面板 |
| Row 3 | 历史决策记录 | 12 | 全宽卡片 |
| Row 4 | 业务数据边界 | 12 | boundary-section |

### 5.3 重要汇报 (reports.html)

| 行 | 内容 | 栏宽分配 | 说明 |
|----|------|----------|------|
| Row 1 | 页头（标题+操作） | 12 | `display:flex; align-items:center; justify-content:space-between; padding:0 2px` |
| Row 2 | 筛选面板 + 汇报列表 | 5 + 7 | 左：筛选/搜索；右：汇报条目列表 |
| Row 3 | 分页/加载更多 | 12 | 全宽 |

### 5.4 战略会议室 (strategy-room.html)

| 行 | 内容 | 栏宽分配 | 说明 |
|----|------|----------|------|
| Row 1 | 页面标识 + 快捷操作 | 4 + 8 | 同决策中心布局模式 |
| Row 2 | 策略画布 + 参与者/状态 | 8 + 4 | 主工作区 span 8；侧面板 span 4 |
| Row 3 | 战略议题列表 | 12 | 全宽卡片 |
| Row 4 | 业务数据边界 | 12 | boundary-section |

### 5.5 项目中心 (project-center.html)

| 行 | 内容 | 栏宽分配 | 说明 |
|----|------|----------|------|
| Row 1 | 页面标识 + 事实徽标 | 4 + 8 | page-identity span 4；fact-row span 8 内 `display:flex; flex-wrap:wrap; gap:14px` |
| Row 2 | 项目概览 + 项目组合 | 8 + 4 | overview-card / portfolio-card |
| Row 3 | 部门项目分布 | 12 | dept-project-section |
| Row 4 | 业务数据边界 | 12 | boundary-section |

### 5.6 项目详情 (project-detail.html) -- 三级详情页

| 区域 | 内容 | 布局说明 |
|------|------|----------|
| 返回链接 | `.back-link` | `margin-bottom: 14px`，返回项目中心 |
| 详情头部 | 标题行 | `margin-bottom: 20px`；标题 24px/700 + 项目名 18px/700 + tag 标签，`gap:10px; flex-wrap:wrap` |
| 内容列 | 详情卡片序列 | `max-width: 960px`，单列纵向排列，卡片之间 `margin-bottom: 14px` |
| 项目信息卡 | `.card` | 信息行: `padding: 10px 14px; background: var(--curis-surface-2); border-radius: var(--radius-sm)`；标签列宽 80px / 12px/600/txt-3 |
| 任务进度卡 | `.card` | 进度条 `height:8px; border-radius:4px; background:var(--curis-line)`，填充条 `var(--curis-primary)`；任务行 `gap:6px; padding:8px 12px` |
| 操作按钮组 | `.action-row` | `display:flex; align-items:center; gap:10px; margin-top:4px` |

### 5.7 组织中心 (org-center.html)

| 行 | 内容 | 栏宽分配 | 说明 |
|----|------|----------|------|
| Row 1 | 页面标识 + 统计数据 | 4 + 8 | 仪表盘标准模式 |
| Row 2 | 组织概览 + 部门列表 | 8 + 4 或 12 | 部门卡片网格 |
| Row 3 | 业务数据边界 | 12 | boundary-section |

### 5.8 部门详情 (department-detail.html) -- 三级详情页

同项目详情布局模式：返回链接 + 标题行 + 单列详情卡片序列（max-width: 960px）。

### 5.9 能力中心 (capability-center.html)

| 行 | 内容 | 栏宽分配 | 说明 |
|----|------|----------|------|
| Row 1 | 页面标识 + 快速操作 | 4 + 8 | 仪表盘标准模式 |
| Row 2 | 能力模块入口卡片 | 12 (多列子网格) | Agent/Skill/Model/Tool/Workflow 入口 |
| Row 3 | 业务数据边界 | 12 | boundary-section |

### 5.10 ~ 5.15 能力子页面 (Agent/Skill/Model/Tool/Workflow 列表)

| 行 | 内容 | 栏宽分配 | 说明 |
|----|------|----------|------|
| Row 1 | 页头 + 搜索/筛选 | 12 | 标题行 + search-box + cat-bar |
| Row 2 | 列表/网格内容 | 12 | 列表卡片或表格 |
| Row 3 | 业务数据边界 | 12 | boundary-section |

### 5.12 Skill 详情 (capability-skill-detail.html) -- 三级详情页

同项目详情布局模式：返回链接 + 标题行 + 单列详情卡片序列（max-width: 960px）。

### 5.16 经营分析 (analysis.html)

| 行 | 内容 | 栏宽分配 | 说明 |
|----|------|----------|------|
| Row 1 | 页面标识 + 脉冲指标 | 4 + 8 | 仪表盘标准模式 |
| Row 2 | 图表主区 + 侧边统计 | 8 + 4 | hero-chart / hero-sidebar |
| Row 3 | 部门分析 | 12 | dept-section |
| Row 4 | 业务数据边界 | 12 | boundary-section |

### 5.17 头脑风暴室 (brainstorm.html)

| 行 | 内容 | 栏宽分配 | 说明 |
|----|------|----------|------|
| Row 1 | 页面标识 + 脉冲指标 | 4 + 8 | 仪表盘标准模式，pulse-row `align-items:stretch` |
| Row 2 | 头脑风暴画布 + 会话面板 | 8 + 4 | hero-canvas / hero-session |
| Row 3 | 历史风暴记录 | 12 | storm-section |

### 5.18 知识中心 (knowledge.html)

| 行 | 内容 | 栏宽分配 | 说明 |
|----|------|----------|------|
| Row 1 | 页面标识 + 操作按钮组 | 4 + 8 | knowledge-actions `display:flex; gap:14px; align-items:flex-start` |
| Row 2 | 关系图谱 + 最近知识 + 领域卡片 | 8 + 4 (第一组) / 4+4+4 (第二组) | relation-map span 8; recent-knowledge span 4; domain-card x3 各 span 4 |
| Row 3 | 知识条目表格 | 12 | table-section |

### 5.19 执行工作台 (workbench.html) -- 特殊 (Runtime)

| 行 | 内容 | 栏宽分配 | 说明 |
|----|------|----------|------|
| Row 1 | 紧凑标题栏 + 事实徽标 | 12 | compact-header: `display:flex; align-items:center; gap:20px`；标题 20px；fact-badges `display:flex; gap:10px` |
| Row 2 | 当前执行队列 + Runtime 事实 | 8 + 4 | queue-card span 8 / runtime-facts span 4 |
| Row 3 | Workflow Runs | 12 | 全宽卡片 |
| Row 4 | 最近 Tasks | 12 | 全宽卡片 |

**事实徽标 (.fact-badge)：**
- 布局: `display:inline-flex; align-items:center; gap:5px; padding:5px 14px; border-radius:9999px`
- 字号: 12px/500
- 变体: `.green` (`state-success-surface`/`state-success`), `.primary` (`curis-primary-light`/`curis-primary`), `.red` (`state-error-surface`/`state-error`)
- 图标: 12x12 SVG

### 5.20 公司 Runtime (company-runtime.html) -- 特殊 (Runtime)

| 行 | 内容 | 栏宽分配 | 说明 |
|----|------|----------|------|
| Row 1 | Runtime 空间 + 侧面板 | 9 + 3 | runtime-space span 9；侧面板 span 3 内 `display:flex; flex-direction:column; gap:14px` |

### 5.21 ~ 5.22 三级详情页 (task-detail / report-detail)

同 5.6 项目详情布局模式：
1. `.back-link` (margin-bottom: 14px)
2. 详情头部 (margin-bottom: 20px)
3. 单列详情卡片序列 (max-width: 960px, 卡片间 margin-bottom: 14px)
4. 底部操作按钮组 (.action-row)

### 5.23 公司设置 (settings.html) -- 特殊 (表单)

| 行 | 内容 | 栏宽分配 | 说明 |
|----|------|----------|------|
| Row 1 | 紧凑标题栏 | 12 | compact-header: `display:flex; align-items:center; gap:20px` |
| Row 2 | 表单卡片组 | 4 + 4 + 4 | 3 个 form-card 各 span 4 |
| Row 3 | 摘要/总览 | 12 | summary-card |
| Row 4 | 业务数据边界 | 12 | boundary-section |

---

## 6. 交互状态规范

### 6.1 导航项 (.nav-item)

| 状态 | 背景变化 | 图标 opacity | 文字颜色 |
|------|----------|-------------|----------|
| 默认 | `transparent` | `.7` | `rgba(255,255,255,.72)` |
| hover | `rgba(255,255,255,.08)` | `1` | `#ffffff` |
| active（一级） | `rgba(255,255,255,.14)` | `1` | `#ffffff` |
| active（二级） | `transparent` + 左侧 `2px solid #fff` 边框 | - | `#ffffff` |
| 过渡 | `transition: background .12s` | - | - |

**二级导航 hover:** `.nav-label` 变为 `rgba(255,255,255,.85)`

### 6.2 按钮

**.btn-new (主按钮)：**

| 状态 | 背景色 |
|------|--------|
| 默认 | `var(--curis-primary)` `#4a7c59` |
| hover | `var(--curis-primary-dark)` `#2f523b` |
| disabled | 待定 (opacity: .5) |
| focus | `box-shadow: 0 0 0 2px var(--curis-bg), 0 0 0 4px var(--curis-primary)` (推荐) |

**.btn-ghost (幽灵按钮)：**

| 状态 | 背景色 |
|------|--------|
| 默认 | `transparent` |
| hover | `var(--curis-surface-2)` `#f7f2ea` |
| disabled | 待定 (opacity: .5) |
| focus | `box-shadow: 0 0 0 2px var(--curis-bg), 0 0 0 4px var(--curis-primary)` (推荐) |

### 6.3 卡片 (.card)

| 状态 | 阴影 |
|------|------|
| 默认 | `var(--shadow-sm)` |
| hover | `var(--shadow-md)` |
| 过渡 | `transition: box-shadow 0.2s` (推荐) |

### 6.4 分类标签 (.cat-chip)

| 状态 | 背景 | 文字 | 边框 |
|------|------|------|------|
| 默认 | `var(--curis-surface)` | `var(--curis-txt-2)` | `var(--curis-line)` |
| hover | `var(--curis-surface-2)` | `var(--curis-txt-2)` | `var(--curis-line)` |
| active | `var(--curis-primary)` | `#ffffff` | `var(--curis-primary)` |
| 过渡 | `transition: all 0.15s` | - | - |

### 6.5 搜索框 (.search-box)

| 状态 | 边框颜色 |
|------|----------|
| 默认 | `var(--curis-line)` `#e8e2d8` |
| focus | `var(--curis-primary)` `#4a7c59` (推荐) |
| hover | `var(--curis-line-2)` `#d9d2c6` (推荐) |

### 6.6 返回链接 (.back-link)

| 状态 | 文字颜色 |
|------|----------|
| 默认 | `var(--curis-txt-3)` `#7a8273` |
| hover | `var(--curis-primary)` `#4a7c59` |
| 过渡 | `transition: color 0.15s` | - |

---

## 7. 空态与错误态规范

### 7.1 空态 (Empty State)

- **保留完整空间构图:** 空态容器保持最终数据加载后的布局尺寸，不收缩
- **居中排列:** 图标 + 主说明 + 补充说明纵向居中
- **图标:** 40x48px SVG，`opacity: 0.4`，颜色 `var(--curis-txt-3)`
- **主说明:** `--font-sans` / 13px / 400 / `line-height: 1.5` / `var(--curis-txt-3)`
- **补充说明:** 11px / `var(--curis-txt-3)` / `margin-top: 4px`
- **示例文案:** "队列为空" / "暂无 Workflow Run 记录" / "暂无 Task 记录"
- **容器:** 使用 `.empty-box` 组件，`height:100%` 继承父级高度

### 7.2 错误态 (Error State)

- **脱敏错误信息:** 不暴露内部堆栈，仅展示用户可理解的操作提示
- **示例文案:** "加载失败，请稍后重试"
- **局部重试:** 在出错区域提供重试按钮（.btn-ghost），不刷新整页
- **错误图标:** 使用 warning 三角形或圆形感叹号 SVG，颜色 `var(--state-error)`
- **错误背景:** `var(--state-error-surface)` `#fae8e7`

### 7.3 加载态 (Loading State)

- **保持最终布局尺寸:** 骨架屏需与实际内容完全等高等宽，避免布局抖动 (CLS = 0)
- **骨架块:** 使用 `var(--curis-surface-2)` `#f7f2ea` 或 `var(--curis-surface-3)` `#f0ebe0` 作为填充色
- **骨架动画:** 推荐使用 `pulse` 动画（opacity 在 0.4~1 之间渐变）
- **圆角匹配:** 骨架块的 border-radius 必须与对应实际组件一致

---

## 8. 响应式策略

- **当前基准:** Desktop 1536 x 1024 (fixed canvas)，设计稿以固定画布方式交付
- **实现方式:** `width: 1536px; overflow: hidden` 居中展示于 `body`
- **后续扩展:** 如需支持更小屏幕，建议断点如下（当前不实现）：
  - Laptop: 1366px
  - Tablet: 1024px
  - Mobile: 768px / 480px
- **注意事项:** 侧栏在窄屏下应考虑折叠为图标模式；12 栏 Grid 可降为 8 栏或 4 栏

---

## 9. 设计验收清单

- [ ] **色彩一致性:** 所有颜色使用 CSS 变量，无硬编码色值（除 body 背景 `#e8e2d8`）
- [ ] **字体规范:** 标题统一使用 serif（Literata），正文和 UI 控件统一使用 sans（Nunito Sans）
- [ ] **间距对齐:** 所有间距使用 8px 基数的 spacing token，无随意数值
- [ ] **圆角统一:** 按照控件 8px / 嵌套 12px / 卡片 16px / 标签 9999px 四档使用
- [ ] **阴影层级:** 静态卡片 shadow-sm，hover 提升 shadow-md，弹出层 shadow-lg
- [ ] **Grid 布局:** 12 栏 Grid，gap 14px，行间距 14px，所有栏宽分配总和 = 12
- [ ] **侧栏规范:** 176px 宽度，`#4a7c59` 背景，一级/二级导航字号和透明度区分正确
- [ ] **状态色彩语义:** success 绿色 / warning 琥珀 / error 红色 / info 青绿，语义一致
- [ ] **边界组件:** 每个数据聚合页面底部均包含 boundary 组件，虚线边框 + 快照时间戳
- [ ] **空态处理:** 列表为空时使用 .empty-box 居中展示，保持布局尺寸不抖动

---

## 10. 状态色彩语义

| 状态 | 前景色 | 背景色 | 使用场景 |
|------|--------|--------|----------|
| 可用/成功 | `--state-success` `#15935a` | `--state-success-surface` `#e8f5ed` | 正常运行、已完成、项目正常推进 |
| 待决/阻塞 | `--state-warning` `#a8742a` | `--state-warning-surface` `#f9f0e0` | 需要关注、等待决策、阻塞项 |
| 错误/失败 | `--state-error` `#b83230` | `--state-error-surface` `#fae8e7` | 异常、失败、P0 紧急 |
| 信息/AI | `--state-info` `#3f7d6e` | - | AI 生成内容、信息标记（无独立 surface 色） |

**状态点 (.status-dot) 颜色映射：**

| 变体 | 对应 CSS 变量 | HEX |
|------|-------------|-----|
| `.green` | `--state-success` | `#15935a` |
| `.amber` | `--state-warning` | `#a8742a` |
| `.red` | `--state-error` | `#b83230` |

**icon-box 背景色映射：**

| 变体 | 背景色 | 图标色 |
|------|--------|--------|
| `.green` | `--state-success-surface` `#e8f5ed` | `--state-success` |
| `.amber` | `--state-warning-surface` `#f9f0e0` | `--state-warning` |
| `.red` | `--state-error-surface` `#fae8e7` | `--state-error` |
| `.cyan` | `#e8f0f0` | `--state-info` (推荐) |
| `.primary` | `--curis-primary-light` `#e8f0e8` | `--curis-primary` (推荐) |
| `.surface` | `--curis-surface-2` `#f7f2ea` | `--curis-txt-3` (推荐) |

---

## 附录 A: 语义别名 (Semantic Aliases)

为兼容 Tailwind CSS v4 `@theme inline`，以下语义别名已映射:

| Tailwind 语义 | 映射到 Curis 变量 |
|---------------|-----------------|
| `--color-background` | `--curis-background` / `#faf6f0` |
| `--color-foreground` | `--curis-foreground` / `#1f241c` |
| `--color-card` | `--curis-card` / `#fffefb` |
| `--color-card-foreground` | `--curis-card-foreground` / `#1f241c` |
| `--color-popover` | `--curis-popover` / `#fffefb` |
| `--color-popover-foreground` | `--curis-popover-foreground` / `#1f241c` |
| `--color-primary` | `--curis-primary` / `#4a7c59` |
| `--color-primary-foreground` | `--curis-primary-foreground` / `#ffffff` |
| `--color-muted` | `--curis-muted` / `#f0ebe0` |
| `--color-muted-foreground` | `--curis-muted-foreground` / `#7a8273` |
| `--color-accent` | `--curis-accent` / `#705c30` |
| `--color-border` | `--curis-border` / `#e8e2d8` |
| `--color-input` | `--curis-input` / `#e8e2d8` |
| `--color-ring` | `--curis-ring` / `#4a7c59` |

## 附录 B: 关键布局数值速查

| 属性 | 值 |
|------|-----|
| 画布总宽 | 1536px |
| 画布总高 | 1024px |
| 侧栏宽 | 176px |
| 主内容宽 | 1536 - 176 = 1360px |
| 主内容内边距 | 24px 24px 20px |
| 可用内容宽 | 1360 - 24*2 = 1312px |
| Grid 栏数 | 12 |
| Grid gap | 14px |
| 单栏宽度 | (1312 - 14*11) / 12 = (1312 - 154) / 12 = 96.5px |
| 行间距 | 14px (margin-bottom) |
| 卡片内边距 (hd/bd) | 14px 18px |
| 列表项内边距 | 10px 14px (项目行) / 8px 12px (任务行) |
| 头像尺寸 | 28px (部门卡片) / 40px (icon-box) |
| 进度条高度 | 6px (项目行) / 8px (详情页) |
