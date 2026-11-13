# 前端团队结构对齐指令 · Curis v1 Desktop（Frozen IA + 页面形态对齐）

> **一句话**：令牌层（`--ui-*`）已对齐、Frozen 红线审计 error=0；但**页面结构与导航 IA 仍与 Frozen 原型不一致**（用户 2026-08-05 复审指出「前端做出来的页面跟 ui 视觉原型完全不一致」）。本次指令 = **把 `frontend/` 的导航分组、页面集合、布局骨架、空态/错误态对齐 Frozen 原型**（`curis-ui-prototype/` + `canonical-nav.js`），不改后端、不改数据逻辑。

| 项 | 内容 |
| --- | --- |
| **From** | 主理人（齐构成） |
| **To** | 前端团队 `software-frontend-align`（team-lead + 工程师 ×2 + QA） |
| **Date** | 2026-08-05 |
| **Gate** | G-前端-结构对齐（完成后需 QA 截图验收 + 主理人复核） |
| **前置基线** | 2026-08-05 已修复：`next.config.js` 默认 API_BASE 改直连 8000（8080 联动 bug）；`app/projects/[project_id]/page.js` 79 处默认调色板已迁 `ui-*`。前端可正常跑通 |

---

## 一、背景：为什么这次是「结构对齐」而不是「令牌改名」

2026-08-05 总控裁定（记忆 #10）：「**之前的前端视觉设计（`terra-*` 令牌 / `Terra*` 组件视觉）全部作废，v1 Desktop 视觉与 UI 以 Frozen `--ui-*` 为准**」。

上一轮（我，主理人）的复审只核了 **令牌层**（`Terra*` 组件内部已用 `bg-ui-*`/`text-ui-*`），就下结论「视觉迁移完成」——这是复审漏洞。用户复审后指出：

> 「前端做出来的页面跟 ui 视觉原型完全不一致，你是怎么复审的」

**用 puppeteer 截图对比后确认**：令牌层（颜色/字号/间距/圆角）已一致，但：
1. **导航 IA 不一致**：原型是 4 级分组 12 项；前端是 10 项平铺，命名与集合几乎对不上
2. **页面集合不一致**：原型有「财务/日历/会议工作台」前端没有；前端有「能力中心/执行工作台/公司运行视图」原型没有
3. **布局骨架不一致**：原型侧栏有分组 label（公司/经营工具/公司资源）+ 底部设置；前端分组结构不同
4. **页面形态不一致**：部分页面（如 projects/[project_id]）曾是浅色异类（已修复），但整体页面结构与原型（卡片层级/信息密度/轨迹行）仍有差距

**本次指令解决的是 1–4（结构层）**。令牌层不动（已达标）。

---

## 二、权威真源（唯一，禁止另立）

| 用途 | 路径 |
| --- | --- |
| **Frozen 侧栏 IA 合同（唯一导航真源）** | `curis-ui-prototype/_system/canonical-nav.js`（NAV_MODEL 定义 + 分组渲染逻辑） |
| **Frozen 视觉规格（验收合同）** | `docs/03_Design/Curis_UI_Frozen_Spec_2026-08-04.md` |
| **冻结令牌真源** | `curis-ui-prototype/_system/tokens.css`（全部 `--ui-*`） |
| **高保真原型页面（视觉细节参考）** | `curis-ui-prototype/*.html`（ceo-desk / operating / business / ai-organization / workspace-portal / decision-room / meeting / finance / calendar / knowledge / assets / founding-flow） |
| **前端现有导航数据源（要改造的目标）** | `frontend/components/terra/TerraNavData.js` |
| **前端现有壳层** | `frontend/components/terra/TerraShell.js` / `TerraSidebar.js` / `TerraPrimitives.js` |
| **Dev Mode 标注** | `curis-ui-prototype/_system/devmode.js`（`?dev=1` / `Shift+D` 悬停看尺寸/间距/令牌） |

> ⚠️ 原型是 **localStorage mock**，不是源码；前端按 Frozen 规格**重建**，不要逐行搬 HTML。

---

## 三、目标 IA（Frozen 原型，对齐到这份）

来自 `canonical-nav.js` NAV_MODEL（权威）：

```
公司       ：CEO 工作台 / 经营 / 业务 / AI 团队 / 工作空间
经营工具   ：会议工作台 / 决策室
办公室     ：（动态：已配置业务空间的部门办公室，按状态生成）
公司资源   ：成果库 / 知识库 / 财务 / 日历
（底部固定）设置 / 帮助
```

前端**必须**按此分组重排侧栏。已存在的路由做**映射**（不是删路由），原型有而前端没有的页面**按需新增**（见 §五 映射表）。

---

## 四、当前状态与差距清单（前端侧，已核）

### 前端当前导航（TerraNavData，10 顶平铺）
```
总裁办公室 / 项目中心 / 组织中心 / 能力中心 / 经营分析 / 头脑风暴室 / 知识中心 / 执行工作台 / 公司设置 / 公司运行视图
```

### 差距（对照 §三 目标）
| 维度 | 原型 | 前端现状 | 动作 |
| --- | --- | --- | --- |
| 分组 | 公司 / 经营工具 / 办公室 / 公司资源 四级 | 10 项平铺，无分组 label | **按原型分组重排** |
| 命名 | CEO 工作台 / 经营 / 业务 / AI 团队 | 总裁办公室 / 经营分析 / 组织中心 / 能力中心 | **重命名映射**（见 §五） |
| 页面集合 | 有：会议工作台 / 财务 / 日历 | 无 | 按需新增（或明确「v1 暂不建」并记录） |
| 页面集合 | 无：能力中心 / 执行工作台 / 公司运行视图 | 有 | 保留，归入合适分组（或明确为「经营工具/公司资源」扩展） |
| 底部 | 设置 / 帮助 | 无帮助入口 | 补「设置 + 帮助」底部固定区 |

---

## 五、路由映射表（必做，防删错）

| 原型页 | 前端路由 | 动作 |
| --- | --- | --- |
| CEO 工作台（ceo-desk） | `/ceo-office` | 对齐命名与形态（现有页面保留，改分组归属） |
| 经营（operating） | `/ceo-office/analytics` | 对齐命名：可加别名「经营」或保留「经营分析」并归「公司」组 |
| 业务（business） | `/ceo-office/projects`（项目中心） | 业务方向 = 项目中心（CEO 视角） |
| AI 团队（ai-organization） | `/ceo-office/organization` | AI 团队 = 组织中心 |
| 工作空间（workspace-portal） | `/ceo-office/organization`（部门空间）或 `/ceo-office/projects` | 按原型「工作空间 = 已配置业务空间入口」落地 |
| 会议工作台（meeting） | `/ceo-office/meeting`（新增占位） | 原型有，前端无 → **新增占位页**（标注「v1 暂不建设」若确定不做） |
| 决策室（decision-room） | `/ceo-office/decisions` | 已有，归「经营工具」组 |
| 成果库（assets） | `/ceo-office/company-runtime`（公司运行视图）或 `/ceo-office/execution` | 成果库语义 = 执行成果 → 归「公司资源」组并重命名 |
| 知识库（knowledge） | `/ceo-office/knowledge` | 已有，归「公司资源」组 |
| 财务（finance） | 无 | 原型有，前端无 → **新增占位**（v1 经营日卡片已含成本信息，可先挂「财务（规划中）」） |
| 日历（calendar） | 无 | 原型有，前端无 → **新增占位**（v1 可不建，标注「规划中」） |
| 设置 | `/ceo-office/settings` | 已有，归底部固定区 |

> 原则：**不删已有功能路由**；原型有而前端无的，用「占位页 + 规划中标注」承接（符合 v1 单机自用、Blueprint §16「明确暂不建设」红线的，在占位页写明原因）；前端独有页面（能力中心/执行工作台/公司运行视图）**保留并归入最接近的分组**。

---

## 六、任务拆解（按顺序执行，T0 先行）

### T0 · 导航 IA 对齐（最高优先，单 commit）
- 改 `frontend/components/terra/TerraNavData.js`：
  - 结构改为 **分组模型**：`[{ group: "公司", items: [...] }, { group: "经营工具", ... }, { group: "公司资源", ... }, { group: "底部", ... }]`
  - 按 §五 映射表归组、重命名（如「总裁办公室」→「CEO 工作台」）
  - 保留 `findActiveNav` 的匹配逻辑（路由不变，只是分组/命名变）
- 同步 `TerraSidebar.js`：渲染分组 label（12px/600 小标题，如原型 `nav-label`）+ 底部固定「设置/帮助」区；图标沿用 TerraIcons
- **验收**：侧栏渲染 = 原型分组结构（截图对比）；`findActiveNav` 仍正确高亮当前页

### T1 · 页面形态对齐（按页面逐个 commit）
- 对 §五 映射表中的已有页面，做**形态对齐**（不是重写业务逻辑）：
  - `ceo-office/page.js`（CEO 工作台）：对齐原型 ceo-desk 的信息层级（首屏公司状态、待处理汇报、运行视图入口）
  - `ceo-office/analytics`（经营）：对齐 operating 的指标卡片/信息密度
  - `ceo-office/projects`（业务）：对齐 business 的方向卡片
  - `ceo-office/organization`（AI 团队）：对齐 ai-organization 的部门/员工空间
  - `ceo-office/knowledge`（知识库）：对齐 knowledge 页
  - 其余页按 §四 差距表逐一对齐
- **原则**：只动视觉形态与布局（className 结构、卡片层级、信息密度），**不新增 API、不改数据逻辑、不伪造数据**；空态/错误态/加载态沿用 `TerraState.js`（八态组件）
- 数据态纪律（沿用 handoff §6）：真实读取或明确快照才渲染；无数据显「未记录/未读取事实/未分配/尚未同步」；成本未知显「未记录」不得写 `$0`

### T2 · 缺失页面占位（原型有、前端无）
- 新增 `/ceo-office/meeting`、`/ceo-office/finance`、`/ceo-office/calendar` 占位页（若确认 v1 不建）：
  - 占位页 = TerraPageHead + TerraEmpty（「会议工作台 · 规划中 · v1 暂不建设（Blueprint §16）」）
  - 归入对应分组（经营工具 / 公司资源）
- 若确认要建真实页（如财务 = 经营日成本卡片聚合），另开 issue，**不在本指令默认范围**

### T3 · 侧栏全局一致性
- 清理页面内联的第二套导航（如有）；侧栏只由 `TerraShell` 渲染一次
- 检查 220px 侧栏 / 52px 顶栏在所有页面一致

---

## 七、硬约束（不可违反）

1. **不新增 API / 数据库 / Admin / 凭证 / 计费 / Workflow Runtime**（纯前端结构对齐）
2. **不引入需要 npm 安装的新依赖**
3. **令牌唯一真源**：只用 `--ui-*`（禁止引入新的私有调色板；不写 `bg-white`/`zinc-*`/`teal-*` 等 Tailwind 默认色）
4. **不伪造数据**：示例数据必须标「示例快照·未接入真实数据」；操作不伪造成功
5. **不改后端契约 / 数据逻辑 / 路由结构**（仅视觉与 IA 分组）
6. **不碰 `app/platform/*`**（Admin 独立 `--admin-*` 规格，按记忆 #10「Admin/Workspace 隔离」）
7. **一个 issue 一提交**；Git 纪律：工作树有他人未提交改动时**不得 `git add -A`**，只暂存本任务路径
8. 所有新增/修改页面**必须通过 `next build`** 与既有审计（`frontend/scripts/ui-audit.mjs`，若脚本仍可用）

---

## 八、验收标准（QA 独立复核，不信工程师自报）

1. **导航截图对比**：`TerraSidebar` 渲染 = 原型 `canonical-nav.js` 分组结构（公司/经营工具/公司资源/底部），至少 3 个页面侧栏一致
2. **页面形态截图对比**：CEO 工作台 / 经营 / 业务 / AI 团队 4 页 vs 原型同页，布局层级一致（puppeteer 1440×900）
3. **路由可用**：§五 映射表所有路由 `curl -o /dev/null -w "%{http_code}"` = 200（占位页允许 200 + 空态）
4. **令牌合规**：全 `app/` 下 `grep -cE "(bg|text|border|ring)-(zinc|teal|amber|sky|emerald|rose|red|slate|gray|neutral)-(50|100|…|950)"` = 0（Admin platform/ 除外）
5. **`next build` 通过**；无 TypeScript 错误
6. 空态/错误态/加载态：占位页与空数据页渲染正常（TerraState 组件）

---

## 九、汇报格式（回主理人）

简洁中文，含：① 创建/修改文件清单 ② 各任务（T0–T3）完成情况 ③ 截图对比结果（或截图路径）④ 路由可用清单 ⑤ 令牌合规计数 ⑥ commit hash ⑦ 风险/未决项（原型有前端无的页面取舍依据）。

---

*主理人 · 齐构成 · 2026-08-05 · 前端团队结构对齐指令 v1*
