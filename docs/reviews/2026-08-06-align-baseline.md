# 前端结构对齐 · 验收基线（T0 前快照）

> **目的**：在 T0（导航 IA 对齐）动工之前，固化当前侧栏视觉/路由/令牌三条基线，作为工程师完成 T0/T1/T2 后验收的 diff 对比基准。
> **快照时间**：2026-08-06
> **基线类型**：只读审计；未修改任何 `frontend/` 源码。
> **权威真源**：`curis-ui-prototype/_system/canonical-nav.js`（NAV_MODEL）；`docs/03_Design/Frontend_Team_Structure_Align_Handoff_2026-08-05.md`（指令 §五 映射表）。

---

## 关键数字（TL;DR）

| 维度 | 基线值 | 期望（指令 §八 验收） |
| --- | --- | --- |
| 路由可用率（§五 11 路由） | **11/11 = 100%** HTTP 200 | 100% (含占位页) |
| 令牌合规（`app/` 排除 `app/platform/`） | **0** 违规 | 0 |
| 令牌合规（`components/terra/`） | **0** 违规 | 0 |
| 截图产物 | **6 张**全部成功 | ≥3 张 |

> 路由与令牌基线 **已达标**；**结构/视觉差异**（详见 §5）需要在 T0–T3 解决。

---

## §1 路由基线表（§五 映射表全量）

测试命令：`curl --noproxy '*' -o /dev/null -w "%{http_code}" --max-time 15 http://127.0.0.1:3000<route>`

| 原型页 / 含义 | 前端路由 | 当前 HTTP | 备注 |
| --- | --- | --- | --- |
| CEO 工作台（ceo-desk） | `/ceo-office` | **200** | 现有 |
| 经营（operating） | `/ceo-office/analytics` | **200** | 现有 |
| 业务（business） | `/ceo-office/projects` | **200** | 现有 |
| AI 团队（ai-organization） | `/ceo-office/organization` | **200** | 现有 |
| 决策室（decision-room） | `/ceo-office/decisions` | **200** | 现有 |
| 知识库（knowledge） | `/ceo-office/knowledge` | **200** | 现有 |
| 成果库（assets） | `/ceo-office/company-runtime` | **200** | 现有（语义需重新对齐） |
| 设置 | `/ceo-office/settings` | **200** | 现有 |
| 能力中心（前端独有） | `/ceo-office/capabilities` | **200** | 现有 |
| 执行工作台（前端独有） | `/ceo-office/execution` | **200** | 现有 |
| 头脑风暴室（前端独有） | `/ceo-office/brainstorm` | **200** | 现有 |
| **（缺失）会议工作台** | `/ceo-office/meeting` | — | 原型有，前端无 → T2 占位 |
| **（缺失）财务** | `/ceo-office/finance` | — | 原型有，前端无 → T2 占位 |
| **（缺失）日历** | `/ceo-office/calendar` | — | 原型有，前端无 → T2 占位 |

**结论**：所有现有路由 200；缺失的 3 条（meeting/finance/calendar）当前不存在，需 T2 创建占位页（指令 §六 T2）。

---

## §2 令牌合规基线

测试命令：
```bash
grep -rEc "(bg|text|border|ring)-(zinc|teal|amber|sky|emerald|rose|red|slate|gray|neutral)-(50|100|200|300|400|500|600|700|800|900|950)" frontend/app --include='*.js' --include='*.jsx' --include='*.css'
```

| 范围 | 违规命中数 | 状态 |
| --- | --- | --- |
| `frontend/app/` 总数（含 platform） | 219 | — |
| **`frontend/app/` 排除 `app/platform/`** | **0** | ✅ 达标 |
| `frontend/components/terra/` | 0 | ✅ 达标 |
| `app/platform/` 命中明细（参考，非阻塞） | UsageDashboardPanel 19 · TenantsPanel 38 · PlanManagementPanel 28 · QuotaManagementPanel 26 · commercial/page 8 · CommercialConsolePanel 56 · BillingEventPanel 22 · ModelCatalogPanel 22 | 排除项（指令 §七.6） |

**结论**：合规基线已为 0，T0–T3 不允许新增违规。

---

## §3 原型侧栏基线（curis-ui-prototype/_system/canonical-nav.js）

### 3.1 NAV_MODEL 合同（权威，冻结）

```js
NAV_MODEL = {
  primary:   [ CEO 工作台, 经营, 业务, AI 团队, 工作空间 ]              // 5 项
  tools:     [ 会议工作台, 决策室 ]                                    // 2 项
  offices:   [ 研发办公室, 小红书运营办公室, 抖音/TikTok 运营办公室, 部门办公室 ]  // 4 项（动态）
  resources: [ 成果库, 知识库, 财务, 日历 ]                             // 4 项
  footer:    [ 设置, 帮助与反馈 ]                                      // 2 项
}
STORAGE_KEY = 'curis-prototype-state'   // 触发办公室组可见性的状态键
```

### 3.2 实际渲染（P2-2 修订版）

canonical-nav.js 在 **DOMContentLoaded** 时清空静态 `<aside class="sidebar">` 内容并重建。**默认布局**：

| 区段 | 渲染内容 | 默认可见 |
| --- | --- | --- |
| 品牌区 | "C Curis"（26×26 绿色圆角徽标 + Curis 文字） | ✅ |
| 主导航 · 常驻 4 项 | CEO 工作台 / 经营 / 业务 / 工作空间 | ✅ |
| 「更多」切换按钮 | 带 ▾ caret，aria-expanded=false | ✅ |
| 折叠面板（点击「更多」后展开） | AI 团队 · 经营工具 (会议工作台, 决策室) · 公司资源 (成果库, 知识库, 财务, 日历) · 办公室（按 localStorage 状态动态） | 默认收起 |
| 底部固定 | 设置 / 帮助与反馈（打开 CEO 助理按钮） | ✅ |

### 3.3 nav-label 视觉特征（来自 `makeSection`）

- 文本：12px 级别（`var(--ui-fs-1)`）；margin `var(--ui-sp-3) 0 var(--ui-sp-1)`；padding `0 var(--ui-sp-2)`
- 容器：`gap: var(--ui-sp-1)` 网格；`border:0`；透明背景
- 出现位置：仅在折叠面板内的「经营工具」「公司资源」「办公室」「当前栏目」上方
- 常驻 4 项上方**无** nav-label（公司组在视觉上隐式表达）

### 3.4 初始化方式（办公室组可见性）

要让「办公室」分组出现（典型 onboarding 完成态），在浏览器 console 执行：

```js
localStorage.setItem('curis-prototype-state', JSON.stringify({
  companyCreatedAt: '2026-08-05T00:00:00Z',
  firstBusiness:    '软件研发 · 小红书运营 · 抖音短视频',
  latestXhsFeedback: true,
  latestExternalFeedback: true,
  calendarEvents:   []
}));
// 然后刷新 ceo-desk.html
```

判定逻辑（`activeOffices`）：
- `/软件|Curis|研发/.test(firstBusiness)` → 研发办公室
- `/小红书/.test(firstBusiness)` 或 `latestXhsFeedback` → 小红书运营办公室
- `/抖音|TikTok|短视频/.test(firstBusiness)` 或 `latestExternalFeedback` → 抖音/TikTok 运营办公室
- `departmentStatus === 'active'` → 部门办公室

### 3.5 截图产物

| 文件 | 状态 | 内容 |
| --- | --- | --- |
| `docs/reviews/align-baseline/prototype-sidebar-default.png` | ✅ | 4 常驻 + 更多（折叠态）+ 底部设置/帮助 |
| `docs/reviews/align-baseline/prototype-sidebar-expanded.png` | ✅ | 4 常驻 + 更多展开（AI 团队/经营工具/公司资源）+ 底部 |
| `docs/reviews/align-baseline/prototype-sidebar-offices.png` | ✅ | 展开 + 办公室组（3 个动态办公室）+ 工作空间角标"3" |

截图来源：puppeteer-core 25（`/Users/yy/.workbuddy/binaries/node/workspace/node_modules/puppeteer-core`），Chrome headless 1440×900 viewport，截取 `aside.sidebar` 元素裁剪。

---

## §4 前端侧栏基线（TerraSidebar.js · 改动前）

### 4.1 数据源（`components/terra/TerraNavData.js`）

10 项平铺，**无分组**：
```
1. 总裁办公室   href=/ceo-office                       subs: 决策中心, 重要汇报, 战略会议室, 运行轨迹
2. 项目中心     href=/ceo-office/projects              subs: —
3. 组织中心     href=/ceo-office/organization          subs: 业务部门, AI 员工管理
4. 能力中心     href=/ceo-office/capabilities          subs: Agent, 模型, 技能, 工具, 工作流, 连接器, CLI, HTTP API, Webhook, MCP
5. 经营分析     href=/ceo-office/analytics             subs: 组织维度, 项目维度, Workflow 维度
6. 头脑风暴室   href=/ceo-office/brainstorm            subs: 进行中的风暴, 已沉淀成果
7. 知识中心     href=/ceo-office/knowledge             subs: 公司知识, 项目知识, 部门知识, 记忆管理
8. 执行工作台   href=/ceo-office/execution             subs: Tasks, Workflow Runs
9. 公司设置     href=/ceo-office/settings              subs: 基本资料, 品牌与显示, 通知偏好
10. 公司运行视图 href=/ceo-office/company-runtime       subs: —
```

### 4.2 渲染（`TerraSidebar.js`，220px 桌面侧栏）

- 品牌区：「C Curis OS」（注意：原型是「C Curis」——品牌文案差异 T3 待对齐）
- 导航列表：`overflow-y-auto flex-1`；一级 14px/600 + 二级 12px/500 缩进 35px
- 激活态：3px 强调线 + 浅底 `bg-ui-surface-2`；hover `bg-ui-surface-2` + `translate-x-[1px]`
- 展开/折叠：当前一级默认展开其 subs；点击右侧 chevron 切换
- 底部固定区：用户信息「齐活林 · Admin」（无设置/帮助按钮 —— 差异项）

### 4.3 截图产物（puppeteer-core，1440×900，截 `<aside>`）

| 文件 | 页面 | 激活态 |
| --- | --- | --- |
| `docs/reviews/align-baseline/frontend-sidebar-before-ceo-office.png` | `/ceo-office` | 总裁办公室（subs: 决策中心/重要汇报/战略会议室/运行轨迹）展开 |
| `docs/reviews/align-baseline/frontend-sidebar-before-analytics.png` | `/ceo-office/analytics` | 经营分析（subs: 组织维度/项目维度/Workflow 维度）展开 |
| `docs/reviews/align-baseline/frontend-sidebar-before-decisions.png` | `/ceo-office/decisions` | 总裁办公室 + sub 决策中心 高亮 |

---

## §5 关键差异（验收 diff 对照表）

| 维度 | 原型（Frozen 合同） | 前端（基线 · 改动前） | 验收方向 |
| --- | --- | --- | --- |
| **侧栏分组** | 4 级分组：公司 / 经营工具 / 公司资源 / 底部 | **10 项平铺，无分组** | T0 改 TerraNavData 为分组模型；TerraSidebar 渲染 nav-label |
| **常驻 vs 抽屉** | 默认 4 常驻 + 「更多」抽屉（P2-2 收敛） | 无抽屉，全部平铺 | T0 重排；可保留抽屉收敛形态 |
| **一级命名** | CEO 工作台 / 经营 / 业务 / AI 团队 / 工作空间 | 总裁办公室 / 经营分析 / 项目中心 / 组织中心 / 头脑风暴室 / 能力中心 / 知识中心 / 执行工作台 / 公司设置 / 公司运行视图 | T0 按 §五 映射表重命名；能力中心/执行工作台/公司运行视图/头脑风暴室 **保留**并归入最接近分组 |
| **经营工具组** | 会议工作台 / 决策室 | 仅有「决策中心」(作为总裁办公室的 sub) | T0 改 sub→分组；T2 新增 /ceo-office/meeting 占位 |
| **公司资源组** | 成果库 / 知识库 / 财务 / 日历 | 仅有「知识中心」(平铺) +「公司运行视图」(平铺，疑似成果库语义) | T0 重映射：成果库 = `/ceo-office/company-runtime`（重命名）；T2 新增 `/ceo-office/finance`、`/ceo-office/calendar` 占位 |
| **底部固定区** | 设置 / 帮助与反馈 | 仅有用户信息「齐活林 · Admin」 | T0 补「设置 + 帮助与反馈」底部区；T3 决定是否保留用户信息 |
| **品牌文案** | 「C Curis」 | 「C Curis OS」 | T3 统一 |
| **侧栏宽度** | var(--ui-sidebar-w) ≈ 220px | 220px（xl）/ 76px（lg） | 一致，保留 |
| **顶栏高度** | var(--ui-topbar-h) | 52px | 一致，保留 |

---

## §6 验收路径建议（不在本任务范围）

T0 完成后建议用同一截图脚本复核：
1. 重新执行 `/tmp/curis-qa-baseline/frontend-sidebar.js` 生成 `frontend-sidebar-after-{ceo-office,analytics,decisions}.png`；
2. 与本报告 §4 截图做并排 diff：分组 label 是否出现 / 一级命名是否变更 / 底部是否有设置·帮助；
3. 重跑 §1 路由表 + §2 令牌合规（应为 0 增 0）；
4. 占位页（meeting/finance/calendar）curl 200 + TerraEmpty 渲染验证。

---

## §7 产物清单

```
docs/reviews/align-baseline/
├── prototype-sidebar-default.png      # 原型侧栏（默认折叠）
├── prototype-sidebar-expanded.png     # 原型侧栏（点击「更多」后）
├── prototype-sidebar-offices.png      # 原型侧栏（展开 + 办公室动态组 + 工作空间角标 3）
├── frontend-sidebar-before-ceo-office.png    # 前端 /ceo-office 侧栏
├── frontend-sidebar-before-analytics.png     # 前端 /ceo-office/analytics 侧栏
└── frontend-sidebar-before-decisions.png     # 前端 /ceo-office/decisions 侧栏
```

**截图脚本**（用于 T0 后回归，可复用）：
- `/tmp/curis-qa-baseline/prototype-sidebar.js`
- `/tmp/curis-qa-baseline/frontend-sidebar.js`

---

*QA · Edward · 2026-08-06 · 只读基线建立完成，未修改任何 `frontend/` 源码*---

# T0 验收 · Round 2 验证（2026-08-06 00:20）

> 工程师-2 完成 T0 导航 IA（commit `e599a0dc`），QA 独立复核。方法：puppeteer-core 截图 + DOM 事实抽取（`frontend-facts-*.json`）。

## 关键数字（与基线对比）

| 维度 | 基线 | T0 后 | 判定 |
| --- | --- | --- | --- |
| 11 既有路由 | 11/11 = 200 | 11/11 = **200** | ✅ |
| 4 占位路由（meeting/finance/calendar/help） | — | **404**（T2 未补，符合预期） | ✅ 待 T2 |
| 令牌合规（`app/` 排除 `app/platform/`） | 0 | **0** | ✅ 0 增 0 |
| 令牌合规（`components/terra/`） | 0 | **0** | ✅ |
| 截图产物 | 6 张 before | **3 张 after + 3 份 DOM facts** | ✅ |

## 侧栏结构 diff 对比表（逐项核对 team-lead 清单）

| # | 验收项 | 期望 | 实测（DOM） | 判定 |
| --- | --- | --- | --- | --- |
| 1 | 常驻区 4 项 | CEO 工作台/经营/业务/工作空间（无 label） | 全部分组展开：公司(CEO 工作台/经营/业务/AI 团队/工作空间) + label「公司」；经营工具(会议工作台/决策室/头脑风暴室/执行工作台) + label；公司资源(成果库/知识库/财务/日历/能力中心) + label | ⚠️ **不一致**：无「4 常驻 + 折叠」默认态；而是「3 组全展开带 label」 |
| 2 | 「更多」按钮 | 存在，点击展开面板含分组 label + AI 团队/经营工具/公司资源 | `hasMoreToggle: false`（3 页均无按钮） | ❌ **缺失** |
| 3 | 底部固定 设置/帮助与反馈 | 底部「设置 / 帮助与反馈」 | footerText = 「设置 帮助与反馈 齐 齐活林 · Admin」 | ✅ |
| 4 | 品牌文案 | 「C Curis」 | brandText = 「C Curis OS」 | ❌ **不一致**（原型「C Curis」） |
| 5 | 决策室高亮（/ceo-office/decisions） | 决策室 3px 高亮；CEO 工作台不高亮 | 决策室 `has3px=true`；CEO 工作台 `has3px=false` | ✅ |
| — | 分组 label 样式 | 12px/600 小标题（原型 nav-label） | `<p class="... text-ui-1 font-semibold text-ui-txt-2">`（12px/600，Frozen 令牌） | ✅ |

## 三个页面激活态核对

| 页面 | 期望激活 | 实测 | 判定 |
| --- | --- | --- | --- |
| /ceo-office | CEO 工作台 | CEO 工作台 `has3px=true` | ✅ |
| /ceo-office/analytics | 经营 | 经营 `has3px=true` | ✅ |
| /ceo-office/decisions | 决策室 | 决策室 `has3px=true`，CEO 工作台 `false` | ✅ |

## 结论

- **通过**：11 路由 200、4 占位 404、令牌 0 增 0、底部设置/帮助、3px 激活态高亮（3 页全对）、分组 label 存在且用 Frozen 令牌。
- **待决**（需 team-lead/工程师裁决，非阻塞性但偏离原型渲染）：
  1. **无「更多」折叠按钮**：原型 canonical-nav.js P2-2 默认是「4 常驻 + 更多抽屉」；T0 实现是「3 组全展开 + label」。若验收标准是"渲染 = 原型分组结构"，需确认是否补「更多」抽屉交互，或将验收标准解释为「分组存在即可」。
  2. **品牌文案**：原型「C Curis」，前端「C Curis OS」——是否对齐（T3 或本轮顺手改）。
- 完整 audit（R1–R8 error 0）等工程师 R4 触达缺陷修完再跑。

## T0 after 截图与事实文件

```
docs/reviews/align-baseline/
├── frontend-sidebar-after-ceo-office.png
├── frontend-sidebar-after-analytics.png
├── frontend-sidebar-after-decisions.png
├── frontend-facts-ceo-office.json
├── frontend-facts-analytics.json
└── frontend-facts-decisions.json
```

---

# T0 验收 · Round 3 最终结论（2026-08-06 00:31）

> 工程师-2 完成 P2-2 折叠交互补做（commit `84e00d93`，`TerraNavData+10` / `TerraSidebar+72-20`），自报 5 项断言。QA 独立复核（puppeteer 截图 + DOM 事实 + ui-audit 双主题）。

## 1. 完整审计（R1–R8 · 21 路由）

| 主题 | error | warn | 备注 |
| --- | --- | --- | --- |
| **light** | **0** | 1 | `/login` warn 1（后端在线 404 既有缺陷，与本任务无关） |
| **dark** | **0** | 1 | 同上 |

**全部 21 路由双主题 error 0** ✅（与工程师自报一致）。

报告：`docs/reviews/2026-08-05-frontend-ui-audit.md`（最新 run 自动追加）。

## 2. 折叠交互复验（4 页面 · 默认 + 更多展开）

| 路由 | 默认态 items | 默认 3px | 默认 groupLabels | moreAria | more-open groupLabels | more-open 3px |
| --- | --- | --- | --- | --- | --- | --- |
| /ceo-office | CEO 工作台 (+subs) / 经营 / 业务 / 工作空间 / 设置 / 帮助与反馈 | CEO 工作台 | []（无 label） | false | [经营工具, 公司资源] | CEO 工作台 |
| /ceo-office/analytics | CEO 工作台 / 经营 (+subs) / 业务 / 工作空间 / 设置 / 帮助与反馈 | 经营 | [] | false | [经营工具, 公司资源] | 经营 |
| /ceo-office/decisions | CEO 工作台 / 经营 / 业务 / 工作空间 / 设置 / 帮助与反馈 | （无 — 决策室在折叠面板内） | [] | false → true | [经营工具, 公司资源] | 决策室 |
| /ceo-office/organization | CEO 工作台 / 经营 / 业务 / 工作空间 / 设置 / 帮助与反馈 | （无 — AI 团队在折叠面板内） | [] | false → true | [经营工具, 公司资源] | AI 团队 |

✅ **4 页面默认态均呈现「4 常驻 + 更多按钮（收起）」，无 group label**；点击「更多」后展开面板含 AI 团队 + [经营工具, 公司资源] label + 全量子项。

## 3. /ceo-office/organization 激活态断言

| 检查项 | 期望 | 实测 | 判定 |
| --- | --- | --- | --- |
| AI 团队 3px 高亮 | ✅ | AI 团队 `has3px=true` | ✅ |
| 工作空间 不高亮 | ✅ | 工作空间 `has3px=false` | ✅ |
| 工作空间 href | /ceo-office/organization | /ceo-office/organization（同路由合并） | ✅（v1 简化方案） |

## 4. Round 2 两项 ❌ 复测 → 判定

| # | Round 2 ❌ | Round 3 实测 | 判定 |
| --- | --- | --- | --- |
| a | hasMoreToggle = false | `hasMoreToggle: true`（4 页全有 button，aria-expanded 初始 false，点击变 true） | ✅ **已修复** |
| b | brandText = 「C Curis OS」 | brandText = 「C Curis」（4 页全测一致，logo mark 「C」+ 文本「Curis」） | ✅ **已修复** |

## 5. 路由回归

11 既有路由全 200（与 Round 2 一致，无回退）：`/ceo-office, /ceo-office/analytics, /ceo-office/projects, /ceo-office/organization, /ceo-office/decisions, /ceo-office/knowledge, /ceo-office/company-runtime, /ceo-office/settings, /ceo-office/capabilities, /ceo-office/execution, /ceo-office/brainstorm`。

## 6. 最终结论：T0 ✅ 通过收官

- **Round 2 两项 ❌ 已全部修复**（折叠按钮存在、品牌 C Curis）
- **审计双主题 21 路由 error 0**（仅遗留 /login 后端 404 warn，与本任务无关）
- **4 路由折叠交互实测与代码 + 视觉 + DOM 三方一致**：默认「4 常驻 + 更多收起」，展开「AI 团队 + [经营工具, 公司资源] 分组 label + 全量子项」
- **激活态 4 路由全对**（CEO 工作台/经营/决策室/AI 团队 各自正确 3px 高亮，工作空间在 organization 页正确不高亮）
- **11 路由 200、令牌 0 增 0**

### 已知残留（非阻塞，可后续 T3 处理）
- 原型 canonical-nav.js 在折叠页（decisions/organization）默认展开时会渲染「当前栏目」内联高亮段，保证 WCAG 2.4.3「当前位置可见」。前端 T0 未实现该内联段，故在折叠页的默认态侧栏无 3px 高亮，需点击「更多」展开后才能看到当前项高亮。是否补「当前栏目」段由主理人/工程师裁决（建议留 T3 或后续工作空间拆分时一起处理）。

## 7. Round 3 产物

```
docs/reviews/align-baseline/
├── frontend-sidebar-after-ceo-office.png         # 默认（4 常驻 + 更多收起）
├── frontend-sidebar-after-ceo-office-more.png    # 展开（AI 团队 + 经营工具 + 公司资源）
├── frontend-sidebar-after-analytics.png
├── frontend-sidebar-after-analytics-more.png
├── frontend-sidebar-after-decisions.png
├── frontend-sidebar-after-decisions-more.png
├── frontend-sidebar-after-organization.png       # 新增（激活态断言）
├── frontend-sidebar-after-organization-more.png  # 新增（AI 团队高亮）
├── frontend-facts-ceo-office-r3.json
├── frontend-facts-analytics-r3.json
├── frontend-facts-decisions-r3.json
└── frontend-facts-organization-r3.json
```

---

# T2 + 当前栏目 · Round 4 复核（2026-08-06 00:41）

> 工程师-2 完成 T2 占位页（commit `1670d74c`，4 文件）+ 当前栏目内联段（commit `0d9ec978`，TerraSidebar +28-5）。QA 独立复核（curl + puppeteer DOM/console + ui-audit 双主题）。

## 1. 4 占位路由

| 路由 | curl HTTP | TerraEmpty（规划中/暂不建设） | Blueprint §16 说明 | consoleErrors |
| --- | --- | --- | --- | --- |
| /ceo-office/meeting | **200** | ✅ | ✅ | 0 |
| /ceo-office/finance | **200** | ✅ | ✅ | 0 |
| /ceo-office/calendar | **200** | ✅ | ✅ | 0 |
| /ceo-office/help | **200** | ✅ | ✅ | 0 |

## 2. 当前栏目内联段（WCAG 2.4.3 · 4 项断言）

| # | 检查项 | 期望 | 实测 | 判定 |
| --- | --- | --- | --- | --- |
| 1 | /ceo-office/decisions 默认态 | 出现「当前栏目」内联单条：决策室 3px + aria-current=page | 默认 items 含内联 决策室 `has3px=true` `ariaCurrent=page`；groupLabels=[当前栏目] | ✅ |
| 2 | /ceo-office/organization 默认态 | 内联 AI 团队 3px + aria-current；工作空间不高亮 | 内联 AI 团队 `has3px=true` `ariaCurrent=page`；工作空间 `has3px=false` | ✅ |
| 3 | /ceo-office/analytics 默认态 | 常驻页不应出现内联段 | groupLabels=[]、inlineCurrent=null；经营 已有 3px 高亮 | ✅ |
| 4 | 点开「更多」后同名项 | 面板内同名项不双高亮 | decisions：内联决策室 3px，面板决策室 `has3px=false`；organization：内联 AI 团队 3px，面板 AI 团队 `has3px=false` | ✅ |

## 3. 完整审计（R1–R8 · 21 路由）

| 主题 | error | warn |
| --- | --- | --- |
| light | **0** | 1（/login 后端 404 既有） |
| dark | **0** | 1（同上） |

报告：`docs/reviews/2026-08-05-frontend-ui-audit.md`

## 4. 结论：T0/T2 批次 ✅ 全部通过

- 4 占位路由 200 + TerraEmpty「规划中」+ Blueprint §16 说明 + 0 console error
- 当前栏目内联段 4 项断言全过（WCAG 2.4.3 当前位置可见已补齐，无双高亮）
- 审计双主题 error 0
- 无新增违规令牌（占位页仅 --ui-*，未碰 app/platform）

## 5. Round 4 产物

```
docs/reviews/align-baseline/
├── frontend-page-{meeting,finance,calendar,help}-r4.png      # 4 占位页截图
├── frontend-placeholder-{meeting,finance,calendar,help}-r4.json
├── frontend-sidebar-after-{ceo-office,analytics,decisions,organization}-r4.png        # 默认态
├── frontend-sidebar-after-{ceo-office,analytics,decisions,organization}-r4-more.png   # 更多展开
└── frontend-facts-{ceo-office,analytics,decisions,organization}-r4.json
```

---

# T1 总验收 · Round 5（2026-08-06 00:57）

> 工程师双线 T1 全部提交。QA 独立复核（puppeteer 1440×900 截图对比 + DOM + ui-audit + token + route + data-state）。

## 1. 6 页截图对比（原型 vs 前端 · 1440×900）

| 页 | 前端路由 / 原型 | 关键对齐点 | 数据态 | 判定 |
| --- | --- | --- | --- | --- |
| **ceo-office** | `/ceo-office` ← `ceo-desk.html` | 首屏公司状态（公司名 + 经营日 + 状态 pill + 3 facts 卡片）+ 今日经营 + 公司脉搏（4 卡） + CEO 业务全景 + 重点项目 + 「运行视图」入口 | 5 业务部门/18 AI 员工/6 项目（真实 workspace）；任务完成率 0.0%（真实） | ✅ |
| **analytics** | `/ceo-office/analytics` ← `operating.html` | 公司脉搏 4 指标卡（业务部门/AI 员工/项目总数/阻塞项目）+ 维度 tabs（组织/项目/工作流）+ 部门快照 | 每卡标注"来自工作区 X 数据"；阻塞项目 0（真实）；负责人"未分配人" | ✅ |
| **projects** | `/ceo-office/projects` ← `business.html` | 业务推进过程 5 步条（1 确定方向→2 开始执行→3 真实反馈→4 决定下一步→5 下一 bet）+ 部门卡（按业务部门组织项目）+ 标签过滤 | 9 个项目（真实 graph IDs）；负责人"未分配负责人" | ✅ |
| **organization** | `/ceo-office/organization` ← `ai-organization.html` | AI Workforce Map（公司/业务部门/AI 员工三层 grid）+ 责任矩阵（每部门含员工数·项目数） | 部门/员工/项目均来自当前 Workspace 真实记录；公司/部门职责"未记录" | ✅ |
| **knowledge** | `/ceo-office/knowledge` ← `knowledge.html` | 4 指标条（可引用资料/最近更新/已连接来源/待确认来源）+ 双栏（公司资料 / 外部来源）+ 使用方式 | 0 条资料（真实计数）；最近更新"未记录"/过去 7 天；已连接来源"尚未配置"；"暂无真实资料" | ✅ |
| **company-runtime** | `/ceo-office/company-runtime` ← `assets.html` | 4 指标卡（已验证成果/可复用工作流/已连接来源/待补证据）+ 所有成果（按业务筛选 tabs）+ 空态 + 入口 | **「未读取事实」**（非假数字）；footer「不填假数字」明确策略；空态 + 「前往设置接入运行端点」 | ✅ |

> 全部 6 页布局层级 + 信息密度对齐原型；数据来源标注或显式空态，无伪造数据。

## 2. 完整审计（R1–R8 · 21 路由）

| 主题 | error | warn |
| --- | --- | --- |
| **light** | **0** | 1（/login 后端 404 既有） |
| **dark** | **0** | 1（同上） |

## 3. 路由回归（15 条 · 含占位）

`/ceo-office, /ceo-office/{analytics, projects, organization, decisions, knowledge, company-runtime, settings, capabilities, execution, brainstorm}` 全部 **200**；4 占位 `/ceo-office/{meeting, finance, calendar, help}` 全部 **200**。

## 4. 令牌合规

| 范围 | 违规命中 | 判定 |
| --- | --- | --- |
| `frontend/app/`（排除 `app/platform/`） | **0** | ✅ |
| `frontend/components/terra/` | **0** | ✅ |

## 5. 数据态抽查（重点 company-runtime / knowledge）

| 页 | 检查项 | 实测 | 判定 |
| --- | --- | --- | --- |
| company-runtime | 4 指标卡无数据时是否用「未读取事实」而非假数字 | 已验证成果/可复用工作流/已连接来源/待补证据 **均显示「未读取事实」** | ✅ |
| company-runtime | 是否显式说明数据态策略 | footer 标「成果库运行事实当前未读取时统一显示『未读取事实』，不填假数字」 | ✅✅ |
| knowledge | 最近更新/待确认来源是否显「未记录」 | 最近更新 **未记录（过去 7 天）**；待确认来源 **未记录（权限或引用范围未确认）** | ✅ |
| knowledge | 已连接来源空态 | **「尚未配置」** + 「尚未配置外部来源·文件导入不可用，你可手工新建资料」 | ✅ |
| projects | 负责人无分配时是否显「未分配」 | 所有项目卡 `负责人：未分配负责人`（不显示人名） | ✅ |
| analytics | 部门无负责人时是否显「未分配人」 | 部门快照每个部门 `未分配人` | ✅ |

## 6. 结论：T1 总验收 ✅ 通过收官

- 6 页全部布局 + 信息密度对齐原型
- 审计双主题 21 路由 error 0
- 15 路由全 200（含 4 占位）
- 令牌 0 增 0
- 数据态纪律执行严格：company-runtime 用「未读取事实」+ 显式「不填假数字」策略，最佳示范；knowledge/projects/analytics 空态诚实

T1 收官。Sidebar T0、占位页 T2、页面形态 T1 全部交付。

## 7. Round 5 产物

```
docs/reviews/align-baseline/
├── t1-frontend-{ceo-office,analytics,projects,organization,knowledge,company-runtime}.png       # 6 前端截图
├── t1-frontend-{...}-text.txt                                                                    # 6 DOM 文本摘录
├── t1-prototype-{ceo-office,analytics,projects,organization,knowledge,company-runtime}.png       # 6 原型截图
└── t1-prototype-{...}-text.txt                                                                   # 6 原型 DOM 文本摘录
```

---

# T3 + 全站终验 · Round 6（2026-08-06 01:05 · 收官）

> 工程师-2 移除死代码 `components/Sidebar.js`（commit `d44465c9`，1 文件 -54 行，全仓库 0 引用）。QA 最终独立复核。

## 1. T3 回归（Sidebar.js 移除后全站无影响）

| 抽查页 | TerraShell（aside） | 顶栏 header | nav + 更多按钮 | 4 常驻 | 当前栏目内联 | 判定 |
| --- | --- | --- | --- | --- | --- | --- |
| /ceo-office | ✅ | ✅ | ✅ | CEO 工作台/经营/业务/工作空间 | —（常驻页无内联） | ✅ |
| /ceo-office/organization | ✅ | ✅ | ✅ | 同上 | AI 团队（WCAG 2.4.3） | ✅ |
| /ceo-office/meeting（占位） | ✅ | ✅ | ✅ | 同上 | 会议工作台 | ✅ |

> 侧栏仍只由 TerraShell/TerraSidebar 渲染一次；无第二套导航残留。`components/Sidebar.js` 已删除、0 引用、0 回归。

## 2. 壳层一致性（4 占位页）

| 路由 | aside | header | nav+更多 | 4 常驻 | 判定 |
| --- | --- | --- | --- | --- | --- |
| /ceo-office/meeting | ✅ | ✅ | ✅ | ✅ | ✅ 无裸页 |
| /ceo-office/finance | ✅ | ✅ | ✅ | ✅ | ✅ |
| /ceo-office/calendar | ✅ | ✅ | ✅ | ✅ | ✅ |
| /ceo-office/help | ✅ | ✅ | ✅ | ✅ | ✅ |

## 3. 最终全站验收快照

| 维度 | 结果 | 判定 |
| --- | --- | --- |
| ui-audit **light**（21 路由） | error **0** · warn 1（/login 既有） | ✅ |
| ui-audit **dark**（21 路由） | error **0** · warn 1（同上） | ✅ |
| 路由全量（15 条：11 既有 + 4 占位） | 全部 **200** | ✅ |
| 令牌合规 `app/`（排除 platform） | **0** | ✅ |
| 令牌合规 `components/terra/` | **0** | ✅ |

## 4. 孤儿路由记录（存档，不处理）

工程师报告 `app/org-center/*` 为旧 IA 遗留独立页（0 TerraShell、不在任何导航）。QA 独立核验，**修正该观察**：

- `app/org-center/page.js`、`app/org-center/dept/[deptId]/page.js`、`app/org-center/emp/[empId]/page.js` **均为 `redirect()` 桩**，分别重定向到：
  - `/org-center` → `/ceo-office/organization`
  - `/org-center/dept/x` → `/ceo-office/organization`
  - `/org-center/emp/x` → `/ceo-office/organization/employees`
- 即旧 URL 已转为深链重定向（HTTP 200，Next prerender 桩），**不属裸页**；导航中无对应项（符合"不在任何导航"）
- **建议**：无需额外处理，保留为兼容旧深链；如需彻底清理可另开 issue 归档 `app/org-center/` 目录（低优先）
- **补充观察**：`app/projects/[project_id]/page.js` 是唯一无 TerraShell 也无 redirect 的旧遗留页（旧暗色项目运行页），不在导航中；建议另开 issue（不在本批次范围）

## 5. 结论：结构对齐批次（T0/T1/T2/T3）✅ 全部收官

- T0 导航 IA（4 常驻 + 更多折叠 + 分组 label + 底部设置/帮助 + 当前栏目 WCAG 2.4.3）✅
- T1 页面形态（6 页）✅ · T2 占位页（4 页）✅ · T3 死代码清理 ✅
- 审计双主题 error 0、15 路由全 200、令牌 0 增 0、壳层全站一致

## 6. Round 6 产物

```
docs/reviews/align-baseline/
├── t3-shell-{meeting,finance,calendar,help}.png   # 4 占位页壳层截图
```
