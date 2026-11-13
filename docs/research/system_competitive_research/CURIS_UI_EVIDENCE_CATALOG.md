# CURIS UI EVIDENCE CATALOG（当前实现证据清单）

> 目的：为后续 UI 审计（竞品研究 / Final UI Master 恢复）提供「当前已实现」证据的唯一入口。
> 生成日期：2026-09-12。范围：frontend/、curis-ui-prototype/、docs/reviews/ 截图资产、四份权威文档摘要、backend/ 与 desktop/ 定位。
> 约束：本文只编目证据，不创建新 Product Truth、不冻结任何视觉。所有路径均为绝对路径（根目录 `/Users/yy/Documents/Curis AI Workspace`，下文省略写为 `ROOT/`，实际引用时请补全）。
> ROOT = `/Users/yy/Documents/Curis AI Workspace`

---

## 1. 当前已实现前端（frontend/）

### 1.1 技术栈与文件组织

- 框架：Next.js App Router（无 tsx，全部 `.js`），Tailwind CSS。入口 `ROOT/frontend/app/layout.js`，`metadata.title = "Curis CEO Office"`，`lang="zh-CN"`，`data-theme="system"`，主题持久化到 `localStorage.curis.theme`。
- Layout 包裹顺序：`RuntimeProvider`（ROOT/frontend/components/runtime/RuntimeProvider.js）→ `GlobalAssistantProvider`（ROOT/frontend/components/assistant/GlobalAssistant.js）→ 页面 → `DevMode`（Frozen 令牌合规标注层，ROOT/frontend/components/terra/DevMode.js）。
- 目录：`ROOT/frontend/app/`（路由）、`ROOT/frontend/components/`（terra/v1/runtime/workspace/rd/xhs/assistant）、`ROOT/frontend/lib/`（api、v1FrontendApi、runtimeApi、knowledge 等）、`ROOT/frontend/design-spec/`（UI规范交付模板.md、ceo-office/、curis-ui-v2/）、`ROOT/frontend/docs/`（FRONTEND_HANDOFF.md、ceo-ui-v2-system-design.md）、`ROOT/frontend/ceo-evidence/`（独立 vite/tailwind 小应用）。

### 1.2 路由清单（route path → 页面 → 主要组件/内容）

**顶层/流程类**
| 路由 | 页面 | 说明 |
| --- | --- | --- |
| `/` | 根入口 | ROOT/frontend/app/page.js |
| `/welcome` | Welcome/App Entry | 使用 `components/v1/AppEntry.js` |
| `/login` | 登录 | |
| `/guide` | 引导 | |
| `/onboarding` | Onboarding | |
| `/dev-console` | 开发控制台 | |
| `/control/secret-vault` | 密钥库 | |

**CEO Office 主区（`/ceo-office/*`）**，均位于 ROOT/frontend/app/ceo-office/：
| 路由 | 页面 | 关键组件 |
| --- | --- | --- |
| `/ceo-office` | CEO 工作台（首页） | page.js |
| `/ceo-office/analytics` | 经营洞察/Operating Intelligence | OperatingIntelligence.js（含内联 #806BE5） |
| `/ceo-office/business` | 业务版图 | page.js |
| `/ceo-office/organization` | 组织中心（公司版图/员工目录） | OrganizationCenter.js + CompanyFormDrawer/DepartmentFormDrawer + organizationCenter.module.css（--org-accent: #806be5） |
| `/ceo-office/organization/departments/[id]` | 部门详情 | + CreateEmployeeDrawer |
| `/ceo-office/organization/employees`、`/employees/[id]` | 员工目录/详情 | EmployeeFormDrawer、EmployeeEditDrawer |
| `/ceo-office/talent-market` | 人才市场 | page.js |
| `/ceo-office/workspace` | 工作空间门户 | page.js |
| `/ceo-office/workspace/studio` | 工作空间搭建 | page.js |
| `/ceo-office/workspace/department`、`/department/[id]` | 部门工作面 | page.js |
| `/ceo-office/workspace/installed/[workspaceId]` | 已安装工作空间运行时 | + `components/workspace/InstalledWorkspaceRuntime.js` |
| `/ceo-office/workspace/xhs`、`/shortvideo`、`/software` | 小红书/短视频/研发专业面 | page.js（+ `components/xhs/XhsWorkspacePhaseOne.js`、`components/rd/RdWorkspacePhaseTwo.js` 等） |
| `/ceo-office/meeting` | 会议工作台 | page.js（含内联 #806BE5、Start Meeting Overlay） |
| `/ceo-office/decisions` | 决策室 | page.js |
| `/ceo-office/knowledge`、`/knowledge/entries/[id]`、`/knowledge/memory` | 资料库/条目/记忆 | page.js |
| `/ceo-office/company-runtime` | 成果库（Company Runtime） | page.js |
| `/ceo-office/conversation` | 会话 | page.js |
| `/ceo-office/strategy-room` | 策略室 | page.js |
| `/ceo-office/brainstorm`、`/brainstorm/sessions/[id]` | 头脑风暴 | page.js |
| `/ceo-office/calendar` | 日历 | page.js |
| `/ceo-office/finance` | 财务 | page.js |
| `/ceo-office/reports`、`/reports/[id]` | 报告 | page.js |
| `/ceo-office/execution`、`/execution/tasks/[id]`、`/execution/runs/[id]`、`/execution/pipeline(/[taskId])` | 旧执行/任务/流水线（legacy） | page.js |
| `/ceo-office/projects`、`/projects/[id]` | 旧项目（legacy） | + ProjectFormDrawer/TaskFormDrawer/ContentRunDrawer/DevelopmentRunDrawer |
| `/ceo-office/settings`、`/ceo-office/help` | 设置/帮助 | page.js |
| `/ceo-office/capabilities`（+ `[type]/[id]`） | 能力管理 | CapabilityFormDrawer、PrivateAgentDrawer、PrivateModelDrawer、ResourceBindingPanel |
| `/ceo-office/runtime-trace` | 运行时追踪 | page.js |

**其他独立路由**
| 路由 | 页面 |
| --- | --- |
| `/capabilities` | 能力（顶层） |
| `/employees` | 员工（顶层，EmployeeFormDrawer） |
| `/org-center`、`/org-center/dept/[deptId]`、`/org-center/emp/[empId]` | 组织中心独立入口 |
| `/projects`、`/projects/[project_id]` | 项目运行时视图（projectRuntimeViewModel.mjs） |
| `/platform`（+ commercial、results） | Admin 平台控制台（TenantsPanel、GatewayPanel、ModelCatalogPanel、QuotaManagementPanel、BillingEventPanel、AuditEventPanel、UsageDashboardPanel、CommercialConsolePanel 等） |

### 1.3 全局壳（Shell / 导航 / Assistant / Composer）

- **TerraShell**（ROOT/frontend/components/terra/TerraShell.js）：顶层壳（nav + main + topbar）。响应式：Desktop ≥1280 常驻 220px 侧栏；Tablet 1024–1279 为 76px 图标态（汉堡按钮）；Mobile <1024 为 286px 抽屉。内含主题切换、`return_to` 返回参数、`TerraPaneContent`（页面声明 Context/Utility pane 内容）与 WorkspacePaneShell 集成。
- **TerraSidebar + TerraNavData**（同目录）：导航分组为「公司」组（CEO 工作台 `/ceo-office`、经营 `/ceo-office/analytics`、业务版图 `/ceo-office/business`、AI 团队 `/ceo-office/organization`（sub：人才市场）、工作空间 `/ceo-office/workspace`）+ 会议工作台、决策室；MORE 折叠组（成果库 `/ceo-office/company-runtime`、知识库、财务、日历）；底部 设置/帮助与反馈；另有 legacy 项「旧项目/旧执行/旧任务流水线」。支持展开/折叠持久化、active 匹配逻辑。
- **WorkspacePaneShell（Four-Pane）**（ROOT/frontend/components/workspace/WorkspacePaneShell.js）：Navigation + Context（260px）+ Main + Utility（360px）四Pane职责；Context/Utility 默认折叠，按需出现；偏好持久化在 `localStorage.curis.workspace-pane.*`；内部复用 V1Sidebar。
- **GlobalAssistant（全局悬浮 CEO 助理）**（ROOT/frontend/components/assistant/GlobalAssistant.js）：跨路由悬浮层，消费 `lib/v1FrontendApi.js` 的 `getCEOAssistantConversation / sendCEOAssistantMessage / getCompanyAttention`；canonical identity（名称/头像/role/canonical_ref）+ SharedConversation 复用；接受页面通过 `useAssistantPageContext` 注入的安全结构化上下文。
- **Composer**：共享会话组件 ROOT/frontend/components/v1/SharedConversation.js、EmployeeConversation.js、ConversationQuickAccess.js；RD 侧有 RdRealExecutionComposer.js。
- **Terra 基础件**：TerraIcons.js（SVG sprite）、TerraPrimitives.js、TerraConfirm.js、TerraState.js、TerraResourcePicker.js、TaskLauncher.js、FirstRunGate.js、RuntimeCapabilitySwitcher.js、PipelineGraphView.js。

### 1.4 代码中实际生效的设计 Token

- **视觉真源**：ROOT/frontend/app/globals.css 顶部 `FROZEN DESIGN TOKENS — Curis v1 Desktop`，注释指明权威文件为 ROOT/docs/03_Design/Curis_UI_Frozen_Spec_2026-08-04.md，`--ui-*` 为唯一视觉真源；旧 `ceo-*` 变量已桥接到 `--ui-*`（globals.css 内注释，2026-08-05 总控裁定）。
- 暗色（默认，`[data-theme="dark"]` / :root）：`--ui-bg #1a1c1f`、`--ui-surface #222529`、`--ui-surface-2 #2b2f34`、`--ui-line #343940`、`--ui-text #f3f4f6`、`--ui-text-2 #a7adb6`、**`--ui-accent / --ui-action-primary-bg #32f08c`（亮绿）**、`--ui-success #3fcf86`、`--ui-warning #d89a3a`、`--ui-danger #e57373`、`--ui-sidebar-w 220px`、`--ui-topbar-h 52px`。
- 亮色（`[data-theme="light"]` / system-light）：`--ui-bg #f5f5f7`、`--ui-surface #ffffff`、`--ui-surface-2 #f7f8fa`、`--ui-line #e5e7eb`、`--ui-text #1a1c1f`、`--ui-action-primary-bg #30333a`、`--ui-accent #1a1c1f`。
- 字体：`--ui-font: "Inter", system-ui, -apple-system, "PingFang SC", "Microsoft YaHei", sans-serif`；`--ui-mono: "SF Mono", ui-monospace, ...`。字号 7 档 `--ui-fs-1..7 = 12/13/14/16/20/24/28px`（html 钉死 7 档）；行高 1.25/1.5/1.7。
- 圆角 5 档 `--ui-r-xs/sm/md/lg/pill = 4/8/12/16/999px`（另有 `--ui-radius 12px`、`--ui-radius-sm 8px`）；间距 8 档 `--ui-sp-1..8 = 4/8/12/16/20/24/32/48px`；阴影 3 档；控件高 32/36/40px；触达下限 32px；z-index 0–500（+ devmode 9000）；动效 120/200/320ms + reduced-motion 全关。
- **Admin 控制台独立 token 组**（同文件）：`--admin-*` 冷色中性 + 专业蓝 `--admin-accent #2563eb`，与 CEO 端绿色系刻意区分。
- **Tailwind 桥接**（ROOT/frontend/tailwind.config.js）：`ui.*` 颜色命名空间全部指向 Frozen CSS 变量（含 `ui-primary-fg` 对比度红线注释）；`SPACE_SNAP` 把 Tailwind 半档间距（0.5/1.5/2.5/3.5/4.5/7/9/10/11）吸附到 Frozen 8 档；`fontSize`/`borderRadius` 把 Tailwind 默认名映射到 Frozen 档位（如 `lg→20px`、`md→8px`）；保留旧 `curis` 别名（ink #172126、teal #0f766e、line #dce4e7）。
- **⚠️ 残留旧品牌色 #806BE5**：出现于 `ROOT/frontend/app/ceo-office/organization/organizationCenter.module.css`（`--org-accent: #806be5`）、`ROOT/frontend/app/ceo-office/meeting/page.js`（焦点边框/选中态内联类）、`ROOT/frontend/app/ceo-office/analytics/OperatingIntelligence.js`。与下方 Visual Standard V1 的 Iris 主品牌色一致，但与 globals.css 的 Frozen 绿色 `#32f08c` 并存 —— 代码中存在**两套 accent（绿 #32f08c 与 Iris #806BE5）未完成迁移**，审计时必须逐页区分。

### 1.5 视觉风格所在位置

- 全局：ROOT/frontend/app/globals.css（Frozen token + admin 体系 + 响应式辅助类）。
- 局部：唯一 CSS Module 为 ROOT/frontend/app/ceo-office/organization/organizationCenter.module.css；其余页面用 Tailwind 原子类 + 大量内联 hex（尤其 #806BE5、#1d232a、#7c8794、#d9dde3 等 Iris/Neutral 值直接写死在 JSX）。
- 设计规范参考：ROOT/frontend/design-spec/（UI规范交付模板.md、curis-ui-v2/）与 ROOT/frontend/docs/ceo-ui-v2-system-design.md。

---

## 2. 原型表面（ROOT/curis-ui-prototype/）

### 2.1 顶层 HTML（全部为 2026-08-03 ~ 08-05 的旧一代原型）

| 文件（ROOT/curis-ui-prototype/） | 表面 | 修改日期 |
| --- | --- | --- |
| index.html | 原型索引/入口 | 2026-08-03 |
| ceo-desk.html | 今日经营 · CEO 工作台 | 2026-08-05 |
| business.html | 业务 | 2026-08-05 |
| workspace-portal.html | 工作空间门户 | 2026-08-05 |
| workspace-shell-reference.html | 工作空间 Shell 参考 | 2026-08-05 |
| workspace-studio.html | 工作空间搭建 | 2026-08-05 |
| workspace-runtime-department.html | 部门办公室（内容增长部）Shell | 2026-08-05 |
| workspace-runtime-xhs.html | 小红书运营办公室 Shell | 2026-08-05 |
| workspace-runtime-shortvideo.html | 抖音/TikTok 运营办公室 | 2026-08-05 |
| workspace-runtime-software.html | 研发办公室 Shell | 2026-08-05 |
| knowledge.html | 知识库 | 2026-08-05 |
| meeting.html | 会议工作台（外部合作方周会） | 2026-08-05 |
| decision-room.html | 待决策事项 · 决策室 | 2026-08-05 |
| operating.html | 经营 | 2026-08-05 |
| finance.html | 财务与经营 | 2026-08-05 |
| calendar.html | 公司日历 | 2026-08-05 |
| assets.html | 成果库 | 2026-08-05 |
| ai-organization.html | AI 团队办公室 | 2026-08-05 |
| founding-flow.html | 创建公司 Founding Flow | 2026-08-05 |
| ceo-day-demo.html | CEO 的一天（真实 API 接入演示） | 2026-08-05 |
| curis-api.js / curis-prototype.js | 共享脚本 | — |

### 2.2 较新的原型子目录

- `ROOT/curis-ui-prototype/coverage-exploration-2026-08-17/`：七区覆盖探索原型，含 00-PAGE-STATE-INVENTORY.md、01-DESIGN-TOKENS.md、02-QUALITY-REVIEW.md、03-DELIVERY.md、04-FINAL-DELIVERY.md + 页面 01-ceo-desk（08-20 更新）、02-business-space、03-org-center、04-talent-market、05-library、06-meeting、07-settings、10-global-search、11-states、index.html（以上 08-17）；**08-rd-workspace、09-xhs-workspace、10-generic-workspace 为 2026-08-20 更新**（本目录中最新）。注意：同目录存在 `coverage-exploration-2026-08-17 2` 副本目录与 .zip。
- `ROOT/curis-ui-prototype/department-business-work-surface-2026-08-18/`：Department/Business Work Surface UX 探索（CURIS_DEPARTMENT_BUSINESS_WORK_SURFACE_UX_EXPLORATION.html + 01-VISUAL-VALIDATION.md、02-DELIVERY-SUMMARY.md）。
- `ROOT/curis-ui-prototype.bak/`：原型备份目录（审计时忽略）。

### 2.3 p1-preview 截图（ROOT/curis-ui-prototype/p1-preview/，37 张，light/dark 成对）

ai-organization-light/dark、assets-light/dark、business-light/dark、calendar-light/dark、ceo-day-demo-light/dark、ceo-desk-drawer-closed、decision-room-light/dark、founding-flow-light/dark、knowledge-light/dark、meeting-light/dark、operating-light/dark、workspace-portal-light/dark/drawer-open/drawer-closed、workspace-runtime-department-light/dark、workspace-runtime-shortvideo-light/dark/drawer-open/drawer-closed、workspace-runtime-software-light/dark、workspace-runtime-xhs-light/dark、workspace-studio-light/dark。覆盖 2.1 全部主要 HTML。
`ROOT/curis-ui-prototype/p0-preview/`（更早）：assets/business/meeting 各 light/dark + after-light/after-dark，共 8 张。

新旧判断：顶层 20 个 HTML + p0/p1-preview = 2026-08-05 代原型（Iris 探索前）；coverage-exploration-2026-08-17 与 department-business-work-surface-2026-08-18 = 更新一代（与 Final UI Master PAUSED 决策同期的结构参考）。

---

## 3. 截图资产清单（ROOT/docs/reviews/）

- **multi-surface-workspace-screenshots/**（多表面工作空间，frontend 实拍）：根目录 8 张 —— 01-research-1440、02-content-1440、03-employee-quick-panel-1440、04-context-collapsed-1440、05-team-scoped-view-1440、06-utility-open-1440、07-assistant-open-1440、08-default-1280x800 + test-chrome.png；子目录 **prototype/** 16 张（01-prototype-overview … 16-prototype-1280，含 research/detail、quick-panel、conversation、handoff、workstation、content、calendar、growth、assistant、team、context collapsed/restored）。
- **2026-08-08-product-audit/**：8 张 —— 01-ceo-office、02-onboarding、03-onboarding-brief、04-ceo-office-projects、05-ceo-office-organization、06-ceo-office-workspace、08-ceo-office-decisions、09-ceo-office-meeting。
- **20260810_product_ui_audit/**：7 张 —— 01-ceo-desk、02-capabilities、03-workspace-studio、04-business-map、05-ai-team、06-meeting-placeholder、07-reports-fixture。
- **20260813_current_state_product_drift_audit/**（最全的一轮 frontend 现状截图）：16 张 —— 01-ceo-office-empty、02~07 founding 流程五态 + company created、08-workspace-portal-empty、09-workspace-studio-draft、10-rd/11-xhs/13-ttk-workspace-runtime-empty、12-xhs-content-item、analytics、business-map、calendar、company-runtime、decisions、finance、help、knowledge、meeting、organization、settings。
- **align-baseline/**：frontend/prototype 侧栏与页面比对（frontend-sidebar-before/after-*、frontend-page-*-r4、prototype-sidebar-*、t1-frontend-*、t1-prototype-*、t3-shell-*），约 40 张。
- **content-workspace-audit-2026-08-09/**：5 张（xhs/ttk runtime、pipeline、approval-bypass）。
- **workspace-engineering-p0-2026-08-16/**：7 张 desktop 桌面端 JPG（main-surface、utility-surface、context-main-utility、dynamic-navigation、restart-recovery、customer-feedback-created、uninstall-navigation-removed）。
- **workspace-engineering-p05-2026-08-16/**：2 张（company-integration before/after restart PNG）。
- 其余目录（20260813_product_rebaseline、content-workspace-runtime-review、frontend-target-alignment、next-stage-product-plan-evoflow、runtime-foundation-review、three-business-runtime-simulation-plan、ui-runtime-migration-review、workspace-engineering-p1-lifecycle、workspace-engineering-p15-migration）以 MD 评审文档为主，未见 PNG。

---

## 4. 权威文档摘要（仅以下四份）

### 4.1 ROOT/docs/01_Product/CURIS_PRODUCT_STRUCTURE_BASELINE_PRE_DESIGN_RESEARCH.md（Frozen，2026-09-10，唯一产品结构基线）

- **§2 七个一级产品区**：CEO 工作台、业务空间、组织中心、人才与能力、经营洞察、资料库、会议，固定为七个；Conversation Quick Access、CEO Assistant、搜索、最近工作、通知、模型与设置是全局 utility，不占第八区；视觉研究不得增删一级区。
- **§3 Company OS**：`Company → Department → Business → Workspace` 单一 canonical 关系；Business 是持续经营身份、Workspace 是实际工作空间，不得混淆；新 Company 出厂即含原装组织：CEO、同一 canonical CEO Assistant、空间工程部（6 名 canonical Employee：空间工程负责人、行业研究专家、经营方法专家、空间设计专家、搭建实施专家、质量验证专家）、数据分析部（至少 1 名 Company Analyst，默认名「司衡」）；原装组织不是 Demo。
- **§4 Employee 模型**：Official Definition → Company Instance → Current Responsibility Holder，禁止第二真源；Employee 是真实员工身份（Identity/Department/Role/Responsibility/Capability/Skill/Model/Work Surface/Current Work/Result/Conversation）；领导链 CEO → Team Leader → Employees，Leader 负目标/分工/整合，CEO 只负责 Goal、Strategy 与 Decision Gate，不管 DAG/路由。
- **§5 Business 激活与 Workspace 形态**：CEO intent → Company → reuse/propose Business → Decision Gate → Department/Business → first Workspace → Team → Operating；Generic Workspace 是合法真实环境，Professional 是目标形态而非强制前置；Content Growth、RD 等只是示例，Channel ≠ Workspace，Project ≠ Business。
- **§7 执行与真值边界**：四层 scope 是统一 canonical execution scope（Assignment/Conversation/Work/Execution/Context/Result/Evidence/Usage/Authorization 共同消费）；Work → Execution → Result/Evidence → Decision/next Work 是 canonical 连续性；Viewed ≠ Accepted；实现状态以 CURRENT_STATE 为准，四层结构 ≠ 四层自主经营已验收。
- **§8 Four-Pane**：App 空间 = Navigation + Context + Main + Utility 四职责；默认 Navigation + Main，Context/Utility 按需出现；Reading/Working/Operating 是同一 Shell 的三种空间职责；具体视觉留给竞品研究。
- **§9/§10**：Conversation Sidebar = 全局会话快捷访问（非 Assistant）；CEO Assistant = 全局悬浮、可拖动/收起、跨七区不销毁、durable Conversation，不占 Four-Pane；Shared Composer 基础合同 = Text/Context/Reference/Attachment/Send + 执行状态；Meeting 是持续多人经营讨论空间，CEO 离开不结束；资料库是 Company Reference Space（Reading/Reference/Source/Used By），不是文件管理器；经营洞察由数据分析部/Company Analyst 承担，不建第二套分析真值。
- **§13/§14/§15 裁定**：19 张 Figma/Batch 1 资产仅为 STRUCTURAL/IA REFERENCE；**FINAL UI MASTER: PAUSED — COMPETITIVE DESIGN RESEARCH REQUIRED；VISUAL AUTHORITY: NOT APPROVED**；下一站即 Desktop AI/Agent UX 竞品研究。

### 4.2 ROOT/docs/03_Design/CURIS_VISUAL_STANDARD_V1.md（Frozen，Direction D）

- **方向**：D = Neutral Foundation + Fresh Iris Company Space；A/B/C 并行主题取消。
- **品牌色**：Primary Brand Accent = **#806BE5（Iris）**；#32f08c 降级为 LEGACY IMPLEMENTATION TOKEN（可暂时残留于代码，代表 MIGRATION REQUIRED）；暗色候选 #9A89F0 未冻结（Dark 验证未完成前 Dark 可用 #806BE5）。
- **中性色 Light**：Canvas #F7F8FA、Base/Elevated #FFFFFF、Surface1 #F1F3F5、Surface2 #E9EDF1、Border #DDE2E7、Primary text #1D232A、Secondary #4D5661、Muted #7C8794、Disabled #AAB2BC；禁止蓝/黄/米色/暖棕/脏白偏色。
- **中性色 Dark**：Canvas #181A1D、Base #1F2125、Surface1 #25292E、Surface2 #2D3238、Elevated #343A41、Border #3C434B、Primary text #F4F6F8、Secondary #C3CAD2、Muted #8F99A4、Disabled #626B75；禁止蓝黑/棕黑/纯黑/终端黑。
- **层级**：PRIMARY/SECONDARY/TERTIARY/QUIET；焦点构建顺序 Typography → Spacing → Alignment → Contrast → Divider/Tonal → Iris（最后）；一屏一个 PRIMARY 焦点、至多一处 Primary Action、至多两处 accent；去掉 Iris 页面仍须可理解。
- **表面/密度**：Open Canvas → Tonal Field → Divider → Raised Surface → Card，Card 稀缺（禁 Card Wall/KPI Wall/Employee Wall）；密度原则 = CALM DENSITY。
- **字体**：FONT FAMILY = OPEN IMPLEMENTATION CHOICE（中文优先、需实测）；仅给出探索区间非 token：Display 28–36/600、Page Title 22–24/600、Section 17–18/500–600、Object 15–17/500、Body 14–15/400、Supporting 13–14/400、Metadata 11–12、Caption 11–12；无冻结 radius/shadow/spacing 数值 token（§10 只冻原则；具体 token 迁移/验证 REQUIRED）。
- **主题**：Light/Dark/System；Dark Company Space 应用未验证（NEEDS VALIDATION）。动效短、静、可中断、reduced-motion 感知；状态色 token 未冻结。

### 4.3 ROOT/docs/01_Product/Curis_Product_UI_Blueprint.html

单文件 HTML 产品 UI 权威（341 行，18 个一级章节 + 2 个治理记录章节），定义：UI 总原则与基础画布、按任务调用的空间原语与空间选择顺序、七区各自的空间组合、对象点击与返回契约、Employee Workstation 表达、研发 Workspace 首版冻结范围、Shell 与视觉规格指针、会议（自然 Conversation → Decision → 继续工作）、Workspace Studio、Reference-Driven 研究方法，末节标记 READY FOR DESIGN。审计时按章节指针消费，不必全文复述。

### 4.4 ROOT/docs/00_Context/CURRENT_STATE.md（Implementation Truth 入口，1276 行）

最新 Current 条目（2026-09-09 Scope + Phase B P0 integrated closure，Status Review / Accepted Candidate）确认：统一 COMPANY/DEPARTMENT/BUSINESS/WORKSPACE Scope 已贯通 Assignment、Conversation、Work、Execution、Context、Result、Evidence、唯一 Usage Ledger 与授权溯源；Phase B A–E 集成证据完成（fresh Company bootstrap → 两原装部门/六工程员工+司衡 → Business=0 → atomic first Generic Workspace → 全局可拖动、收起、跨七区的同一 CEO Assistant），Browser + fresh packaged Desktop + restart 验证通过（后端 120 PASS、前端 19 PASS）。此前各能力验收（Knowledge、Meeting Core、Operating Intelligence、Organization Center、Talent & Capability、Conversation、General Workspace lifecycle、Cloud/Keychain）为 scoped ACCEPTED 证据。**FINAL UI MASTER: PAUSED — COMPETITIVE DESIGN RESEARCH REQUIRED；RELEASE: BLOCKED**（贯穿全文件）。

---

## 5. 差距相关事实（CURRENT_STATE 明示的 已实现 vs 缺失）

**已实现/已验收（scoped）**：七区基本实现并有 Browser + packaged Desktop 证据；Company/Department/Business/Workspace 四层 canonical execution scope；原装组织 bootstrap（两部门 + 6+1 Employee + 司衡）；共享 Four-Pane（TerraShell + WorkspacePaneShell）；全局悬浮 CEO Assistant（可拖动、收起、跨七区持久、同一 canonical identity）；Shared Composer + Conversation 持久化 + Work/Decision/Result/Knowledge reference return + Result Viewed ≠ Accepted；Knowledge Library（五段结构 UI ACCEPTED）；Meeting Core + 自主讨论（Accepted Candidate，多周期真实验收 pending）；Operating Intelligence、Organization Center、Talent & Capability、Cloud/Keychain、General Workspace lifecycle（pause/resume/cancel/archive/restart no-replay）。

**明确 Remaining Core P1（2026-09-09 条目，第 28 行附近）**：
- Global Object Search（全局对象搜索）—— 未完成；且 2026-09-08 条目记录 global search 目前 disabled（prefetch 404）。
- 更丰富的 Leader operating entry（Leader 运营入口）。
- legacy route escapes（旧路由逃逸，如 /ceo-office/projects、/execution 系列仍在导航中）。
- professional return/projection（专业面返回/投影）。
- **Employee/Result 最终工作面（Employee/Result work surface）** —— 未完成。
- **Knowledge reference/return UX** —— 实现有基础合同（reference return 已验），但最终 UX 仍在 P1 清单。
- **Capability 用户语言（Capability 用户语言表达）** —— 未完成。

**P2 / 待验证**：位置记忆、拖动选中文字打磨、**Dark / 1024 宽度支持**（多份 UI ACCEPTED 记录 Dark、1024、accessibility/keyboard 均为 P2；Visual Standard V1 亦载明 Dark Company Space NEEDS VALIDATION）、full accessibility、native-console certification、connectors/formats。

**显式暂停**：FINAL UI MASTER PAUSED（竞品研究是恢复前置）；RELEASE BLOCKED；未授权任何发布/commit。

---

## 6. 后端与桌面端定位（仅方向性）

- **ROOT/backend/**：Python 服务端（requirements.txt），核心在 `backend/app/` —— 大量运行时模块：company_instantiation.py（原装组织 bootstrap）、assistant_runtime.py、conversation_service.py、context_service.py、agent_execution_kernel.py、agent_adapter.py、codex_executor.py、capability_*/catalog_*、credential_vault.py（Keychain）、ceo_context.py / ceo_evidence_api.py、billing_store.py、budget_guard.py、d1_gateway_client.py 等；`backend/api/` 为接口层；数据落 SQLite（backend/curis.sqlite、curis_dev.db，有三保护指纹纪律）。UI 审计如需验证「实现 ≠ 截图」，由此处 API 与 runtime 模块取实现证据；本次未深入逻辑。
- **ROOT/desktop/**：Tauri 桌面壳（productName `Curis`，identifier `com.curis.desktop`，窗口标题 `Curis — CEO Office`，src/main.rs + lib.rs）。`desktop/runtime/` 携带 sidecar（gateway/guardian/recovery/workspace 的 build/dist 在 desktop/.runtime/），负责打包 frontend、拉起 backend sidecar、同 root restart/恢复（对应 workspace-engineering-p0 截图中的 restart-recovery 证据）。UI 审计的「fresh packaged Desktop」证据链即来自此目录构建产物。

---

## 7. 推荐审计用截图清单（七个一级产品区）

每区给出「前端实拍（首选，代表当前实现）+ 原型 p1-preview（代表旧一代完整视觉）」，便于像素级审计时对照实现 vs 原型 vs 视觉标准（Iris/Neutral，见 §4.2）。路径省略 ROOT 前缀（docs/reviews/…、curis-ui-prototype/p1-preview/…）。

| 产品区 | 首选实拍 | 原型对照 |
| --- | --- | --- |
| 1. CEO 工作台 | docs/reviews/20260810_product_ui_audit/01-ceo-desk.png；docs/reviews/2026-08-08-product-audit/01-ceo-office.png | p1-preview/ceo-day-demo-light.png、ceo-desk-drawer-closed.png |
| 2. 业务空间 | docs/reviews/20260813_current_state_product_drift_audit/business-map.png；08-workspace-portal-empty.png、09-workspace-studio-draft.png | p1-preview/business-light.png、workspace-portal-light.png（+ drawer-open/closed）、workspace-studio-light.png |
| 3. 组织中心 | docs/reviews/20260810_product_ui_audit/05-ai-team.png；docs/reviews/20260813_.../organization.png | p1-preview/ai-organization-light.png |
| 4. 人才与能力 | docs/reviews/20260810_product_ui_audit/02-capabilities.png | coverage-exploration-2026-08-17/04-talent-market.html（无 PNG，需现截） |
| 5. 经营洞察 | docs/reviews/20260813_current_state_product_drift_audit/analytics.png | p1-preview/operating-light.png |
| 6. 资料库 | docs/reviews/20260813_current_state_product_drift_audit/knowledge.png | p1-preview/knowledge-light.png |
| 7. 会议 | docs/reviews/20260813_current_state_product_drift_audit/meeting.png；docs/reviews/20260810_product_ui_audit/06-meeting-placeholder.png | p1-preview/meeting-light.png |

工作空间运行时（跨区）首选：docs/reviews/multi-surface-workspace-screenshots/01-research-1440.png、02-content-1440.png、07-assistant-open-1440.png、08-default-1280x800.png；对照 p1-preview/workspace-runtime-{department,xhs,shortvideo,software}-light.png。全局壳/导航：docs/reviews/align-baseline/prototype-sidebar-default.png + frontend-sidebar-after-*-r4.png 成对。浅/暗双主题批量基线：curis-ui-prototype/p1-preview/ 全套 light/dark（§2.3）。

审计注意事项（与 §1.4/§4.2 联动）：
1. 实拍截图反映的是 Frozen `#32f08c` 绿色系（部分页面残留 Iris `#806BE5`），而 Visual Standard V1 冻结的是 Iris 主品牌 —— 差异本身是审计对象，不是错误引用。
2. 2026-08-08/0810/0813 三轮截图时间早于 2026-09-09 Phase B 集成（原装组织、悬浮 Assistant），部分画面可能已过时，审计时以后端/API 证据校验。
3. talent-market 与 organization（员工详情）两区缺少高质量前端实拍 PNG，建议审计时现场补截。
