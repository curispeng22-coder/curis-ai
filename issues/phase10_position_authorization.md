# Phase-10 岗位级能力授权（Position Capability Authorization）

Status: Review

Owner Seat: 产品规划席（slice 验收）/ 系统交付席（实现）

Source contracts:

- `docs/plan/position-authorization-design.md`（本 Issue 设计）
- `docs/plan/evoflow-verified-reuse-plan.md`（EvoFlow 复用决策：A 档已落地，岗位授权为扩展）
- `docs/00_Context/CURRENT_STATE.md`（能力/员工基线）

## Background

EvoFlow 多 Agent 管理最有价值的机制是「角色工具白名单」（方案不给 terminal、审查纯只读）。
Curis 已落地 A1（能力 effect_class 标签），但只有标签、无「谁能用」检查——员工绑了工具就能用。
本 Issue 补岗位级授权：岗位模板声明允许的 effect_class 集合，绑定与调用时检查。

业务驱动约束（用户拍板）：授权规则挂岗位模板（业务数据，引导按业务生成），能力标签是通用引擎；
新业务品类 = 新岗位模板，引擎不动，**不定死业务类型**；不照搬 EvoFlow 按业务写死的预设团队。

## Goal

- 岗位模板（employee_templates）增 `allowed_effect_classes_json`（岗位允许的 effect_class 白名单）。
- 授权引擎 `CapabilityAuthorizer`：绑定校验（422）+ 调用校验（deny-by-default），授权先于降级求值。
- 业务引导蓝图 employees 增 `allowed_effect_classes`，落地写岗位模板——职责面（responsibility）与权限面合体。
- 内置 et_* 模板按职责补授权（架构师/技术负责人=read+retrieve；开发=read+retrieve+write；QA=read+retrieve）。

## Scope

- employee_templates 增列（_ensure_column，幂等）。
- 新 `capability_authorizer.py` + `capability_resolver.py` 挂前置谓词。
- 绑定端点校验 + 引导蓝图扩展 + et_* seed 补授权。
- 测试：引擎 / 绑定 422 / 调用拒绝 / 引导生成四类。

## Non-goals

- 相位闸门（B1，何时能用）——留 S0（Blueprint 4.4 评审后）。
- 不引入 EvoFlow 预设团队（software/media 按业务写死的固定角色）。
- 不改任务 schema / 状态机语义；不碰商业化红线。

## Acceptance

- 岗位未声明授权 → 拒绝一切能力（deny-by-default）。
- 绑定超授权能力 → 422；调用越权能力 → 拒绝且写 trace。
- 引导生成岗位含授权白名单，落库可查；全量回归不回退（基线 1202 passed）。
