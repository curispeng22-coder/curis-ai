# CURIS V1 — UI GAP MAP

> Status: Review
> Authority Class: REVIEW
> Disposition: Product-to-Frontend gap inventory; no implementation authorization
> Scope: Current Product Truth versus static Frontend assembly

## 1. Gap matrix

| ID | Current Product Truth | Frontend state | Class | Owner / next gate |
|---|---|---|---|---|
| UI-G01 | 七区顺序固定；人才与能力、经营洞察是正式名称 | `WorkspacePaneShell.js` 仍六项；`TerraNavData.js` 保留旧五/六项与旧分组 | P0 · IA | Frontend baseline owner；七区 nav issue + route regression |
| UI-G02 | First Run 从“你想开始做什么？”接受任意业务意图 | `/onboarding` 仍是 FoundingRun 状态表单，未落 canonical Business/Workspace | P0 · product path | First-run owner；V1-P0-001 packaged E2E |
| UI-G03 | 模板不是业务创建门槛；无模板进入 General Workspace | Business/Studio 路径偏模板/配置，General creation UI 缺失 | P0 · product assembly | Business Spine integration + generic Workspace proof |
| UI-G04 | CEO Desk 是经营日注意力/结果/决定投影 | `/ceo-office` 暴露 Runtime snapshot、Resource Check、Simulation/Staffing | P0 · projection | CEO Desk page contract + ordinary-user browser evidence |
| UI-G05 | 会议是事实、分歧、决定、责任、跟进工作面 | `/ceo-office/meeting` 仅“规划中” | P0 · missing page | Meeting Page Contract + implementation authorization |
| UI-G06 | Business 是分类/聚合，Workspace 是独立业务产品 | Business directory 有基础；Business create、General path、duplicate/deep-link 不完整 | P0 · flow | Business creation + canonical parent resolver evidence |
| UI-G07 | Workspace Main 先表现 Domain Primary Surface，Employee 是操作者 | generic installed surface 可打开，但没有完整 ordinary-user assembly；部分页面以 Employee/Runtime 为主 | P1 · productization | Generic/Professional Workspace E2E |
| UI-G08 | Organization = 公司版图 + 员工目录 | `organization/page.js` 仍注释/实现 `AI Workforce Map`，混入旧 project/capacity 语义 | P1 · semantics | Company Map page contract + data proof |
| UI-G09 | 专家、技能、连接器是“人才与能力”内部 Surface；专家经招募才成为 Employee | `/talent-market` 交互有搜索/招募/技能，但产品入口与语义仍旧 | P1 · language | Talent & Ability route/copy review |
| UI-G10 | 经营洞察消费真实 Company/Business/Workspace/Employee/Model/Capability 数据 | `/analytics` 仍把 pulse、queues、机会、约束混成 Dashboard | P1 · analytics | Operating Intelligence UX/page contract + source/freshness proof |
| UI-G11 | 资料库负责来源、索引、搜索、引用、权限、沉淀 | `/knowledge` 本地/范围/导入基础存在，外部来源和引用链未闭合 | P1 · knowledge | Library page contract + connector/source evidence |
| UI-G12 | Assistant 是跨页公司级 Employee；协调/汇总/跟进/升级，不替代专家 | GlobalAssistant/state seam 存在，但持续 context、主动注意力、回原范围未完整 | P1 · continuity | Assistant integration + packaged revisit |
| UI-G13 | Runtime State ≠ UI expand/collapse；Employee UI 只三态 | Shared Shell 已有大部分语义，部分 CEO/legacy 页面仍显示技术 lifecycle/status | P1 · status | Shared status projection scan + UI regression |
| UI-G14 | Work/Result/Evidence/Decision/Recovery 要能回原上下文 | Runtime/API 有真实基础，通用页面只有部分投影 | P1 · recovery | result/decision/recovery deep-link evidence |
| UI-G15 | Professional Workspace 可多 Surface，Domain primary 最大 | XHS/RD reference 与当前 frontend assembly 未统一，旧多 Tab/console 遗留仍可误导 | P1 · domain surface | Domain visual delta / browser QA |
| UI-G16 | 任意业务可创建；Professional 只在能力成熟时加速 | 当前没有完整 fresh ordinary-user arbitrary Business→Workspace packaged path | P0 · E2E | V1 whole-app packaged proof |
| UI-G17 | Product language 使用 Company/Business/Workspace/Employee/Result；Office 仅 provenance | 当前源码/旧 routes/comments 仍出现 Office/办公室、旧项目/AI Team 等 | P1 · copy | focused stale-term scan + copy review |
| UI-G18 | Global Capability ≠ Global Topbar；Pane-local Header | Shell contract 正确，但 legacy prototype/old spec/部分 components 仍可能把旧 topbar 当实现依据 | P1 · shell | source/reference cleanup review |
| UI-G19 | 真实数据缺失须显式 Unknown/未记录，不得 sample 当事实 | readiness 已标多处示例/partial；settings/old pages 仍存在 sample snapshot patterns | P1 · trust | data provenance/copy audit |
| UI-G20 | Whole-app V1 必须 packaged/restart/reload 可回访 | readiness audit 标记 whole-app E2E MISSING，视觉 reference 不能替代 | P0 · proof | isolated packaged E2E + regression |

## 2. Gap categories

### Product contract already exists, frontend missing

UI-G01、02、03、04、05、06、08、10、16、20 属于当前产品责任已经足够明确，但 Frontend 尚未完整装配。它们不需要重新发明产品概念；需要按 Issue/Allowed Files 接通正确入口和投影。

### Frontend function exists, product surface is stale

UI-G07、09、11、12、13、14、15、17、18、19 多数已有组件、数据 seam 或局部页面，但阅读模型仍混有旧导航、技术状态、样例数据或 prototype 结构。应先保留可验证功能，再迁入 Current surface。

### Evidence gap, not automatically a design gap

UI-G20 以及所有“完整 E2E/真实外部来源/重启后连续性”问题，不能仅靠页面改造解决。必须由实现与证据任务证明；静态 UI 审计只登记缺口。

## 3. Prioritization for next implementation planning

1. **P0 用户入口**：七区导航、First Run、canonical Business + General Workspace、CEO Desk ordinary projection。
2. **P0 可回访闭环**：Work → Result/Evidence → Decision/Recovery → reload/restart；至少一个 Professional Workspace packaged E2E。
3. **P1 共享产品面**：Organization two-view semantics、Talent & Ability naming/boundary、Assistant continuity、Insights scoped analysis、Library source chain。
4. **P1 Domain surfaces**：在 Shared Shell 中分别验证 RD 与 Content Growth 的 Domain Primary Surface；不把样本写成固定业务。
5. **P2 退役与清理**：legacy routes/prototypes/admin surfaces，需 replacement 后执行。

## 4. Non-goals / not blockers for this audit

- 本表不授权改 Runtime、Schema、DB、Package technical architecture 或 Autonomous V1 Issue。
- 不以 UI gap 推断缺少 Runtime primitive；先查现有 seam，再登记 Product → Implementation Gap。
- 不把 XHS、Douyin、RD 变成 Curis 固定业务类型。
- 不把视觉 reference、静态 mock、单个 API 200 或局部测试当作完整交付。

## 5. Final UI rebuild starting point (cross-reference)

最终重建应继承 Frozen Shell 与共享工作区/结果/责任 seam；保留 RD/XHS 的真实业务功能；重新设计 First Run、CEO Desk、Business/Organization/Talent/Insights/Meeting、General Workspace 与 Domain Primary Surfaces；旧导航、技术 onboarding、Runtime Console 和 prototype 只能在替代与回归完成后删除。

— READ-ONLY GAP MAP · STOP FOR CEO REVIEW
