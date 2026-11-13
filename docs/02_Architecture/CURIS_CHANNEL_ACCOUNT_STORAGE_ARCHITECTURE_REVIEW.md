# ChannelAccount 存储架构评审（S1 前置）

> Status: Review · Authority Class: REVIEW / ARCHITECTURE
> Date: 2026-10-07 · Task: CURIS-V1-PLATFORM-ACCOUNT-S1-20261007
> 输入: [平台/账号本地链合同](../01_Product/CURIS_PLATFORM_ACCOUNT_LOCAL_CHAIN_CONTRACT.md)（Frozen，D1–D5）· 代码证据见 §2
> 裁定人: Main Development（工程决策；按治理「定义存储优先复用」评审）

## 1. 问题

合同 §2.2 新增 ChannelAccount（D2：business 级 scope）。治理规则：新 primitive/schema 须先过 Architecture Review。需裁定存储形态。

## 2. 代码事实

1. CG 对象链存储 = `runtime_entities`，范式：`entity_type='PACKAGE_DOMAIN_OBJECT'` + `json_extract(data_json,'$.objectType')` 过滤，`verification_status='UNVERIFIED'`、`evidence_condition='MISSING'`（[content_growth_service.py L453-462](../../backend/app/content_growth_service.py#L453-L462)）。
2. `runtime_entities` 列：entity_id / tenant_id / entity_type / company_id / workspace_id / parent_id / owner_ref / lifecycle_status / blueprint_version / verification_status / evidence_condition / data_json / created_at / updated_at（同上 L453-455）。**无 business_id 列**。
3. **公司级行先例**：employee_templates.py 插入 runtime_entities 时省略 workspace_id（[employee_templates.py L127-130](../../backend/app/employee_templates.py#L127-L130)）——company scope 行已有在先模式。
4. 另一通用链 `workspace_package_objects`（workspace_package_runtime.py L45-91 + `_validate_domain_schema`）与 CG 读写链**无关**（CG 写入走 ContentGrowthService.workspace helpers，调查证实）。
5. Router：`build_content_growth_router` 挂 `/api/workspace/v1/companies/{company}/content-growth/{workspace}`，错误映射 KeyError/RuntimeScopeError→404、ContentGrowthConflict→409、ValueError→422（content_growth_router.py L41-80）；main.py L5695-5723 构造接线。
6. content item 已带 `platform` / `target_account_refs` 元数据及读取校验钩子（content_growth_service.py L90-119、runtime/workspace.py L3348-3375）。

## 3. 裁定

**复用 `runtime_entities`，零新表、零 schema 迁移**——ChannelAccount 不构成新 primitive：

1. 存储为 `entity_type='PACKAGE_DOMAIN_OBJECT'`、`data_json.objectType='ChannelAccount'`，`verification_status='UNVERIFIED'`、`evidence_condition='MISSING'`（与 CG Learning 同型）。
2. **D2 business 级落法**：行写 `company_id`，`workspace_id` 写创建时所在 CG workspace（可空沿用 employee_templates 先例），业务归属以 `data_json.business_ref`（创建工作区所属 business，经既有 workspace→business 关联解析）承载；**可见性查询按 company_id + business_ref 过滤**（json_extract 既有查询范式），实现跨工作区复用。S1 实施时以「同公司同业务双工作区互见」QA 证实。
3. 平台目录（D1 六平台）为后端常量 + 响应内嵌目录；不落库、不可编辑。
4. Router：在既有 `build_content_growth_router` 上扩 `/accounts` 端点（同前缀同错误映射）；scope 校验复用 `ContentGrowthEntryService.authoring_scope`。
5. S3 的回执/表现观察：同 PACKAGE_DOMAIN_OBJECT 模式，`scope_ref` 校验命中 ChannelAccount 实体否则 404；时点不可变与幂等/409 语义在 data_json 承载 revision/identity_ref/previous_ref（对齐 Music/Writing 范式）。
6. 红线落地：`connection_status='NOT_CONNECTED'` 为服务端常量，写入路径忽略客户端该字段；账本/事件零新增（无新表无新事件类型）。

## 4. 影响与边界

- 无 schema 迁移 ⇒ 无数据库演进风险；老库直接可用。
- 不触碰 `workspace_package_objects` 链、不触碰 legacy connectors。
- 若未来 V2 引入真实连接器需 business/账号身份升级（如 secret 引用），届时另立 Architecture Review；本裁定不预设。

## 5. Next Gate

S1 Issue（CURIS-V1-PLATFORM-ACCOUNT-S1-20261007）按本裁定实施；验收证据须包含 §3.2 的跨工作区可见性 QA 与 NOT_CONNECTED 不可变 QA。
