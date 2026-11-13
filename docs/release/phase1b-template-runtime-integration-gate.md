# Phase-1B Template Runtime Integration Gate Report

状态：已完成 Contract + Runtime Design，尚未进入 UI 或跨线实现。

日期：2026-07-10

## 产品进度

Curis Workspace 已明确官方 Template 如何转换为 tenant 私有 Company、Department、Employee、Workflow、Skill 和 Tool 运行时实例，为以 Company / Project 为入口的 Phase-1B UI 准备了可追溯的产品契约。

## 已冻结决策

- 模板与实例分离：Template 只读，Instance / Binding 属于 Workspace tenant。
- 每个模板化实例必须保留不可变的 `created_from_template_id` 与 `created_from_template_version`；空白创建明确标记为 `tenant_private` 来源。
- CEO 可以定制名称、允许范围内的 Skill、Tool、Persona 预留与 Workflow 配置，但不能修改来源追溯、官方定义、能力治理或敏感配置。
- 公司创建支持“空白公司”与“CompanyPackage”两种产品流程；CompanyPackage 未来按原子 bootstrap 生成 Company -> Department -> Employee -> Skill -> Tool -> Workflow。
- Project 仍是 Workflow 的唯一产品触发上下文；Task 仍是内部执行底座。

## 当前实现基础与缺口

| 项目 | 当前基础 | 后续实现缺口 |
| --- | --- | --- |
| `created_from_template_id` | Company、Department、Employee、Tool、Workflow 已有或已对齐 | 跨对象一致性验证 |
| `created_from_template_version` | 未实现 | 需独立数据迁移与 API Issue |
| 官方模板目录 | 仅已有局部官方目录/契约 | 需 Shared Contract 定义只读目录与版本读取 |
| CompanyPackage bootstrap | 未实现 | 需原子创建、失败回滚与 tenant 隔离设计 |
| Template Runtime UI | 未实现 | 由 产品规划席 先定义 Phase-1B 信息架构和交互 |

## 禁止范围

- CEO Office、会议、秘书、商业功能、Marketplace。
- Admin 侧代码与治理逻辑变更。
- Credential Vault、Model Gateway、Tool Router、Workflow Engine 改动。
- 模板自动升级、自动同步、自动改写实例，或实例化时复制敏感配置。

## 进入 Phase-1B 的 Gate 条件

1. 产品规划席先批准 Company / Project-first 的 UI 信息架构、页面范围与关键交互。
2. 任何官方模板目录、版本读取或跨线接口先建立 Shared Contract / Gate。
3. UI 实现不得假定尚未存在的 CompanyPackage bootstrap 或模板版本 API。
4. 若 Phase-1B 需要持久化 `created_from_template_version`，必须单独开后端迁移 Issue 并经安全边界复核。

## 结论

可以进入 Phase-1B UI 产品设计；不能直接进入官方模板同步、CompanyPackage 自动实例化或模板版本持久化实现。
