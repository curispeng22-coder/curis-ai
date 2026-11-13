# 能力中心 · Dev Mode 标注（前端直读）

> 对应高保真原型：`frontend/design-spec/ceo-office/handoff/capability-center/capability-center.hifi.html`
> 设计系统：Terra 暖奶油 + 森林绿（与 `DESIGN.md` 一致）
> 用途：前端 1:1 还原的尺寸 / 色值 / 间距 / 字号标注，无需打开 Figma
> 画布：内容区 max-width 1280（侧边栏 248 + 主区自适应），卡片网格 `repeat(auto-fill, minmax(280px,1fr))`，gap 16

---

## 1. 设计 Token（与 DESIGN.md 对齐）

| Token | 值 | 用途 |
|---|---|---|
| `--curis-primary` | `#4a7c59` | 主色 / 按钮 / 激活态 |
| `--curis-primary-dark` | `#2f523b` | 侧边栏底 / 按钮 hover |
| `--curis-primary-light` | `#e8f0e8` | 主色浅底（图标盒/标签） |
| `--curis-accent` | `#705c30` | 强调（CEO 决策） |
| `--curis-bg` | `#faf6f0` | 页面背景 |
| `--curis-surface` | `#fffefb` | 卡片 / 弹出层 |
| `--curis-surface-2` | `#f7f2ea` | 卡片脚 / 次级底 |
| `--curis-txt` | `#1f241c` | 主文字 |
| `--curis-txt-2` | `#4a5346` | 次级文字 |
| `--curis-txt-3` | `#7a8273` | 辅助 / 占位 |
| `--curis-line` | `#e8e2d8` | 边框 / 分割线 |
| `--state-success` | `#15935a` | 可用 |
| `--state-warning` | `#a8742a` | 阻塞 |
| `--state-error` | `#b83230` | 错误 / 自定义 |
| `--radius-sm/md/lg` | `8 / 12 / 16px` | 控件 / 图标盒 / 卡片 |
| `--shadow-sm` | `0 1px 2px rgba(74,85,66,.04),0 4px 12px rgba(74,85,66,.05)` | 卡片默认 |
| `--shadow-lg` | `0 8px 24px rgba(74,85,66,.08)` | 卡片 hover / 抽屉 |
| `--space-1..12` | `4/8/12/16/24/32/48px` | 间距阶梯 |

---

## 2. 排版系统（字号分层）

| 角色 | 字体 | 字号 | 行高 | 字重 | 颜色 |
|---|---|---|---|---|---|
| 页面标题 `.ph-title` | Literata(serif) | 24px | 1.1 | 700 | `--curis-txt` |
| 模块名 `.module-title` | Literata(serif) | 18px | 1.2 | 700 | `--curis-txt` |
| 卡片标题 `.card-title` | Literata(serif) | 15px | 1.3 | 600 | `--curis-txt` |
| 一级导航 `.nav-1` | Nunito Sans | 14px | 1.3 | 600 | `#dbe7dd`(侧栏) |
| 二级导航 `.nav-2` | Nunito Sans | 13px | 1.35 | 500 | `#cdddd2`(侧栏) |
| 正文 `.body-text` | Nunito Sans | 14px | 1.6 | 400 | `--curis-txt` |
| 标签文字 `.label-text` | Nunito Sans | 12px | 1.4 | 500 | `--curis-txt-2` |
| 辅助 `.helper-text` | Nunito Sans | 11px | 1.45 | 400 | `--curis-txt-3` |
| 按钮 `.btn-new` | Nunito Sans | 12px | 1.0 | 700 | `#fff` |

---

## 3. 组件 Inspect 表

### 3.1 侧边栏 Sidebar
| 属性 | 值 |
|---|---|
| 宽度 | 248px（fixed） |
| 背景 | `--curis-primary-dark` (#2f523b) |
| 内边距 | 24px 16px |
| 导航项 | padding 8px 10px，radius 8px，字号 14/600 |
| 激活态 | 背景 `--curis-primary`，文字 #fff |
| hover | 背景 rgba(255,255,255,.08) |

### 3.2 页面头 Page Head
| 属性 | 值 |
|---|---|
| 面包屑 | 字号 13/500，色 `--curis-txt-3`，hover `--curis-primary` |
| 标题 | `.ph-title` 24/700 serif |
| 副标题 | 字号 13，色 `--curis-txt-3`，margin-top 4px |

### 3.3 工具栏 Toolbar
| 属性 | 值 |
|---|---|
| 搜索框 | padding 8px 14px，radius 8px，border 1px `--curis-line`，字号 13，min-width 240，flex:1 |
| 主按钮 | padding 8px 16px，radius 8px，背景 `--curis-primary`，文字 #fff，字号 12/700；hover 背景 `--curis-primary-dark` |
| 间距 | 工具栏与下方分类栏 gap 12px，与页面头 gap 24px |

### 3.4 分类 Chip 栏
| 属性 | 值 |
|---|---|
| chip | padding 5px 14px，radius 9999(full)，border 1px `--curis-line`，字号 12/500，色 `--curis-txt-2` |
| 激活 chip | 背景 `--curis-primary`，文字 #fff，border `--curis-primary` |
| hover | 背景 `--curis-surface-2` |
| 容器 | overflow-x auto，padding 8px 0 |

### 3.5 能力卡片 Card（核心）
| 属性 | 值 |
|---|---|
| 网格 | `repeat(auto-fill, minmax(280px,1fr))`，gap 16px |
| 卡片 | 背景 `--curis-surface`，border 1px `--curis-line`，radius 16px，shadow-sm，overflow hidden |
| 卡片 body | flex gap 12px，padding 16px |
| 图标盒 | 40×40，radius 12px，flex-shrink 0；色系：green/primary/amber/cyan 对应 surface |
| 模块名 | `.module-title` 18/700 serif |
| 描述 | 字号 13/1.5，色 `--curis-txt-2`，margin-top 2px |
| 卡片脚 | flex space-between，padding 12px 16px，border-top 1px `--curis-line`，背景 `--curis-surface-2` |
| **hover 态** | border-color `--curis-primary`，box-shadow `--shadow-lg`，transform translateY(-2px)，transition .2s |
| **点击** | 打开右侧 Drawer（见 3.8） |

### 3.6 状态标签 Tag
| 属性 | 值 |
|---|---|
| 基础 | padding 3px 10px，radius 9999，字号 11/600，line-height 1.3 |
| 绿色(可用) | 背景 `--state-success-surface`，色 `--state-success` |
| 琥珀(阻塞) | 背景 `--state-warning-surface`，色 `--state-warning` |
| 红(自定义) | 背景 `--state-error-surface`，色 `--state-error` |
| 主色(默认) | 背景 `--curis-primary-light`，色 `--curis-primary-dark` |

### 3.7 空态 / 错误态
| 属性 | 值 |
|---|---|
| 空态盒 | flex-col center，padding 48px 24px，border 1px dashed `--curis-line`，radius 16px，背景 `--curis-surface`；图标 opacity .4，文字 13/1.5 `--curis-txt-3` |
| 错误盒 | padding 16px，背景 `--state-error-surface`，border 1px `--state-error`，radius 12px；标题 13/700 `--state-error`，正文 12 `--curis-txt-2` |

### 3.8 抽屉 Drawer（点击卡片触发）
| 属性 | 值 |
|---|---|
| 遮罩 overlay | fixed inset 0，背景 rgba(31,36,28,.32)，opacity 0→1 transition .25s |
| 抽屉 | fixed right 0，height 100vh，width 420px(max 90vw)，背景 `--curis-surface`，shadow-lg，transform translateX(100%)→0 transition .28s |
| 抽屉头 | flex space-between，padding 16px，border-bottom 1px `--curis-line`；标题 18/700 serif |
| 抽屉行 | flex space-between，padding 12px，背景 `--curis-surface-2`，radius 12px；名称 14/600，meta 12 `--curis-txt-3` |

---

## 4. 交互状态清单（前端必实现）
| 态 | 触发 | 表现 |
|---|---|---|
| 默认 | 初始 | 5 大类卡片网格 |
| hover | 鼠标悬停卡片 | 边框转主色 + 抬升阴影 + 上移 2px |
| 点击 | 点击卡片 | 右侧抽屉滑出 + 遮罩 |
| 空态 | 筛选无结果 / 手动切换 | 虚线空态盒 |
| 错误态 | 加载失败 / 手动切换 | 红色错误盒 + 重试按钮 |
| 分类切换 | 点击 chip | 激活态变色，列表按类过滤（路线图） |

---

## 5. 还原检查项（QA）
- [ ] 卡片网格列宽 ≥280px、gap 16px
- [ ] icon-box 严格 40×40 / radius 12
- [ ] tag 圆角 full、字号 11、三色状态正确
- [ ] hover 抬升 2px + 阴影 lg
- [ ] 抽屉 420px、右滑 0.28s、遮罩 0.32 alpha
- [ ] 字体 Literata 用于标题、Nunito Sans 用于正文
- [ ] 全部色值取自 §1 token，无硬编码
