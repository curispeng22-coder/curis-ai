# CURIS V1 — FRONTEND CLEANUP MAP

> Status: Review
> Authority Class: REVIEW
> Disposition: Read-only cleanup recommendations; no deletion authorized
> Scope: Current Frontend inventory mapped to Current Product Truth

## 1. Classification legend

- **KEEP**：实现责任仍正确，保留并只做必要接线。
- **RE-SKIN**：功能/结构可复用，产品名称、文案、状态或视觉层需要更新。
- **REFACTOR**：仍有价值但当前 IA、责任边界或用户路径不正确。
- **REPLACE**：应由新的 Current 产品路径替代。
- **REMOVE AFTER REPLACEMENT**：只有 replacement、测试、deep-link、Runtime 依赖和回归均通过后才退役。
- **REMOVE NOW**：本轮不建议任何项目使用此分类。

## 2. Shared foundation

| 位置 | 分类 | 保留/清理判断 | 后续证据 |
|---|---|---|---|
| `frontend/components/workspace/WorkspacePaneShell.js` | KEEP + REFACTOR | 继承 Pane、resize、search、maximize、状态隔离；修正六区 `NAV_ITEMS` 与当前七区 | Nav route inventory、browser responsive regression |
| `frontend/components/runtime/RuntimeProvider.js` | KEEP | 共享运行状态 seam，不变成用户导航 | Runtime contract regression |
| `frontend/lib/runtimeApi.js`、`frontend/lib/api.js` | KEEP | 继续承载 API seam；不把函数名/内部状态当产品页面 | API/error/recovery regression |
| `frontend/components/workspace/InstalledWorkspaceRuntime.js` | KEEP + REFACTOR | Generic package renderer 是任意业务 fallback 的可复用基础；普通用户产品入口仍缺 | generic Business→Workspace E2E |
| `frontend/components/workspace/SharedEmployeeWorkArea.js`、`TeamOperatingDefinitionEditor.js` | KEEP + RE-SKIN | 共享员工工作区/责任编辑保留；技术配置按需隐藏 | Employee Workstation/Team Operating UI proof |
| `frontend/components/terra/TerraPrimitives.js`、`TerraIcons.js`、`globals.css`、`layout.js` | KEEP + RE-SKIN | 令牌、主题、通用控件保留；文案和旧页面用法需审计 | theme/contrast/console/layout QA |
| `frontend/components/assistant/GlobalAssistant.js`、`assistantState.mjs` | REFACTOR | 全局 Assistant seam 有价值，连续 context/attention/回原上下文不完整 | assistant continuity packaged proof |

## 3. Navigation and shell cleanup

| 位置 | 分类 | 现状 | 建议 |
|---|---|---|---|
| `frontend/components/terra/TerraNavData.js` | REPLACE | 旧分组包含“经营、业务版图、AI 团队、人才市场、工作空间、兼容入口” | 以七区 Current Truth 为唯一数据源；兼容入口下沉到非普通用户层 |
| `frontend/components/terra/TerraSidebar.js` | REFACTOR | 注释和渲染仍按旧五项常驻 + More 分组；`AI 团队`与 Workspace 混路由 | 只消费新的 nav data；保留折叠/重开行为，不保留旧阅读模型 |
| `frontend/components/terra/TerraShell.js` | RE-SKIN / REFACTOR | 共享壳层仍可用，页面 crumbs 和 assistant context 需要 Current 语义 | 与 Pane-local Header、七区、Global Capability 对账 |
| legacy aliases under `/projects`, `/employees`, `/platform`, `/dev-console`, `/control/*` | REMOVE AFTER REPLACEMENT | 可能仍被兼容、测试或迁移使用 | 先做引用清单、替代路径和回归，再退役 |

## 4. Product pages

| 路由/组件 | 分类 | 清理动作 |
|---|---|---|
| `/onboarding` + `FirstRunGate` | REPLACE | 由技术 FoundingRun 表单改为“你想开始做什么？”；落到 canonical Business + General/Professional Workspace；保留 fail-closed 与恢复说明 |
| `/ceo-office` | REFACTOR | 从 Runtime snapshot / Resource Check / Simulation 控制台改为 CEO Operating Day：Brief、Matters、重要 Result、Exception/Handoff、Decision、下一步；运行细节下钻 |
| `/ceo-office/business` | REFACTOR | 保留 canonical Business/Workspace directory；补创建任意 Business、General Workspace、Business duplicate/deep-link；减少技术字段 |
| `/ceo-office/workspace` | REFACTOR | 作为 Operating Work Directory；按 Department/Business/Workspace 进入正确 Surface，不能成为模板列表 |
| `/ceo-office/workspace/installed/[workspaceId]` | KEEP + REFACTOR | 作为 generic installed Workspace 入口；必须让普通用户看到业务目标、当前工作、结果和下一步，而非安装/runtime 状态 |
| `/ceo-office/workspace/studio` | REFACTOR | 用 Operating Intent→Current Truth→Proposal→Reuse/Compose→Validate→Establish；模板可复用但未知业务不被表单阻挡 |
| `/ceo-office/organization/*` | REFACTOR | 组织中心拆成公司版图/员工目录的阅读与反查；Company→Department→Business→Workspace；Role 展开才到 Employee Binding |
| `/ceo-office/talent-market` | RE-SKIN + REFACTOR | 正式产品名“人才与能力”；内部专家/技能/连接器；专家只有完成招募、岗位/责任和授权后成为 Employee |
| `/ceo-office/analytics` | REFACTOR | 经营洞察作为 scoped analysis；明确 source/freshness/unknown/manual；支持比较但不造 Analytics Runtime |
| `/ceo-office/knowledge` | KEEP + REFACTOR | 本地资料与 scope seam 可保留；补外部来源、索引、引用、权限、来源追踪、沉淀语义 |
| `/ceo-office/meeting` | REPLACE | 当前是“规划中”占位；待 Page Contract 后承载事实、分歧、Decision、责任和跟进 |
| `/ceo-office/settings` | KEEP + RE-SKIN | 入口保留在头像菜单；去掉示例数据假象，接入真实设置边界；品牌配置仍是 Future direction |

## 5. Domain surfaces

| 位置 | 分类 | 处理原则 |
|---|---|---|
| `/ceo-office/workspace/xhs`、`/shortvideo` | KEEP FUNCTION + REFACTOR ENTRY | 仅作为 Content Growth/Channel validation examples；不能把 XHS/Douyin 变成 Workspace identity 或一级导航 |
| `/ceo-office/workspace/software`、RD components | KEEP FUNCTION + RE-SKIN | 保留研发工作对象、Version/Build/Test/Review/Blocker、Codex/Evidence；Domain Primary Surface 最大，Employee Work Area 不是主视觉 |
| `XhsWorkspacePhaseOne.js`、`RdWorkspacePhaseTwo.js` 等 | KEEP FUNCTION | 迁入经过 Page Contract 的 Domain Surface；不复制 Shared Employee/Runtime |
| `PipelineGraphView.js`、`TaskLauncher.js`、`RuntimeCapabilitySwitcher.js` | REFACTOR / REMOVE AFTER REPLACEMENT | 仅在专业或高级/审计面需要时保留；不能主导普通用户 Workspace |

## 6. Legacy / admin surface retirement

| 范围 | 分类 | 说明 |
|---|---|---|
| `/ceo-office/projects*`、`/projects*` | REMOVE AFTER REPLACEMENT | Project 是 legacy compatibility object，不是 Current Business；必须先完成 Business/Workspace replacement |
| `/ceo-office/execution*`、`runtime-trace`、`company-runtime` | REMOVE AFTER REPLACEMENT | Runtime/Execution 属实现或审计层；普通用户由 Work/Result/Recovery 投影消费 |
| `/platform/*`、`/dev-console`、`control/secret-vault` | REMOVE AFTER REPLACEMENT | 高级管理/诊断/安全入口；保留合法内部入口直到替代与权限审计完成 |
| `curis-ui-prototype/`、`.bak/`、旧 Flow Pack | REMOVE AFTER REPLACEMENT | 历史/原型，不删本轮；当前 Agent 必须读 Pointer/Blueprint，不读它们作 Current |

## 7. Safety gates for a deletion issue

任何未来删除 Issue 必须写明：Owner、Allowed Files、replacement route、对象/Runtime 依赖、兼容 deep-link、测试、fresh Browser/Desktop evidence、reload/restart、rollback。没有这些证据时只能 `REMOVE AFTER REPLACEMENT`，不能 `REMOVE NOW`。

— READ-ONLY CLEANUP MAP · STOP FOR CEO REVIEW
