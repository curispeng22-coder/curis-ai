# CURIS CANONICAL BUSINESS SPINE
## PRODUCT / RUNTIME AUTHORITY REVIEW

Authority Class: REVIEW  
Status: Frozen  
Disposition: CEO ACCEPTED — IMPLEMENTATION AUTHORIZED / FRONTEND OWNER ASSIGNED  
日期：2026-08-20  
Owner：Product Architecture Authority

## 0. 范围与结论

本 Review 只收敛 Company → Department → Business → Workspace 的 canonical persisted product spine。
本轮没有修改 Runtime、Schema、数据库、Frontend、Prototype、活动数据或迁移数据。

CEO 已接受本合同，并指定主开发为 Frontend Baseline Promotion Integration Owner。接受只解除实现授权，不把当前代码或数据库误报为已完成。

当前事实分为两层：

| 层 | 结论 |
| --- | --- |
| Product Truth | `Business` 是唯一的公司内业务身份；长期 Business 必须属于 Department，并至少拥有一个 Workspace。 |
| Implementation Truth | 当前代码仍由 `business_directions`、`projects`、`department_instances` 与 `workspaces.business_id` 多条旧/过渡链共同承载；Business relation 尚未成为可验证的 canonical persisted relation。 |

因此本 Review **不宣称 Business Spine 已实现**。实现必须按本 Review §I 的顺序进入正式 Issue，并在每个 Stop Gate 处独立 Review。

## A. Canonical Business Object

### A.1 产品合同

`Business` 是 Company OS 中拥有独立经营身份的持久化对象，不等于 Business Direction、Project、Workspace label 或任意 free-form reference。

最小字段合同：

| 字段 | 语义 | 来源 / 约束 |
| --- | --- | --- |
| `business_id` | 全局唯一、可被 Workspace / Result / Assignment / Route 引用的身份 | Canonical Business identity |
| `company_id` | 所属 Company | 必须解析到真实 Company |
| `department_id` | 所属 Department | 长期 Business 必填；不得直属 Company |
| `name` | 对 CEO 可读的业务名称 | 非空 |
| `lifecycle_status` | Business 生命周期 | 至少支持 draft / active / paused / archived 等经批准状态 |
| `goal` / `positioning` | Business-level 方向与目标 | 产品字段；不与 Workspace-level Goal 混淆 |
| `created_at` / `updated_at` | 生命周期审计时间 | 持久化事实 |

`business_directions` 不再作为 Business identity 的默认答案。根据当前代码审计，它更接近 Business 下的 Strategy / Direction truth；在 canonical Business 对象落地前，保留为 supporting / compatibility object，不允许其 `direction_id` 继续伪装为 `business_id`。

### A.2 当前实现证据

- `backend/app/runtime/models.py` 的 `business_directions` 没有 `company_id` / `department_id`。
- 同文件的 `workspaces.business_id` 为文本字段，没有 Business 外键或存在性约束。
- `backend/app/runtime/workspace.py` 的 Workspace 创建路径接收 `business_ref`，并未证明该值对应真实 Business。
- `backend/app/shared_workspace_projection.py` 将 `workspaces.business_id` 直接按 `business_directions.direction_id` 读取；找不到时返回 `UNKNOWN`，因此当前仍是兼容投影，不是 canonical resolver。
- 旧 `projects` 表拥有 `company_id` / `department_id`，但其产品语义是 Project / work container，不是 Business；不能因字段形状相近而升格为 Business。

## B. Hierarchy Invariants

Current Product Truth 冻结为：

```text
Company
└── Department
    └── Business
        └── Workspace
```

### B.1 不变量

1. Department 必须属于 Company。
2. Business 必须属于 Department。
3. Workspace 必须属于 Business。
4. Business 不允许 orphan。
5. Workspace 不允许引用不存在、已越权或无法解析的 Business。
6. 长期 Business 至少拥有一个 Workspace；一个 Business 只有一个 Workspace 是正常状态。
7. Company-level Employee 可以不属于 Department。
8. Employee hierarchy / Responsibility Assignment 不得反向改变 Business hierarchy。

### B.2 分层保证责任

| 层 | 必须保证 |
| --- | --- |
| DB / Schema | 唯一 ID、非空归属、外键或等价存在性约束、事务原子性、禁止 orphan。具体采用 FK 还是等价约束需由实现 Issue 决定。 |
| API / Service | Tenant / Company / Department / Business scope 校验；禁止 free-form relation；所有 deep link 返回 canonical parent path。 |
| Runtime | 执行、结果、Assignment、Workspace 投影只消费已解析的 Business identity；关系失效时 fail-closed，不运行、不伪造 parent。 |
| Frontend | 只消费 API read model；不硬编码部门、业务或 Workspace 名称，不自行拼接 parent。 |

## C. Business Creation Contract

### C.1 原子创建

用户创建一个长期 Business 时，最小成功结果必须是：

```text
Business
+ First Workspace
+（若进入 active：Workspace Leader Assignment / 最小责任承载）
```

推荐事务语义：

```text
BEGIN
  Create Business (draft or active)
  Create First Workspace
  If active: create or bind minimum Workspace Leader Assignment
COMMIT
```

任一环节失败必须 `ROLLBACK`。禁止留下 Business 已存在但 First Workspace 不存在的半成品 Current Truth，也禁止留下 Workspace 指向不存在 Business。

### C.2 Draft 与 Active

- `DRAFT` 可以保留“Leader 尚未完成配置”的显式阻塞，但 Business 与 First Workspace 必须同时存在且关系可解析。
- 只有满足长期 Workspace 的真实责任承载后，才能进入 `ACTIVE / OPERATING`；不能用 UI 卡片或默认字符串假装 Leader。
- Company-level Employee 仍可在没有 Department 的情况下存在；这不改变 Business 的 Department 必填关系。

## D. Legacy Coexistence / Migration Classification

| 现有对象 / 概念 | 本 Review 分类 | 当前用途 | 禁止误读 | 后续处理 |
| --- | --- | --- | --- | --- |
| `business_directions` | Supporting object + compatibility / migration source | CEO Day 与部分 Runtime 的方向、目标、验证和生命周期事实 | 不等于 canonical Business identity | 新 Business 建立后，将 Direction 作为 Business 下 Strategy / Direction 子对象；旧记录需显式映射。 |
| `projects` / Project | Legacy compatibility object / migration source | 旧 Company → Project work container、旧研发/任务链 | 不等于 Business，不得作为 Business Directory 的最终来源 | 保留旧路由和历史引用；新 Business Spine 不再写入 Project。 |
| `department_instances` | Existing Department implementation candidate | 当前 Company 下的部门实例、员工归属和责任关系 | 不等于新 Business，也不能与 `departments` catalog 混为一物 | Phase 1 明确其与 canonical Department identity 的桥接 / promotion 方式。 |
| `departments` / department catalog | Supporting catalog / historical implementation surface | 部门类型或旧部门聚合定义 | 不自动等于 Company 的 Department instance | 只作为类型/目录来源，实例关系由 canonical Department 决定。 |
| 旧 Office | Deprecated terminology / migration source | 历史 Workspace 命名和页面隐喻 | 不新增 Office 层级，不形成第二套组织关系 | 只做显示/迁移映射，Current 使用 Workspace。 |
| CEO Day Business Direction | Supporting Strategy / Direction truth | 经营意图、目标、周期和证据入口 | 不可再充当 Business 主键 | 通过 Business ID 反挂到 canonical Business。 |
| `workspaces.business_id` free-form value | Legacy compatibility reference | 当前 Workspace 关联字段 | 不是 authoritative relation | 只允许通过兼容读取；新写入必须使用 canonical Business ID。 |

### D.1 结论

当前没有两个 equally-valid 的 canonical Business 实现候选。`business_directions` 最接近现有 Runtime 的业务方向来源，`projects` 最接近旧 Company work container，但二者都不满足本合同的 Company + Department + Business identity 不变量。因此本 Review 冻结产品答案，不擅自把任一旧表升格为 canonical。

## E. Existing Data Policy

在没有可靠映射前，禁止把现有 free-form Workspace 自动挂到默认 Business。

### E.1 迁移选项评估

| 方案 | 结论 | 原因 |
| --- | --- | --- |
| 一次性迁移 | 不作为默认方案 | 当前 source 混合、活动数据与历史引用边界未完成审计；一次性误挂不可接受。 |
| Lazy resolution + migration | 推荐候选 | 先按现有 ID 只读解析；可确定时生成映射，无法确定时保留原值并进入隔离状态。 |
| Compatibility bridge | 必须有的过渡层 | 旧 Project / Direction / Workspace 引用需要在迁移期间可追溯，但不能继续产生新的 free-form authoritative relation。 |
| 重建 isolated/current development data | 只适用于开发验证 | 不替代真实数据政策；只能在隔离 SQLite / fixture 中验证新契约。 |

### E.2 无法确定归属的记录

无法解析 Company / Department / Business 的旧 Workspace 必须进入：

```text
UNRESOLVED → QUARANTINED
```

它可以被审计和人工修复，但不得出现在可运行的 Business Directory、不得进入 Operating、不得生成假 Parent Path。原始引用、来源、发现时间和修复责任必须保留。

## F. Parent Resolution Contract

唯一 canonical resolver：

```text
Workspace → Business → Department → Company
```

resolver 必须按当前 Tenant / Company scope 解析并返回：

- canonical IDs 与可读名称；
- `parentPath` / reverse entry；
- Business Workspace Directory 所需的成员关系；
- direct route / deep link 所需的安全目标；
- `resolved / unknown / stale / quarantined` 状态与原因；
- deleted / archived parent 的 fail-closed 处理；
- refresh 后不改变 ID 的稳定读取。

前端不得硬编码“内容增长部”“小红书运营”“AI 科技”等名称。它们只能来自 relation truth；没有 relation truth 时显示 Unknown / Unresolved 和恢复入口。

## G. Business Read Model

Business 页面已经冻结为：

```text
Definition
Operating Summary
Workspace Directory
Business Team
```

本轮只冻结来源，不设计 UI：

| 页面区 | 真实来源 | 规则 |
| --- | --- | --- |
| Business Definition | Canonical Business identity + Business-level Goal / Positioning + Strategy / Direction references | 不从 Project 或 Workspace label 拼接。 |
| Operating Summary | Derived read model：Business-level Strategy / Direction + Work + Result + Need + Decision + Assignment + Workspace status | 标记 source / freshness / unknown；不复制底层事实。 |
| Workspace Directory | `Workspace.business_id = canonical Business.business_id` 的关系查询 | 只返回已解析、当前 Company scope 内的 Workspace。 |
| Business Team | Responsibility Assignment + Role + Employee binding / membership projection | 不从 Project owner 字段猜测团队。 |
| Risk / Result / Next | Existing Work / Result / Need / Decision / Evidence references | 只做投影，不新建第二套 Business truth。 |

## H. Frontend Baseline Ownership Gate

当前 Frontend 不能直接 promotion 为 clean baseline。原因是关键 Business / Workspace / RD / XHS 路由依赖 untracked mixed-source 文件，且共享 Runtime seams 跨 Domain 共用。

| FILE | SOURCE | OWNER | CURRENT STATUS | PROMOTION DECISION |
| --- | --- | --- | --- | --- |
| `frontend/app/ceo-office/business/page.js` | 当前 Business Map candidate | Business / Company OS UI owner 未正式指定 | UNTRACKED | BLOCKED；需单独 owner + provenance + tracked promotion。 |
| `frontend/app/ceo-office/workspace/page.js` | Workspace Portal candidate | Shared Workspace UI owner 未正式指定 | UNTRACKED | BLOCKED；不能整文件直接 add。 |
| `frontend/components/runtime/WorkspaceRuntimeView.js` | Shared Runtime / RD / Content mixed view | Shared Runtime UI + Domain owners 交叉 | UNTRACKED / MIXED | BLOCKED；先拆清 ownership 或建立受控 promotion slice。 |
| `frontend/lib/runtimeApi.js` | Shared Runtime API client | Shared Runtime UI | TRACKED，但依赖 mixed source | 保留；不能单独视为完整 baseline。 |
| `frontend/app/ceo-office/workspace/software/page.js` | RD Domain candidate | RD UI owner | UNTRACKED | BLOCKED；需与 Runtime source 同一 provenance。 |
| `frontend/app/ceo-office/workspace/xhs/page.js` | XHS Domain candidate | Content Growth UI owner | UNTRACKED | BLOCKED；需与 shared Runtime / API 同步审计。 |
| `frontend/app/ceo-office/workspace/shortvideo/page.js` | TikTok Domain candidate | Shortvideo UI owner | UNTRACKED | BLOCKED；不得从静态页面推断交付。 |
| `frontend/app/ceo-office/projects/**` | Legacy Project surface | Legacy compatibility owner | TRACKED | 不 promotion 为 Business UI；保留迁移入口，直到 replacement 有独立 Review。 |
| `frontend/app/ceo-office/organization/**` | Organization / Department surface | Organization UI owner | TRACKED | 可作为现有 Department candidate；canonical Business promotion 仍等待 Spine implementation。 |

### H.1 Promotion 门禁

必须先完成：source manifest、owner、Allowed Files、旧/新关系 provenance、clean tracked baseline、最小路由与 API 依赖审计；禁止 whole-file add 作为“完成”或用视觉验收覆盖 ownership 缺口。

## I. Implementation Order（仅供 CEO 接受后拆 Issue）

| Phase | 内容 | 前置 / 退出条件 |
| --- | --- | --- |
| 0 | Canonical Business / Department identity decision 与 legacy disposition | CEO 接受本 Review；明确旧 ID 映射责任。 |
| 1 | Canonical Business persistence / Company + Department + Business references | Schema/API Issue；不存在 orphan / free-form authoritative write。 |
| 2 | Legacy compatibility / migration bridge | `business_directions`、Project、Department Instance、旧 Workspace 引用可追溯；UNRESOLVED / QUARANTINED fail-closed。 |
| 3 | Atomic Business + First Workspace create | 同事务；失败 rollback；Active 前满足 Leader responsibility。 |
| 4 | Parent resolver / deep route | Workspace → Business → Department → Company 稳定读取、刷新、删除/失效处理。 |
| 5 | Business read model | Definition / Summary / Directory / Team 从同一 canonical relation 投影。 |
| 6 | Frontend baseline promotion | owner、manifest、tracked source、clean build、no mixed whole-file promotion。 |
| 7 | Single / Multi / Generic E2E | fresh isolated DB、restart、failure/recovery、deep links、Company scope 与旧数据策略证据。 |

## J. Product → Implementation Gaps

以下是本 Review 明确登记的 Gap，不是已完成能力：

- Canonical Business persisted object 尚未存在于当前实现；
- Department / Business / Workspace DB invariant 尚未完整保证；
- Business + First Workspace 原子创建尚未实现；
- Parent resolver / deep route 尚未实现；
- Business read model 尚未从 canonical relation 生成；
- Legacy mapping 与 UNRESOLVED / QUARANTINED policy 尚未实现；
- Frontend baseline ownership / promotion 尚未完成。

## K. CEO Decision Required

以下 CEO Decision 已于 2026-08-20 正式接受：

1. 接受 Business 作为唯一 canonical persisted identity；
2. 接受 `business_directions` 为 Strategy / Direction supporting object，而非 Business identity；
3. 接受 Project 为 legacy compatibility object，不再作为 Business 入口；
4. 接受无法映射的旧 Workspace 进入 `UNRESOLVED → QUARANTINED`；
5. 指定 Frontend baseline promotion owner；
6. 主开发担任 Frontend Baseline Promotion Integration Owner；XHS / RD / Shared Workspace 仍分别保留 Domain / Product Authority。
7. 授权后续按 Phase 1–7 建立正式 Issue，允许安全依赖下合并阶段，但每个 Stop Gate 单独 Review。

以下仍是实现门禁，而不是产品决策阻塞：active DB migration、ambiguous legacy mapping、destructive rewrite、bulk frontend promotion、Product Contract conflict，以及 commit / push gate。主开发不得猜测映射、升级旧对象或整文件提交 mixed-source Frontend。

## STOP STATE

CURIS CANONICAL BUSINESS SPINE  
— PRODUCT CONTRACT DEFINED  
— CANONICAL BUSINESS IDENTITY FROZEN AS PRODUCT SEMANTICS  
— COMPANY / DEPARTMENT / BUSINESS / WORKSPACE INVARIANTS DEFINED  
— LEGACY COEXISTENCE POLICY DEFINED  
— ATOMIC CREATION CONTRACT DEFINED  
— PARENT RESOLUTION CONTRACT DEFINED  
— BUSINESS READ MODEL SOURCES DEFINED  
— FRONTEND BASELINE OWNERSHIP GATE IDENTIFIED  
— FRONTEND BASELINE INTEGRATION OWNER ASSIGNED  
— IMPLEMENTATION AUTHORIZED THROUGH FORMAL ISSUE  
— STOP FOR IMPLEMENTATION QUEUE / GATE REVIEW
