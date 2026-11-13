# CURIS PROFESSIONAL WORKSPACE ARCHITECTURE
## INTERNAL PRODUCT / ARCHITECTURE RESEARCH

**Authority Class:** REVIEW  
**Status:** Review  
**Disposition:** READY FOR CEO REVIEW / CANDIDATE ONLY  
**Date:** 2026-08-21  
**Scope:** Internal Authority audit and architecture research only  
**External track:** `PENDING EXTERNAL SYNTHESIS`  
**Implementation:** Not authorized  

> 本文不修改 Product Blueprint、Master Map、UI Blueprint、Company OS Shared Authority、Workspace Engineering Methodology、Workspace Package Proposal、Runtime、Schema、DB、Frontend 或 Prototype。文中 `NEW RESEARCH INFERENCE` 与 `CANDIDATE` 不等于过去已 Frozen，也不等于当前实现。

---

## A. Executive Summary

### A.1 Verdict

1. **`Workspace ≠ Page` 成立，并与 Current Product Truth 兼容。** Current Product Truth 已把 Workspace 定义为独立经营单元、专业业务应用和专业工作环境，而非页面或统一 Dashboard。
2. **`Workspace = Professional Operating Environment` 是对当前定义的准确收敛，但该英文术语本身不是历史 Frozen 事实。** 应标记为 `NEW ARCHITECTURE DISCOVERY / CANDIDATE TERM`，等待 CEO 接受后再决定是否进入 Current Authority。
3. **一个 canonical Workspace 可以承载多个 Professional Surfaces。** 现有 Authority 已允许业务自定页面布局、工作对象、专业阶段和工具，并要求 Domain-specific Primary Work Surface；但“多个可导航 Professional Surfaces 的注册、默认选择、route 与 availability contract”尚未被完整定义。
4. **不需要 Sub-Workspace、Mini Workspace、Workspace App 或 Office inside Workspace。** 保持 `Company → Department → Business → Workspace`；Surface 只是同一 Workspace 内的工作视图，不获得 canonical identity。
5. **Domain Navigation 应由 Workspace Package 声明，由 Curis Core 校验、解析和渲染。** Workspace Engineering / Domain Expert 负责形成候选 IA；Package 固化版本化声明；Instance 只保存允许的启用状态和用户偏好；Core 不写死 XHS、RD 或电商菜单。
6. **Four-Pane 继续是责任模型，不是可见列数。** Global Navigation、Context、Main、Utility 的职责保持；Domain Navigation 候选主要进入 Context 的 workspace-local context/navigation 区，Main 承载当前 Professional Surface，Utility 承载按需 Detail / Work / Preview。Global CEO Assistant 不是第五 Pane。
7. **Operating Context 只保留一份 Workspace-scoped truth projection。** 固定用户语义仍是“经营状态 / 本轮重点 / 最新判断 / 下一步”；各 Surface 消费同一投影，不重复存储。
8. **当前 Workspace Package contract 是 `PARTIAL`。** 它已支持 Package local navigation、`surfaces.json` 和一组 Main / Context / Utility 声明；当前受控实现也已证明动态 Workspace 入口与单组 Pane Surface。但它没有表达多个 Professional Surface 的 registry、stable key、default、route、object/detail mapping、conditional availability 和 scoped shared projections。
9. **当前 RD / XHS / installed Package 实现不是 multi-surface Workspace。** RD 与 XHS 是按业务类型映射到编译路由的单一专业入口；installed Package 是一个固定 object-list / object-detail / create-form 组合。它们提供可复用证据，但不证明本 Candidate 已实现。
10. **XHS 的确切 Surface 集合仍需等待外部研究。** `Research / Content / Growth / Commercialization` 仅为内部压力测试候选，不得写入 Core 或冒充真实 XHS operating-practice 结论。

### A.2 Candidate in one line

```text
One canonical Workspace
→ package-declared stable Domain Navigation
→ one selected Professional Surface at a time
→ object/detail/scoped projections
→ shared Team / Knowledge / Capability / Operating truth
```

---

## B. Historical Authority Audit

### B.1 Truth classification

| Class | Evidence | What it already says | What it does not prove |
|---|---|---|---|
| `CURRENT / FROZEN` | `docs/01_Product/Curis_Product_Blueprint.html` | Workspace 是“专业业务应用 + 多 Agent 自动工作现场”；业务决定布局、工作对象、专业阶段、工具、节奏和结果窗口；四种空间角色是 Navigation / Context / Main / Utility | 未定义多个 Professional Surface 的 registry、route、default 与 availability |
| `CURRENT / FROZEN` | `docs/01_Product/Curis_Product_Master_Map.md`、`Curis_Product_UI_Blueprint.html`、`Curis_Product_Context.md` | Workspace 是独立专业经营单元；Domain-specific Primary Work Surface + Shared Work Area；不同 Workspace UI / object / cadence 可以不同 | 未把 Workspace 内导航建模为完整 Domain Navigation contract |
| `FROZEN SHARED AUTHORITY` | `docs/03_Design/Curis_Company_OS_Shared_Authority.md` §9 | 长期 Workspace = Operating Team + Professional Workspace；Assistant、Leader、Employee、Team、Responsibility、Handoff 共用 Company OS 真相 | 不定义 XHS/RD/e-commerce 的 Surface 清单 |
| `FROZEN SHELL` | `docs/03_Design/Curis_Workspace_Shell_Contract_And_Shared_Patterns.md` | 固定空间职责而非固定四栏；Main 必有，Context/Utility adaptive；Main = Domain Business Surface + Shared Work Area | Context 是否承担稳定 Domain Navigation 尚未 Frozen；Shell 不定义 Domain IA |
| `CEO ACCEPTED REVIEW` | `docs/reviews/CURIS_AUTONOMOUS_OPERATION_PRODUCT_SURFACE_MAPPING.md` | Workspace Current Operating 固定为经营状态、本轮重点、最新判断、下一步；Domain Primary Surface 保持最大专业主体 | 不新增 Surface Registry；不证明 UI/Runtime 已实现 |
| `CEO ACCEPTED CANDIDATE` | `docs/reviews/CURIS_OPERATING_LIFECYCLE_CONTRACT_CANDIDATE.md` | Operating Series / Cycle / Result / Evidence / Review / Learning / Next-cycle Decision 的唯一经营真相链 | 不授权 Autonomous UI Runtime，也不决定 Domain Navigation |
| `CEO ACCEPTED REVIEW` | `docs/reviews/CURIS_THREE_LAYER_OPERATING_MODEL_RECONCILIATION.md` | User Surface → Employee Operating Layer → System Runtime；Package 是 Domain Operating Capability Package；不新增 Playbook/Runtime | 未定义 multi-surface Package contract |
| `REVIEW / APPROVED CANDIDATE` | Workspace Engineering Methodology / Lifecycle | Package First、Semantic Model Before Instance、Business-Drives-Surface、IA Composition、Reuse First | 文件中的旧“Dynamic Package 未实现”陈述已被后续 P0/P0.5 Accepted Implementation 更新，不可当当前实现状态 |
| `REVIEW / TECHNICAL DIRECTION` | `WORKSPACE_PACKAGE_TECHNICAL_PROPOSAL.md` | Package 可声明 local navigation、Main/Context/Utility composition、Domain Schema、Capabilities、Knowledge、Result/Evidence presentation | 当前 `surfaces.json` 语义主要是 Pane composition，不是 multiple Professional Surface registry |
| `CURRENT IMPLEMENTATION / ACCEPTED BOUNDED` | Workspace Engineering P0/P0.5 Reviews | 动态 Package navigation、单组 Main/Context/Utility、对象持久化、restart、Company OS integration 已验收 | 未证明多 Professional Surface、XHS/RD Package migration 或 generic professional environment |
| `CURRENT IMPLEMENTATION / MIXED SOURCE` | RD / XHS routes and components | XHS 与 RD 各有独立专业组件；XHS bounded slice accepted；RD bounded execution slices accepted | 仍为编译 route 和单一 domain entry；完整 multi-surface / complete domain delivery 未验收 |
| `HISTORICAL` | 旧 Product Bible：Project Workspace、Workspace Renderer、Workspace/Admin | 早期已把 Workspace 视为用户实际工作处，并探索可渲染工作区 | 历史文件不能覆盖 Current Product Truth；也不能证明今天的 multi-surface model 早已 Frozen |
| `SUPERSEDED / REFERENCE` | 旧 Pane Closure、旧 RD closeout、Prototype / High Fidelity | 提供 Pane 分配、Calendar、Diff、Workstation 等 provenance | 只能重新归位，不得直接升级为 Current Architecture |
| `NEW RESEARCH INFERENCE` | 本文 | 一个 canonical Workspace 内含多个 route-addressable Professional Surfaces；Package 提供 Surface Registry 和 Domain Navigation | 等待 CEO 接受；未实现 |

### B.2 Historical conclusion

Curis 过去已经定义了以下基础语义：

- Workspace 是实际专业工作处，不是纯项目卡片；
- Workspace 可有 Domain-specific UI、对象、阶段、工具和 cadence；
- Shell 只固定空间职责，Domain 决定专业内容；
- Package 可以声明 Surface composition 和 local navigation；
- Team、Knowledge、Capability、Result、Evidence、Decision、Handoff 应复用 Core。

过去**没有明确 Frozen**：

- 一个 Workspace 内存在多个同级 Professional Surfaces；
- Surface 是稳定、可路由、可条件开放的 Package declaration；
- Context Pane 承担 Workspace 内部 Domain Navigation；
- `surfaceKey`、default surface、last active surface、object/detail mappings 的统一合同。

因此本轮不是恢复旧架构，而是在已有语义上登记一个最小的新架构发现。

---

## C. Workspace Definition

### C.1 Current-compatible definition

**Workspace 是 Company OS 中一个 canonical、持久、受 Business 管辖的独立经营范围，由真实 Operating Team 承载，并提供该业务所需的专业工作环境。**

Workspace 拥有或锚定：

- canonical `workspace_id` 与 Company / Department / Business parent path；
- Workspace Goal / Positioning / Strategy scope；
- Workspace Leader、Team、Responsibility Assignment；
- Operating Series / Cycle 的作用域；
- Package / Package Version 与 Domain semantics；
- Domain objects、Results、Evidence、Artifacts、Knowledge refs；
- Capability requirements、permissions、external side-effect boundaries；
- 一组 Professional Surfaces 及其稳定导航。

### C.2 Identity rule

以下任一变化**不创建新 Workspace**：

- 从 Research 切到 Content；
- 从 Issue 切到 Build/Test；
- 打开某个对象详情；
- 查看 Team 或资料；
- 打开 Utility / Assistant；
- Runtime 推荐用户关注另一个 Surface。

只有当目标、Leader/Team、Operating Series、权限/数据边界和生命周期需要独立负责、独立运行、独立归档时，才考虑在同一 Business 下创建**并列 Workspace**，而不是 Sub-Workspace。

---

## D. Workspace vs Surface

### D.1 Classification rules

| Type | Classification question | Own canonical identity? | Typical persistence | Example |
|---|---|---:|---|---|
| Workspace | 是否拥有独立 Goal、Leader/Team、Operating Series、permission/data boundary 与 lifecycle？ | Yes | Core Workspace truth | `AI 科技` |
| Professional Surface | 是否在同一 Workspace 内回答一个稳定的专业工作问题，并组合一组对象、动作和工具？ | No | Package definition + Instance availability | Content、Growth Analysis |
| Object View | 是否只是某类对象的列表、看板、日历、图或筛选投影？ | No | Query/projection；少量 view preference | Note Calendar、Issue Board |
| Detail View | 是否围绕一个已选对象检查、编辑、预览或审阅？ | No | Object truth elsewhere；UI selection local | Note Detail、Diff、Order Detail |
| Scoped View | 是否只是把 Company OS / Knowledge 等共享真相按当前 Workspace 过滤？ | No | Shared source of truth + scoped query | Team、资料、Evidence |
| UI-only state | 是否只影响展开、排序、选中、宽度、last visited？ | No | Local/user preference | Context open、selected tab |

### D.2 Name-independent test

不要凭 `Research`、`Team`、`资料`、`Calendar` 等名字判断。按以下顺序判断：

1. 是否形成独立经营责任？是 → Workspace candidate。
2. 是否改变当前专业工作问题和对象/动作组合？是 → Professional Surface candidate。
3. 是否只是同一 Surface 的对象呈现方式？是 → Object View。
4. 是否围绕一个选中对象？是 → Detail View。
5. 是否投影共享 Truth？是 → Scoped View。
6. 其余仅为交互偏好 → UI-only state。

### D.3 XHS examples are provisional

| Candidate | Provisional classification | Reason |
|---|---|---|
| `AI 科技` | Workspace | 独立账号经营范围、目标、团队和经营循环 |
| Content / Publishing | Professional Surface candidate | 稳定内容计划、生产、审核、发布问题 |
| Calendar | Object View inside Content / Publishing | `Note × Time` 的投影，不是 identity |
| Research | Professional Surface candidate | 若有稳定研究对象、方法、结果与重复工作；等待外部证据确认 |
| Growth | Professional Surface candidate | 若承载指标、实验、解释、复盘；等待外部证据确认 |
| Commercial Opportunity | Professional Surface candidate | 是否独立成立等待商业化实践证据 |
| Team | Scoped Company OS view | 不造 XHS Team System |
| 资料 | Scoped Knowledge / Artifact view | 不造 XHS Knowledge Base |

---

## E. Domain Navigation Ownership

### E.1 Recommended ownership

| Responsibility | Owner |
|---|---|
| 形成真实 Domain IA 与 Surface 候选 | Workspace Engineering + Domain Expert + Product Expert |
| 声明 stable `surfaceKey`、label、role、order、default candidate、object mappings | Workspace Package |
| 校验 key、route collision、Core component/action/capability legality | Curis Core |
| 渲染 Shell、route resolution、accessibility、loading/failure/forbidden | Curis Core |
| 记录 Package version、instance availability 与 pinned definition | Package Registry / Workspace Instance |
| 记录用户 last active、展开、排序等非业务偏好 | User/UI preference store |
| 决定当前业务阶段、Capability、permission 是否使 Surface 可用 | Shared Runtime truth + Package-declared rule 的 derived projection |
| 自由创建任意 Surface / route | **Nobody in V1**；必须回到 Package Candidate + validation |

### E.2 Why Package-provided declarative navigation fits

它符合现有：

- `Package First`：新业务优先改变 Package declaration，不改 Core menu；
- `Semantic Model Before Instance`：导航来自真实业务对象和工作方法，不由 UI 猜；
- `Business-Drives-Surface`：Domain 决定专业工作面，Core 只提供受控容器；
- `Declarative Workspace`：Package 描述结构，Core 掌握 identity、安全、渲染与 Runtime truth。

### E.3 Hard boundary

Curis Core 只认识通用字段与行为，不认识 `Research / Content / Growth / Commercialization` 或 `Issue / Build / Release` 的业务含义。Core 不得写死 XHS、RD、电商菜单。

---

## F. Four-Pane Reconciliation

| Responsibility | Candidate mapping in multi-surface Workspace | What must not happen |
|---|---|---|
| Global Curis Navigation | Company-level seven-area location and Workspace entry | 放入 XHS/RD 内部菜单；变成 Employee list |
| Context Pane | Workspace-local Domain Navigation + current surface context / collections，按需展开 | 承载 Employee Conversation；成为永久第二主页面 |
| Main | 当前 selected Professional Surface + Shared Work Area | 永远等于 Workspace Home；变成统一 Runtime dashboard |
| Utility | selected Object Detail / editor / preview / evidence / specialized tool | 永久工具墙；复制 Main；形成独立 identity |
| Global CEO Assistant | 同一公司级 Assistant，以当前 Company/Business/Workspace/Surface scope 工作 | 第五 Pane、Workspace Assistant 或第二套任务系统 |

**结论：** 对象数量或可见区域超过四，不产生 Five-Pane。Pane 是职责；Surface 是 Main 中当前工作的专业语义；Detail 可在 Utility、Drawer、Focus 或 Main split 中按需出现。

---

## G. Context Pane Candidate Role

### G.1 Compatibility

Frozen Product Truth 已允许 Context 持续浏览项目、Thread、资料目录、文件、业务对象集合和历史工作；Frozen Shell 也规定每个 Workspace 自己声明 Context 内容。因此把 Workspace-local Domain Navigation 与 current context 放入 Context，**兼容但属于扩展 Candidate**。

### G.2 Candidate behavior, not visual design

- **1440:** Navigation + optional Context + Main；Utility 仅在选中 Detail/Tool 时出现。Context 可同时包含稳定 Domain Navigation 与当前 Surface 的上下文分组，但保持窄、可收起。
- **1280:** 优先保证 Main 最小可用宽度。Context / Utility 采用 adaptive overlay/focus 或一次只保留一个 secondary surface；选中的 `surfaceKey` 不因折叠而改变。
- **Surface retention:** 收起 Context 不改变 Surface；重新展开仍回到同一导航位置与当前上下文。
- **Detail composition:** Detail 打开时不挤掉 Domain identity；窄宽度下 Detail 优先 overlay/focus，关闭后回到原 Surface / Object selection。

本文不冻结 breakpoint、像素、组件结构或高保真。

---

## H. Primary Surface Model

**Main 应被理解为当前选中的 Professional Surface，而不是固定 Workspace Home Page。**

Workspace Home / Operating Overview 只是一个可能的 default/overview Surface 或 projection，不是 Main 的永久定义。切换 Surface 时：

- `workspace_id`、Business parent、Team、Operating Series 不变；
- Main 的专业对象、动作、节奏和布局改变；
- Shared Work Area、Operating Context、Assistant scope 和 return contract 继续存在；
- Context / Utility 依据 selected Surface 重新投影，但不复制 Truth。

---

## I. Default Surface Model

### I.1 Candidate policy

采用可预测的优先级，而不是让 Runtime 任意跳页：

1. explicit deep link / user action；
2. 当前用户在该 Workspace 的 valid last active Surface；
3. Package-defined deterministic default；
4. Package default 不可用时，按 Package-declared fallback order 选择第一个 available required Surface；
5. 无可用 Surface → honest blocked / capability-gap state。

### I.2 Runtime influence

Runtime 可以：

- 给 Surface 增加 attention / suggested / needs-review 状态；
- 在 Workspace entry 提供“建议进入 Growth Analysis”之类的建议；
- 在明确恢复操作、CEO Decision return、deep link 时打开目标 Surface。

Runtime 不可以：

- 用户工作中因阶段变化自动跳页；
- 每次 Cycle 状态改变就改 selected Surface；
- 用动态排序破坏导航位置；
- 在没有可解释原因与返回路径时覆盖 last active selection。

---

## J. Operating Context Placement

### J.1 Single source

Operating Context 是 Workspace-scoped shared projection，消费 Operating Lifecycle truth：

```text
Operating Series / current Cycle / Goal / Strategy / Review / Next-cycle Decision
→ one Workspace Current Operating projection
→ all Professional Surfaces consume it
```

不在每个 Surface 重复保存“经营状态 / 本轮重点 / 最新判断 / 下一步”。

### J.2 Placement candidate

- 每个 Professional Surface 的 Main Header / top strip 可显示同一份轻量四字段；
- Operating Overview 可展开更多 Workspace-level projection；
- Context / Utility / Detail 按需展示 Strategy、Review、Evidence、Learning、Decision 的完整来源；
- Domain Primary Surface 继续表达进展和专业工作，不新增进展字段与其竞争。

---

## K. Autonomous Operating Mapping

| Truth | Workspace-wide | Surface-scoped | Detail on demand | CEO attention |
|---|:---:|:---:|:---:|:---:|
| Operating Series / Goal | Yes | Surface 可引用 | Goal/contract detail | 变更/终止时 |
| Current Cycle | Yes | Surface 显示相关 phase/work | Cycle detail | 异常/等待时 |
| Strategy / Envelope | Yes | Surface 显示相关 hypothesis/tactic | version/evaluation detail | 越界调整时 |
| Plan | Workspace-level release | Work 可归属一个或多个 Surface | plan lineage | 超预算/权限时 |
| Work / Assignment | Shared Team Operating truth | 主要在相关 Surface 投影 | responsibility detail | 阻塞/升级时 |
| Result / Artifact | Workspace truth | 由产出 Surface 首要呈现 | full artifact | material result 时 |
| Evidence | Workspace truth | 相关 Surface 引用 | provenance/full evidence | 缺证/冲突时 |
| Signal | Derived from evidence | Growth/Analysis 等 Surface 可主呈现 | formula/window/source | material risk 时 |
| Review / Learning | Workspace truth | 相关 Surface 显示摘要 | full review | protected change 时 |
| Next-cycle Decision | Workspace truth | Surface 显示 next action | decision packet | CEO Gate / escalation |

不创建 `Autonomous UI Runtime`。Surface 只消费既有 Truth 与 projection。

---

## L. Domain Object Ownership

| Class | Use when | Owner / source | Example |
|---|---|---|---|
| A. Existing Curis canonical object | 涉及 Company、Business、Workspace、Employee、Role、Responsibility、Work、Cycle、Decision、Result、Evidence | Curis Core | Workspace Leader Assignment |
| B. Domain Package object | 业务特有、需持久化和有 lifecycle | Package Domain Schema + instance data | XHS Note、RD Issue candidate |
| C. External Provider object | 外部系统拥有 identity/lifecycle | Provider；Curis 存 ref/snapshot/provenance | GitHub PR、XHS post receipt、Shop order |
| D. Artifact | 人或 Agent 产出的可查看工作产物 | Artifact / Result system | Strategy report、design、code diff |
| E. Evidence | 支撑判断且需 provenance/freshness | Evidence system | test report、analytics receipt |
| F. Result | 对 Result Contract 的已提交/已接受结果 | Shared Result truth | Published content result |
| G. View projection | 可从 canonical/domain/external truth 重算 | Query/read model | Growth dashboard、Team list |
| H. UI-only state | 不影响业务真相 | user/local preference | selected Surface、pane width |

**Rule:** 如果删除 UI 后该事实仍影响责任、审计、恢复或下一轮决策，才考虑持久化；否则优先 projection 或 UI-only state。

---

## M. Team Scoped View

Workspace Team Surface / entry 只应是：

```text
Company OS Employee / Role / Responsibility / Assignment / Handoff truth
→ filtered by workspace_id and current permissions
→ Workspace-scoped Team projection
```

它可以成为 stable scoped view 或 Domain Navigation entry，但不拥有独立 Team model。禁止 XHS Team System、RD Team System、E-commerce Team System。

---

## N. Knowledge / Artifact Scoped View

“资料 / 素材 / 知识 / 研究报告 / 历史 Artifact”使用同一规则：

- Knowledge、Artifact、Evidence、Result 的 source of truth 保持共享；
- Package 声明需要哪些 scoped collection / query / asset type；
- Workspace view 只按 scope、type、relation、permission、freshness 投影；
- Package 不携带用户私有 Knowledge 内容；
- 长期历史不自动全量注入 Employee Session；按 reference-first / retrieve-on-demand 消费。

---

## O. Capability Provider Mapping

```text
Professional Surface
→ declares capability requirements / allowed actions
→ Capability Resolver checks requested / configured / effective / bound
→ Provider routing chooses Agent / Model / Tool / Connector
→ Shared execution returns Result / Evidence
```

Surface 可以需要 `research.write`、`image.generate`、`channel.publish`、`analytics.read` 等能力语义，但不得绑定死 Codex、ChatGPT、某模型或某 SaaS。Provider 更换不改变 Surface identity、Workspace identity、Employee identity 或 Result lineage。

---

## P. Workspace Package Gap

### P.1 Already present

现有 Proposal / bounded implementation 已有：

- Package identity/version/Core compatibility；
- one Workspace navigation label/icon；
- `surfaces.json`；
- Main / Context / Utility finite component declaration；
- Domain schemas、allowed action、capability requirements candidate；
- Registry-driven installed Workspace route；
- Package version pin、instance persistence、migration lifecycle；
- shared Core truth / safety boundary。

### P.2 Minimal gap

当前缺的不是第二个 Runtime，而是把现有 Surface declaration 从“一个 Workspace 的 Pane composition”扩展为“一个 Workspace 的 Professional Surface registry”。最小候选 metadata：

| Field | Purpose | Authority level |
|---|---|---|
| `surfaceKey` | Package-version-stable local key | Candidate |
| `label` / `icon` | Domain navigation presentation | Candidate |
| `role` | `overview / professional / scoped / settings-like` 等有限语义 | Candidate；避免过多 enum |
| `routeSegment` | Workspace-local route segment | Candidate |
| `default` / `fallbackOrder` | deterministic entry | Candidate |
| `objectViews` | object list/calendar/board/chart mapping | Candidate |
| `detailMappings` | selected object → Utility/Focus/detail mode | Candidate |
| `capabilityRequirements` | availability check | 已有概念，需 Surface scope |
| `availability` | required/optional/conditional/capability/stage rule | Candidate |
| `scopedProjections` | Team/Knowledge/Result/Evidence refs | Candidate |
| `operatingContext` | consume shared projection, never duplicate | Candidate |

本文不定义 JSON Schema，不授权加表。

---

## Q. Package Composition

### Q.1 Recommended semantic model

保持一个 canonical Workspace Package / pinned package composition，而不是每个 Surface 变成独立 Workspace 或微服务：

```text
Workspace Operating Package
├── Domain Navigation + Surface Registry
├── Domain schemas / object views
├── Surface modules (declarative composition units)
├── capability requirements / allowed actions
└── shared Core references
```

`Research / Writing / Image / Publishing / Analytics` 更适合作为 Capability Packages / requirements，被一个或多个 Surface 消费；它们不自动拥有 Workspace identity。只有未来真实复用、版本和独立交付需要证明后，才把 Surface module 固化为独立可组合包。

### Q.2 YAGNI boundary

本轮不拆微服务、不设计 Package dependency solver、不定义第三方 module marketplace。先证明一个 Package 内的 multi-surface declaration 足够。

---

## R. Optional / Conditional Surface Model

| Availability | Meaning | Navigation behavior |
|---|---|---|
| `required` | Workspace 专业身份不可缺 | 永远有稳定入口；缺能力时显示 blocked reason |
| `optional` | 用户/实例可启用 | 启用后位置稳定；关闭后不删除历史对象 |
| `conditional` | Package-declared business condition | 入口位置稳定，可显示 unavailable/locked explanation |
| `capability-dependent` | effective capability/binding required | 缺能力时不伪装可用，提供合法修复入口 |
| `stage-dependent` | Operating stage 影响可用性/attention | 位置不移动；只改变状态、badge 和可进入性 |

Stable Navigation 优先于每天重排。渐进开放通过状态与解释实现，不通过菜单随机出现/消失实现。

---

## S. Unknown Domain Bootstrap

以“我要经营一个宠物寄养业务”为例：

```text
Business Intent
→ read current Company / Business / Workspace truth
→ Domain research (external evidence required)
→ capability discovery / gap classification
→ Operating Model + Semantic Model
→ Workspace IA Composition
→ Domain Navigation Candidate + Professional Surface Candidate
→ Operating Team / Leader / Responsibility design
→ Workspace Package Candidate
→ Core expressibility / capability / safety check
→ validation / CEO Gate
→ canonical Workspace instance
```

用户只表达目标、约束、风险和必要偏好；不要求用户画导航、定义 Surface、配置 Workflow 或理解 Package。未知 Domain 失败时应返回 `RESEARCH / ADAPT / BUILD / ACQUIRE / ESCALATE / REFUSE` 等诚实路径，不生成万能 Dashboard。

---

## T. XHS Mapping

> 以下只用作 architecture validation。真实 Surface 边界、顺序与专业对象必须等待 WorkBuddy 外部 XHS research：`PENDING EXTERNAL SYNTHESIS`。

| Candidate Surface / View | Possible primary objects | Shared truth reused | Status |
|---|---|---|---|
| Operating Overview | Workspace Current Operating projection | Goal/Strategy/Cycle/Result/Decision | Candidate |
| Research | signal/source/hypothesis/report | Knowledge/Artifact/Evidence/Capability | Pending external evidence |
| Content / Publishing | Note、Calendar、review、publication | Team Operating/Handoff/Result | Strong internal evidence；exact boundary pending |
| Growth Analysis | metric/signal/experiment/review | Evidence/Signal/Review/Learning | Pending external evidence |
| Commercial | opportunity/offer/partner/commitment | Decision/permission/external side effect | Pending external evidence |
| Team | scoped view | Company OS | Shared projection |
| 资料 | scoped view | Knowledge/Artifact/Evidence | Shared projection |

`Research / Content / Growth / Commercialization` 绝不进入 Curis Core。

---

## U. RD Cross-check

| Candidate Surface | Professional question | Existing evidence repositioned |
|---|---|---|
| Operating Overview | 当前研发为何做、结果如何、下一步是什么 | Operating Context projection |
| Issue / Development | 当前要解决什么，谁在开发 | Issue、Workstation、Conversation |
| Build / Test | 构建与验证是否满足合同 | Build/Test result + Evidence |
| Release | 是否可发布、风险与回退是什么 | Release Result / Decision / Gate |
| Architecture | 当前结构与关键决定是什么 | Architecture Artifact / Decision |
| Code / Diff / Preview | selected object detail/tool modes | Utility / Focus，不是 Workspace |
| Team / Knowledge | scoped projections | Shared Company OS / Knowledge |

RD 能使用同一 Workspace → Navigation → Surface → Object/Detail → Shared Truth 模型，不要求 XHS Calendar，也不要求 Sub-Workspace。因此跨域抽象通过。

---

## V. E-commerce Stress Test

### V.1 Mapping

市场、竞品、渠道、商品、选品、库存、订单、营销、客服、售后、内容制作、财务、供应链可被组织为若干 Professional Surfaces；商品、订单、库存记录等是 Domain / external objects；Team 与资料是 scoped shared views；单个商品/订单/供应商是 Detail。

### V.2 Stress result

**Architecture passes, domain design not performed.** 该模型不需要 Workspace inside Workspace。Surface 数量过多时，通过 Domain IA grouping、stable navigation、progressive availability 和搜索处理，而不是增加层级。

如果某渠道/品牌/区域需要独立 Goal、Leader、Team、Operating Series、permission/data boundary 和 lifecycle，应创建同一 Business 下的并列 Workspace；否则保留为 Surface、filter 或 object scope。

---

## W. Routing / Persistence Implications

### W.1 Candidate route

```text
/ceo-office/workspace/{workspaceId}/{surfaceKey}
```

- `workspaceId` 是 canonical identity；
- `surfaceKey` 只在 pinned Package version 内解析；
- object/detail 作为后续 path/query/ref，不获得 Workspace identity；
- invalid/removed Surface 使用 Package migration/fallback/archived explanation，不能默默跳到错误页面。

当前 `/ceo-office/workspace/xhs?workspace_id=...`、`/software?...`、`/installed/{workspaceId}` 是 Implementation Truth，不是本 Candidate route 已实现的证据。

### W.2 Source of truth candidate

| Concern | Source of truth |
|---|---|
| Surface definition / nav order / stable key / default / mappings | Package metadata pinned by version |
| Installed package / version / workspace relation | Package Registry + Workspace instance |
| Available/blocked/attention state | Derived from Package rule + Runtime/Capability/Permission/Operating truth |
| Last active / pane width / selected view | user preference; not business truth |
| Domain objects | Package Domain Schema instance data or external provider refs |
| Team / Knowledge / Result / Evidence | existing Core/shared truth |
| Renderer components | finite Core registry; not truth store |

不直接加表。先确认现有 package registry / instance data / preference store 能否承载；只有验收证明不足时再建 bounded implementation Issue。

---

## X. Current Implementation Gap

| Capability | Classification | Evidence / boundary |
|---|---|---|
| Canonical Workspace under Business | `PARTIAL` | Product contract Frozen；当前 resolver/frontend changes 属 mixed/unaccepted baseline，Canonical Business Spine implementation 仍有独立 gate |
| Workspace Portal / entry | `PARTIAL` | 当前页面可列 Workspace 与进入专业工作面，但不承载 Domain Surface navigation |
| RD professional entry | `PARTIAL` | 编译 route + domain component；bounded slices accepted，完整 multi-surface / complete RD 未验收 |
| XHS professional entry | `PARTIAL` | bounded XHS slice accepted；Calendar/Note flow，不是 multi-surface registry；Publishing/Analytics 外部能力仍受限 |
| TTK / generic compatibility entry | `LEGACY / PARTIAL` | 明确显示未验收，不伪装专业面 |
| Installed Package navigation | `ALREADY EXISTS` | P0 Accepted：Registry-driven Workspace navigation |
| Installed Package Main/Context/Utility | `ALREADY EXISTS` for one fixed composition | P0 Accepted；fixed safe component set |
| Multi-Professional-Surface Registry | `MISSING` | validator 只接受 `main/context/utility` 三键和一组 fixed components |
| Package-declared Domain Navigation inside Workspace | `MISSING` | manifest 仅一个 Workspace navigation label/icon |
| Package-defined default / fallback / stable surface route | `MISSING` | 无相关 contract |
| Optional/conditional/stage/capability Surface availability | `MISSING` | capabilityRequirements 当前 P0 被限制为空；无 Surface-level rule |
| Surface-scoped object/detail mappings | `PARTIAL` | fixed object-list/detail/create form；无 registry/general mapping |
| Shared Team / Knowledge scoped projections per Surface | `MISSING` as declaration | shared primitives exist；未形成 Surface mapping contract |
| Operating Context four-field projection | `PRODUCT ACCEPTED / IMPLEMENTATION UNVERIFIED` | Product Surface Mapping accepted；未以当前 code/runtime evidence证明 multi-surface consumption |
| Domain route mapping | `CONFLICTING WITH TARGET / CURRENT LEGACY` | `workspaceOfficeHref` 以 RD/XHS/TTK hardcoded business type 映射 route；target 应由 package/registry resolution |
| Surface selection persistence | `MISSING` | Pane open/width preference exists；selected Professional Surface contract absent |

### X.1 Minimal Product → Implementation Gap

不是“重写 Workspace Runtime”。最小 gap 是：

1. Surface Registry contract；
2. Workspace-local route resolver；
3. Domain Navigation projection；
4. default/fallback/availability；
5. object/detail/scoped projection mapping；
6. RD/XHS migration strategy and acceptance。

在 CEO 接受 Candidate、更新 Product/Package Authority 并建立正式 Issue 前，不实施。

---

## Y. Trae Prototype Reposition Matrix

| Existing prototype element | Reposition | Keep / change | Authority note |
|---|---|---|---|
| XHS Publishing Calendar | Content / Publishing Surface 的 Calendar Object View | `REPOSITION`，不推翻 | XHS Instance evidence；不升 Core |
| XHS Note Split | Content Surface 的 Object Work View | `REPOSITION` | 同一 Note 的不同 view，不是新页面 identity |
| XHS 选题库 / 信号 | Content Context；若外部研究证明独立重复研究工作，可升级为 Research Surface | `KEEP AS CONTEXT NOW` | exact boundary pending external synthesis |
| XHS 图文预览 | Utility detail/preview | `KEEP` | shared Utility mechanism + XHS content |
| XHS Analytics | Growth Analysis Surface candidate 或 Content Result detail | `REPOSITION / PENDING` | 外部实践决定是否独立 Surface |
| XHS Calendar default | Package default candidate | `PRESERVE AS CURRENT XHS EVIDENCE` | 不自动推广为所有 XHS future package default |
| RD Issue / active development | Issue / Development Surface | `REPOSITION` | professional primary work |
| RD Build / Test | Build / Test Surface candidate | `REPOSITION` | Result/Evidence driven |
| RD Release | Release Surface candidate | `REPOSITION` | high-impact Gate remains shared |
| RD Architecture | Architecture Surface candidate | `REPOSITION` | Artifact/Decision truth reused |
| RD Diff / Source / Preview | Utility modes / selected object detail | `KEEP` | 不成为独立 Workspace |
| Employee Workstations | Shared Work Area available across Surface context | `KEEP SHARED` | 不变成 Domain Navigation tabs |
| Operating Context strip | Workspace-wide shared projection consumed by each Surface | `KEEP ONE SOURCE` | 不在每个 Surface 存一份 |
| Global CEO Assistant | Global company employee with current scope | `KEEP GLOBAL` | 不降级为 RD/XHS Assistant，不是第五 Pane |

当前根目录 `Curis-Professional-Workspace-Operating-Reconciliation-CEO-Review.md` 是未登记、未跟踪的 visual review artifact；本研究只把它视为 local observation，不把它升级为 Authority 或 WorkBuddy external research conclusion。

---

## Z. CEO Decisions

### Z.1 20 review questions answered

| # | Question | Research answer | CEO decision needed? |
|---:|---|---|:---:|
| 1 | Workspace ≠ Page 是否成立？ | **YES**，与 Current Truth 兼容 | Confirm wording |
| 2 | Workspace 是否应定义为 Professional Operating Environment？ | **YES as Candidate term**；不是历史 Frozen | **YES** |
| 3 | 一个 Workspace 是否允许多个 Professional Surfaces？ | **YES as Candidate architecture** | **YES** |
| 4 | Domain Navigation 应由谁声明？ | Workspace Package；由 Workspace Engineering/Domain Expert 形成，Core 校验渲染 | **YES** |
| 5 | Core 是否知道 XHS 菜单？ | **NO** | No if model accepted |
| 6 | Context 是否适合承担 Domain Navigation / Context？ | **YES, candidate extension**；adaptive，不承载 Conversation | **YES** |
| 7 | Main 是否承载当前 Professional Surface？ | **YES** | **YES** |
| 8 | Detail 是否仍按需出现？ | **YES**，Utility/Drawer/Focus/Main split 按对象需要 | No |
| 9 | CEO Assistant 如何保持 Global？ | 单一 Company employee identity + scoped current context；不成为第五 Pane | No new system |
| 10 | Operating Context 放哪里？ | 单一 Workspace projection；各 Surface Main top strip 消费，Detail on demand | Confirm placement principle |
| 11 | Team 是否只是 scoped Company OS view？ | **YES** | No |
| 12 | Knowledge 是否只是 scoped Curis Knowledge view？ | **YES**，Artifact/Evidence/Result 同理 | No |
| 13 | Package 是否需要 Surface Registry？ | **YES as Candidate** | **YES** |
| 14 | 当前 Package Contract 是否足够？ | **PARTIAL**；单 Pane composition 足够，multi-surface 不足 | Accept minimal gap |
| 15 | Unknown Domain 如何生成环境？ | Intent → research → semantics → IA/navigation/surfaces → team → package → validation | Confirm process |
| 16 | RD 是否适配？ | **YES** | No architecture blocker |
| 17 | 电商压力测试是否通过？ | **YES at architecture level**；Domain design 未做 | No architecture blocker |
| 18 | XHS Calendar 应归位哪里？ | Content / Publishing Surface 的 Calendar Object View | Confirm after external synthesis |
| 19 | 哪些仍等待 WorkBuddy 外部研究？ | XHS exact lifecycle、Surface set/order/boundaries、Research/Growth/Commercial semantics、required objects/metrics、real tool/agent evidence | No premature freeze |
| 20 | CEO 真正需要决定什么？ | 接受/拒绝 Z.2 的六项 Candidate architecture decisions | **YES** |

### Z.2 Decision packet

CEO 只需决定六件事：

1. 接受 `Workspace = canonical Professional Operating Environment` 为 Candidate architecture term；
2. 接受一个 Workspace 可有多个 Professional Surfaces，且不增加 Sub-Workspace；
3. 接受 Package-declared Domain Navigation + Surface Registry、Core validate/render 的 ownership；
4. 接受 Context = Domain Navigation + current context、Main = selected Surface、Utility = on-demand detail 的职责补充；
5. 接受 deterministic default + last active + suggestion-not-auto-jump；
6. 接受在 WorkBuddy external XHS research 返回前，只冻结 Universal model，不冻结 XHS exact Surface set。

### Z.3 If accepted, next gate

```text
CEO ACCEPTS REVIEW
→ reconcile Candidate into the applicable Product / Package Authority through a separate authorized task
→ external XHS synthesis
→ Domain IA / Surface contract
→ bounded implementation Issue
→ RD/XHS/Package migration and real Browser/Desktop acceptance
```

---

## STOP STATE

```text
CURIS PROFESSIONAL WORKSPACE ARCHITECTURE
— INTERNAL AUTHORITY AUDITED
— WORKSPACE / PAGE DISTINCTION REVIEWED
— MULTI-SURFACE MODEL REVIEWED
— DOMAIN NAVIGATION OWNERSHIP REVIEWED
— FOUR-PANE RECONCILED
— CONTEXT ROLE REVIEWED
— AUTONOMOUS OPERATING MAPPED
— PACKAGE IMPLICATIONS IDENTIFIED
— XHS MAPPED AS PROVISIONAL
— RD CROSS-CHECKED
— E-COMMERCE STRESS-TESTED
— UNKNOWN DOMAIN PATH REVIEWED
— TRAE PROTOTYPE REPOSITIONED
— PENDING EXTERNAL SYNTHESIS
— NO AUTHORITY CHANGE
— NO IMPLEMENTATION
— STOP FOR CEO REVIEW
```
