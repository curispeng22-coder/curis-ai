# CURIS WORKSPACE / SURFACE OWNERSHIP MATRIX

**Authority Class:** REVIEW  
**Status:** Review  
**Disposition:** CANDIDATE / ANTI-DUPLICATION MATRIX / READY FOR CEO REVIEW  
**Date:** 2026-08-21  
**Implementation:** Not authorized  

> 用途：防止未来为每个 Domain 重造 Workspace、Team、Knowledge、Capability、Runtime、Result、Evidence、Navigation 或 UI state 系统。`Candidate` 行等待 CEO 接受；本表不修改现有 Authority 或 Schema。

## 1. Layer rule

| Layer | Responsibility |
|---|---|
| Core | canonical identity、安全、Shell、shared truth、route validation、finite renderer、failure/recovery |
| Package | Domain semantics、Domain Navigation、Professional Surface composition、object mappings、requirements |
| Instance | pinned Package version、canonical Workspace scope、instance-owned data、allowed optional enablement |
| View | read projection、selection、layout、last active；不制造业务真相 |

## 2. Ownership matrix

| Object / Concern | Owner | Source of Truth | Declared By | Rendered By | Runtime Used | Persistence | Example XHS | Example RD | Example E-commerce |
|---|---|---|---|---|---|---|---|---|---|
| Company identity | Core | Company OS canonical Company | Company bootstrap / Core | Company Shell | Existing Company OS | Core DB | 当前公司 | 当前公司 | 当前公司 |
| Department identity | Core | canonical Department | Organization truth | Company / Organization surfaces | Existing Company OS | Core DB | 内容增长部 | 研发部 | 电商运营部 |
| Business identity | Core | canonical Business | Business creation contract | Business Surface / Directory | Existing Company OS | Core DB | 小红书运营 | Curis 产品研发 | 自营电商业务 |
| Workspace identity | Core | canonical Workspace under Business | Workspace creation / Package materialization | Workspace Portal + Shell | Existing Workspace Runtime | Core DB | `AI 科技` | 产品研发 Workspace | 某品牌店铺经营 Workspace |
| Workspace parent path | Core | Workspace → Business → Department → Company resolver | canonical relations | Breadcrumb / return route | Parent Resolver | Core DB + derived read | 内容增长部 / 小红书运营 / AI科技 | 研发部 / 产品研发 / Workspace | 电商部 / 自营业务 / Workspace |
| Workspace Goal / Positioning / Strategy | Core shared truth | Workspace operating truth | CEO / authorized Leader | Current Operating + Detail | Operating Lifecycle / Decision | Versioned Core truth | 账号经营目标 | 产品目标 / 研发策略 | 店铺经营目标 |
| Operating Series / Cycle | Core shared truth | Operating Lifecycle contract | authorized Trigger / Leader | Current Operating projection | Existing Cycle + candidate controller | Durable Core truth | 增长验证轮次 | 发布验证轮次 | 选品/转化轮次 |
| Workspace Leader / Team | Core shared truth | Employee × Role × Workspace scope Assignment | Organization / Staffing | scoped Team view + Shared Work Area | Team Operating / Responsibility Router | Core DB | 运营 Leader + 内容团队 | 研发 Leader + 工程团队 | 店长/运营/客服/供应链团队 |
| Employee Workstation | Shared UI capability | Employee identity + current scoped responsibility/session | Core + Provider binding | Main Shared Work Area | Provider execution + Team Operating | Runtime truth + UI preference | 内容创作员工会话 | 工程师会话 | 客服/运营员工会话 |
| Global CEO Assistant | Core / Company employee | one Company-level Employee identity and scoped context | Company OS | global Assistant surface / overlay | Existing Assistant coordination paths | Core identity + scoped sessions | 当前 Workspace 上下文 | 当前 Issue/Workspace 上下文 | 当前订单/业务上下文 |
| Workspace Package identity/version | Core Package Registry | installed Package + digest + pinned version | Package install | Workspace entry / provenance detail | Workspace Package Runtime | Package Registry | XHS operating package candidate | RD package candidate | commerce package candidate |
| Domain Semantic Model | Package | Package Domain Schema / references | Workspace Engineering + Domain Expert | Surface object views | Package validation + Core object APIs | Package metadata + instance data | Note / account semantics | Issue / build semantics | Product / order / inventory semantics |
| Domain Navigation definition | Package `Candidate` | versioned navigation declaration | Workspace Engineering + Domain Expert + Product Expert | Context / Workspace-local nav | Core route resolver | Package metadata | Research / Content / Growth candidates | Development / Build-Test / Release | Product / Order / Marketing / Service groups |
| Navigation validation | Core | finite contract, route/key/permission checks | Core contract | Shell | Core validator / resolver | Code + registry state | rejects invalid XHS key | rejects route collision | rejects unsupported module |
| Navigation availability | Derived shared projection `Candidate` | Package rule + capability/permission/stage truth | Package rule, evaluated by Core | stable nav state/badge/explanation | Capability Resolver + Operating truth | Recomputable; optional cache | Commercial unavailable explanation | Release blocked by permission | Warehouse connector unavailable |
| User navigation preference | View/User | last active / expanded group / local order within allowed limits | user action | Shell | None | local/user preference | last Content Surface | last Build/Test Surface | last Orders Surface |
| Professional Surface definition | Package `Candidate` | Surface Registry in pinned Package version | Workspace Engineering / Domain Expert | Main | finite Core renderer + domain components | Package metadata | Content / Growth candidates | Development / Release | Orders / Service |
| Selected Professional Surface | View/User | explicit route or valid last active | user / deep link / deterministic entry policy | Main | route resolver | URL + user preference | Content | Development | Orders |
| Default / fallback Surface | Package `Candidate` | pinned Package declaration | Package authoring process | Workspace entry | route resolver | Package metadata | Calendar/Content candidate | Development candidate | Operating Overview candidate |
| Runtime Surface recommendation | Derived view | current Need/Risk/Review/Decision state | Operating projection | badge / suggestion only | Operating Lifecycle truth | no separate truth; optional dismissal preference | suggest Growth Analysis | suggest Build/Test review | suggest Inventory attention |
| Operating Overview | View projection | Workspace Current Operating | shared mapping, consumed by Package | Main Surface or entry summary | Operating Lifecycle projection | Recomputable | 经营状态/重点/判断/下一步 | 研发状态/重点/判断/下一步 | 店铺状态/重点/判断/下一步 |
| Workspace Current Operating | Core shared projection | Goal/Strategy/Cycle/Review/Decision | Operating Lifecycle contract | every Surface light summary + detail on demand | Operating Lifecycle / read model | one derived/versioned projection | 同一四字段 | 同一四字段 | 同一四字段 |
| Domain business object | Package or external Provider | Package instance data or provider canonical object | Domain Schema / Connector contract | Object View / Detail | Package Runtime / Connector adapters | Domain data or external ref | Note | Issue / PR ref | Product / Order / SKU |
| Object list / calendar / board / chart | View projection | query over domain/Core/external truth | Surface declaration | Main / Context | read APIs | recomputable + filters | Note Calendar | Issue board / build list | Order queue / inventory view |
| Selected object | View/User | current route/query/selection | user interaction | Main split / Utility | None | URL/local UI state | selected Note | selected Issue/Artifact | selected Order |
| Object Detail | Package mapping + Core container | underlying object truth | Surface detail mapping | Utility / Drawer / Focus / Main split | object read/write APIs | no duplicate object | Note detail | Issue detail | Order detail |
| Professional editor / tool mode | Package mapping + Core finite registry | selected object + allowed action | Surface declaration | Utility / Focus | Core action / Provider capability | edits persist only to owning object | content editor / preview | Diff / Source / Preview | product editor / shipment action |
| Work / Assignment | Core shared truth | Work, Responsibility, Assignment | Team Operating / Leader | relevant Surface + Workstation | Responsibility Router / Provider execution | Core DB | content task assignment | development task | customer-service work |
| Handoff / Consult / Review / Return | Core shared truth | responsibility routing events | authorized Team Operating action | Workstation / Detail / activity | Responsibility Router | durable Core truth | 创作→审核→发布 | Dev→QA→Review | 客服→售后/财务 |
| Result | Core shared truth | Result Contract / accepted output | producing Assignment + acceptance owner | source Surface + reference | Result Store / existing Runtime | durable Core truth | published content result | build/test/release result | fulfilled order / campaign result |
| Artifact | Core shared asset truth | Artifact store / Result reference | Employee / Provider / import | reference + Utility full view | Artifact APIs | retained by policy | research report / content asset | design / code diff | product image / finance report |
| Evidence | Core shared truth | Evidence with provenance/freshness | source/verifier | reference + Detail | Evidence APIs | durable per policy | platform receipt / analytics source | test log / review evidence | payment/shipping/stock receipt |
| Signal | Derived shared truth | formula/window/baseline/source refs | evaluation logic | Growth/Analysis view + Detail | Operating Review | recomputable; material use pinned | engagement trend | defect/build trend | conversion/stock risk |
| Review / Learning | Core shared truth | authorized Review / accepted Learning | Leader / reviewer | Surface summary + Detail | Operating Lifecycle | versioned/append-only | content pattern learning | release/process learning | pricing/fulfillment learning |
| Next-cycle Decision | Core shared truth | Decision / Packet / Cycle refs | Leader or CEO by policy | Current Operating / Decision detail | Decision + Operating Lifecycle | durable Core truth | CONTINUE/ADJUST/WAIT | CONTINUE/ESCALATE | WAIT/ADJUST/PAUSE |
| Team view | View projection | Company OS Employees/Roles/Assignments filtered by Workspace | Package asks for scoped projection | Context/Main scoped view | Company OS queries | recomputable | XHS team | RD team | store operating team |
| Knowledge view | View projection | global Knowledge refs filtered by Workspace/Surface permission | Package asks for scoped projection | Context/Main/Utility | Knowledge retrieval | shared truth + refs | brand materials / research | specs / ADRs | product manuals / policies |
| Historical work view | View projection | Work/Result/Decision/Artifact retention truth | Package IA declaration | scoped history surface | shared history/read model | business-significant history | past campaigns | past releases | past orders/campaigns |
| Capability requirement | Package | semantic capability requirement | Package | Surface blocked/ready state | Capability Resolver | Package metadata | research/write/publish/analytics | code/test/deploy | catalog/order/payment/shipping |
| Capability configured/effective/bound | Core | Capability Catalog / Connection / Health / Binding | Settings/Employee/Workspace owner | status/detail, not fake success | Capability Resolver | Core DB / secure config | XHS connector state | Git/provider state | store/payment/logistics state |
| Provider selection | Core routing | effective capability and authorized binding | policy / user where allowed | usually hidden; detail on demand | Model/Agent/Tool/Connector adapters | config + execution provenance | model/tool chosen for content | Codex/CI provider | commerce SaaS/connector |
| External side-effect permission | Core | permission/policy/CEO Gate | authorized owner | Decision / blocked state | permission + execution gateway | secure/audit truth | publish permission | deploy permission | refund/payment/shipment permission |
| Context Pane open/width | View/User | local preference | user action | Shell | None | local preference | 选题库展开 | source tree/context expanded | catalog filter expanded |
| Utility open/mode/width | View/User | local preference + selected object | user action / object reference | Shell | None | local preference | preview mode | Diff mode | order detail mode |
| Search | Core shared capability | scoped indexed/read truth | Shell + Package search facets | Search Surface | shared query | index/read model | Note/Result/资料 | Issue/Artifact/Evidence | Product/Order/Customer |
| Route | Core resolver + Package mapping `Candidate` | canonical `workspaceId` + Package-local `surfaceKey` | Package declaration validated by Core | App router | route resolver | URL + registry | `/workspace/{id}/content` | `/workspace/{id}/development` | `/workspace/{id}/orders` |
| Retention / archive | Core policy + Package domain rule | retention contract, Result/Evidence/Artifact policy | Core policy / Package constraint | read-only archive/history | Package lifecycle + shared retention | durable/audited | removed Surface keeps Notes/results | old release evidence retained | closed orders retained |
| UI-only badge / attention | View projection | Need/Risk/Decision/availability | derived from truth | navigation / header | read model | no new business entity | Growth needs review | Release blocked | Inventory risk |

## 3. Anti-duplication decisions

| If a Domain asks for… | Reuse | Do not create |
|---|---|---|
| Team | Company OS scoped Team projection | `XhsTeam`, `RdTeam`, `CommerceTeam` systems |
| Knowledge / Materials | shared Knowledge / Artifact / Evidence scoped view | per-Domain Knowledge Base Runtime |
| Work routing | Work + Responsibility + Assignment + Handoff | per-Surface Workflow/Task engine |
| autonomy | Operating Series / Cycle / Review / Decision projection | Autonomous Surface Runtime |
| provider work | Capability Resolver + Provider adapters | Surface-bound model/SaaS identity |
| navigation | Package declaration + Core renderer | hardcoded Core Domain menu |
| details | object mapping + Utility/Focus | new Workspace or duplicate entity |
| analytics | Evidence/Signal/Review projections | second Result/Evidence/Analytics truth |

## 4. Boundary test

Create a **new sibling Workspace** only when all or most are independently owned:

- Goal / Positioning / Strategy;
- Leader / Operating Team;
- Operating Series / Cycle;
- permission and data boundary;
- lifecycle / archive / accountability.

Otherwise stop at the first fitting type: Professional Surface → Object View → Detail → Scoped View → UI-only state.

```text
CANDIDATE ONLY
NO AUTHORITY CHANGE
NO SCHEMA CHANGE
NO IMPLEMENTATION
STOP FOR CEO REVIEW
```
