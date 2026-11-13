# 岗位级能力授权（Position Capability Authorization）设计

> 状态：Draft（待评审）
> 日期：2026-08-04
> 依据：EvoFlow 复核（角色工具白名单机制）+ Curis 原则③（员工=动态调用能力的岗位）+ 已落地 A1 effect_class（能力副作用标签）
> 定位：把 EvoFlow「角色工具白名单」中最值得搬的**授权矩阵**搬进 Curis，同时保持**业务驱动、不定死业务类型**（机制与数据分离）。

---

## 1. 背景与目标

EvoFlow 的多 Agent 管理核心机制之一是**角色工具白名单**：方案角色不给 terminal/delete、审查角色纯只读、开发角色能写——每个岗位按职责精细授权。Curis 已落地 A1（能力 effect_class 标签：read/retrieve/write/exec），但**只有标签、没有「谁能用」的检查**：员工绑了工具就能用，任何阶段都能碰。

本设计补上「岗位级」授权：**每个岗位声明「允许碰哪类 effect_class 的能力」，能力调用/绑定时先过这道闸**。

### 关键约束（用户拍板，业务驱动）

1. **不定死业务类型**：授权规则挂在**岗位模板**上（业务数据，引导按业务生成），能力标签是**通用引擎**（业务无关）——新业务品类 = 新岗位模板，引擎一行不改。
2. **不照搬 EvoFlow 预设团队**：EvoFlow 的 software/media 团队按业务写死，Curis 不引入「按业务预设的固定角色」。
3. **与职责面合体**：UI 原型「创建业务时定义岗位职责」= 职责面（已有 responsibility 字段）；本设计 = 权限面（允许的 effect_class 集合），同一岗位定义的两面，业务引导生成时一起落地。

---

## 2. 数据模型

### 2.1 岗位模板增字段（employee_templates / employee_instances）

```sql
-- 幂等 _ensure_column：岗位允许的 effect_class 白名单（JSON 数组）
-- 模板级：岗位模板默认授权
allowed_effect_classes_json  text not null default '[]'
-- 实例级：员工实例覆盖（空 = 继承模板；非空 = 覆盖）
allowed_effect_classes_json  text not null default '[]'
```

语义：`["read","retrieve","write","exec"]` 子集。**空数组 = deny-by-default**（该岗位不通过任何能力调用；通常应至少声明 read）。解析优先级：实例覆盖 > 模板默认 > 空集拒绝。

### 2.2 默认授权规则

- **标签自动派生 + 例外覆盖（用户拍板）**：新工具不手打标签——官方工具按类型/名称自动派生（A1），用户自定义工具注册时 metadata 可选声明 `effect_class`，不声明按类型默认；**声明的值只能比默认更安全（收窄），不能放宽**（防 exec 伪造成 read 绕过安全）。
- **兼容策略（实现决议）**：内置 `et_*` 模板迁移回填**全开**（read/retrieve/write/exec）作为兼容基线（不破坏既有绑定/测试），后续单独收敛；**新岗位（引导生成的 tenant_private）必须显式声明**（未声明 = 拒绝一切，deny-by-default），引导按业务品类生成收敛授权。
- **CEO / 用户直接调用放行**：无员工上下文（用户本人发起）不受岗位授权约束（天然全开）；岗位授权只约束「员工执行任务时的能力调用」。
- **实例级覆盖**：`employee_instances` 增 `allowed_effect_classes_json`（默认空 = 继承岗位模板；非空 = 实例级覆盖）——业务引导生成的员工按业务收敛授权即落此列。

### 2.3 评审决议（2026-08-04 用户拍板）

1. 绑定校验 + 调用校验**都做**（早失败优于晚失败）。
2. 未声明授权的新岗位 → **拒绝一切**（强制显式）。
3. exec 类能力**允许**进岗位白名单，但调用记审计（复用 A2 trace）。

---

## 3. 授权引擎

### 3.1 检查点（两个正交入口）

| 检查点 | 时机 | 行为 |
|---|---|---|
| **绑定校验** | 员工绑定能力（`POST /api/workspace/capabilities/bind` 或等价） | 能力 effect_class ∉ 岗位允许集 → 422 拒绝绑定 |
| **调用校验** | 能力路由/解析时（capability_resolver 选路前） | 岗位允许集 ∩ 能力标签为空 → 拒绝（403/降级），deny-by-default |

### 3.2 组件

- `backend/app/capability_authorizer.py`（新）：`CapabilityAuthorizer.authorize(employee_id, capability) -> bool`（读岗位模板 allowed_effect_classes + 能力 effect_class 派生）。
- 挂载点：`capability_resolver.py`（选能力前）——不改执行语义，只加前置谓词（与 A1 同款「先于降级求值」约束：授权是硬约束，降级是软策略）。

### 3.3 与未来相位闸门的关系（正交）

- **岗位级授权** = 「谁能用」（空间维度：岗位→能力类别）
- **相位闸门**（B1，S0 后）= 「何时能用」（时间维度：规划/执行/验收相位）
- 两个维度叠加：`规划相位 && 岗位允许 && 能力标签` 全部满足才放行。本设计只做岗位维度，相位维度留 S0。

---

## 4. 与业务引导合体（不定死业务的关键）

`workbench_guide` 蓝图 `employees[].template_id` 扩展：

```json
{ "template_id": "et_content_editor", "name": "主编",
  "allowed_effect_classes": ["read", "retrieve", "write"] }
```

- **业务引导生成岗位时**：蓝图含职责（name/role）+ 权限（allowed_effect_classes），落地时写入 `employee_templates`（source=tenant_private）或作为员工实例的岗位授权快照。
- **默认生成规则**（引导 AI 蓝图 schema 内）：按业务品类给默认授权（内容业务 → read/retrieve/write；研发业务 → read/retrieve/write/exec 按角色）；用户可在确认表单调整（与蓝图确认同一步）。
- 这样**新业务 = 引导生成新岗位模板（含授权）**，引擎（CapabilityAuthorizer + effect_class）不动。

---

## 5. 影响范围

| 层 | 改动 |
|---|---|
| 持久层 | `employee_templates` 增列 `allowed_effect_classes_json`（_ensure_column，幂等） |
| 引擎 | 新 `capability_authorizer.py` + `capability_resolver.py` 挂前置谓词 |
| 绑定 | 绑定端点校验授权（422） |
| 引导 | `workbench_guide` 蓝图 employees 增 `allowed_effect_classes`，落地写岗位模板 |
| 内置模板 | `et_*` seed 补 allowed_effect_classes |
| 测试 | 引擎/绑定/调用/引导四类用例 |

**不触碰**：任务 schema、状态机语义、商业化红线、前端（除引导表单的授权字段，属引导已有确认步骤的扩展）。

## 6. 安全与降级

- deny-by-default：未声明 allowed_effect_classes 的岗位 = 空集 = 拒绝一切（强制显式声明）。
- 授权是硬约束、降级是软策略：**授权先于降级求值**（与 A1 effect_class 同约束）。
- 拒绝记录写入 trace（复用 A2 runtime_trace_event），不静默丢弃。

## 7. 待办

实现状态：**已实现并全量回归通过（1208 passed / 2 skipped / 0 failed，2026-08-04）**。

1. [x] 迁移：employee_templates + employee_instances 增 `allowed_effect_classes_json`（_ensure_column 幂等 + 内置 et_* 回填全开兼容基线）
2. [x] `capability_authorizer.py`（CapabilityAuthorizer：实例覆盖 > 模板默认 > 空集拒绝；无岗位模板放行）+ resolver 挂载（employee 分支获取授权、选链 effect_class 过滤）
3. [x] 绑定端点校验（PUT capabilities：越权 422，早失败）
4. [x] 引导蓝图 employees 增 `allowed_effect_classes` + instantiator 落实例级覆盖
5. [x] 内置 et_* 兼容回填（全开，后续单独收敛）
6. [x] 测试 6 用例 + 全量回归（含列契约测试同步）
7. [x] 文档同步（CURRENT_STATE / CHANGE_LOG）

## 8. 待确认（评审时拍板）

1. 绑定校验 vs 仅调用校验：是否要求「员工绑定能力时」就拦截（我建议是——早失败优于晚失败）。
2. 岗位模板缺省：新岗位模板未声明授权时，是「拒绝一切」还是「继承部门/业务默认」？建议拒绝一切（强制显式）。
3. exec 类能力（如 test_runner）是否允许出现在岗位白名单？建议允许但记录审计（exec 是执行类，需与沙箱/相位闸门联动）。
