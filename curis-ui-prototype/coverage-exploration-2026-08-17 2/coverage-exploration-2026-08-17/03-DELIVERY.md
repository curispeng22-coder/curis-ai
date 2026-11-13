# Curis Complete Product UI Coverage — 交付说明 (DELIVERY)

> 生成时间：2026-08-17
> 交付物类型：**Coverage First / Visual Exploration**（覆盖优先 · 视觉探索）
> 交付专家：export-specialist（交付达）

---

## 0. 重要性质标注（务必先读）

本目录为 **Coverage Exploration（覆盖探索）原型**，请明确区分以下三种性质，避免误用：

| 性质 | 说明 | 本交付是否属于 |
|------|------|----------------|
| **Coverage Exploration（覆盖探索）** | 以「覆盖全部一级页面与关键状态」为首要目标的视觉探索原型，验证 Frozen 视觉系统 + Workspace Shell 的承载可行性 | ✅ **本交付属于此类** |
| **Production Visual（生产视觉）** | 经过像素级打磨、可交付工程实现的正式视觉 | ❌ 不属于 |
| **Frozen Authority（冻结权威）** | 设计令牌、Shell Contract、Shared Pattern 的权威定义来源 | ❌ 不属于（本交付**复用** Frozen，但**不是** Frozen 本身） |

所有页面**复用** Frozen 设计令牌（`--ui-*`）、四独立 Pane Workspace Shell、以及 Shared Pattern（Employee Row / Conversation / Composer / Result Reference / Needs CEO / Employee Detail）。示例数据均标记「示例数据」，不可作为真实业务数据。

---

## 1. 交付物清单

### 1.1 HTML 原型（12 个，单目录内可独立双击打开）

| # | 文件 | 说明 |
|---|------|------|
| 0 | `index.html` | 统一入口 / 目录总览（覆盖进度表 + 快速进入） |
| 1 | `01-ceo-desk.html` | 首页 / CEO 工作台 |
| 2 | `02-business-space.html` | 业务空间 |
| 3 | `03-org-center.html` | 组织中心 |
| 4 | `04-talent-market.html` | 人才市场 |
| 5 | `05-library.html` | 资料库 |
| 6 | `06-meeting.html` | 会议 |
| 7 | `07-settings.html` | 设置（头像菜单进入） |
| 8 | `08-rd-workspace.html` | RD Workspace（研发办公室） |
| 9 | `09-xhs-workspace.html` | Content Growth / 小红书运营办公室 |
| 10 | `10-global-search.html` | 全局能力（全局对象搜索） |
| 11 | `11-states.html` | 重要状态集（跨页面关键状态示例） |

### 1.2 文档（3 份）

| 文件 | 说明 |
|------|------|
| `00-PAGE-STATE-INVENTORY.md` | 页面 / 状态清单（一级区域与页面总览、各页面子状态、Shared Pattern 复用矩阵、设计缺口记录） |
| `01-DESIGN-TOKENS.md` | 设计令牌文档（Frozen 视觉变量说明） |
| `03-DELIVERY.md` | 本交付说明 |

> 注：12 个 HTML + 3 份文档 = 15 个交付文件，全部位于本目录 `coverage-exploration-2026-08-17/` 内。

---

## 2. 如何浏览

**推荐入口：双击打开 `index.html`**（`coverage-exploration-2026-08-17/index.html`）。

1. `index.html` 提供「页面覆盖进度」总表与「快速进入」卡片网格。
2. 点击任意页面卡片或左侧六区导航，即可在同目录内跳转至对应原型页。
3. 每个原型页为静态 HTML，含内联交互（导航收起 / 上下文面板 / 专业工具面板 / 折叠员工行 / Tab 切换），**无需启动任何服务、无需安装依赖**，浏览器直接打开即可。
4. 顶部「全局对象搜索」按钮（导航栏搜索图标）可展开 Utility 面板，展示搜索入口与 Recent 列表。

**前提条件（关键）**：浏览器需能加载同级 `_system/` 目录（见第 3 节）。只要保持本目录与 `_system/` 的相对位置不变，双击即可正常渲染。

---

## 3. 文件与一级产品区 / 页面的对应关系表

> 编号沿用页面清单（A–K）。「文件」列即本目录内的 HTML；双击即可打开。

| 编号 | 一级区域 | 文件 | 核心覆盖目标 |
|------|---------|------|--------------|
| — | 覆盖总览（入口） | `index.html` | 覆盖进度表、快速进入、已知约束与设计缺口 |
| A | 首页 / CEO 工作台 | `01-ceo-desk.html` | 简报/今日变化、问题处理/待决定、当前运行、结果复盘、首次创建、空态 |
| B | 业务空间 | `02-business-space.html` | 业务总览、业务详情、Workspace 入口、空间工程、新建业务 |
| C | 组织中心 | `03-org-center.html` | 组织总览三视图、部门、员工列表/详情、招聘组队 |
| D | 人才市场 | `04-talent-market.html` | 专家/Skill/Connector 浏览、详情、招募流程、已安装状态 |
| E | 资料库 | `05-library.html` | 首页、文件阅读、搜索结果、外部连接/权限/同步、空态 |
| F | 会议 | `06-meeting.html` | 会议首页、Company/Workspace Meeting、Proposal/Decision |
| G | 设置 | `07-settings.html` | 个人/公司/AI 能力/Connector/权限/运行成本 |
| H | RD Workspace | `08-rd-workspace.html` | 研发办公室、多 Employee Workstation、Context 文件树、Utility Code/Diff/Preview |
| I | Content Growth / XHS | `09-xhs-workspace.html` | 小红书运营办公室、日历/内容/数据、创作/审核 Presence、发布后 Analytics |
| J | 全局能力 | `10-global-search.html` | 全局对象搜索、搜索结果、Recent |
| K | 重要状态集 | `11-states.html` | Empty / Loading / Failure / Needs CEO / Permission / Offline / First-use / Success |

---

## 4. 资源依赖说明（Frozen 共享，不可改）

### 4.1 依赖来源

所有原型页通过**相对路径** `../_system/` 引用 Frozen 设计系统，位于本级目录的**同级**：

```
curis-ui-prototype/
├── _system/                         ← Frozen 共享设计系统（本交付的依赖，不可修改）
│   ├── tokens.css                   ← 设计令牌（被 12 个 HTML 引用）
│   ├── shell.css                    ← Workspace Shell 布局（被 12 个 HTML 引用）
│   ├── theme.js                     ← 主题切换（被 12 个 HTML 引用）
│   ├── assistant-drawer.css / .js
│   ├── canonical-nav.js             ← 旧 5 区模型，与本探索的六区冲突，故未被加载
│   ├── devmode.js
│   └── runtime-capability.js
└── coverage-exploration-2026-08-17/ ← 本交付目录
    ├── index.html + 01~11-*.html    ← 通过 ../_system/ 引用上述资源
    ├── 00-PAGE-STATE-INVENTORY.md
    ├── 01-DESIGN-TOKENS.md
    └── 03-DELIVERY.md（本文件）
```

### 4.2 实际引用清点（已自检）

- 12 个 HTML **全部**引用：`../_system/tokens.css`、`../_system/shell.css`、`../_system/theme.js`（各 12 次，无遗漏）。
- 未引用 `_system/` 下其他文件；`canonical-nav.js` 因与 Frozen 六区冲突，由 `index.html` 内联等价导航替代，**未加载**。
- `_system/` 为 **Frozen 共享资源**：**禁止复制、改写、内联进 HTML**，必须保持外部引用。任何对 `_system/` 的修改都会影响所有复用该系统的原型，不在本交付权限内。

### 4.3 浏览前置条件

- 任意 HTML 必须能在 `../_system/` 找到 `tokens.css`、`shell.css`、`theme.js`。
- **传输 / 移动时，必须连同 `_system/` 一起保留相对位置**（见第 5 节 Zip 说明），否则样式与主题切换将失效。

---

## 5. Zip 打包说明

已生成 `coverage-exploration-2026-08-17.zip`，**为保持 `../_system/` 相对引用关系，zip 顶层同时包含 `_system/` 与 `coverage-exploration-2026-08-17/` 两个同级目录**：

```
coverage-exploration-2026-08-17.zip
├── coverage-exploration-2026-08-17/   ← 12 HTML + 3 文档
└── _system/                            ← Frozen 共享设计系统（依赖）
```

**使用方式**：
1. 解压后保留 `coverage-exploration-2026-08-17/` 与 `_system/` 在同一目录下（勿拆散、勿改名）。
2. 打开 `coverage-exploration-2026-08-17/index.html` 即可浏览全部原型。
3. 若仅拷贝 `coverage-exploration-2026-08-17/` 单目录（不含 `_system/`），页面将丢失样式——此时需确保 `_system/` 仍位于其上级同级位置，或将 `_system/` 一并放入。

> 设计取舍：因原型依赖同级 `_system/`，无法将内容压成「单目录 zip 且不带 `_system/`」而不破坏引用，故采取「双目录同级打包」方案，确保解压即开箱可用。

---

## 6. 自检结论（export-specialist 验证）

| 检查项 | 结果 |
|--------|------|
| 12 个 HTML 文件全部存在 | ✅ 通过 |
| `index.html` 链接到的全部页面均可解析（无断链） | ✅ 通过（11 个内容页 + 自身） |
| `../_system/tokens.css` / `shell.css` / `theme.js` 引用路径正确且文件存在 | ✅ 通过 |
| 仅引用 Frozen 资源，无私有/内联改写 Frozen 令牌 | ✅ 通过 |
| `_system/` 未被复制或改写（保持外部引用） | ✅ 通过（未触碰任何 Frozen 文件） |
| Zip 内相对引用关系保持 | ✅ 通过（双目录同级打包） |

---

## 7. 约束遵守声明

- ❌ 未修改任何 Frozen 文件（`_system/tokens.css` 等）。
- ❌ 未修改产品代码 / 原型 HTML 本身（仅新增说明文档与 Zip）。
- ❌ 未新建 Blueprint 外的产品系统。
- ✅ 仅新增 `03-DELIVERY.md` 与 `coverage-exploration-2026-08-17.zip`（交付物），其余文件保持原样。

---

*Delivered by export-specialist（交付达）· 2026-08-17 · Coverage Exploration，非 Production Visual、非 Frozen Authority*
